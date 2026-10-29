"""Incremental results walk; raw pages are the permanent source of truth."""

from concurrent.futures import ThreadPoolExecutor
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
    workers=1,
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
        tasks = []
        for row in rows:
            if row.day < since or row.day >= today:
                continue
            need_match = not cache.has(cache.match_path(row.match_id))
            need_economy = row.day >= economy_since and not cache.has(
                cache.economy_path(row.match_id)
            )
            if not need_match:
                summary.skipped += 1
            if need_match or need_economy:
                tasks.append((row.match_id, need_match, need_economy))
        if max_matches is not None:
            # Keep economy-only tasks; cap the new match pages at the remaining quota.
            room, kept = max_matches - summary.matches_fetched, []
            for task in tasks:
                if task[1]:
                    if room <= 0:
                        continue
                    room -= 1
                kept.append(task)
            tasks = kept
        attempted = bool(tasks)
        if workers > 1 and len(tasks) > 1:
            with ThreadPoolExecutor(max_workers=workers) as pool:
                results = list(pool.map(lambda t: _fetch(fetcher, *t), tasks))
        else:
            results = [_fetch(fetcher, *task) for task in tasks]
        for fetched_match, fetched_economy, errors in results:
            summary.matches_fetched += fetched_match
            summary.economy_fetched += fetched_economy
            summary.errors += errors
        if max_matches is not None and summary.matches_fetched >= max_matches:
            return summary
        # Failed requests still count as new work, never as a known page.
        known_pages = 0 if attempted else known_pages + 1
        if known_pages >= stop_after_known_pages:
            break
        page += 1
    return summary


def _fetch(fetcher, match_id, need_match, need_economy):
    """Fetch and cache one match's missing pages: (match, economy, errors) counts."""
    fetched_match = fetched_economy = errors = 0
    if need_match:
        try:
            cache.save(
                cache.match_path(match_id),
                fetcher.text(f"https://www.vlr.gg/{match_id}"),
            )
            fetched_match = 1
        except Exception:
            return 0, 0, 1
    if need_economy:
        try:
            cache.save(
                cache.economy_path(match_id),
                fetcher.text(f"https://www.vlr.gg/{match_id}/?game=all&tab=economy"),
            )
            fetched_economy = 1
        except Exception:
            errors += 1
    return fetched_match, fetched_economy, errors
