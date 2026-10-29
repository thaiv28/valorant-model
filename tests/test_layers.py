"""Causal feature histories, frozen fits and benchmark integration."""

import sqlite3

import numpy as np
import pandas as pd
import pytest
import test_evaluation as evaluation

from promval.ratings.layers import (
    HALF_LIVES,
    REGIONS,
    FormLayer,
    RegionalFormLayer,
    RegionalLayer,
    causal_features,
)

benchmark = evaluation.benchmark
database = evaluation.database


def history_db():
    conn = sqlite3.connect(":memory:")
    conn.executescript("""
        CREATE TABLE events(event_id, region, international);
        CREATE TABLE matches(match_id, start_utc, team1_id, team2_id, event_id);
        CREATE TABLE maps(game_id, match_id, "order", score1, score2);
        CREATE TABLE player_maps(game_id, player_id, team, rating);
    """)
    conn.executemany(
        "INSERT INTO events VALUES (?,?,?)",
        [(1, "us", 0), (2, "de", 0), (3, "cn", 1), (4, "unknown", 0)],
    )
    # Two maps in one match exercise map order; insertion order is reversed.
    conn.executemany(
        "INSERT INTO matches VALUES (?,?,?,?,?)",
        [
            (6, "2024-01-06", 10, 20, 4),
            (5, "2024-01-05", 10, 20, 2),
            (4, "2024-01-04", 10, 20, 2),
            (3, "2024-01-03", 10, 20, 3),
            (2, "2024-01-02", 10, 20, 2),
            (1, "2024-01-01", 10, 20, 1),
        ],
    )
    games = [
        (7, 6, 1),
        (6, 5, 1),
        (5, 4, 1),
        (4, 3, 1),
        (3, 2, 1),
        (2, 1, 2),
        (1, 1, 1),
    ]
    conn.executemany("INSERT INTO maps VALUES (?,?,?,13,8)", games)
    lineups = {game: ((100, 101, 999), (200,)) for game, _, _ in games}
    # 999 never has a rating, 101 starts fresh on map 2 then has a null map.
    conn.executemany(
        "INSERT INTO player_maps VALUES (?,?,?,?)",
        [
            (game, player, side, rating)
            for game, _, _ in games
            for player, side, rating in (
                (100, 1, 2.0 if game == 1 else 0.0),
                (101, 1, 1.0 if game == 2 else None),
                (999, 1, None),
                (200, 2, 1.0),
            )
        ],
    )
    return conn, lineups


def test_causal_homes_decay_missing_and_order():
    conn, lineups = history_db()
    features = causal_features(conn, lineups)
    assert list(features.index) == list(range(1, 8))
    assert features.loc[1, "home1"] is None
    assert np.isnan(features.loc[1, "form1_5"])
    # Two US maps; DE ties retain Americas; international China never counts.
    assert features.home1.tolist() == [None] + ["Americas"] * 5 + ["EMEA"]
    assert features.home2.tolist() == features.home1.tolist()
    for h in HALF_LIVES:
        decay = 0.5 ** (1 / h)
        assert features.loc[2, f"form1_{h}"] == 2
        expected = (2 * decay / (decay + 1) + 1) / 2
        assert features.loc[3, f"form1_{h}"] == pytest.approx(expected)
        # A missing observation decays 101's weights, but leaves its mean at 1.
        expected = (2 * decay**2 / (decay**2 + decay + 1) + 1) / 2
        assert features.loc[4, f"form1_{h}"] == pytest.approx(expected)
        assert features.loc[7, f"form2_{h}"] == 1
    assert features.loc[4, "form1_5"] < features.loc[4, "form1_20"]
    conn.execute("UPDATE player_maps SET rating=100 WHERE game_id>=5")
    conn.execute("UPDATE maps SET score1=0,score2=13 WHERE game_id>=5")
    pd.testing.assert_frame_equal(
        features.loc[:5], causal_features(conn, lineups).loc[:5]
    )
    conn.close()


def test_all_maps_and_starter_history():
    conn, lineups = history_db()
    conn.execute("UPDATE maps SET score1=0,score2=0 WHERE game_id=1")
    # A substitute with no history is skipped, and an absent player has no weight.
    lineups[2] = ((100, 300), ())
    features = causal_features(conn, lineups)
    assert features.loc[2, "form1_5"] == 2
    assert np.isnan(features.loc[2, "form2_5"])
    conn.execute("DELETE FROM maps")
    assert causal_features(conn, lineups).empty
    conn.close()


def planted(n=10000):
    rng = np.random.default_rng(38)
    a = rng.integers(0, 4, n)
    b = (a + rng.integers(1, 4, n)) % 4
    logits = rng.normal(0, 1, n)
    frame = pd.DataFrame({"game_id": np.arange(n), "p": 1 / (1 + np.exp(-logits))})
    features = pd.DataFrame(
        {"home1": np.array(REGIONS)[a], "home2": np.array(REGIONS)[b]}
    )
    features.index.name = "game_id"
    for h in HALF_LIVES:
        features[f"form1_{h}"] = rng.normal(1, 0.4, n)
        features[f"form2_{h}"] = rng.normal(1, 0.4, n)
    effects = np.array([0.45, -0.35, 0.15, -0.25])
    return rng, frame, features, logits, effects[a] - effects[b]


def sample(rng, z):
    return rng.binomial(1, 1 / (1 + np.exp(-z)))


def test_regional_recovery_scope_zero_sum_and_index():
    rng, frame, features, logits, effect = planted()
    frame["won"] = sample(rng, 1.25 * logits + effect)
    layer = RegionalLayer()
    layer._features = features
    layer.fit(frame)
    assert layer.rows == len(frame)
    assert layer.s == pytest.approx(1.25, abs=0.08)
    assert list(layer.effects.values()) == pytest.approx(
        [0.45, -0.35, 0.15, -0.25], abs=0.08
    )
    assert sum(layer.effects.values()) == pytest.approx(0, abs=1e-14)
    features.loc[0, "home2"] = features.loc[0, "home1"]
    features.loc[1, "home1"] = None
    apply = frame.iloc[:4].copy()
    apply.index = [8, 3, 3, 7]
    adjusted = layer.apply(apply)
    assert adjusted.index.equals(apply.index)
    assert adjusted.iloc[:2].tolist() == apply.p.iloc[:2].tolist()
    assert not np.allclose(adjusted.iloc[2:], apply.p.iloc[2:])
    assert "rows=10000" in layer.describe() and "ridge=4" in layer.describe()


def test_regional_threshold_ridge_and_refit():
    _, frame, features, logits, effect = planted(100)
    # Fractional targets make the unpenalized optimum exact, isolating shrinkage.
    frame["won"] = 1 / (1 + np.exp(-(1.7 * logits + effect)))
    small = RegionalLayer()
    small._features = features
    small.fit(frame.iloc[:49])
    pd.testing.assert_series_equal(small.apply(frame), frame.p)
    assert "identity (<50" in small.describe()
    small.fit(frame.iloc[:50])
    large = RegionalLayer()
    large._features = features
    large.fit(pd.concat([frame.iloc[:50]] * 100, ignore_index=True))
    assert abs(small.s - 1) < abs(large.s - 1)
    assert np.linalg.norm(list(small.effects.values())) < np.linalg.norm(
        list(large.effects.values())
    )
    small.fit(frame.iloc[:0])
    assert small.s == 1 and all(e == 0 for e in small.effects.values())


def test_form_recovery_selection_missing_and_clipping():
    rng, frame, features, logits, _ = planted()
    delta = features.form1_10 - features.form2_10
    frame["won"] = sample(rng, logits + 2.3 * delta)
    layer = FormLayer()
    layer._features = features
    layer.fit(frame)
    assert layer.half_life == 10
    assert layer.w == pytest.approx(2.3, abs=0.15)
    assert layer.rows == len(frame)
    features.loc[0, "form1_10"] = np.nan
    features.loc[1:2, "form1_10"] = [1e6, -1e6]
    adjusted = layer.apply(frame.iloc[:3])
    assert adjusted.iloc[0] == frame.p.iloc[0]
    assert adjusted.iloc[1] == 1 - 1e-6
    assert adjusted.iloc[2] == 1e-6
    assert "H=10" in layer.describe() and "rows=10000" in layer.describe()


@pytest.mark.parametrize("cls", [FormLayer, RegionalLayer, RegionalFormLayer])
def test_frozen_fit_uses_only_given_rows(cls):
    rng, frame, features, logits, effect = planted(1000)
    frame["won"] = sample(rng, logits + effect + features.form1_5 - features.form2_5)
    layer = cls()
    layer._features = features
    layer.fit(frame.iloc[:700])
    description = layer.describe()
    prediction = layer.apply(frame.iloc[700:])
    frame.loc[700:, "won"] = 1 - frame.loc[700:, "won"]
    layer.fit(frame.iloc[:700])
    assert layer.describe() == description
    pd.testing.assert_series_equal(layer.apply(frame.iloc[700:]), prediction)
    # Empty stage 1 is a supported identity, including in the combined layer.
    layer.fit(frame.iloc[:0])
    pd.testing.assert_series_equal(layer.apply(frame), frame.p)


def test_combination_order_and_shared_cache():
    rng, frame, features, logits, effect = planted(1500)
    frame["won"] = sample(
        rng, logits + effect + 2 * (features.form1_20 - features.form2_20)
    )
    combined = RegionalFormLayer()
    combined._features = features
    combined.fit(frame)
    regional, form = RegionalLayer(), FormLayer()
    regional._features = form._features = features
    regional.fit(frame)
    adjusted = frame.copy()
    adjusted["p"] = regional.apply(frame)
    form.fit(adjusted)
    pd.testing.assert_series_equal(combined.apply(frame), form.apply(adjusted))
    assert combined.regional._features is combined.form._features is features
    assert (
        combined.describe()
        == f"regional_form: {regional.describe()}; {form.describe()}"
    )


def test_real_context_caches_once():
    conn, lineups = history_db()
    frame = pd.DataFrame({"game_id": [3, 4, 5], "p": [0.4, 0.5, 0.6], "won": [0, 1, 0]})
    layer = FormLayer({"conn": conn, "lineups": lineups})
    layer.fit(frame)
    prediction = layer.apply(frame)
    cached = layer._features
    conn.execute("UPDATE player_maps SET rating=100")
    pd.testing.assert_series_equal(layer.apply(frame), prediction)
    assert layer._features is cached
    conn.close()


def test_end_to_end_layers(database, tmp_path, monkeypatch):
    path, data = database
    monkeypatch.setenv("PROMVAL_DATA", str(data))
    out = tmp_path / "layers.md"
    benchmark.main(
        [
            "--db",
            str(path),
            "--out",
            str(out),
            "--models",
            "team_elo",
            "--report-models",
            "team_elo",
            "--layers",
            "regional,form,regional_form",
            "--k-grid",
            "32",
            "--jobs",
            "1",
            "--quote",
            "prestart",
        ]
    )
    report = out.read_text()
    for name in ("regional", "form", "regional_form"):
        section = report.split(f"### team_elo+{name}: Kalshi comparison and returns")[1]
        assert section.lstrip().startswith(f"{name}: ")
        assert "rows=" in section.split("####")[0]
        assert f"team_elo+{name} − team_elo" in report
