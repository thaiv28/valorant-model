# Tech

## Stack

Python ≥ 3.12 with uv; SQLite rebuilt from raw caches; raw SQL; Typer CLI (`promval`); BeautifulSoup + lxml for HTML; ruff; pytest (offline, fixtures in `tests/fixtures/`).

## Layout

| Path | Purpose |
|---|---|
| `promval/main.py` | CLI entry; mounts the `kalshi` and `vlr` command groups |
| `promval/kalshi/` | Kalshi collector |
| `promval/vlr/` | VLR.gg crawler, raw cache and parsers |
| `scripts/001_create_tables.sql`, `002_load_vlr.py`, `setup_db.sh` | Rebuild SQLite from VLR cache |
| `scripts/work_log.py`, `.githooks/` | Work-log tooling |
| `tests/test_vlr_*.py` | Offline parser, crawl and DB checks |
| `tests/test_steering.py` | Doc guard |
| `tests/fixtures/` | Saved Kalshi JSON and gzipped VLR pages |

## Kalshi collector

Not built yet.

## VLR scraper

Run `uv run promval vlr crawl --since 2021-01-01`; options: `--economy-since 2023-01-01`, `--max-matches N`, `--min-interval 2.0`, `--full` (walk back to `--since` past cached pages; use it to resume an interrupted backfill, since a normal run stops after 3 pages with nothing new). Build offline with `bash scripts/setup_db.sh`; it deletes and rebuilds `db/valorant.db` in numeric script order. Failures roll back one match, continue, and log to `db/parse_errors.txt`.

Cache: `${PROMVAL_DATA:-data}/vlr/raw/matches/<id>.html.gz` and `<id>_economy.html.gz`. Writes use atomic gzip replacement. Results listings are uncached. Never re-fetch cached match pages; missing economy tabs can be retried independently. Skip same-day matches until tomorrow (Eastern date). Stop at empty/older pages, three consecutive pages without new work, or the match limit.

Requests start at least 2 seconds apart. User-Agent: `valorant-model/0.1 (+https://github.com/thaiv28/valorant-model)`. Retry 429, 5xx, URL errors and timeouts up to five attempts, sleeping 5/10/20/40 seconds. Fetching is injectable; parsers never fetch.

Results parser extracts IDs, slugs and day headings. Match parser extracts event/stage, team IDs/names, best-of, patch, UTC start, series score/winner, ordered veto (short tags; “remains” is decider), played maps, picks, scores, side totals, duration, overtime beyond 24 rounds, players/agents/stats, and round winners/sides/types. Skip unplayed maps. Missing stats are null. Reject inconsistent round counts, round wins or series map wins. An 11–13 score is 24 regulation rounds, not overtime. A drawn series (1–1 Bo2) has a null winner. The economy tab omits overtime rounds, so its per-round rows cover regulation only.

Economy fixtures (2020–2026) show pistol/conversion/bonus won/played, eco (<10k), half buy (10–18k), full buy (18k+) matchup counts, plus per-round team equipment and bank amounts (displayed in thousands). Summary grids exclude each half’s first three rounds; aggregate their counts by own buy category. Preserve every round’s category/buy/bank. Separate semi-eco and semi-buy are absent, stored null; half buy stays separate. Unavailable values remain null.

Tables: `matches` (match_id), `vetoes` (match_id/step), `maps` (game_id), `rounds` (game_id/round), `player_maps` (game_id/player_id), `economy` (game_id/team); declared foreign keys connect them. Agents and economy round details use JSON text; other fields are scalar SQL columns.

Time gotcha: VLR `data-utc-ts` is America/New_York local time, despite its name. Convert with zoneinfo (EST/EDT) to ISO UTC ending Z.

Backfill estimate: roughly 590 results pages back to 2021, about 29k matches; approximately two requests per match from 2023 and one before, at 2 seconds, roughly a day of crawling. Not run against the live site.
