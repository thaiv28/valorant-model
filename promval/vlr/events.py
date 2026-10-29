"""VLR event listings: pure parsing and refreshable raw collection."""

import re
from dataclasses import dataclass

from bs4 import BeautifulSoup

from promval.vlr import cache

TIERS = {60: "vct", 61: "vcl", 62: "t3", 63: "gc", 64: "collegiate", 67: "offseason"}
PRIORITY = [60, 63, 61, 67, 62, 64]
INTERNATIONAL = re.compile(
    r"\bMasters\s+\S|^Valorant Champions \d{4}\b|"
    r"^Champions Tour \d{4}: Champions\b|LOCK//IN|Esports World Cup|"
    r"Game Changers( \d{4})?:? Championship",
    re.IGNORECASE,
)
# Third-party "Masters" cups are common in T3/collegiate lists; qualifiers are regional.
INTERNATIONAL_SECTIONS = {"vct", "gc", "offseason"}


def is_international(name: str, section: str) -> bool:
    return (
        section in INTERNATIONAL_SECTIONS
        and "qualifier" not in name.casefold()
        and bool(INTERNATIONAL.search(name))
    )


@dataclass
class EventRow:
    event_id: int
    slug: str
    name: str
    status: str | None = None
    dates: str | None = None
    region: str | None = None
    prize: str | None = None


def parse_event_list(html: str) -> list[EventRow]:
    soup = BeautifulSoup(html, "lxml")
    rows = {}
    for node in soup.select('a[href^="/event/"]'):
        link = re.fullmatch(r"/event/(\d+)/([^/?]+)/?", node["href"])
        if not link:
            continue
        for label in node.select(".event-item-desc-item-label"):
            label.decompose()

        def text(selector, card=node):
            item = card.select_one(selector)
            if item is None:
                return None
            return " ".join(item.stripped_strings) or None

        flag = node.select_one(".flag")
        region = (
            next(
                (
                    c.removeprefix("mod-")
                    for c in flag.get("class", [])
                    if c.startswith("mod-")
                ),
                None,
            )
            if flag
            else None
        )
        row = EventRow(
            int(link[1]),
            link[2],
            text(".event-item-title"),
            text(".event-item-desc-item-status"),
            text(".mod-dates"),
            region,
            text(".mod-prize"),
        )
        rows[row.event_id] = row
    return list(rows.values())


@dataclass
class Summary:
    pages_read: int = 0
    events: int = 0


def crawl_events(fetcher) -> Summary:
    summary = Summary()
    ids = set()
    for tier in TIERS:
        page = 1
        while True:
            html = fetcher.text(f"https://www.vlr.gg/events/?tier={tier}&page={page}")
            cache.save(cache.events_path(tier, page), html)
            rows = parse_event_list(html)
            summary.pages_read += 1
            ids.update(row.event_id for row in rows)
            if not rows:
                # A listing can shrink; discard obsolete trailing cached pages.
                for path in cache.events_path(tier, page).parent.glob(
                    f"tier{tier}_p*.html.gz"
                ):
                    cached_page = int(path.name.split("_p")[1].split(".")[0])
                    if cached_page > page:
                        path.unlink()
                break
            page += 1
    summary.events = len(ids)
    return summary
