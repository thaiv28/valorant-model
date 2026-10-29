"""Incremental results walk; raw pages are the permanent source of truth."""

from dataclasses import dataclass
from datetime import date, datetime
from zoneinfo import ZoneInfo

from promval.vlr import cache
from promval.vlr.parse import parse_results_page


@dataclass
class Summary:
    pages_read: int = 0
    matches_fetched: int = 0
    economy_fetched: int = 0
    skipped: int = 0
    errors: int = 0


def crawl(
    fetcher,
    since: date,
    economy_since=date(2023, 1, 1),
    max_matches=None,
    stop_after_known_pages=3,
    today=None,
) -> Summary:
    if max_matches is not None and max_matches < 0:
        raise ValueError("max_matches must be nonnegative")
    if stop_after_known_pages < 1:
        raise ValueError("stop_after_known_pages must be positive")
    today = today or datetime.now(ZoneInfo("America/New_York")).date()
    summary, known_pages = Summary(), 0
    if max_matches == 0:
        return summary
    page = 1
    while True:
        rows = parse_results_page(
            fetcher.text(f"https://www.vlr.gg/matches/results/?page={page}")
        )
        summary.pages_read += 1
        if not rows or all(r.day < since for r in rows):
            break
        attempted = False
        for row in rows:
            if row.day < since or row.day >= today:
                continue
            match = cache.match_path(row.match_id)
            economy = cache.economy_path(row.match_id)
            need_match = not cache.has(match)
            need_economy = row.day >= economy_since and not cache.has(economy)
            if not need_match:
                summary.skipped += 1
            if not (need_match or need_economy):
                continue
            attempted = True
            if need_match:
                try:
                    cache.save(
                        match, fetcher.text(f"https://www.vlr.gg/{row.match_id}")
                    )
                    summary.matches_fetched += 1
                except Exception:
                    summary.errors += 1
                    continue
            if need_economy:
                try:
                    cache.save(
                        economy,
                        fetcher.text(
                            f"https://www.vlr.gg/{row.match_id}/?game=all&tab=economy"
                        ),
                    )
                    summary.economy_fetched += 1
                except Exception:
                    summary.errors += 1
            if max_matches is not None and summary.matches_fetched >= max_matches:
                return summary
        # Failed requests still count as new work, never as a known page.
        known_pages = 0 if attempted else known_pages + 1
        if known_pages >= stop_after_known_pages:
            break
        page += 1
    return summary
