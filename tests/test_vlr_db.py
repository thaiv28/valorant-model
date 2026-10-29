"""Build the relational database from fixture cache, without network access."""

import importlib.util
import json
import shutil
import sqlite3
from pathlib import Path

import pytest

from promval.vlr import cache

REPO = Path(__file__).resolve().parents[1]
FIXTURES = REPO / "tests" / "fixtures" / "vlr"


@pytest.fixture
def builder(tmp_path, monkeypatch):
    monkeypatch.setenv("PROMVAL_DATA", str(tmp_path / "data"))
    target = cache.root() / "matches"
    target.mkdir(parents=True)
    for path in FIXTURES.glob("match_*.html.gz"):
        shutil.copyfile(path, target / path.name.removeprefix("match_"))
    (tmp_path / "db").mkdir()
    with sqlite3.connect(tmp_path / "db" / "valorant.db") as conn:
        conn.executescript((REPO / "scripts" / "001_create_tables.sql").read_text())
    spec = importlib.util.spec_from_file_location(
        "load_vlr", REPO / "scripts" / "002_load_vlr.py"
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    monkeypatch.setattr(module, "REPO", tmp_path)
    return module, tmp_path


def test_fixture_build(builder, capsys):
    loader, root = builder
    loader.main()
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
    # This error occurs during insertion, after the match/veto rows are inserted.
    cache.save(
        cache.economy_path(610432),
        cache.load(FIXTURES / "match_773441_economy.html.gz"),
    )
    cache.match_path(6805).write_bytes(b"not gzip")
    loader.main()
    assert "matches=2 maps=5 rounds=94 players=50 errors=3" in capsys.readouterr().out
    errors = (root / "db" / "parse_errors.txt").read_text()
    assert all(str(id) in errors for id in (163803, 610432, 6805))
    with sqlite3.connect(root / "db" / "valorant.db") as conn:
        assert conn.execute(
            "SELECT match_id FROM matches ORDER BY match_id"
        ).fetchall() == [(654971,), (773441,)]
        assert conn.execute("PRAGMA foreign_key_check").fetchall() == []


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
    loader.main()
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
