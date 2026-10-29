"""Real saved pages exercise the current and historical markup offline."""

from datetime import date
from pathlib import Path

import pytest
from bs4 import BeautifulSoup

from promval.vlr.cache import load
from promval.vlr.parse import ParseError, parse_economy, parse_match, parse_results_page

FIXTURES = Path(__file__).parent / "fixtures" / "vlr"
CASES = [
    (
        773441,
        "KRÜ BLAZE",
        "Team Liquid Brazil",
        3,
        [("Summit", 13, 9), ("Haven", 13, 6)],
        "13.06",
    ),
    (
        654971,
        "Gen.G GC",
        "Meikai Dolls",
        5,
        [("Lotus", 13, 4), ("Haven", 13, 5), ("Fracture", 13, 5)],
        None,
    ),
    (
        610432,
        "UCAM Esports Club",
        "NOVO Esports",
        5,
        [("Pearl", 13, 6), ("Haven", 13, 2), ("Corrode", 13, 5)],
        "12.01",
    ),
    (163803, "Team Queso", "KPI Gaming", 1, [("Pearl", 11, 13)], None),
    (6805, "LDM Esports", "IGNIS Esports", 1, [("Haven", 13, 5)], "1.12"),
]


@pytest.mark.parametrize("id,t1,t2,bo,maps,patch", CASES)
def test_match(id, t1, t2, bo, maps, patch):
    match = parse_match(load(FIXTURES / f"match_{id}.html.gz"), id)
    assert (match.team1.name, match.team2.name, match.best_of) == (t1, t2, bo)
    assert [(m.map, m.score1, m.score2) for m in match.maps] == maps
    if patch:
        assert match.patch == patch
    assert (match.score1, match.score2) == (
        sum(a > b for _, a, b in maps),
        sum(b > a for _, a, b in maps),
    )
    assert match.winner == (1 if match.score1 > match.score2 else 2)
    assert match.event and match.event_id and match.stage
    assert match.team1.team_id and match.team2.team_id
    for game in match.maps:
        assert len(game.rounds) == game.score1 + game.score2
        assert len(game.players) == 10
        assert {p.team for p in game.players} == {1, 2}
        assert all(p.agents and p.name for p in game.players)
        assert game.team1_atk + game.team1_def == game.score1
        assert game.team2_atk + game.team2_def == game.score2
        assert game.duration and game.overtime == 0
        assert {r.winner_side for r in game.rounds} <= {"atk", "def"}
        assert {r.win_type for r in game.rounds} <= {"elim", "boom", "defuse", "time"}
    if id in (6805, 163803):
        assert match.veto == []


@pytest.mark.parametrize(
    "id,stamp",
    [
        (773441, "2026-10-28T19:40:00Z"),
        (163803, "2023-01-08T20:00:00Z"),
        (6805, "2020-11-29T02:00:00Z"),
    ],
)
def test_eastern_time(id, stamp):
    assert parse_match(load(FIXTURES / f"match_{id}.html.gz"), id).start_utc == stamp


@pytest.mark.parametrize(
    "id,expected",
    [
        (
            773441,
            [
                ("KRUB", "ban", "Sunset"),
                ("TLV", "ban", "Lotus"),
                ("KRUB", "pick", "Summit"),
                ("TLV", "pick", "Haven"),
                ("KRUB", "ban", "Abyss"),
                ("TLV", "ban", "Split"),
                (None, "decider", "Ascent"),
            ],
        ),
        (
            654971,
            [
                ("GEN.GC", "ban", "Pearl"),
                ("GEN.GC", "ban", "Breeze"),
                ("5D", "pick", "Lotus"),
                ("GEN.GC", "pick", "Haven"),
                ("5D", "pick", "Fracture"),
                ("GEN.GC", "pick", "Bind"),
                (None, "decider", "Split"),
            ],
        ),
    ],
)
def test_veto(id, expected):
    m = parse_match(load(FIXTURES / f"match_{id}.html.gz"), id)
    assert [(v.team_tag, v.action, v.map) for v in m.veto] == expected
    assert [v.step for v in m.veto] == list(range(1, 8))
    assert all(g.picked for g in m.maps)
    if id == 773441:
        assert m.event == "Game Changers 2026: Championship São Paulo"
        assert m.event_id == 3134
        player = m.maps[0].players[0]
        assert (player.player_id, player.name, player.agents) == (
            35660,
            "tok1o",
            ["chamber"],
        )
        assert (
            player.rating,
            player.acs,
            player.kills,
            player.deaths,
            player.assists,
            player.kast,
            player.adr,
            player.hs_pct,
            player.fk,
            player.fd,
        ) == (1.33, 275, 21, 15, 2, 73, 177, 34, 9, 5)


@pytest.mark.parametrize("page", [1, 300, 600, 1500])
def test_results(page):
    rows = parse_results_page(load(FIXTURES / f"results_p{page}.html.gz"))
    assert len(rows) == (0 if page == 1500 else 50)
    assert all(r.slug and r.match_id for r in rows)
    assert [r.day for r in rows] == sorted((r.day for r in rows), reverse=True)
    if page == 1:
        assert (rows[0].match_id, rows[0].day) == (773441, date(2026, 10, 28))


@pytest.mark.parametrize("id", [c[0] for c in CASES])
def test_economy(id):
    match = parse_match(load(FIXTURES / f"match_{id}.html.gz"), id)
    economy = parse_economy(load(FIXTURES / f"match_{id}_economy.html.gz"))
    assert set(economy) == {m.game_id for m in match.maps}
    for game in match.maps:
        teams = economy[game.game_id].teams
        assert sum(t.pistols_won for t in teams) == 2
        for team in teams:
            assert team.pistols_played == 2
            assert team.semi_eco_played is None and team.semi_buy_played is None
            assert len(team.rounds) == len(game.rounds)
            assert all(r.buy is not None and r.bank is not None for r in team.rounds)
            assert (
                len(team.rounds) - 6
                == team.eco_played + team.half_buy_played + team.full_buy_played
            )
            # Summary grids omit pistol/conversion/bonus rounds in each half.
            for category in ("eco", "half_buy", "full_buy"):
                assert getattr(team, category + "_played") == sum(
                    r.buy_type == category
                    for r in team.rounds
                    if r.number not in (1, 2, 3, 13, 14, 15)
                )
    if id == 6805:
        assert match.maps[0].players[0].rating is None
        assert match.maps[0].players[0].kast is None
    if id == 773441:
        team = economy[286505].teams[0]
        assert (
            team.pistols_won,
            team.eco_played,
            team.half_buy_won,
            team.full_buy_won,
        ) == (1, 1, 2, 9)
        assert (team.rounds[0].buy_type, team.rounds[0].buy, team.rounds[0].bank) == (
            "pistol",
            3800,
            200,
        )


@pytest.mark.parametrize(
    "mutation,reason",
    [("round", "rounds"), ("series", "series score"), ("winner", "round winners")],
)
def test_broken_invariants(mutation, reason):
    soup = BeautifulSoup(load(FIXTURES / "match_773441.html.gz"), "lxml")
    game = soup.select_one('.vm-stats-game[data-game-id="286505"]')
    if mutation == "round":
        game.select_one(".vlr-rounds-row-col[title]").decompose()
    elif mutation == "series":
        soup.select_one(".match-header-vs-score-winner").string = "3"
    else:
        squares = game.select_one(".vlr-rounds-row-col[title]").select(".rnd-sq")
        squares[1]["class"] = ["rnd-sq"]
        squares[0]["class"] = ["rnd-sq", "mod-win", "mod-ct"]
    with pytest.raises(ParseError, match=reason) as error:
        parse_match(str(soup), 773441)
    assert error.value.match_id == 773441


def test_full_regulation_header_and_optional_fields():
    soup = BeautifulSoup(load(FIXTURES / "match_163803.html.gz"), "lxml")
    game = soup.select_one('.vm-stats-game[data-game-id="108884"]')
    assert len(game.select(".vlr-rounds-row-col[title]")) == 25
    for node in soup.select(
        '.match-header-date [style*="italic"], .match-header-vs-note'
    ):
        node.decompose()
    match = parse_match(str(soup), 163803)
    assert len(match.maps[0].rounds) == 24
    assert match.best_of is None and match.patch is None
