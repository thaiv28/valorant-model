import itertools
import sqlite3
from copy import deepcopy
from types import SimpleNamespace

import numpy as np
import pytest

from promval.ratings.elo import EloConfig, EloModel, TeamElo
from promval.ratings.models import MODELS, PARAM_GRIDS
from promval.ratings.regions import REGION_CODES, macro_region
from promval.ratings.replay import load_maps
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
    assert len(MODELS) == len(PARAM_GRIDS) == 20
    assert "team_binary" not in MODELS
    for name in MODELS:
        if name == "coin":
            continue
        grid = PARAM_GRIDS[name]
        if "_glicko" in name:
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
            "k": (16, 24, 32, 48, 64),
            "tau": (0.4, 0.5, 0.6, 0.8),
            "rd_new": (280, 350, 450, 600),
            "rd_info": (0.125, 0.25, 0.5, 1.0),
            "new_player": ("fixed", "teammates"),
        }
        if region:
            grid["region_k"] = (2, 4)
        assert PARAM_GRIDS[name] == grid
        model = MODELS[name]()
        assert model.unit == "player" and model.credit == "round" and model.rd
        assert bool(model.region_k) == region
        assert model.rd_floor == 140 and model.rd_growth == 10
        assert model.predict(row()) == 0.5
        assert model.rd_variance == model.last_seen == {}


@pytest.mark.parametrize("maps", [0, 1, 10, 29, 30, 40])
def test_rookie_log_discount_and_update_only_counts(maps):
    from math import log1p

    model = EloModel(
        unit="player", rookie_penalty=100, rookie_maps=30, lineups={1: ((1,), (2,))}
    )
    for _ in range(maps):
        model.update(row())
    model.ratings = {1: 1600, 2: 1500}
    before = model.ratings.copy()
    discount = 100 * (1 - log1p(maps) / log1p(30)) if maps < 30 else 0
    assert model._strength((1,)) == pytest.approx(1600 - discount)
    for _ in range(2):
        model.predict(row())
    assert model.ratings == before
    assert model.map_counts == ({1: maps, 2: maps} if maps else {})
    model.update(row())
    assert model.map_counts == {1: maps + 1, 2: maps + 1}


@pytest.mark.parametrize("credit", ["binary", "round"])
def test_adjusted_strengths_drive_update_expectation(credit):
    model = EloModel(
        unit="player",
        credit=credit,
        rookie_penalty=100,
        move_up_penalty=80,
        lineups={1: ((1,), (2,))},
    )
    model.ratings = {1: 1600, 2: 1500}
    model.map_counts = {1: 30}
    model.tier_homes = {1: 2, 2: 3}
    model.tier_counts = {1: {2: 5}, 2: {3: 5}}
    game = row(section="vct")
    # Side 1 is promoted (1600 - 80); side 2 is a rookie (1500 - 100).
    expected = 1 / (1 + 10 ** ((1400 - 1520) / 400))
    assert model._state(game)[-1] == pytest.approx(expected)
    before = model.ratings.copy()
    model.predict(game)
    assert model.ratings == before
    model.update(game)
    assert model.ratings[1] == pytest.approx(1600 + 32 * (model.score(game) - expected))
    assert model.ratings[2] == pytest.approx(1500 - 32 * (model.score(game) - expected))


@pytest.mark.parametrize(
    "home,target,adjustment", [("vcl", "vct", -100), ("vct", "vcl", 50)]
)
def test_tier_moves_fade_with_prior_rank_count(home, target, adjustment):
    model = EloModel(
        unit="player",
        move_up_penalty=100,
        move_down_bonus=50,
        move_maps=4,
        lineups={1: ((1,), (2,))},
    )
    for _ in range(10):
        model.update(row(section=home))
    for played in range(6):
        model.ratings = {1: 1500, 2: 1500}
        counts = {p: c.copy() for p, c in model.tier_counts.items()}
        homes = model.tier_homes.copy()
        game = row(section=target)
        model.predict(game)
        model.predict(game)
        rank = 3 if target == "vct" else 2
        assert model._strength((1,), rank) == 1500 + adjustment * max(0, 1 - played / 4)
        assert model.ratings == {1: 1500, 2: 1500}
        assert model.tier_counts == counts and model.tier_homes == homes
        model.update(game)


def test_tier_home_majority_ties_and_unranked_maps():
    model = EloModel(
        unit="player",
        move_up_penalty=100,
        move_down_bonus=50,
        lineups={1: ((1,), (2,))},
    )
    model.predict(row(section="vct"))
    assert model.tier_homes == model.tier_counts == {}
    for section, home in [
        ("collegiate", 0),
        ("t3", 0),
        ("t3", 1),
        ("vcl", 1),
        ("vct", 1),
        ("vct", 1),
        ("vct", 3),
    ]:
        model.update(row(section=section))
        assert model.tier_homes == {1: home, 2: home}
    counts = {p: c.copy() for p, c in model.tier_counts.items()}
    for section in ("gc", "offseason", "unknown", None):
        model.ratings = {1: 1600, 2: 1500}
        assert model.predict(row(section=section)) == 1 / (1 + 10 ** (-100 / 400))
        model.update(row(section=section))
        assert model.tier_counts == counts
        assert model.tier_homes == {1: 3, 2: 3}


def test_default_glicko_exact_pre_adjustment_predictions():
    model = MODELS["player_round_glicko"](
        k=48,
        tau=0.5,
        new_player="teammates",
        lineups={1: ((1, 2), (3, 4)), 2: ((1, 5), (3, 6)), 3: ((2, 5), (4, 6))},
    )
    # Captured from HEAD's original EloModel, before adding either adjustment.
    expected = [
        0.5,
        0.6049514936541424,
        0.4895232774269876,
        0.5494500189842346,
        0.34805927231445377,
        0.5873668334641886,
        0.36348696685987575,
        0.4842849065470713,
        0.41388964763129493,
    ]
    for i, probability in enumerate(expected):
        game = row(
            game_id=i % 3 + 1,
            score1=13 if i % 2 == 0 else 7,
            score2=9 if i % 2 == 0 else 13,
            won=int(i % 2 == 0),
            start_utc=f"2026-01-{i + 1:02d}T12:00:00Z",
            section=("vcl", "vct", "gc")[i % 3],
            map=("Ascent", "Bind", "Haven")[i % 3],
            picked_by=(1, 2, None)[i % 3],
        )
        assert model.predict(game) == probability
        model.update(game)
    assert model.map_counts == model.tier_counts == model.tier_homes == {}


@pytest.mark.parametrize("variant", ["rookie", "moves", "rookie_moves"])
def test_rookie_moves_registry_exact_grids(variant):
    name = f"player_round_glicko_{variant}"
    grid = {
        "k": (32, 48),
        "tau": (0.4, 0.5),
        "rd_new": (280, 350),
        "rd_info": (0.25,),
        "new_player": ("teammates",),
    }
    if "rookie" in variant:
        grid.update(
            k=(32,),
            rd_new=(280,),
            rookie_penalty=(50, 100, 150, 200, 300),
            rookie_maps=(100, 200, 400, 800),
        )
    if "moves" in variant:
        grid.update(move_up_penalty=(50, 100, 200), move_down_bonus=(0, 50))
    assert PARAM_GRIDS[name] == grid
    model = MODELS[name](**{p: values[0] for p, values in grid.items()})
    assert model.unit == "player" and model.credit == "round" and model.rd
    assert model.move_maps == 20
    assert model.predict(row()) == 0.5


def test_teams_ignore_player_adjustments():
    original = EloModel()
    adjusted = EloModel(rookie_penalty=200, move_up_penalty=100, move_down_bonus=50)
    for game in (row(section="vcl"), row(section="vct"), row(section="collegiate")):
        assert original.predict(game) == adjusted.predict(game)
        original.update(game)
        adjusted.update(game)
        assert original.ratings == adjusted.ratings
    assert adjusted.map_counts == adjusted.tier_counts == adjusted.tier_homes == {}


@pytest.mark.parametrize(
    "options",
    [
        {"rookie_penalty": -1},
        {"rookie_maps": 0},
        {"move_up_penalty": -1},
        {"move_down_bonus": -1},
        {"move_maps": 0},
        {"rookie_maps": float("nan")},
        {"move_up_penalty": float("inf")},
    ],
)
def test_invalid_player_adjustment_parameters(options):
    with pytest.raises(ValueError, match="rookie/move"):
        EloModel(unit="player", **options)


@pytest.mark.parametrize(
    "unit,map_unit,keys",
    [
        ("player", "player", {1, 2, 3, 4}),
        ("player", "team", {10, 20}),
        ("team", "player", {10, 20}),
        ("team", "team", {10, 20}),
    ],
)
def test_map_offsets_learn_centred_strengths_and_unit_keys(unit, map_unit, keys):
    model = EloModel(
        unit=unit, map_k=16, map_unit=map_unit, lineups={1: ((1, 2), (3, 4))}
    )
    model.update(row(map="Bind", won=0))
    assert set(model.map_offsets) == keys
    assert all(offsets == {"Bind": 0} for offsets in model.map_offsets.values())
    for _ in range(8):
        game = row(map="Ascent")
        error = model.score(game) - model._state(game)[-1]
        before = deepcopy(model.map_offsets)
        model.update(game)
        for key, offsets in model.map_offsets.items():
            sign = 1 if key in {1, 2, 10} else -1
            assert offsets["Ascent"] == pytest.approx(
                before[key].get("Ascent", 0) + sign * 16 * error / 2
            )
            assert sum(offsets.values()) == pytest.approx(0, abs=1e-12)
    assert model.predict(row(map="Ascent")) > model.predict(row(map="Bind"))


def test_map_strength_averages_starter_offsets_before_round_transform():
    model = EloModel(
        unit="player",
        credit="round",
        map_k=8,
        lineups={1: ((1, 2), (3,))},
        pick_bonus=20,
    )
    model.map_offsets = {1: {"Bind": 40}, 2: {"Bind": 20}, 3: {"Bind": -10}}
    expected = 1 / (1 + 10 ** (-60 / 400))
    game = row(map="Bind", picked_by=1)
    assert model._state(game)[-1] == expected
    assert model.predict(game) == map_win(expected)


@pytest.mark.parametrize("picker", [None, float("nan"), 0, 3])
def test_pick_bonus_unknown_and_decider(picker):
    model = EloModel(pick_bonus=40)
    assert model.predict(row(picked_by=picker)) == model.predict(row()) == 0.5


@pytest.mark.parametrize("picker,sign", [(1, 1), (2, -1)])
def test_pick_bonus_prediction_and_update_expectation(picker, sign):
    model = EloModel(pick_bonus=40)
    game = row(picked_by=picker)
    expected = 1 / (1 + 10 ** (-sign * 40 / 400))
    assert model.predict(game) == expected
    assert (model.predict(game) > 0.5) == (picker == 1)
    model.update(game)
    assert model.ratings[10] == pytest.approx(1500 + 32 * (1 - expected))


@pytest.mark.parametrize("map_name", [None, float("nan"), 3])
def test_missing_map_does_not_record_offsets(map_name):
    model = EloModel(map_k=8)
    for game in (row(), row(map=map_name)):
        model.update(game)
    assert model.map_offsets == {}


@pytest.mark.parametrize("credit", ["binary", "margin", "round"])
@pytest.mark.parametrize("map_unit", ["player", "team"])
def test_predict_maps_matches_predict_and_does_not_record_state(credit, map_unit):
    model = EloModel(
        unit="player",
        credit=credit,
        rd=True,
        map_k=16,
        map_unit=map_unit,
        pick_bonus=40,
        rookie_penalty=200,
        region_k=4,
        move_up_penalty=100,
        lineups={1: ((1, 2), (3, 4))},
    )
    for game in (
        row(map="Bind", region="us", section="vcl"),
        row(map="Ascent", section="vct"),
    ):
        model.update(game)
    # Snapshot all model dictionaries, including counts, lineups, RD and history.
    before = deepcopy({k: v for k, v in vars(model).items() if isinstance(v, dict)})
    for picker in (1, 2, None, float("nan")):
        game = row(map="Ascent", picked_by=picker, start_utc="2030-01-01T00:00:00Z")
        values = model.predict_maps(
            game, ["Ascent", "Bind", "Haven"], {"Ascent": picker}
        )
        assert values["Ascent"] == model.predict(game)
        assert values["Bind"] == model.predict(row(map="Bind"))
        assert model.predict_maps(game, ["Ascent"])["Ascent"] == model.predict(
            row(map="Ascent", picked_by=None)
        )
        assert set(values) == {"Ascent", "Bind", "Haven"}
        assert vars(game)["map"] == "Ascent"
    assert {k: v for k, v in vars(model).items() if isinstance(v, dict)} == before
    # The wrapper also accepts the pandas namedtuple rows used by replay.
    import pandas as pd

    game = next(
        pd.DataFrame([vars(row(map="Bind", picked_by=2))]).itertuples(index=False)
    )
    assert model.predict_maps(game, [game.map], {game.map: game.picked_by})[
        game.map
    ] == model.predict(game)


def test_predict_maps_only_initializes_unseen_starters():
    model = EloModel(
        unit="player",
        map_k=8,
        rd=True,
        new_player="teammates",
        lineups={1: ((1, 2), (3,))},
    )
    model.ratings[1] = 1600
    before = deepcopy(
        {k: v for k, v in vars(model).items() if isinstance(v, dict) and k != "ratings"}
    )
    model.predict_maps(row(), ["Bind", "Ascent"])
    assert model.ratings == {1: 1600, 2: 1600, 3: 1500}
    assert {
        k: v for k, v in vars(model).items() if isinstance(v, dict) and k != "ratings"
    } == before


@pytest.mark.parametrize(
    "options",
    [
        {"map_k": -1},
        {"map_k": float("nan")},
        {"map_k": float("inf")},
        {"pick_bonus": -1},
        {"pick_bonus": float("nan")},
        {"pick_bonus": float("inf")},
        {"map_unit": "unknown"},
    ],
)
def test_invalid_map_pick_parameters(options):
    with pytest.raises(ValueError, match="map/pick"):
        EloModel(**options)


@pytest.mark.parametrize("variant", ["maps", "pick"])
def test_map_pick_registry_exact_grids_and_adopted_defaults(variant):
    name = f"player_round_glicko_rookie_{variant}"
    base = {
        "k": 32,
        "tau": 0.5,
        "rd_new": 280,
        "rd_info": 0.25,
        "new_player": "teammates",
        "rookie_penalty": 200,
        "rookie_maps": 400,
    }
    grid = {key: (value,) for key, value in base.items()}
    grid.update(
        map_k=(0.5, 1, 2, 4) if variant == "maps" else (0,),
        pick_bonus=(0, 3) if variant == "maps" else (1, 2, 3, 5, 8),
    )
    if variant == "maps":
        grid["map_unit"] = ("player", "team")
    assert PARAM_GRIDS[name] == grid
    for params in itertools.product(*grid.values()):
        model = MODELS[name](**dict(zip(grid, params)))
        assert model.unit == "player" and model.credit == "round" and model.rd
        assert all(getattr(model, key) == value for key, value in base.items())


def test_load_maps_includes_picker_and_nulls():
    with sqlite3.connect(":memory:") as conn:
        conn.executescript("""
            CREATE TABLE maps (game_id, match_id, "order", map, picked_by, score1, score2);
            CREATE TABLE matches (match_id, start_utc, team1_id, team2_id, best_of, event_id, winner);
            CREATE TABLE events (event_id, region, section, international);
            INSERT INTO matches VALUES (1, '2026-01-01T12:00:00Z', 10, 20, 3, 1, 1);
            INSERT INTO maps VALUES (1, 1, 1, 'Bind', 1, 13, 11),
                                    (2, 1, 2, 'Ascent', 2, 13, 11),
                                    (3, 1, 3, 'Haven', NULL, 13, 11);
        """)
        maps = load_maps(conn)
    assert maps["picked_by"].iloc[:2].tolist() == [1, 2]
    assert np.isnan(maps["picked_by"].iloc[2])
