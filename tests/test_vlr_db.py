"""Build the relational database from fixture cache, without network access."""

import importlib
import json
import os
import shutil
import sqlite3
from pathlib import Path

import pytest

from promval.vlr import cache, parse

REPO = Path(__file__).resolve().parents[1]
FIXTURES = REPO / "tests" / "fixtures" / "vlr"


@pytest.fixture
def builder(tmp_path, monkeypatch):
    monkeypatch.setenv("PROMVAL_DATA", str(tmp_path / "data"))
    monkeypatch.setenv("PROMVAL_JOBS", "1")
    target = cache.root() / "matches"
    target.mkdir(parents=True)
    for path in FIXTURES.glob("match_*.html.gz"):
        shutil.copyfile(path, target / path.name.removeprefix("match_"))
    (tmp_path / "db").mkdir()
    with sqlite3.connect(tmp_path / "db" / "valorant.db") as conn:
        conn.executescript((REPO / "scripts" / "001_create_tables.sql").read_text())
    # Import by its real module name so spawn workers can import it, too.
    monkeypatch.syspath_prepend(str(REPO / "scripts"))
    module = importlib.import_module("002_load_vlr")
    monkeypatch.setattr(module, "REPO", tmp_path)
    return module, tmp_path


def test_fixture_build(builder, capsys):
    loader, root = builder
    loader.main([])
    assert (
        "matches=5 maps=10 rounds=188 players=100 errors=0" in capsys.readouterr().out
    )
    assert (root / "db" / "parse_errors.txt").read_text() == ""
    with sqlite3.connect(root / "db" / "valorant.db") as conn:
        for table, count in [
            ("matches", 5),
            ("vetoes", 21),
            ("maps", 10),
            ("rounds", 188),
            ("player_maps", 100),
            ("economy", 20),
        ]:
            assert conn.execute(f"SELECT count(*) FROM {table}").fetchone()[0] == count
        assert conn.execute("PRAGMA foreign_key_check").fetchall() == []
        assert (
            conn.execute(
                "SELECT start_utc FROM matches WHERE match_id=6805"
            ).fetchone()[0]
            == "2020-11-29T02:00:00Z"
        )
        agents = conn.execute(
            "SELECT agents FROM player_maps WHERE game_id=286505 AND player_id=35660"
        ).fetchone()[0]
        assert json.loads(agents) == ["chamber"]
        rounds = conn.execute(
            "SELECT rounds FROM economy WHERE game_id=286505 AND team=1"
        ).fetchone()[0]
        assert len(json.loads(rounds)) == 22
        assert (
            conn.execute("SELECT semi_eco_played FROM economy").fetchall()
            == [(None,)] * 20
        )


def test_bad_match_does_not_abort_or_leave_partial_rows(builder, capsys):
    loader, root = builder
    cache.save(cache.match_path(163803), "broken page")
    # Economy belonging to another match must also be isolated.
    cache.save(
        cache.economy_path(610432),
        cache.load(FIXTURES / "match_773441_economy.html.gz"),
    )
    cache.match_path(6805).write_bytes(b"not gzip")
    loader.main([])
    assert "matches=2 maps=5 rounds=94 players=50 errors=3" in capsys.readouterr().out
    errors = (root / "db" / "parse_errors.txt").read_text()
    assert all(str(id) in errors for id in (163803, 610432, 6805))
    with sqlite3.connect(root / "db" / "valorant.db") as conn:
        assert conn.execute(
            "SELECT match_id FROM matches ORDER BY match_id"
        ).fetchall() == [(654971,), (773441,)]
        assert conn.execute("PRAGMA foreign_key_check").fetchall() == []
    assert all(not cache.parsed_path(mid).exists() for mid in (163803, 610432, 6805))


def test_draw_and_overtime_economy_regressions(builder, capsys):
    """Real pages: 29754 is a 1–1 Bo2 draw; 582286 has a 14–12 map whose
    economy tab lists only the 24 regulation rounds."""
    loader, tmp_path = builder
    target = cache.root() / "matches"
    for path in target.glob("*.html.gz"):
        path.unlink()
    for name in ("29754", "582286", "582286_economy"):
        shutil.copyfile(
            FIXTURES / f"regress_{name}.html.gz", target / f"{name}.html.gz"
        )
    loader.main([])
    assert "errors=0" in capsys.readouterr().out
    with sqlite3.connect(tmp_path / "db" / "valorant.db") as conn:
        assert conn.execute(
            "SELECT score1, score2, winner FROM matches WHERE match_id = 29754"
        ).fetchone() == (1, 1, None)
        overtime = conn.execute(
            "SELECT game_id FROM maps WHERE match_id = 582286 AND overtime > 0"
        ).fetchall()
        assert overtime
        assert conn.execute(
            "SELECT count(*) FROM economy WHERE game_id = ?", overtime[0]
        ).fetchone() == (2,)


TABLES = ("matches", "vetoes", "maps", "rounds", "player_maps", "economy")


def reset_db(root):
    path = root / "db" / "valorant.db"
    path.unlink()
    with sqlite3.connect(path) as conn:
        conn.executescript((REPO / "scripts" / "001_create_tables.sql").read_text())


def table_contents(root):
    with sqlite3.connect(root / "db" / "valorant.db") as conn:
        return {
            table: conn.execute(f"SELECT * FROM {table} ORDER BY rowid").fetchall()
            for table in TABLES
        }


def test_warm_cache_never_parses(builder, monkeypatch, capsys):
    loader, root = builder
    loader.main([])
    expected = table_contents(root)
    reset_db(root)

    def fail(*args):
        raise AssertionError("warm rebuild called a parser")

    monkeypatch.setattr(loader, "parse_match", fail)
    monkeypatch.setattr(loader, "parse_economy", fail)
    capsys.readouterr()
    loader.main([])
    assert "parsed=0 cached=5 jobs=1" in capsys.readouterr().out
    assert table_contents(root) == expected
    assert (root / "db" / "parse_errors.txt").read_text() == ""


@pytest.mark.parametrize("raw_path", [cache.match_path, cache.economy_path])
def test_raw_newer_than_pickle_is_reparsed(builder, monkeypatch, capsys, raw_path):
    loader, root = builder
    loader.main([])
    expected = table_contents(root)
    reset_db(root)
    match_id = 773441
    raw = raw_path(match_id)
    stamp = cache.parsed_path(match_id).stat().st_mtime_ns + 1
    os.utime(raw, ns=(stamp, stamp))
    assert not cache.has_parsed(match_id)
    calls = []
    original = loader.parse_match

    def recording_parser(html, mid):
        calls.append(mid)
        return original(html, mid)

    monkeypatch.setattr(loader, "parse_match", recording_parser)
    capsys.readouterr()
    loader.main([])
    assert "parsed=1 cached=4 jobs=1" in capsys.readouterr().out
    assert calls == [match_id]
    assert cache.has_parsed(match_id)
    assert table_contents(root) == expected


def test_parser_version_uses_new_directory(builder, monkeypatch, capsys):
    loader, root = builder
    loader.main([])
    old = cache.parsed_path(773441)
    expected = table_contents(root)
    reset_db(root)
    monkeypatch.setattr(parse, "PARSER_VERSION", parse.PARSER_VERSION + 1)
    new = cache.parsed_path(773441)
    assert new.parent.name == f"v{parse.PARSER_VERSION}"
    assert new != old
    assert not cache.has_parsed(773441)
    capsys.readouterr()
    loader.main([])
    assert "parsed=5 cached=0 jobs=1" in capsys.readouterr().out
    assert old.is_file() and new.is_file()
    assert table_contents(root) == expected


def test_parallel_and_serial_cold_and_warm_rows_match(builder, capsys):
    loader, root = builder
    loader.main(["--jobs", "1"])
    expected = table_contents(root)
    shutil.rmtree(cache.parsed_path(773441).parent)
    for warm in (False, True):
        reset_db(root)
        capsys.readouterr()
        loader.main(["--jobs", "2"])
        output = capsys.readouterr().out
        assert ("parsed=0 cached=5" if warm else "parsed=5 cached=0") in output
        assert "jobs=2" in output
        assert table_contents(root) == expected
        assert (root / "db" / "parse_errors.txt").read_text() == ""


@pytest.mark.parametrize("jobs", [1, 2])
def test_parse_errors_are_retried_and_not_cached(builder, capsys, jobs):
    loader, root = builder
    cache.save(cache.match_path(163803), "broken page")
    for _ in range(2):
        loader.main(["--jobs", str(jobs)])
        assert "errors=1" in capsys.readouterr().out
        errors = (root / "db" / "parse_errors.txt").read_text()
        assert errors.startswith("163803: ")
        assert len(errors.splitlines()) == 1
        assert not cache.parsed_path(163803).exists()
        reset_db(root)


def test_insert_failure_rolls_back_every_table(builder, monkeypatch, capsys):
    loader, root = builder
    original = loader.insert

    def failing_insert(conn, table, rows):
        if table == "economy" and rows:
            match_id = conn.execute(
                "SELECT match_id FROM maps WHERE game_id = ?", (rows[0]["game_id"],)
            ).fetchone()[0]
            if match_id == 610432:
                raise sqlite3.IntegrityError("injected economy insert failure")
        return original(conn, table, rows)

    monkeypatch.setattr(loader, "insert", failing_insert)
    loader.main([])
    assert "errors=1" in capsys.readouterr().out
    assert (root / "db" / "parse_errors.txt").read_text() == (
        "610432: injected economy insert failure\n"
    )
    with sqlite3.connect(root / "db" / "valorant.db") as conn:
        for table in ("matches", "vetoes", "maps"):
            assert (
                conn.execute(
                    f"SELECT * FROM {table} WHERE match_id = 610432"
                ).fetchall()
                == []
            )
        assert conn.execute("PRAGMA foreign_key_check").fetchall() == []
        assert conn.execute("SELECT count(*) FROM matches").fetchone()[0] == 4
