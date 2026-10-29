"""Offline event-list parsing, collection, tier assignment and pool history."""

import importlib.util
import json
import shutil
import sqlite3
from pathlib import Path
from urllib.parse import parse_qs, urlparse

import pytest
from test_vlr_db import builder  # noqa: F401
from typer.testing import CliRunner

from promval.vlr import cache, cli
from promval.vlr.events import TIERS, crawl_events, is_international, parse_event_list

REPO = Path(__file__).resolve().parents[1]
FIXTURES = REPO / "tests" / "fixtures" / "vlr"


def script(name):
    spec = importlib.util.spec_from_file_location(name, REPO / "scripts" / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@pytest.mark.parametrize(
    "path", sorted(FIXTURES.glob("events_*.html.gz")), ids=lambda p: p.name
)
def test_lists(path):
    rows = parse_event_list(cache.load(path))
    if "tier62_p35" in path.name:
        assert rows == []
        return
    assert rows
    assert all(row.event_id > 0 and row.slug and row.name for row in rows)
    assert all(row.status in {"completed", "ongoing", "upcoming"} for row in rows)
    if "tier63_p1" in path.name:
        row = next(
            r for r in rows if r.slug == "game-changers-2026-championship-s-o-paulo"
        )
        assert (row.name, row.status, row.dates, row.region, row.prize) == (
            "Game Changers 2026: Championship São Paulo",
            "ongoing",
            "Oct 22—Nov 2",
            "br",
            "$500,000",
        )
    if "tier60_p6" in path.name:
        assert "champions-tour-korea-stage-1-challengers-2" in {r.slug for r in rows}


def test_absent_fields():
    (row,) = parse_event_list(
        '<a href="/event/1/test"><div class="event-item-title">Test</div></a>'
    )
    assert (row.status, row.dates, row.region, row.prize) == (None,) * 4


class FakeFetcher:
    def __init__(self):
        self.calls = []

    def text(self, url):
        params = parse_qs(urlparse(url).query)
        tier, page = int(params["tier"][0]), int(params["page"][0])
        self.calls.append((tier, page))
        assert page <= 2
        return cache.load(
            FIXTURES
            / (
                f"events_tier{tier}_p1.html.gz"
                if page == 1
                else "events_tier62_p35.html.gz"
            )
        )


def test_crawl_refresh_and_stop(tmp_path, monkeypatch):
    monkeypatch.setenv("PROMVAL_DATA", str(tmp_path))
    cache.save(cache.events_path(60, 1), "obsolete")
    cache.save(cache.events_path(60, 3), "obsolete trailing page")
    fetcher = FakeFetcher()
    result = crawl_events(fetcher)
    assert result.pages_read == 12 and result.events > 0
    assert fetcher.calls == [(t, p) for t in TIERS for p in (1, 2)]
    for tier, page in fetcher.calls:
        assert cache.events_path(tier, page).is_file()
        assert bool(parse_event_list(cache.load(cache.events_path(tier, page)))) == (
            page == 1
        )
    assert not cache.events_path(60, 3).exists()


def test_cli(monkeypatch):
    fetcher = FakeFetcher()
    monkeypatch.setattr(cli, "Fetcher", lambda: fetcher)
    # Collection itself is covered above; avoid writing the default raw cache.
    import promval.vlr.events as events

    monkeypatch.setattr(
        events,
        "crawl_events",
        lambda f: events.Summary(12, 100) if f is fetcher else None,
    )
    result = CliRunner().invoke(cli.app, ["events"])
    assert result.exit_code == 0
    assert result.stdout == "pages=12 events=100\n"


@pytest.mark.parametrize(
    "name,expected",
    [
        ("Champions Tour 2024: Masters Madrid", True),
        ("Valorant Champions 2025", True),
        ("Champions Tour 2023: LOCK//IN São Paulo", True),
        ("Esports World Cup 2026", True),
        ("Champions Tour 2021: Champions", True),
        ("Champions Tour North America Stage 2: Masters", False),
        ("VCT 2026: Americas Stage 1", False),
        ("China Evolution Series 2026: Act 3", False),
        ("Game Changers 2026: Championship São Paulo", True),
        ("Valorant Masters London 2026", True),
    ],
)
def test_international(name, expected):
    section = "offseason" if "World Cup" in name else "vct"
    if "Game Changers" in name:
        section = "gc"
    assert is_international(name, section) is expected


@pytest.mark.parametrize(
    "name,section",
    [
        ("Metafy Masters #1", "t3"),
        ("University Esports Masters 2023", "collegiate"),
        ("Esports World Cup 2026: EMEA Qualifier", "offseason"),
        ("Champions Tour 2023: Champions China Qualifier", "vct"),
    ],
)
def test_not_international(name, section):
    assert not is_international(name, section)


def copy_events():
    for path in FIXTURES.glob("events_*.html.gz"):
        target = cache.root() / "events" / path.name.removeprefix("events_")
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(path, target)


def test_primary_and_overrides(tmp_path, monkeypatch):
    monkeypatch.setenv("PROMVAL_DATA", str(tmp_path))
    copy_events()
    loader = script("003_events")
    overrides = tmp_path / "overrides.json"
    overrides.write_text(
        json.dumps({"3122": {"international": True, "section": "custom"}})
    )
    monkeypatch.setattr(loader, "OVERRIDES", overrides)
    with sqlite3.connect(":memory:") as conn:
        loader.build(conn)
        row = conn.execute(
            "SELECT vlr_tier, section, tiers, international FROM events WHERE slug='project-blender-2026'"
        ).fetchone()
        assert row[:2] == (61, "custom")
        assert json.loads(row[2]) == [61, 67]
        assert row[3] == 1
    # Overrides can also turn off a name-based international classification.
    html = '<a href="/event/1/test"><div class="event-item-title">Valorant Champions 2025</div></a>'
    cache.save(cache.events_path(60, 1), html)
    with sqlite3.connect(":memory:") as conn:
        loader.build(conn, {"1": {"international": False}})
        assert conn.execute(
            "SELECT international FROM events WHERE event_id=1"
        ).fetchone() == (0,)


def test_no_pages(tmp_path, monkeypatch, capsys):
    monkeypatch.setenv("PROMVAL_DATA", str(tmp_path))
    with sqlite3.connect(":memory:") as conn:
        script("003_events").build(conn)
        assert conn.execute("SELECT count(*) FROM events").fetchone() == (0,)
    assert "no cached pages" in capsys.readouterr().out


def synthetic(conn, sequence):
    conn.executescript("""
        CREATE TABLE matches(match_id INTEGER PRIMARY KEY, start_utc TEXT, event_id INTEGER);
        CREATE TABLE vetoes(match_id INTEGER, map TEXT);
        CREATE TABLE events(event_id INTEGER, section TEXT);
    """)
    for i, (pool, event_id) in enumerate(sequence, 1):
        conn.execute(
            "INSERT INTO matches VALUES (?, ?, ?)",
            (i, f"2026-01-{i:02}T00:00:00Z", event_id),
        )
        conn.executemany("INSERT INTO vetoes VALUES (?, ?)", [(i, m) for m in pool])


A = ["Ascent", "Bind", "Breeze", "Haven", "Icebox", "Lotus", "Split"]
B = ["Abyss", *A[1:]]
C = ["Corrode", *A[1:]]


@pytest.mark.parametrize("filtered", [False, True])
def test_pool_history(filtered):
    with sqlite3.connect(":memory:") as conn:
        sequence = [(p, 1) for p in [A, A, A, C, A, A, A, B, B, B]]
        sequence += [(A[:6], 1), (A + ["Fracture"], 1)]
        if filtered:
            sequence += [(C, 2)] * 3
        synthetic(conn, sequence)
        if filtered:
            conn.executemany(
                "INSERT INTO events VALUES (?, ?)", [(1, "vct"), (2, "vcl")]
            )
        script("004_map_pool").build(conn)
        rows = conn.execute(
            "SELECT * FROM map_pool_periods ORDER BY first_utc"
        ).fetchall()
        assert rows == [
            (",".join(sorted(A)), "2026-01-01T00:00:00Z", "2026-01-07T00:00:00Z", 7),
            (",".join(sorted(B)), "2026-01-08T00:00:00Z", "2026-01-10T00:00:00Z", 3),
        ]
        assert conn.execute("SELECT count(*) FROM veto_pools").fetchone() == (
            13 if filtered else 10,
        )
        assert conn.execute(
            "SELECT first_utc, last_utc FROM map_pool WHERE map='Bind'"
        ).fetchall() == [(rows[0][1], rows[1][2])]
        assert conn.execute(
            "SELECT last_utc FROM map_pool WHERE map='Ascent'"
        ).fetchone() == (rows[0][2],)
        assert conn.execute(
            "SELECT first_utc FROM map_pool WHERE map='Abyss'"
        ).fetchone() == (rows[1][1],)


def test_pool_edge_runs_and_returning_maps():
    module = script("004_map_pool")
    assert module.periods([]) == []
    assert module.periods(
        [(str(i), p) for i, p in enumerate(["x", "a", "a", "a", "b"])]
    ) == [("a", "0", "4", 5)]
    assert module.periods([("1", "a"), ("2", "b")]) == [("a", "1", "2", 2)]
    with sqlite3.connect(":memory:") as conn:
        synthetic(conn, [(p, 1) for p in [A] * 3 + [B] * 3 + [A] * 3])
        module.build(conn)
        assert conn.execute(
            "SELECT count(*) FROM map_pool WHERE map='Ascent'"
        ).fetchone() == (2,)
        assert conn.execute(
            "SELECT count(*) FROM map_pool WHERE map='Bind'"
        ).fetchone() == (1,)


def test_fixture_build(request, monkeypatch):
    loader, root = request.getfixturevalue("builder")
    copy_events()
    loader.main()
    for name in ("003_events", "004_map_pool"):
        module = script(name)
        monkeypatch.setattr(module, "REPO", root)
        module.main()
    with sqlite3.connect(root / "db" / "valorant.db") as conn:
        assert conn.execute("SELECT count(*) FROM events").fetchone()[0] > 0
        assert conn.execute("SELECT count(*) FROM veto_pools").fetchone()[0] > 0
        assert conn.execute("PRAGMA foreign_key_check").fetchall() == []
