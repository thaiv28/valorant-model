"""Derive seven-map pools and observed active spans from match vetoes."""

import sqlite3
from itertools import groupby
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]


def periods(rows):
    """Absorb short runs into the preceding stable run, or the next at the start.

    Without any run of three, retain one period using the longest observed run.
    Period endpoints are inclusive observed match times, not patch boundaries.
    """
    runs = [list(group) for _, group in groupby(rows, key=lambda row: row[1])]
    if not runs:
        return []
    stable = [i for i, run in enumerate(runs) if len(run) >= 3]
    if not stable:
        pool = max(runs, key=len)[0][1]
        return [(pool, runs[0][0][0], runs[-1][-1][0], sum(map(len, runs)))]
    assigned = []
    pool = runs[stable[0]][0][1]
    for run in runs:
        if len(run) >= 3:
            pool = run[0][1]
        assigned.extend((stamp, pool) for stamp, _ in run)
    result = []
    for pool, group in groupby(assigned, key=lambda row: row[1]):
        group = list(group)
        result.append((pool, group[0][0], group[-1][0], len(group)))
    return result


def build(conn):
    conn.executescript("""
        CREATE TABLE veto_pools (
            match_id INTEGER PRIMARY KEY REFERENCES matches(match_id),
            start_utc TEXT, pool TEXT
        );
        CREATE TABLE map_pool_periods (
            pool TEXT, first_utc TEXT, last_utc TEXT, matches INTEGER
        );
    """)
    rows = conn.execute("""
        SELECT m.match_id, m.start_utc, v.map FROM matches m
        JOIN vetoes v USING (match_id)
        WHERE v.map IS NOT NULL AND v.map != ''
        ORDER BY m.start_utc, m.match_id, v.map
    """)
    pools = []
    for (match_id, stamp), group in groupby(rows, key=lambda row: row[:2]):
        maps = sorted({row[2] for row in group})
        if len(maps) == 7:
            pools.append((match_id, stamp, ",".join(maps)))
    conn.executemany("INSERT INTO veto_pools VALUES (?, ?, ?)", pools)
    has_events = conn.execute("SELECT EXISTS(SELECT 1 FROM events)").fetchone()[0]
    rows = conn.execute(
        "SELECT p.start_utc, p.pool FROM veto_pools p "
        "JOIN matches m USING (match_id) "
        + (
            "JOIN events e ON e.event_id=m.event_id WHERE e.section='vct' "
            if has_events
            else ""
        )
        + "ORDER BY p.start_utc, p.match_id"
    ).fetchall()
    history = periods(rows)
    conn.executemany("INSERT INTO map_pool_periods VALUES (?, ?, ?, ?)", history)
    # Split pools, then merge a map across adjacent periods even if other maps change.
    conn.executescript("""
        CREATE VIEW map_pool AS
        WITH RECURSIVE split(period, first_utc, last_utc, map, rest) AS (
            SELECT rowid, first_utc, last_utc, '', pool || ',' FROM map_pool_periods
            UNION ALL
            SELECT period, first_utc, last_utc,
                   substr(rest, 1, instr(rest, ',') - 1),
                   substr(rest, instr(rest, ',') + 1)
            FROM split WHERE rest != ''
        ), numbered AS (
            SELECT map, first_utc, last_utc,
                   period - row_number() OVER (PARTITION BY map ORDER BY period) AS span
            FROM split WHERE map != ''
        )
        SELECT map, min(first_utc) AS first_utc, max(last_utc) AS last_utc
        FROM numbered GROUP BY map, span;
    """)
    print(f"veto_pools={len(pools)} map_pool_periods={len(history)}")


def main():
    with sqlite3.connect(REPO / "db" / "valorant.db") as conn:
        build(conn)


if __name__ == "__main__":
    main()
