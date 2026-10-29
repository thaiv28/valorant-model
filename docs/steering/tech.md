# Tech

## Stack

Python ≥ 3.12 with uv; SQLite rebuilt from raw caches; raw SQL; Typer CLI (`promval`); BeautifulSoup + lxml for HTML; ruff; pytest (offline, fixtures in `tests/fixtures/`).

## Layout

| Path | Purpose |
|---|---|
| `promval/main.py` | CLI entry; mounts the `kalshi` and `vlr` command groups |
| `promval/kalshi/api.py` | Public HTTP client, pacing, retries and pagination |
| `promval/kalshi/collect.py` | Raw catalog, trade, candle and book files |
| `promval/kalshi/cli.py` | Collector and book-loop commands |
| `tests/test_kalshi_collect.py` | Offline fixture-based collector and CLI tests |
| `promval/vlr/` | VLR.gg crawler, raw cache and parsers |
| `scripts/001_create_tables.sql`, `002_load_vlr.py`, `setup_db.sh` | Rebuild SQLite from VLR cache |
| `scripts/work_log.py`, `.githooks/` | Work-log tooling |
| `tests/test_vlr_*.py` | Offline parser, crawl and DB checks |
| `tests/test_steering.py` | Doc guard |
| `tests/fixtures/` | Saved Kalshi JSON and gzipped VLR pages |

## Kalshi collector

`promval kalshi collect [--no-books] [--limit N]` refreshes both Valorant series (`KXVALORANTGAME`, `KXVALORANTMAP`), saves final-market histories and snapshots active books. `--limit` caps new trade/candle fetches combined (each file attempt counts separately). `promval kalshi books --every 60 --minutes 60` refreshes active tickers each pass; pass summaries include failures. No schedule installed.

Public base: `https://api.elections.kalshi.com/trade-api/v2`. Paginate `/markets` and `/historical/markets` by series; merge by ticker, preferring `/markets`. Historical-catalog markets use `/historical/trades?ticker=T` and `/historical/markets/T/candlesticks`; recent markets use `/markets/trades?ticker=T` and `/series/S/markets/T/candlesticks`. Trades paginate with `limit=1000`; hourly candles use market open/close unix timestamps and `period_interval=60`. Preserve raw fields. Books use `/markets/T/orderbook`; the books loop discovers tickers through `/markets?series_ticker=S&status=open`.

Under `data/kalshi/` (or `$PROMVAL_DATA/kalshi/`):

- `markets/<SERIES>.json`: raw market list sorted by ticker, refreshed each run.
- `trades/<TICKER>.jsonl.gz`: raw full tape sorted by (`created_time`, `trade_id`).
- `candles/<TICKER>.json.gz`: raw candlesticks list.
- `books/<TICKER>.jsonl`: append-only lines with `at` (UTC ISO Z, second precision) and raw `orderbook_fp`.

New files and refreshed catalogs use temporary files plus atomic rename. Only finalized/settled markets get histories; existing trade/candle files are never rewritten. Empty tapes with positive `volume_fp` (or `volume`) and empty candle lists report errors without writing files, allowing retries. Zero-volume empty tapes are saved as complete. Other markets continue after failures; failed catalogs skip that series. Initial book creation is atomic; later snapshots append.

The standard-library client uses a repository User-Agent, 30-second timeout and at least 0.06 seconds between requests. HTTP 429/5xx, URL errors and timeouts retry up to five attempts with 1/2/4/8-second backoff. First-run estimate: about 10k final markets × two requests at ~0.06-second spacing plus latency, roughly an hour; pagination and retries can add time.

## VLR scraper

Run `uv run promval vlr crawl --since 2021-01-01`; options: `--economy-since 2023-01-01`, `--max-matches N`, `--min-interval 2.0`, `--full` (walk back to `--since` past cached pages; use it to resume an interrupted backfill, since a normal run stops after 3 pages with nothing new). Build offline with `bash scripts/setup_db.sh`; it deletes and rebuilds `db/valorant.db` in numeric script order. Failures roll back one match, continue, and log to `db/parse_errors.txt`.

Cache: `${PROMVAL_DATA:-data}/vlr/raw/matches/<id>.html.gz` and `<id>_economy.html.gz`. Writes use atomic gzip replacement. Results listings are uncached. Never re-fetch cached match pages; missing economy tabs can be retried independently. Skip same-day matches until tomorrow (Eastern date). Stop at empty/older pages, three consecutive pages without new work, or the match limit.

Requests start at least 2 seconds apart. User-Agent: `valorant-model/0.1 (+https://github.com/thaiv28/valorant-model)`. Retry 429, 5xx, URL errors and timeouts up to five attempts, sleeping 5/10/20/40 seconds. Fetching is injectable; parsers never fetch.

Results parser extracts IDs, slugs and day headings. Match parser extracts event/stage, team IDs/names, best-of, patch, UTC start, series score/winner, ordered veto (short tags; “remains” is decider), played maps, picks, scores, side totals, duration, overtime beyond 24 rounds, players/agents/stats, and round winners/sides/types. Skip unplayed maps. Missing stats are null. Reject inconsistent round counts, round wins or series map wins. An 11–13 score is 24 regulation rounds, not overtime. A drawn series (1–1 Bo2) has a null winner. The economy tab omits overtime rounds, so its per-round rows cover regulation only.

Economy fixtures (2020–2026) show pistol/conversion/bonus won/played, eco (<10k), half buy (10–18k), full buy (18k+) matchup counts, plus per-round team equipment and bank amounts (displayed in thousands). Summary grids exclude each half’s first three rounds; aggregate their counts by own buy category. Preserve every round’s category/buy/bank. Separate semi-eco and semi-buy are absent, stored null; half buy stays separate. Unavailable values remain null.

Tables: `matches` (match_id), `vetoes` (match_id/step), `maps` (game_id), `rounds` (game_id/round), `player_maps` (game_id/player_id), `economy` (game_id/team); declared foreign keys connect them. Agents and economy round details use JSON text; other fields are scalar SQL columns.

Time gotcha: VLR `data-utc-ts` is America/New_York local time, despite its name. Convert with zoneinfo (EST/EDT) to ISO UTC ending Z.

Backfill estimate: roughly 590 results pages back to 2021, about 29k matches; approximately two requests per match from 2023 and one before, at 2 seconds, roughly a day of crawling. Not run against the live site.
