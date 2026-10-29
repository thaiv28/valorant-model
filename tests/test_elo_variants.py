import itertools
from types import SimpleNamespace

import numpy as np
import pytest

from promval.ratings.elo import EloConfig, EloModel, TeamElo
from promval.ratings.models import MODELS, PARAM_GRIDS
from promval.ratings.regions import REGION_CODES, macro_region
from promval.ratings.rounds import map_win


def row(**kwargs):
    values = {
        "start_utc": "2026-01-01T12:00:00Z",
        "game_id": 1,
        "team1_id": 10,
        "team2_id": 20,
        "score1": 13,
        "score2": 11,
        "won": 1,
        "region": "un",
        "international": 0,
    }
    return SimpleNamespace(**(values | kwargs))


def test_map_win_dp():
    assert map_win(0.5) == pytest.approx(0.5)
    assert map_win(0.52) == pytest.approx(0.583, abs=0.0005)
    assert map_win(0.55) == pytest.approx(0.701, abs=0.0005)
    assert map_win(0) == 0 and map_win(1) == 1
    values = [map_win(p) for p in np.linspace(0, 1, 101)]
    assert all(a <= b for a, b in itertools.pairwise(values))
    for p in (0.12, 0.52, 0.77):
        assert map_win(p) + map_win(1 - p) == pytest.approx(1)
    assert map_win(0.520001) == map_win(0.52)
    with pytest.raises(ValueError):
        map_win(-0.1)


def test_margin_and_round_credit():
    margin = EloModel(credit="margin", c=4, k=32)
    assert margin.score(row()) == pytest.approx(0.7310585786)
    assert margin.score(row(score2=3)) == pytest.approx(0.9933071491)
    assert margin.score(row(score1=11, score2=13, won=0)) == pytest.approx(
        1 - margin.score(row())
    )
    round_model = EloModel(credit="round", k=48, tau=0.6)
    round_model.update(row())
    assert round_model.ratings[10] == pytest.approx(1500 + 48 * (13 / 24 - 0.5))
    assert round_model.ratings[20] == pytest.approx(1500 - 48 * (13 / 24 - 0.5))
    e = 1 / (1 + 10 ** (-4 / 400))
    p = map_win(e)
    assert round_model.predict(row()) == pytest.approx(1 / (1 + ((1 - p) / p) ** 0.6))


def test_player_mean_equal_updates_and_initialization():
    lineups = {1: ((1, 2, 3, 4, 5), (6, 7, 8, 9, 11))}
    model = EloModel(unit="player", k=32, lineups=lineups)
    model.ratings.update({1: 1600, 2: 1400})
    assert model.predict(row()) == 0.5
    before = model.ratings.copy()
    model.update(row())
    assert [model.ratings[p] - before[p] for p in lineups[1][0]] == [16] * 5
    assert [model.ratings[p] - before[p] for p in lineups[1][1]] == [-16] * 5
    for mode, initial in (("fixed", 1500), ("teammates", 1600)):
        model = EloModel(unit="player", lineups=lineups, new_player=mode)
        model.ratings[1] = 1600
        model.predict(row())
        assert model.ratings[2] == initial
        assert model.ratings[6] == 1500
        mean = (1600 + 4 * initial) / 5
        assert model.predict(row()) == pytest.approx(
            1 / (1 + 10 ** ((1500 - mean) / 400))
        )


def test_lineup_fallback_and_unusual_sizes():
    model = EloModel(
        unit="player", lineups={1: ((1, 2), (3,)), 3: ((4, 5, 6, 7, 8, 9), ())}
    )
    model.predict(row())
    # A prediction alone must not save the current map's lineup as history.
    assert model.last_lineups == {}
    model.update(row())
    assert model._units(row(game_id=2), 1) == (1, 2)
    assert model._units(row(game_id=2, team2_id=99), 2) == (("team", 99),)
    model.update(row(game_id=2))
    model.update(row(game_id=3))
    assert model._units(row(game_id=4), 1) == (4, 5, 6, 7, 8, 9)
    assert model.last_lineups[20] == (3,)
    assert model.ratings[4] == model.ratings[9]


def test_region_table_and_unknowns():
    assert {
        macro_region(code) for codes in REGION_CODES.values() for code in codes
    } == set(REGION_CODES)
    assert [macro_region(c) for c in ("US", "br", "de", "sa", "vn", "cn")] == [
        "Americas",
        "Americas",
        "EMEA",
        "EMEA",
        "Pacific",
        "China",
    ]
    assert macro_region("un") is None
    assert macro_region("unknown") is None


def test_home_majority_earlier_maps_ties_and_international():
    model = EloModel(region_k=16)
    first = row(region="us")
    assert model.predict(first) == 0.5
    assert model.homes == {}
    model.update(first)
    assert model.homes == {10: "Americas", 20: "Americas"}
    model.update(row(region="de"))  # tie retains previous
    assert model.homes[10] == "Americas"
    model.update(row(region="de", international=1))
    model.update(row(region="un"))
    assert model.home_counts[10] == {"Americas": 1, "EMEA": 1}
    model.predict(row(region="de"))
    assert model.homes[10] == "Americas"  # no current-map leakage
    model.update(row(region="de"))
    assert model.homes[10] == "EMEA"
    assert model.offsets == {}  # same homes throughout


def test_region_offsets_only_cross_region_and_zero_sum():
    model = EloModel(region_k=16)
    model.update(row(team1_id=1, team2_id=2, region="us"))
    model.update(row(team1_id=3, team2_id=4, region="kr"))
    cross = row(team1_id=1, team2_id=3, region="cn")
    expected = model.predict(cross)
    model.update(cross)
    assert model.offsets["Americas"] == pytest.approx(16 * (1 - expected))
    assert sum(model.offsets.values()) == pytest.approx(0)
    assert "China" not in model.offsets  # current host isn't either earlier home
    offsets = model.offsets.copy()
    model.update(row(team1_id=1, team2_id=99, region="un"))
    assert model.offsets == offsets
    model.update(row(team1_id=3, team2_id=4, region="un"))
    assert model.offsets == offsets
    no_offset = EloModel(region_k=0)
    no_offset.ratings = model.ratings.copy()
    # Set known unequal offsets to isolate their contribution to prediction.
    model.homes[1], model.homes[3] = "Americas", "Pacific"
    model.offsets = {"Americas": 10, "Pacific": -10}
    assert model.predict(cross) > no_offset.predict(cross)


def test_registry_grids_and_v1_regression():
    assert len(MODELS) == len(PARAM_GRIDS) == 15
    assert "team_binary" not in MODELS
    for name in MODELS:
        if name == "coin":
            continue
        grid = PARAM_GRIDS[name]
        if name.endswith("_glicko"):
            continue
        assert grid["k"] == (16, 24, 32, 48, 64, 96)
        assert ("region_k" in grid) == name.endswith("_region")
        assert ("new_player" in grid) == name.startswith("player")
        assert ("c" in grid) == ("margin" in name)
        assert ("tau" in grid) == ("round" in name)
        model = MODELS[name](**{p: values[0] for p, values in grid.items()})
        assert model.predict(row()) == 0.5
    old = TeamElo(EloConfig(k=48))
    new = MODELS["team_elo"](k=48)
    probabilities = []
    for a, b, won in ((10, 20, 1), (10, 20, 0), (20, 30, 1), (30, 10, 0), (10, 20, 1)):
        game = row(team1_id=a, team2_id=b, won=won)
        probabilities.append(new.predict(game))
        assert new.predict(game) == old.expected(a, b)
        new.update(game)
        old.update(a, b, won)
        assert new.ratings == old.ratings
    assert probabilities == pytest.approx(
        [
            0.5,
            0.5686413919,
            0.5047414372393056,
            0.4705644068707748,
            0.48881289673471856,
        ],
        abs=1e-9,
    )


@pytest.mark.parametrize("credit", ["binary", "margin", "round"])
def test_rd_first_move_and_update_expectation(credit):
    from math import log

    lineups = {1: ((1, 2), (3, 4))}
    base = EloModel(unit="player", credit=credit, k=12, lineups=lineups)
    model = EloModel(unit="player", credit=credit, k=12, lineups=lineups, rd=True)
    # Unequal strengths distinguish map-win prediction from round expectation.
    for candidate in (base, model):
        candidate.ratings.update({1: 1510, 2: 1510, 3: 1490, 4: 1490})
    expected = base._state(row())[-1]
    before = model.ratings.copy()
    base.update(row())
    model.update(row())
    for player in (1, 2, 3, 4):
        assert model.ratings[player] - before[player] == pytest.approx(
            4 * (base.ratings[player] - before[player])
        )
    information = 0.125 * (log(10) / 400) ** 2 * expected * (1 - expected)
    assert model.rd_variance[1] == pytest.approx(1 / (1 / 280**2 + information))
    assert model.rd_variance[1] < 280**2


def test_rd_growth_cap_floor_and_prediction_has_no_leakage():
    from math import log

    model = EloModel(unit="player", rd=True, k=12, lineups={1: ((1,), (2,))})
    model.update(row())
    first_variance = model.rd_variance.copy()
    first_seen = model.last_seen.copy()
    # Repeated and future predictions must not age/shrink RD or save dates.
    future = row(start_utc="2026-01-04T00:00:00Z")
    model.predict(future)
    model.predict(future)
    assert model.rd_variance == first_variance
    assert model.last_seen == first_seen
    model.ratings = {1: 1500, 2: 1500}
    aged = first_variance[1] + 10**2 * 2.5
    model.update(future)
    assert model.ratings[1] - 1500 == pytest.approx(6 * aged / 140**2)
    information = 0.125 * (log(10) / 400) ** 2 * 0.25
    assert model.rd_variance[1] == pytest.approx(1 / (1 / aged + information))
    assert model.last_seen[1].isoformat() == "2026-01-04T00:00:00+00:00"
    model.ratings = {1: 1500, 2: 1500}
    model.update(row(start_utc="2030-01-01T00:00:00Z"))
    assert model.ratings[1] == pytest.approx(1524)  # Growth capped at new RD.
    for _ in range(1000):
        model.ratings = {1: 1500, 2: 1500}
        model.update(row(start_utc="2030-01-01T00:00:00Z"))
    assert model.rd_variance == {1: 140**2, 2: 140**2}


@pytest.mark.parametrize("credit", ["binary", "margin", "round"])
@pytest.mark.parametrize("region_k", [0, 4])
def test_rd_disabled_preserves_existing_player_variants(credit, region_k):
    options = {
        "unit": "player",
        "credit": credit,
        "region_k": region_k,
        "lineups": {1: ((1, 2), (3, 4)), 2: ((1, 5), (6, 7))},
    }
    original = EloModel(**options)
    disabled = EloModel(**options, rd=False, rd_new=350, rd_info=0.25)
    games = [
        row(region="us"),
        row(game_id=2, team1_id=30, team2_id=40, region="kr"),
        row(team2_id=30, international=1, region="cn"),
        row(game_id=2, score1=4, score2=13, won=0),
    ]
    for game in games:
        assert original.predict(game) == disabled.predict(game)
        original.update(game)
        disabled.update(game)
        assert original.ratings == disabled.ratings
        assert original.offsets == disabled.offsets
    assert disabled.rd_variance == disabled.last_seen == {}


def test_team_ignores_rd_and_player_validates_parameters():
    original = EloModel()
    ignored = EloModel(rd=True, rd_new=-1, rd_info=-1)
    for game in [row(), row(won=0), row(team2_id=30)]:
        assert original.predict(game) == ignored.predict(game)
        original.update(game)
        ignored.update(game)
        assert original.ratings == ignored.ratings
    assert ignored.rd_variance == ignored.last_seen == {}
    for invalid in (
        {"rd_floor": 0},
        {"rd_new": 100},
        {"rd_info": 0},
        {"rd_growth": -1},
        {"rd_info": float("inf")},
        {"rd_new": float("nan")},
    ):
        with pytest.raises(ValueError, match="RD"):
            EloModel(unit="player", rd=True, **invalid)


def test_glicko_registry_and_exact_grids():
    for region in (False, True):
        name = "player_round" + ("_region" if region else "") + "_glicko"
        grid = {
            "k": (8, 12, 16, 24, 32, 48),
            "tau": (0.4, 0.5, 0.6, 0.8),
            "rd_new": (200, 280, 350),
            "rd_info": (0.0625, 0.125, 0.25),
            "new_player": ("fixed", "teammates"),
        }
        if region:
            grid["region_k"] = (2, 4, 8)
        assert PARAM_GRIDS[name] == grid
        model = MODELS[name]()
        assert model.unit == "player" and model.credit == "round" and model.rd
        assert bool(model.region_k) == region
        assert model.rd_floor == 140 and model.rd_growth == 10
        assert model.predict(row()) == 0.5
        assert model.rd_variance == model.last_seen == {}
