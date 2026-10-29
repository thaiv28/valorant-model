"""Load the raw cache into SQLite, isolating errors by match."""

import argparse
import json
import os
import sqlite3
import sys
import time
from collections import deque
from concurrent.futures import ProcessPoolExecutor
from contextlib import nullcontext
from dataclasses import asdict
from itertools import islice
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))

from promval.vlr import cache
from promval.vlr.parse import ParseError, parse_economy, parse_match


def insert(conn, table, rows):
    if not rows:
        return
    values = rows[0]
    columns = ", ".join(f'"{k}"' for k in values)
    placeholders = ", ".join("?" for _ in values)
    conn.executemany(
        f"INSERT INTO {table} ({columns}) VALUES ({placeholders})",
        [list(row.values()) for row in rows],
    )


def validate_match(match, economy):
    games = {m.game_id: m for m in match.maps}
    if economy.keys() - games.keys():
        raise ParseError(match.match_id, "economy contains unknown played maps")
    for game in match.maps:
        if game.game_id in economy:
            for team in economy[game.game_id].teams:
                # The economy tab omits overtime rounds.
                if team.rounds and len(team.rounds) != min(len(game.rounds), 24):
                    raise ParseError(
                        match.match_id, "economy round count disagrees with map"
                    )


def load_match(conn, match, economy):
    validate_match(match, economy)
    rows = {
        table: []
        for table in ("matches", "vetoes", "maps", "rounds", "player_maps", "economy")
    }
    values = asdict(match)
    for field in ("maps", "veto"):
        values.pop(field)
    for name in ("team1", "team2"):
        team = values.pop(name)
        values[name + "_name"] = team["name"]
        values[name + "_id"] = team["team_id"]
    rows["matches"].append(values)
    for veto in match.veto:
        rows["vetoes"].append({"match_id": match.match_id, **asdict(veto)})
    for game in match.maps:
        values = asdict(game)
        values.pop("rounds")
        values.pop("players")
        rows["maps"].append({"match_id": match.match_id, **values})
        for rnd in game.rounds:
            values = asdict(rnd)
            values["round"] = values.pop("number")
            rows["rounds"].append({"game_id": game.game_id, **values})
        for player in game.players:
            values = asdict(player)
            values["agents"] = json.dumps(values["agents"], ensure_ascii=False)
            rows["player_maps"].append({"game_id": game.game_id, **values})
        if game.game_id in economy:
            for team in economy[game.game_id].teams:
                values = asdict(team)
                values["rounds"] = json.dumps(values["rounds"]) if team.rounds else None
                rows["economy"].append({"game_id": game.game_id, **values})
    for table, values in rows.items():
        insert(conn, table, values)


def parse_one(match_id):
    """Workers only read raw pages and write parsed cache; SQLite stays in main."""
    try:
        match = parse_match(cache.load(cache.match_path(match_id)), match_id)
        ep = cache.economy_path(match_id)
        economy = parse_economy(cache.load(ep)) if cache.has(ep) else {}
        validate_match(match, economy)
        result = (match, economy)
        cache.save_parsed(match_id, result)
        return match_id, result, None
    except Exception as exc:
        return match_id, None, str(exc).replace(chr(10), " ")


def parallel_results(pool, match_ids, jobs):
    # Bound queued results so a slow insert cannot retain 30k parsed matches.
    remaining = iter(match_ids)
    pending = deque(pool.submit(parse_one, mid) for mid in islice(remaining, jobs * 2))
    while pending:
        yield pending.popleft().result()
        match_id = next(remaining, None)
        if match_id is not None:
            pending.append(pool.submit(parse_one, match_id))


def positive_jobs(value):
    value = int(value)
    if value < 1:
        raise argparse.ArgumentTypeError("jobs must be at least 1")
    return value


def main(argv=()):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--jobs",
        type=positive_jobs,
        default=os.environ.get("PROMVAL_JOBS", min(os.cpu_count() or 1, 8)),
    )
    jobs = parser.parse_args(argv).jobs
    start = time.monotonic()
    directory = REPO / "db"
    directory.mkdir(exist_ok=True)
    errors = []
    match_ids = []
    for path in (cache.root() / "matches").glob("*.html.gz"):
        if path.name.endswith("_economy.html.gz"):
            continue
        match_id = path.name.removesuffix(".html.gz")
        try:
            match_ids.append(int(match_id))
        except ValueError as exc:
            errors.append(f"{match_id}: {str(exc).replace(chr(10), ' ')}")
    match_ids.sort()
    cached = {match_id for match_id in match_ids if cache.has_parsed(match_id)}
    to_parse = [match_id for match_id in match_ids if match_id not in cached]
    pool = ProcessPoolExecutor(max_workers=jobs) if jobs > 1 and to_parse else None
    with (
        sqlite3.connect(directory / "valorant.db") as conn,
        pool if pool is not None else nullcontext(),
    ):
        conn.execute("PRAGMA foreign_keys = ON")
        results = iter(
            parallel_results(pool, to_parse, jobs) if pool else map(parse_one, to_parse)
        )
        for match_id in match_ids:
            try:
                if match_id in cached:
                    match, economy = cache.load_parsed(match_id)
                else:
                    _, result, error = next(results)
                    if error is not None:
                        errors.append(f"{match_id}: {error}")
                        continue
                    match, economy = result
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
        f"errors={len(errors)} seconds={time.monotonic() - start:.2f} "
        f"parsed={len(to_parse)} cached={len(cached)} jobs={jobs}"
    )


if __name__ == "__main__":
    main(sys.argv[1:])
