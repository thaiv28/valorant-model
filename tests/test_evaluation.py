import ast
import gzip
import importlib.util
import json
import os
import sqlite3
import subprocess
import sys
from pathlib import Path

import numpy as np
import pytest

from promval.evaluation import (
    ece,
    game_losses,
    interval,
    paired_bootstrap,
    resamples,
    series_probability,
)
from promval.ratings.models import TeamEloModel
from promval.ratings.replay import load_lineups, load_maps, replay

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "evaluate_elo", ROOT / "scripts/evaluate_elo.py"
)
benchmark = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(benchmark)


def test_series_probability():
    assert series_probability(0.6, 1) == 0.6
    assert series_probability(0.6, 3) == pytest.approx(0.648)
    assert series_probability(0.5, 5) == pytest.approx(0.5)
    assert series_probability(0, 5) == 0
    assert series_probability(1, 5) == 1
    assert np.diff([series_probability(p, 5) for p in np.linspace(0, 1, 21)]).min() > 0
    for n in (0, 2, -1):
        with pytest.raises(ValueError):
            series_probability(0.5, n)


def test_scoring_helpers():
    losses = game_losses([0.5, 0.8, 0.2], [1, 1, 1])
    assert losses.accuracy.tolist() == [0.5, 1, 0]
    assert losses.brier.tolist() == pytest.approx([0.25, 0.04, 0.64])
    assert losses.log_loss.tolist() == pytest.approx(-np.log([0.5, 0.8, 0.2]))
    assert np.isfinite(game_losses([0, 1], [1, 0]).log_loss).all()
    assert ece([0.2, 0.2, 0.8, 1], [0, 1, 1, 1]) == pytest.approx(0.2)
    assert interval([0, 1, 2, 3, 4]) == pytest.approx((0.1, 3.9))
    draws = list(resamples(3, 2, seed=0))
    assert [x.tolist() for x in draws] == [[2, 1, 1], [0, 0, 0]]
    clustered = list(resamples([np.array([0, 1]), np.array([2])], 1, seed=0))
    assert clustered[0].tolist() == [2, 2]
    assert paired_bootstrap([2, 4], [1, 3], clusters=[1, 2]) == (1, 1, 1)
    # A single match's unequal map errors must stay together in every draw.
    assert paired_bootstrap([0, 4], [0, 0], clusters=[7, 7]) == (2, 2, 2)
    with pytest.raises(ValueError, match="equal length"):
        paired_bootstrap([1, 2], [0, 0], clusters=[1])


@pytest.mark.parametrize(
    "fixture,key",
    [("candles.json", "close_dollars"), ("candles_historical.json", "close")],
)
def test_candle_formats(fixture, key):
    raw = json.loads((ROOT / "tests/fixtures/kalshi" / fixture).read_text())
    candles = raw["candlesticks"]
    end = candles[1]["end_period_ts"]
    expected = sum(float(candles[1][side][key]) for side in ("yes_bid", "yes_ask")) / 2
    from datetime import UTC, datetime

    start = datetime.fromtimestamp(end, UTC).isoformat()
    assert benchmark.candle_mid(raw, start) == pytest.approx(expected)
    assert benchmark.candle_mid(list(reversed(candles)), start) == pytest.approx(
        expected
    )
    assert benchmark.candle_mid(candles, "2000-01-01T00:00:00Z") is None


def test_candle_missing_closes_and_cutoff():
    candles = [
        {"end_period_ts": 10, "yes_bid": {"close": "0.2"}, "yes_ask": {"close": "0.4"}},
        {"end_period_ts": 20, "yes_bid": {"close": "0.8"}, "yes_ask": {}},
        {"end_period_ts": 30, "yes_bid": {"close": "0.8"}, "yes_ask": {"close": "1.0"}},
    ]
    assert benchmark.candle_mid(candles, "1970-01-01T00:00:20Z") == pytest.approx(0.3)


def table_definitions(filename):
    """Extract SQL literals only: never execute a loader or touch real caches."""
    tree = ast.parse((ROOT / "scripts" / filename).read_text())
    return [
        node.value
        for node in ast.walk(tree)
        if isinstance(node, ast.Constant)
        and isinstance(node.value, str)
        and "CREATE TABLE" in node.value
    ]


@pytest.fixture
def database(tmp_path):
    path = tmp_path / "tiny.db"
    with sqlite3.connect(path) as conn:
        conn.executescript((ROOT / "scripts/001_create_tables.sql").read_text())
        for filename in ("003_events.py", "005_load_kalshi.py", "006_link_kalshi.py"):
            for sql in table_definitions(filename):
                conn.executescript(sql)
        conn.execute(
            "INSERT INTO events(event_id,section,international) VALUES (1,'vct',1)"
        )
        for match_id, start, best_of, winner, wins in (
            (1, "2022-01-01T00:00:00Z", 1, 1, [1]),
            (2, "2023-01-01T00:00:00Z", 3, 1, [1, 0, 1]),
            (3, "2026-06-30T23:00:00Z", 2, None, [1, 0]),
            (4, "2026-07-01T00:00:00Z", 1, 2, [0]),
            (5, "2026-07-02T00:00:00Z", None, 1, [1]),
        ):
            conn.execute(
                "INSERT INTO matches VALUES (?, 'Test', ?, NULL, ?, ?, NULL, 'A', 10, 'B', 20, ?, ?, ?)",
                (
                    match_id,
                    1 if match_id != 3 else 99,
                    start,
                    best_of,
                    sum(wins),
                    len(wins) - sum(wins),
                    winner,
                ),
            )
            for order, won in enumerate(wins, 1):
                conn.execute(
                    """INSERT INTO maps(game_id,match_id,"order",map,picked,score1,score2,overtime)
                       VALUES (?, ?, ?, 'Ascent', 0, ?, ?, 0)""",
                    (
                        match_id * 10 + order,
                        match_id,
                        order,
                        13 if won else 8,
                        8 if won else 13,
                    ),
                )
        conn.executemany(
            "INSERT INTO player_maps(game_id,player_id,team) VALUES (?,?,?)",
            [
                (game_id, side * 100 + starter, side)
                for (game_id,) in conn.execute("SELECT game_id FROM maps")
                for side in (1, 2)
                for starter in range(5)
            ],
        )
        for competitor, team in (("a", 10), ("b", 20), ("other", 99)):
            conn.execute(
                "INSERT INTO team_aliases(competitor_id,vlr_team_id) VALUES (?,?)",
                (competitor, team),
            )
        for event, kind, game_id in (("S", "series", None), ("M", "map", 22)):
            conn.execute(
                "INSERT INTO kalshi_links VALUES (?,2,?,?, 'exact', NULL)",
                (event, game_id, kind),
            )
            for competitor in ("a", "b", "other", "unresolved"):
                conn.execute(
                    "INSERT INTO kalshi_markets(ticker,series,event_ticker,kind,competitor_id) VALUES (?,?,?,?,?)",
                    (event + competitor, "KXVALORANTGAME", event, kind, competitor),
                )
    directory = tmp_path / "data/kalshi/candles"
    directory.mkdir(parents=True)
    for event in ("S", "M"):
        for competitor, mid in (
            ("a", 0.7),
            ("b", 0.4),
            ("other", 0.9),
            ("unresolved", 0.1),
        ):
            with gzip.open(directory / f"{event + competitor}.json.gz", "wt") as handle:
                json.dump(
                    [
                        {
                            "end_period_ts": 1672531200,
                            "yes_bid": {"close_dollars": str(mid - 0.01)},
                            "yes_ask": {"close_dollars": str(mid + 0.01)},
                        }
                    ],
                    handle,
                )
    return path, tmp_path / "data"


def test_load_series_and_market_pairing(database):
    path, data = database
    with sqlite3.connect(path) as conn:
        loaded = load_maps(conn)
        assert loaded.loc[loaded.game_id == 11, ["score1", "score2"]].iloc[
            0
        ].tolist() == [13, 8]
        lineups = load_lineups(conn)
        assert lineups[11] == (tuple(range(100, 105)), tuple(range(200, 205)))
        assert set(lineups) == set(loaded.game_id)
        maps = replay(loaded, TeamEloModel())
        assert list(maps.game_id) == [11, 21, 22, 23, 31, 32, 41, 51]
        assert set(maps[maps.match_id == 3].section) == {"unknown"}
        assert set(maps[maps.match_id == 3].international) == {0}
        series = benchmark.series_rows(maps)
        assert list(series.match_id) == [1, 2, 4]
        first = maps[maps.match_id == 2].iloc[0]
        assert series[series.match_id == 2].p.iloc[0] == pytest.approx(
            series_probability(first.p, 3)
        )
        market = benchmark.kalshi_rows(conn, maps, series, data / "kalshi")
        assert len(market) == 2
        assert market.market_p.tolist() == pytest.approx([0.7, 0.7])
        assert market.ask.tolist() == pytest.approx([0.71, 0.71])
        assert market.bid.tolist() == pytest.approx([0.69, 0.69])
        map_row = market[market.kind == "map"].iloc[0]
        # Map markets are compared with the pre-match chance (first map of match 2).
        assert map_row.p == maps[maps.game_id == 21].p.iloc[0]
        assert map_row.won == 0
        (data / "kalshi/candles/Ma.json.gz").unlink()
        market = benchmark.kalshi_rows(conn, maps, series, data / "kalshi")
        assert market[market.kind == "map"].market_p.iloc[0] == pytest.approx(0.6)
        assert market[market.kind == "map"].ask.iloc[0] == pytest.approx(0.61)
        assert market[market.kind == "map"].bid.iloc[0] == pytest.approx(0.59)
        for candle in (data / "kalshi/candles").glob("*.json.gz"):
            candle.unlink()
        assert benchmark.kalshi_rows(conn, maps, series, data / "kalshi").empty
        conn.execute("DROP TABLE kalshi_links")
        assert benchmark.kalshi_rows(conn, maps, series, data / "kalshi").empty


def test_end_to_end_variants_and_weights(database, tmp_path, monkeypatch):
    path, data = database
    env = dict(os.environ, PROMVAL_DATA=str(data))
    report_path = tmp_path / "report.md"
    command = [
        sys.executable,
        str(ROOT / "scripts/evaluate_elo.py"),
        "--db",
        str(path),
        "--out",
        str(report_path),
        "--k-grid",
        "16,32",
        "--jobs",
        "2",
        "--models",
        "team_elo,team_round,player_binary_region",
        "--report-models",
        "team_elo,team_round,player_binary_region",
    ]
    result = subprocess.run(
        command, env=env, text=True, capture_output=True, check=True
    )
    report = report_path.read_text()
    assert "## Holdout" not in report
    assert "Holdout maps=" not in result.stdout
    assert "## Leaderboard" in report
    assert "| team_elo | all | 5 |" in report
    assert "| team_elo | all | 1 |" in report
    for name in ("team_elo", "team_round", "player_binary_region"):
        assert f"| {name} |" in report
        assert f"### {name}: Kalshi comparison and returns" in report
    assert "team_round − team_elo (paired log loss)" in report
    assert "player_binary_region − team_elo (paired log loss)" in report
    assert "Unknown host-region map rows: 6" in report
    assert "Total wall time:" in result.stdout
    assert len(result.stdout.splitlines()) <= 20
    # Redirect learned artifacts into scratch space, and run imported workers inline.
    monkeypatch.setattr(benchmark, "REPO", tmp_path)
    (tmp_path / "promval/ratings").mkdir(parents=True)
    monkeypatch.setenv("PROMVAL_DATA", str(data))
    args = command[2:] + ["--jobs", "1", "--write-weights"]
    selected = benchmark.main(args)
    weights = json.loads((tmp_path / "promval/ratings/elo_weights.json").read_text())
    assert set(weights) == {"team_elo", "team_round", "player_binary_region"}
    for name, params in selected.items():
        assert weights[name] == {**params, "fit_through": "2026-06-30"}
    # Future rows must not affect the tuning leaderboard or chosen parameters.
    leaderboard = report.split("## Leaderboard")[1].split("Kalshi uses")[0]
    with sqlite3.connect(path) as conn:
        conn.execute("UPDATE maps SET score1=13,score2=1 WHERE match_id>=4")
        conn.execute("DROP TABLE kalshi_links")
    assert benchmark.main(args) == selected
    assert (
        report_path.read_text().split("## Leaderboard")[1].split("Kalshi uses")[0]
        == leaderboard
    )
    assert "no linked markets" in report_path.read_text()


def test_empty_windows_and_invalid_selection(database, tmp_path, monkeypatch):
    path, data = database
    monkeypatch.setenv("PROMVAL_DATA", str(data))
    with sqlite3.connect(path) as conn:
        tuning = benchmark.scored_rows(load_maps(conn), "2023-01-01")
        assert set(tuning.match_id) == {2, 3}
    args = [
        "--db",
        str(path),
        "--out",
        str(tmp_path / "report.md"),
        "--models",
        "team_elo",
        "--jobs",
        "1",
        "--k-grid",
        "32",
    ]
    for extra in (
        ["--score-from", "2026-07-01"],
        ["--k-grid", "nan"],
        ["--score-from", "2026-06-30T23:30:00"],
        ["--models", "nonexistent"],
        ["--jobs", "0"],
    ):
        with pytest.raises(SystemExit) as error:
            benchmark.main(args + extra)
        assert error.value.code == 2


def test_baseline_always_included(database, tmp_path, monkeypatch):
    path, data = database
    monkeypatch.setenv("PROMVAL_DATA", str(data))
    selected = benchmark.main(
        [
            "--db",
            str(path),
            "--out",
            str(tmp_path / "report.md"),
            "--models",
            "team_round",
            "--report-models",
            "team_elo,team_round",
            "--jobs",
            "1",
            "--k-grid",
            "32",
        ]
    )
    assert set(selected) == {"team_elo", "team_round"}
    assert "| coin | all | 5 |" in (tmp_path / "report.md").read_text()


def test_glicko_report_default_and_explicit_models(
    database, tmp_path, monkeypatch, capsys
):
    path, data = database
    monkeypatch.setenv("PROMVAL_DATA", str(data))
    # Exercise actual registry factories with a small grid in the synthetic DB.
    for name in ("player_round_glicko", "player_round_region_glicko"):
        monkeypatch.setitem(
            benchmark.PARAM_GRIDS,
            name,
            {key: (values[0],) for key, values in benchmark.PARAM_GRIDS[name].items()},
        )
    out = tmp_path / "glicko.md"
    args = [
        "--db",
        str(path),
        "--out",
        str(out),
        "--models",
        "team_elo",
        "--jobs",
        "1",
        "--k-grid",
        "12",
    ]
    selected = benchmark.main(args)
    assert set(selected) == {
        "team_elo",
        "player_round_glicko",
        "player_round_region_glicko",
    }
    report = out.read_text()
    assert report.index("## Combined summary") < report.index("## Leaderboard")
    assert report.count("#### Log loss vs Kalshi") == 3
    assert report.count("#### Full-Kelly returns") == 3
    assert "| series | vct |" in report and "| map | international=0 |" in report
    assert "in-sample" in report and "unrounded" in report
    assert "no depth limit or slippage" in report
    assert "unplayed maps are not in the rows" in report
    printed = capsys.readouterr().out
    assert "Series flat ROI" in printed and "Map Kelly $" in printed
    assert len(printed.splitlines()) <= 20
    selected = benchmark.main(args + ["--report-models", "team_elo,team_elo"])
    assert set(selected) == {"team_elo"}
    assert out.read_text().count("#### Full-Kelly returns") == 1
    with pytest.raises(SystemExit):
        benchmark.main(args + ["--report-models", "unknown"])
