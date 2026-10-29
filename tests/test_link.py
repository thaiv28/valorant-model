"""Offline matching, settlement and catalog-to-database regression checks."""

import importlib.util
import json
import sqlite3
from dataclasses import replace
from pathlib import Path

import pytest

from promval.link import (
    Event,
    cross_check,
    link,
    market_row,
    normalize,
    scheduled_utc,
)

REPO = Path(__file__).resolve().parents[1]
FIXTURES = REPO / "tests" / "fixtures" / "kalshi"
TIME = "2026-10-28T21:00:00Z"


def event(
    ticker="series",
    names=("KRÜ Blaze", "MIBR Female"),
    ids=("kr", "mibr"),
    scheduled=TIME,
    **kwargs,
):
    return Event(
        ticker,
        tuple(
            {
                "ticker": f"{ticker}-{i}",
                "team_name": name,
                "competitor_id": cid,
                "team_code": str(i),
                "scheduled_utc": scheduled,
                "open_time": "2026-10-27T21:00:00Z",
                "result": "yes" if i == 0 else "no",
            }
            for i, (name, cid) in enumerate(zip(names, ids))
        ),
        **kwargs,
    )


def match(mid=1, names=("KRÜ BLAZE", "MIBR GC"), ids=(10, 20), start=TIME):
    return {
        "match_id": mid,
        "team1_name": names[0],
        "team2_name": names[1],
        "team1_id": ids[0],
        "team2_id": ids[1],
        "start_utc": start,
        "winner": 1,
        "maps": [{"game_id": 100 + mid, "order": 1, "score1": 13, "score2": 6}],
    }


@pytest.mark.parametrize(
    ("a", "b", "equal"),
    [
        ("KRÜ Blaze", "KRÜ BLAZE", True),
        ("MIBR Female", "MIBR GC", True),
        ("Team Liquid", "Team Liquid Brazil", False),
        ("G2 Esports", "G2", True),
        ("The Team G2 Gaming Club", "G2 Esport", True),
        ("MIBR Women", "MIBR GC", True),
    ],
)
def test_normalize(a, b, equal):
    assert (normalize(a) == normalize(b)) == equal
    assert isinstance(normalize(a), tuple)


@pytest.mark.parametrize(
    ("date", "zone", "expected"),
    [
        ("Oct 30, 2026", "EDT", "2026-10-30T21:00:00Z"),
        ("Dec 30, 2026", "EST", "2026-12-30T22:00:00Z"),
    ],
)
def test_schedule(date, zone, expected):
    assert (
        scheduled_utc(f"match originally scheduled for {date} at 5:00 PM {zone}, then")
        == expected
    )


def test_invalid_schedule():
    assert scheduled_utc("no schedule") is None
    assert scheduled_utc("originally scheduled for Oct 99, 2026 at 5:00 PM EDT") is None


def test_three_passes():
    exact = event()
    renamed = event("renamed", names=("New Brand", "Other Brand"))
    fuzzy = event("fuzzy", names=("Krü Blaz", "MIBR GC"), ids=("unknown", "unknown2"))
    result = link([renamed, fuzzy, exact], [match()])
    assert {r.event_ticker: r.method for r in result.links} == {
        "series": "exact",
        "renamed": "alias",
        "fuzzy": "anchor",
    }
    assert {a.competitor_id: (a.vlr_team_id, a.events) for a in result.aliases} == {
        "kr": (10, 2),
        "mibr": (20, 2),
        "unknown": (10, 1),
        "unknown2": (20, 1),
    }
    assert cross_check([renamed, fuzzy, exact], result.links, [match()]).agreements == 6


def test_order_free_and_alias_conflict():
    reversed_match = match(names=("MIBR GC", "KRÜ BLAZE"), ids=(20, 10))
    result = link([event()], [reversed_match])
    assert result.links[0].team_ids == (10, 20)
    assert cross_check([event()], result.links, [reversed_match]).checked == 2
    later = event("later", scheduled="2026-11-10T21:00:00Z")
    conflicting = match(2, ids=(99, 20), start="2026-11-10T21:00:00Z")
    renamed = event("renamed", names=("New Brand", "Other Brand"))
    result = link([event(), later, renamed], [match(), conflicting])
    assert [a.competitor_id for a in result.aliases] == ["mibr"]
    assert result.links[-1].match_id is None
    assert result.aliases[0].events == 2


def test_ambiguous_and_missing():
    result = link([event()], [match(), match(2)])
    assert result.links[0].match_id is None
    assert "ambiguous" in result.links[0].reason
    assert not result.aliases
    incomplete = replace(event(), markets=event().markets[:1])
    assert (
        link([incomplete], [match()]).links[0].reason
        == "expected two competitor markets"
    )
    no_time = replace(
        event(),
        markets=tuple(
            {**m, "scheduled_utc": None, "open_time": None} for m in event().markets
        ),
    )
    assert "missing" in link([no_time], [match()]).links[0].reason


@pytest.mark.parametrize(
    ("start", "linked"),
    [
        ("2026-10-29T21:00:00Z", True),
        ("2026-10-27T21:00:00Z", True),
        ("2026-10-30T03:00:00Z", True),
        ("2026-10-30T04:00:00Z", False),
    ],
)
def test_slip_window(start, linked):
    assert (
        link([event()], [match(start=start)]).links[0].match_id is not None
    ) == linked


def test_fallback_and_no_partial_alias():
    assert link([event(scheduled=None)], [match()]).links[0].method == "exact"
    renamed = event("rename", names=("New Brand", "Other Brand"), ids=("kr", "unknown"))
    assert link([event(), renamed], [match()]).links[-1].match_id is None


def test_maps_and_results():
    series = event("KXVALORANTGAME-26X")
    # Reverse market ordering to verify inherited competitor identities.
    played = replace(
        event("KXVALORANTMAP-26X-1", kind="map", map_number=1),
        markets=tuple(reversed(series.markets)),
    )
    unplayed = event("KXVALORANTMAP-26X-2", kind="map", map_number=2)
    result = link([series, played, unplayed], [match()])
    assert result.links[1].game_id == 101
    assert result.links[1].team_ids == (20, 10)
    assert result.links[2].match_id == 1
    assert result.links[2].reason == "unplayed"
    checked = cross_check([series, played, unplayed], result.links, [match()])
    assert (checked.agreements, checked.checked, checked.mismatches) == (4, 4, [])
    wrong = match()
    wrong["winner"] = 2
    wrong["maps"][0]["score2"] = 14
    checked = cross_check([series, played], result.links[:2], [wrong])
    assert checked.agreements == 0 and checked.checked == 4
    assert len(checked.mismatches) == 4
    assert "game_id=101" in checked.mismatches[-1]
    assert link([played], [match()]).links[0].game_id == 101


def test_scalar_draw_and_unresolved_skipped():
    scalar = replace(
        event(), markets=tuple({**m, "result": "scalar"} for m in event().markets)
    )
    result = link([scalar], [match()])
    assert cross_check([scalar], result.links, [match()]).checked == 0
    drawn = {**match(), "winner": None}
    assert cross_check([event()], result.links, [drawn]).checked == 0


def load_script(name, root, monkeypatch):
    spec = importlib.util.spec_from_file_location(name, REPO / "scripts" / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    monkeypatch.setattr(module, "REPO", root)
    return module


@pytest.fixture
def builder(tmp_path, monkeypatch):
    monkeypatch.setenv("PROMVAL_DATA", str(tmp_path / "data"))
    (tmp_path / "db").mkdir()
    with sqlite3.connect(tmp_path / "db" / "valorant.db") as conn:
        conn.executescript((REPO / "scripts" / "001_create_tables.sql").read_text())
    return (
        load_script("005_load_kalshi", tmp_path, monkeypatch),
        load_script("006_link_kalshi", tmp_path, monkeypatch),
        tmp_path,
    )


def test_fixture_db_build(builder, capsys):
    loader, linker, root = builder
    catalog = root / "data" / "kalshi" / "markets"
    catalog.mkdir(parents=True)
    games = json.loads((FIXTURES / "markets_settled_game.json").read_text())["markets"]
    games += json.loads((FIXTURES / "historical_markets_game.json").read_text())[
        "markets"
    ]
    maps = json.loads((FIXTURES / "markets_open_map.json").read_text())["markets"]
    (catalog / "KXVALORANTGAME.json").write_text(json.dumps(games))
    (catalog / "KXVALORANTMAP.json").write_text(json.dumps(maps))
    seeds = [
        ("KRÜ BLAZE", "Team Liquid Brazil", "2026-10-28T21:00:00Z"),
        ("MIBR GC", "SK Nebula", "2026-10-28T18:00:00Z"),
        ("T1", "KIWOOM DRX", "2026-08-28T11:00:00Z"),
        ("Global Esports", "VARREL", "2026-08-27T11:00:00Z"),
        ("KRÜ BLAZE", "MIBR GC", "2026-10-30T21:00:00Z"),
    ]
    with sqlite3.connect(root / "db" / "valorant.db") as conn:
        for mid, (a, b, start) in enumerate(seeds, 1):
            # Shared identities for the two GC teams across events.
            aid = 10 if a == "KRÜ BLAZE" else 20 if a == "MIBR GC" else mid * 100
            bid = 20 if b == "MIBR GC" else mid * 100 + 1
            conn.execute(
                "INSERT INTO matches "
                "(match_id,event,event_id,start_utc,team1_name,team1_id,team2_name,team2_id,score1,score2,winner) "
                "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (mid, "Fixture", 1, start, a, aid, b, bid, 2, 0, 1),
            )
        conn.execute(
            "INSERT INTO maps "
            '(game_id,match_id,"order",map,picked,score1,score2,overtime) '
            'VALUES (501,5,1,"Ascent",1,13,6,0)'
        )
    for _ in range(2):  # Re-running refreshes rather than duplicates rows.
        loader.main()
        linker.main()
    output = capsys.readouterr().out
    assert "kalshi_markets=12" in output
    assert "series=4/4 map=1/2 aliases=8 results=8/8 mismatches=0" in output
    with sqlite3.connect(root / "db" / "valorant.db") as conn:
        assert conn.execute("SELECT count(*) FROM kalshi_links").fetchone()[0] == 6
        assert conn.execute("SELECT count(*) FROM team_aliases").fetchone()[0] == 8
        assert conn.execute(
            "SELECT scheduled_utc, event_name FROM kalshi_markets WHERE ticker=?",
            (maps[0]["ticker"],),
        ).fetchone() == ("2026-10-30T21:00:00Z", "VCT Game Changers Championship 2026")
        assert conn.execute(
            "SELECT event_name FROM kalshi_markets WHERE ticker=?",
            (games[0]["ticker"],),
        ).fetchone() == ("VCT Game Changers Championship 2026",)
        assert conn.execute(
            "SELECT volume FROM kalshi_markets WHERE ticker=?", (games[0]["ticker"],)
        ).fetchone()[0] == float(games[0]["volume_fp"])
        assert conn.execute("PRAGMA foreign_key_check").fetchall() == []
        conn.execute("UPDATE matches SET winner=2 WHERE match_id=1")
    linker.main()
    assert "mismatches=2" in capsys.readouterr().out
    report = (root / "db" / "link_report.txt").read_text()
    assert "unplayed" in report and games[0]["ticker"] in report
    assert "DRX → KIWOOM DRX" in report
    assert "scheduled=2026-10-30T21:00:00Z" in report
    assert "event=VCT Game Changers Championship 2026" in report
    assert "KRÜ Blaze" in report or "KRÜ BLAZE" in report
    with sqlite3.connect(root / "db" / "valorant.db") as conn:
        conn.execute(
            "UPDATE matches SET start_utc='2020-01-01T00:00:00Z' WHERE match_id=1"
        )
    linker.main()
    report = (root / "db" / "link_report.txt").read_text()
    assert f"{games[0]['event_ticker']}: no candidate within 30h" in report or (
        f"{games[0]['event_ticker']}: no team match" in report
    )


def test_missing_catalog(builder, capsys):
    loader, linker, root = builder
    loader.main()
    linker.main()
    output = capsys.readouterr().out
    assert output.count("Missing Kalshi catalog:") == 2
    assert "series=0/0 map=0/0 aliases=0 results=0/0 mismatches=0" in output
    assert (root / "db" / "link_report.txt").exists()


def test_old_ticker_does_not_supply_date():
    row = market_row(
        {
            "ticker": "KXVALORANTGAME-25-DRX",
            "event_ticker": "KXVALORANTGAME-25",
            "yes_sub_title": "DRX",
        },
        "KXVALORANTGAME",
    )
    assert row["scheduled_utc"] is None
    assert row["team_code"] == "DRX"


@pytest.mark.parametrize(
    ("kalshi", "vlr", "code", "method"),
    [
        ("DRX", "KIWOOM DRX", "DRX", "anchor"),
        (
            "Bilibili Gaming",
            "Guangzhou Huadu Bilibili Gaming (Bilibili Gaming)",
            "BLG",
            "exact",
        ),
        (
            "Guangzhou Huadu Bilibili Gaming",
            "Guangzhou Huadu Bilibili Gaming (Bilibili Gaming)",
            "BLG",
            "exact",
        ),
        ("XLG Gaming", "Xi Lai Gaming", "XLG", "anchor"),
        ("eSports Cologne", "CGN Esports", "CGN", "anchor"),
        ("SGE Vision", "Eintracht Frankfurt Team Vision", "SGE", "anchor"),
        ("SGE Vision", "Eintracht Frankfurt", "SGE", None),
        ("Valorando", "VALORANDO", "VAL", "exact"),
    ],
)
def test_real_name_variants(kalshi, vlr, code, method):
    target = event(names=(kalshi, "Opponent"))
    target.markets[0]["team_code"] = code
    result = link([target], [match(names=(vlr, "Opponent"))])
    assert result.links[0].method == method
    if method is None:
        assert result.links[0].reason == "anchor: other team implausible"


def test_fuzzy_last_without_confirmed_side():
    target = event(names=("Kru Blaz", "MIBR G"), ids=("x", "y"))
    result = link([target], [match()])
    assert result.links[0].method == "fuzzy"
    assert not result.aliases


@pytest.mark.parametrize("name", ["RIZON", "ALTERNATE aTTaX"])
def test_exact_team_preferred_over_subteam(name):
    target = event(names=(name, "Opponent"))
    matches = [
        match(
            1,
            names=(name + " Cherry" if name == "RIZON" else name + " Ruby", "Opponent"),
            ids=(30, 20),
        ),
        match(2, names=(name, "Opponent")),
    ]
    assert link([target], matches).links[0].match_id == 2
    # The exact team exists in the window, but plays somebody else.
    matches[1]["team2_name"] = "Different"
    matches[1]["team2_id"] = 40
    assert link([target], matches).links[0].match_id is None


def test_anchor_requires_unique_confirmed_team_and_plausible_other():
    target = event(names=("DRX", "Opponent"))
    candidates = [
        match(names=("KIWOOM DRX", "Opponent")),
        match(2, names=("DRX Academy", "Opponent"), ids=(30, 20)),
    ]
    assert link([target], candidates).links[0].match_id is None
    rejected = link([target], [match(names=("Unrelated", "Opponent"))]).links[0]
    assert rejected.match_id is None
    assert rejected.reason == "anchor: other team implausible"


def test_alias_learned_from_anchor_enables_later_round():
    later = "2026-11-10T21:00:00Z"
    renamed = event("first", names=("New Brand", "Other Brand"), scheduled=later)
    anchored = event("second", names=("DRX", "Opponent"))
    result = link(
        [renamed, anchored],
        [
            match(names=("KIWOOM DRX", "Opponent")),
            match(2, names=("KIWOOM DRX", "Opponent"), start=later),
        ],
    )
    assert [(r.match_id, r.method) for r in result.links] == [
        (2, "alias"),
        (1, "anchor"),
    ]
    assert {a.events for a in result.aliases} == {2}


def test_anchor_conflict_drops_alias_permanently():
    later = "2026-11-10T21:00:00Z"
    last = "2026-11-20T21:00:00Z"
    events = [
        event("first", names=("DRX", "Opponent")),
        event("second", names=("DRX", "Opponent"), scheduled=later),
        event("third", names=("New Brand", "Other Brand"), scheduled=last),
    ]
    result = link(
        events,
        [
            match(names=("KIWOOM DRX", "Opponent")),
            match(2, names=("KIWOOM DRX", "Opponent"), ids=(99, 20), start=later),
            match(3, names=("KIWOOM DRX", "Opponent"), start=last),
        ],
    )
    assert [r.method for r in result.links] == ["anchor", "anchor", None]
    assert [a.competitor_id for a in result.aliases] == ["mibr"]


def test_sge_short_name_via_learned_alias():
    later = "2026-11-10T21:00:00Z"
    events = [
        event("short", names=("SGE Vision", "Opponent"), scheduled=later),
        event("long", names=("SGE Vision", "Opponent")),
    ]
    result = link(
        events,
        [
            match(names=("Eintracht Frankfurt Team Vision", "Opponent")),
            match(2, names=("Eintracht Frankfurt", "Opponent"), start=later),
        ],
    )
    assert [r.method for r in result.links] == ["alias", "anchor"]
