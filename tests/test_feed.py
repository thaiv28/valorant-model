"""The website feed is reproducible with local inputs and injected HTTP."""

import gzip
import json
import os
import re
import sqlite3
from datetime import UTC, datetime, timedelta
from pathlib import Path

import pytest

from promval.feed import export, series_call
from promval.vlr.cache import load, save
from promval.vlr.parse import ParseError, parse_schedule_page, parse_upcoming_match

FIXTURES = Path(__file__).parent / "fixtures" / "upcoming"
NOW = datetime(2026, 10, 29, 18, tzinfo=UTC)
START = datetime(2026, 10, 30, 9, tzinfo=UTC)
MID = 777962


def page(mid=MID, start="2026-10-30 05:00:00", best_of=3, team2="A Team"):
    return f'''<div class="match-header">
    <a class="match-header-event" href="/event/3166/test"><div><div>Test event</div></div></a>
    <a class="match-header-link" href="/team/12064/nova"><div class="wf-title-med">Nova Esports</div></a>
    <a class="match-header-link" href="/team/20603/a"><div class="wf-title-med">{team2}</div></a>
    <div class="moment-tz-convert" data-utc-ts="{start}"></div>
    {f"Bo{best_of}" if best_of else ""}</div>'''


def listing(mid=MID, live=False):
    return f"""<a class="match-item" href="/{mid}/test">
    <div class="match-item-vs-team-name"><div class="text-of">Nova Esports</div></div>
    <div class="match-item-vs-team-name"><div class="text-of">A Team</div></div>
    <div class="match-item-vs-team-score">{1 if live else "–"}</div>
    <div class="match-item-vs-team-score">{0 if live else "–"}</div>
    <div class="ml-status">{"LIVE" if live else "Upcoming"}</div>
    <div class="match-item-event">Test event<div class="match-item-event-series">Final</div></div></a>"""


def add_match(conn, mid, start, score1=13, score2=3, best_of=1):
    conn.execute(
        "INSERT INTO matches VALUES (?, ?, 3166, 'Test event', 12064, 20603, 'Nova Esports', 'A Team', ?, 1, 0, 1)",
        (mid, start, best_of),
    )
    conn.execute(
        "INSERT INTO maps VALUES (?, ?, 1, 'Ascent', NULL, ?, ?)",
        (mid, mid, score1, score2),
    )
    conn.executemany(
        "INSERT INTO player_maps VALUES (?, ?, ?)",
        [(mid, side * 10 + p, side) for side in (1, 2) for p in range(5)],
    )


@pytest.fixture
def setup(tmp_path, monkeypatch):
    monkeypatch.setenv("PROMVAL_DATA", str(tmp_path))
    conn = sqlite3.connect(":memory:")
    conn.executescript("""
        CREATE TABLE events(event_id INTEGER PRIMARY KEY, section TEXT, region TEXT, international INTEGER);
        CREATE TABLE matches(match_id INTEGER PRIMARY KEY, start_utc TEXT, event_id INTEGER, event TEXT,
          team1_id INTEGER, team2_id INTEGER, team1_name TEXT, team2_name TEXT,
          best_of INTEGER, score1 INTEGER, score2 INTEGER, winner INTEGER);
        CREATE TABLE maps(game_id INTEGER, match_id INTEGER, "order" INTEGER, map TEXT, picked_by INTEGER, score1 INTEGER, score2 INTEGER);
        CREATE TABLE player_maps(game_id INTEGER, player_id INTEGER, team INTEGER);
        CREATE TABLE team_aliases(competitor_id TEXT, vlr_team_id INTEGER);
        CREATE TABLE kalshi_links(match_id INTEGER, event_ticker TEXT, kind TEXT);
        CREATE TABLE kalshi_markets(ticker TEXT, event_ticker TEXT, competitor_id TEXT);
        INSERT INTO events VALUES (3166, 'vct', 'CN', 0);
    """)
    add_match(conn, 1, "2025-12-01T09:00:00Z")
    add_match(conn, 2, "2026-10-01T09:00:00Z")
    yield conn, tmp_path
    conn.close()


def cached(root, html=None, mid=MID, when=NOW):
    path = root / "upcoming" / f"{mid}.html.gz"
    save(path, html or page())
    os.utime(path, (when.timestamp(), when.timestamp()))
    return path


def by_id(feed, mid=MID):
    return next(m for m in feed["matches"] if m["match_id"] == str(mid))


def test_upcoming_parsers_real_fixtures():
    rows = parse_schedule_page(load(FIXTURES / "vlr_matches.html.gz"))
    first = next(r for r in rows if r.match_id == MID)
    assert (first.name1, first.name2, first.score1, first.score2) == (
        "Nova Esports",
        "A Team",
        None,
        None,
    )
    assert first.status == "upcoming" and first.event and first.stage
    match = parse_upcoming_match(load(FIXTURES / "match_777962.html.gz"), MID)
    assert (match.team1.team_id, match.team2.team_id, match.best_of) == (
        12064,
        20603,
        3,
    )
    assert match.start_utc == "2026-10-30T09:00:00Z" and match.event_id == 3166
    with pytest.raises(ParseError):
        parse_upcoming_match(page(team2="TBD"), MID)
    assert parse_upcoming_match(page(best_of=None), MID).best_of is None
    live = parse_schedule_page(listing(live=True))[0]
    assert (live.status, live.score1, live.score2) == ("live", 1, 0)


def test_export_shape_log_and_bo1(setup):
    conn, root = setup
    requests = []

    def fetch(url):
        requests.append(url)
        return (
            listing()
            if url.endswith("/matches")
            else ""
            if "?page=" in url
            else page(best_of=1)
        )

    feed = export(
        db=conn,
        now=NOW,
        vlr_fetch=fetch,
        kalshi_fetch=lambda url: {"markets": [], "cursor": ""},
    )
    assert set(feed) == {
        "version",
        "game",
        "name",
        "model",
        "generated",
        "data_through",
        "source",
        "sections",
        "matches",
    }
    assert (
        feed["version"] == 1
        and feed["game"] == "valorant"
        and feed["data_through"] == "2026-10-01"
    )
    assert feed["source"] == {
        "name": "VLR.gg",
        "url": "https://www.vlr.gg",
        "license": None,
    }
    assert feed["sections"] == [{"key": "VCT", "label": "VCT", "major": True}]
    assert re.fullmatch(r"\d{4}-\d\d-\d\dT\d\d:\d\dZ", feed["generated"])
    match = by_id(feed)
    assert set(match) == {
        "match_id",
        "start",
        "best_of",
        "name1",
        "name2",
        "event",
        "section",
        "p_game",
        "p_series",
        "status",
        "reconstructed",
        "score1",
        "score2",
        "winner",
        "url",
        "market",
    }
    assert match["p_series"] == match["p_game"] and 0 < match["p_game"] < 1
    assert match["status"] == "upcoming" and match["score1"] is None
    assert isinstance(match["reconstructed"], bool)
    assert by_id(feed, 2)["reconstructed"] is True
    saved = json.loads((root / "predictions.json").read_text())[str(MID)]
    assert saved["p_game"] == match["p_game"] and saved["saved_at"] == feed["generated"]
    assert json.loads((root / "feed" / "valorant.json").read_text()) == feed
    assert "https://www.vlr.gg/matches?page=2" in requests
    requests.clear()
    export(
        db=conn,
        now=NOW + timedelta(hours=1),
        vlr_fetch=fetch,
        kalshi_fetch=lambda url: {"markets": []},
    )
    assert f"https://www.vlr.gg/{MID}" not in requests


def test_call_freezes_after_start_and_final_uses_log(setup):
    conn, root = setup
    cached(root)
    initial = export(db=conn, no_fetch=True, now=NOW)
    call = by_id(initial)
    old_log = json.loads((root / "predictions.json").read_text())[str(MID)]
    conn.execute("UPDATE maps SET score1=1, score2=13")
    later = export(db=conn, no_fetch=True, now=START + timedelta(hours=1))
    assert by_id(later)["status"] == "live"
    assert by_id(later)["p_game"] == call["p_game"]
    assert json.loads((root / "predictions.json").read_text())[str(MID)] == old_log
    add_match(conn, MID, "2026-10-30T09:00:00Z", best_of=3)
    final = by_id(export(db=conn, no_fetch=True, now=START + timedelta(hours=7)))
    assert final["status"] == "final" and final["reconstructed"] is False
    assert (final["p_game"], final["p_series"]) == (call["p_game"], call["p_series"])
    assert (final["score1"], final["score2"], final["winner"]) == (1, 0, 1)


@pytest.mark.parametrize(
    "hours,status", [(1, "live"), (6, "final"), (167, "final"), (169, None)]
)
def test_missing_schedule_status_fallback(setup, hours, status):
    conn, root = setup
    path = cached(root)
    export(db=conn, no_fetch=True, now=NOW)
    path.unlink()
    result = export(db=conn, no_fetch=True, now=START + timedelta(hours=hours))
    matches = [m for m in result["matches"] if m["match_id"] == str(MID)]
    if status is None:
        assert matches == []
    else:
        assert matches[0]["status"] == status
        assert matches[0]["winner"] is None and matches[0]["score1"] is None


def test_removed_future_call_deleted_and_stale_cache_ignored(setup):
    conn, root = setup
    path = cached(root)
    export(db=conn, no_fetch=True, now=NOW)
    path.unlink()
    export(db=conn, no_fetch=True, now=NOW)
    assert str(MID) not in json.loads((root / "predictions.json").read_text())
    cached(root, when=NOW - timedelta(days=8))
    result = export(db=conn, no_fetch=True, now=NOW)
    assert not any(m["match_id"] == str(MID) for m in result["matches"])


@pytest.mark.parametrize(
    "ask,expected,aliased",
    [("0.64", 0.38, False), ("0.75", None, False), ("0.64", 0.38, True)],
)
def test_kalshi_team2_orientation_and_spread(setup, ask, expected, aliased):
    conn, _root = setup
    markets = json.loads((FIXTURES / "kalshi_open_KXVALORANTGAME.json").read_text())[
        "markets"
    ][:2]
    for raw, name, competitor in zip(markets, ("Nova Esports", "A Team"), ("n", "a")):
        raw.update(
            event_ticker="KXVALORANTGAME-TEST",
            ticker=f"KXVALORANTGAME-TEST-{competitor}",
            yes_sub_title=f"Unrelated {competitor}" if aliased else name,
            custom_strike={"esports_competitor": competitor},
            rules_primary="originally scheduled for Oct 30, 2026 at 5:00 AM EDT",
            yes_bid_dollars="0.00",
            yes_ask_dollars="0.00",
        )
    markets[1].update(yes_bid_dollars="0.60", yes_ask_dollars=ask)
    conn.executemany(
        "INSERT INTO team_aliases VALUES (?, ?)", [("n", 12064), ("a", 20603)]
    )
    requests = []

    def kalshi(url):
        requests.append(url)
        return (
            {"markets": [], "cursor": ""}
            if "cursor=" in url
            else {"markets": markets, "cursor": "next"}
        )

    def vlr(url):
        return (
            listing() if url.endswith("/matches") else "" if "?page=" in url else page()
        )

    match = by_id(export(db=conn, now=NOW, vlr_fetch=vlr, kalshi_fetch=kalshi))
    assert len(requests) == 2 and "series_ticker=KXVALORANTGAME" in requests[0]
    if expected is None:
        assert match["market"] is None
    else:
        assert match["market"] == {
            "p": expected,
            "at": "2026-10-29T18:00Z",
            "url": "https://kalshi.com/markets/kxvalorantgame/kxvalorantgame-test",
        }
    fallback = by_id(
        export(
            db=conn,
            now=START + timedelta(hours=1),
            vlr_fetch=lambda url: "",
            kalshi_fetch=kalshi,
        )
    )
    assert fallback["status"] == "live"
    assert (fallback["market"]["p"] if fallback["market"] else None) == expected


def test_live_listing_scores_and_closing_candle(setup):
    conn, root = setup
    conn.execute("INSERT INTO team_aliases VALUES ('a', 20603)")
    conn.execute("INSERT INTO kalshi_links VALUES (2, 'KXVALORANTGAME-PAST', 'series')")
    conn.execute(
        "INSERT INTO kalshi_markets VALUES ('PAST-A', 'KXVALORANTGAME-PAST', 'a')"
    )
    candle_dir = root / "kalshi" / "candles"
    candle_dir.mkdir(parents=True)
    start = datetime(2026, 10, 1, 9, tzinfo=UTC).timestamp()
    with gzip.open(candle_dir / "PAST-A.json.gz", "wt") as handle:
        json.dump(
            {
                "candlesticks": [
                    {
                        "end_period_ts": start + offset,
                        "yes_bid": {"close_dollars": bid},
                        "yes_ask": {"close_dollars": ask},
                    }
                    for offset, bid, ask in [
                        (-3600, ".5", ".6"),
                        (0, ".6", ".64"),
                        (3600, ".8", ".9"),
                    ]
                ]
            },
            handle,
        )

    def vlr(url):
        return (
            listing(live=True)
            if url.endswith("/matches")
            else ""
            if "?page=" in url
            else page()
        )

    feed = export(
        db=conn,
        now=START + timedelta(minutes=10),
        vlr_fetch=vlr,
        kalshi_fetch=lambda url: {"markets": []},
    )
    assert (by_id(feed)["status"], by_id(feed)["score1"], by_id(feed)["score2"]) == (
        "live",
        1,
        0,
    )
    assert by_id(feed, 2)["market"]["p"] == 0.38
    assert by_id(feed, 2)["market"]["at"] == "2026-10-01T09:00Z"

    from promval.feed import build_state, load_state, save_state

    snapshot = root / "state.pkl.gz"
    save_state(build_state(conn, root), snapshot)
    assert (
        export(
            state=load_state(snapshot),
            now=START + timedelta(minutes=10),
            vlr_fetch=vlr,
            kalshi_fetch=lambda url: {"markets": []},
        )
        == feed
    )


def test_series_temperature_unknown_and_bo1():
    assert series_call(0.7, 1, {"1": 0.2}) == 0.7
    assert series_call(0.7, None, {"3": 0.81}) == series_call(0.7, 3, {"3": 0.81})


def test_pagination_stops_at_horizon_skips_tbd_and_live_refetches(setup, capsys):
    conn, root = setup
    cached(root)
    requests = []

    def vlr(url):
        requests.append(url)
        if url.endswith("/matches"):
            return listing(live=True) + listing(8)
        if "?page=2" in url:
            return listing(9)
        if url.endswith(f"/{MID}"):
            return page()
        if url.endswith("/8"):
            return page(team2="TBD")
        if url.endswith("/9"):
            return page(start="2026-11-10 05:00:00")
        raise AssertionError(f"Unexpected fetch: {url}")

    result = export(
        db=conn,
        now=NOW,
        vlr_fetch=vlr,
        kalshi_fetch=lambda url: {"markets": []},
    )
    assert f"https://www.vlr.gg/{MID}" in requests
    assert not any("page=3" in url for url in requests)
    assert {m["match_id"] for m in result["matches"]} == {"2", str(MID)}
    assert "skipped=1" in capsys.readouterr().out


def test_no_fetch_never_uses_injected_network_and_unknown_event(setup):
    conn, root = setup
    cached(root)
    conn.execute("DELETE FROM events")

    def forbidden(url):
        raise AssertionError(f"Network is forbidden: {url}")

    result = export(
        db=conn,
        now=NOW,
        no_fetch=True,
        vlr_fetch=forbidden,
        kalshi_fetch=forbidden,
    )
    assert by_id(result)["section"] == "?"
    assert result["sections"] == [{"key": "?", "label": "Unknown", "major": False}]
    assert by_id(result)["market"] is None


def test_upcoming_requires_an_earlier_rated_map(setup):
    conn, root = setup
    cached(root)
    conn.execute("UPDATE matches SET start_utc='2026-11-01T09:00:00Z'")
    feed = export(db=conn, no_fetch=True, now=NOW)
    assert str(MID) not in {match["match_id"] for match in feed["matches"]}
    assert str(MID) not in json.loads((root / "predictions.json").read_text())


def test_snapshot_roundtrip_and_cli_without_db(setup, monkeypatch):
    from typer.testing import CliRunner

    import promval.feed as feed_module
    from promval.feed import build_state, load_state, save_state
    from promval.main import app

    conn, root = setup
    conn.execute("INSERT INTO team_aliases VALUES ('a', 20603)")
    cached(root)
    db_path = root / "synthetic.db"
    with sqlite3.connect(db_path) as target:
        conn.commit()
        conn.backup(target)
    fetchers = {
        "vlr_fetch": lambda url: (
            listing() if url.endswith("/matches") else "" if "?page=" in url else page()
        ),
        "kalshi_fetch": lambda url: {"markets": []},
    }
    expected = export(db=db_path, now=NOW, **fetchers)
    path = root / "state.pkl.gz"
    state = build_state(conn, root)
    save_state(state, path)
    restored = load_state(path)
    assert restored["team_aliases"] == {"a": 20603}
    assert restored["version"] == 1 and restored["rated_teams"]
    assert restored["built"].endswith("Z")

    def forbidden(*args, **kwargs):
        raise AssertionError("Snapshot export must not open a DB")

    monkeypatch.setattr(sqlite3, "connect", forbidden)
    monkeypatch.setattr(
        feed_module, "export", lambda *a, **kw: export(*a, now=NOW, **fetchers, **kw)
    )
    output = root / "snapshot.json"
    result = CliRunner().invoke(
        app, ["export", "--state", str(path), "--out", str(output)]
    )
    assert result.exit_code == 0, result.output
    assert json.loads(output.read_text()) == expected
    # Reusing one state cannot mutate its reconstructed finals.
    assert export(state=restored, now=NOW, **fetchers) == expected
    assert export(state=restored, now=NOW, **fetchers) == expected


def test_snapshot_rejects_incompatible_version(setup):
    from promval.feed import load_state, save_state

    _, root = setup
    path = root / "state.pkl.gz"
    save_state({"version": 999}, path)
    with pytest.raises(
        ValueError, match=r"Unsupported feed state version 999.*feed-state"
    ):
        load_state(path)
