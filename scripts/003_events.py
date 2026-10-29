"""Build event tiers from cached VLR lists; no network access."""

import json
import sqlite3
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))

from promval.vlr import cache
from promval.vlr.events import PRIORITY, TIERS, is_international, parse_event_list

OVERRIDES = REPO / "promval" / "vlr" / "event_overrides.json"


def build(conn, overrides=None):
    if overrides is None:
        overrides = json.loads(OVERRIDES.read_text())
    conn.execute("""CREATE TABLE events (
        event_id INTEGER PRIMARY KEY, slug TEXT, name TEXT, vlr_tier INTEGER,
        section TEXT, tiers TEXT, international INTEGER,
        status TEXT, dates TEXT, region TEXT, prize TEXT
    )""")
    events, memberships, pages = {}, {}, 0
    for tier in PRIORITY:
        paths = sorted(
            (cache.root() / "events").glob(f"tier{tier}_p*.html.gz"),
            key=lambda p: int(p.name.split("_p")[1].split(".")[0]),
        )
        for path in paths:
            pages += 1
            rows = parse_event_list(cache.load(path))
            if not rows:
                break
            for row in rows:
                events.setdefault(row.event_id, row)
                memberships.setdefault(row.event_id, set()).add(tier)
    for event_id, row in events.items():
        tiers = sorted(memberships[event_id])
        primary = next(t for t in PRIORITY if t in tiers)
        override = overrides.get(str(event_id), {})
        section = override.get("section", TIERS[primary])
        international = override.get(
            "international", is_international(row.name, section)
        )
        conn.execute(
            "INSERT INTO events VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (
                event_id,
                row.slug,
                row.name,
                primary,
                section,
                json.dumps(tiers),
                int(international),
                row.status,
                row.dates,
                row.region,
                row.prize,
            ),
        )
    print(
        f"events={len(events)} pages={pages}"
        + (" (no cached pages)" if not pages else "")
    )


def main():
    with sqlite3.connect(REPO / "db" / "valorant.db") as conn:
        build(conn)


if __name__ == "__main__":
    main()
