"""Load the raw cache into SQLite, isolating errors by match."""

import json
import sqlite3
import sys
import time
from dataclasses import asdict
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))

from promval.vlr import cache
from promval.vlr.parse import ParseError, parse_economy, parse_match


def insert(conn, table, values):
    columns = ", ".join(f'"{k}"' for k in values)
    placeholders = ", ".join("?" for _ in values)
    conn.execute(
        f"INSERT INTO {table} ({columns}) VALUES ({placeholders})",
        list(values.values()),
    )


def load_match(conn, match, economy):
    values = asdict(match)
    for field in ("maps", "veto"):
        values.pop(field)
    for name in ("team1", "team2"):
        team = values.pop(name)
        values[name + "_name"] = team["name"]
        values[name + "_id"] = team["team_id"]
    insert(conn, "matches", values)
    for veto in match.veto:
        insert(conn, "vetoes", {"match_id": match.match_id, **asdict(veto)})
    games = {m.game_id: m for m in match.maps}
    if economy.keys() - games.keys():
        raise ParseError(match.match_id, "economy contains unknown played maps")
    for game in match.maps:
        values = asdict(game)
        values.pop("rounds")
        values.pop("players")
        insert(conn, "maps", {"match_id": match.match_id, **values})
        for rnd in game.rounds:
            values = asdict(rnd)
            values["round"] = values.pop("number")
            insert(conn, "rounds", {"game_id": game.game_id, **values})
        for player in game.players:
            values = asdict(player)
            values["agents"] = json.dumps(values["agents"], ensure_ascii=False)
            insert(conn, "player_maps", {"game_id": game.game_id, **values})
        if game.game_id in economy:
            for team in economy[game.game_id].teams:
                # The economy tab omits overtime rounds.
                if team.rounds and len(team.rounds) != min(len(game.rounds), 24):
                    raise ParseError(
                        match.match_id, "economy round count disagrees with map"
                    )
                values = asdict(team)
                values["rounds"] = json.dumps(values["rounds"]) if team.rounds else None
                insert(conn, "economy", {"game_id": game.game_id, **values})


def main():
    start = time.monotonic()
    directory = REPO / "db"
    directory.mkdir(exist_ok=True)
    errors = []
    with sqlite3.connect(directory / "valorant.db") as conn:
        conn.execute("PRAGMA foreign_keys = ON")
        for path in sorted((cache.root() / "matches").glob("*.html.gz")):
            if path.name.endswith("_economy.html.gz"):
                continue
            match_id = path.name.removesuffix(".html.gz")
            try:
                match_id = int(match_id)
                match = parse_match(cache.load(path), match_id)
                ep = cache.economy_path(match_id)
                economy = parse_economy(cache.load(ep)) if cache.has(ep) else {}
                with conn:
                    load_match(conn, match, economy)
            except Exception as exc:
                errors.append(f"{match_id}: {str(exc).replace(chr(10), ' ')}")
        counts = [
            conn.execute(f"SELECT count(*) FROM {table}").fetchone()[0]
            for table in ("matches", "maps", "rounds", "player_maps")
        ]
    (directory / "parse_errors.txt").write_text("".join(e + "\n" for e in errors))
    print(
        f"matches={counts[0]} maps={counts[1]} rounds={counts[2]} players={counts[3]} "
        f"errors={len(errors)} seconds={time.monotonic() - start:.2f}"
    )


if __name__ == "__main__":
    main()
