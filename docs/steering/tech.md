# Tech

## Stack

Python ≥ 3.12 with uv; SQLite rebuilt from raw caches; raw SQL; Typer CLI (`promval`); BeautifulSoup + lxml for HTML; ruff; pytest (offline, fixtures in `tests/fixtures/`).

## Layout

| Path | Purpose |
|---|---|
| `promval/ratings/` | Team Elo, model registry, chronological map replay; optional `elo_weights.json` |
| `promval/evaluation.py`, `scripts/evaluate_elo.py` | Scoring helpers and offline benchmark report |
| `tests/test_elo.py`, `tests/test_evaluation.py` | Ratings, leakage, candle formats and synthetic-DB benchmark checks |
| `promval/main.py` | CLI entry; mounts the `kalshi` and `vlr` command groups |
| `promval/kalshi/api.py` | Public HTTP client, pacing, retries and pagination |
| `promval/kalshi/collect.py` | Raw catalog, trade, candle and book files |
| `promval/kalshi/cli.py` | Collector, manifest and book-loop commands |
| `tests/test_kalshi_collect.py` | Offline fixture-based collector and CLI tests |
| `promval/vlr/` | VLR.gg crawler, raw cache and parsers |
| `scripts/001_create_tables.sql`, `002_load_vlr.py`, `003_events.py`, `004_map_pool.py`, `setup_db.sh` | Rebuild SQLite from VLR cache |
| `promval/link.py` | Pure team normalization, event linking and settlement checks |
| `scripts/005_load_kalshi.py`, `006_link_kalshi.py` | Load catalogs, learn aliases and link Kalshi to VLR |
| `tests/test_link.py` | Offline linking and catalog-to-DB checks |
| `scripts/work_log.py`, `.githooks/` | Work-log tooling |
| `tests/test_vlr_*.py` | Offline parser, crawl and DB checks |
| `tests/test_steering.py` | Doc guard |
| `tests/fixtures/` | Saved Kalshi JSON and gzipped VLR pages |

## Kalshi collector

`promval kalshi collect [--no-books] [--limit N]` refreshes both Valorant series (`KXVALORANTGAME`, `KXVALORANTMAP`), saves final-market histories and snapshots active books. `--limit` caps new trade/candle fetches combined (each file attempt counts separately). `promval kalshi books --every 60 --minutes 60` refreshes active tickers each pass; pass summaries include failures. GitHub Actions collects every six hours (see Deployment).

Public base: `https://api.elections.kalshi.com/trade-api/v2`. Paginate `/markets` and `/historical/markets` by series; merge by ticker, preferring `/markets`. Historical-catalog markets use `/historical/trades?ticker=T` and `/historical/markets/T/candlesticks`; recent markets use `/markets/trades?ticker=T` and `/series/S/markets/T/candlesticks`. Trades paginate with `limit=1000`; hourly candles use market open/close unix timestamps and `period_interval=60`. Preserve raw fields. Books use `/markets/T/orderbook`; the books loop discovers tickers through `/markets?series_ticker=S&status=open`.

Under `data/kalshi/` (or `$PROMVAL_DATA/kalshi/`):

- `markets/<SERIES>.json`: raw market list sorted by ticker, refreshed each run.
- `trades/<TICKER>.jsonl.gz`: raw full tape sorted by (`created_time`, `trade_id`).
- `candles/<TICKER>.json.gz`: raw candlesticks list.
- `books/<YYYY-MM-DD>/<YYYYMMDDTHHMMSSZ>.jsonl.gz`: one new gzip file per pass, one line per snapshot with `at` (UTC ISO Z, second precision), `ticker` and raw `orderbook_fp`. No appends; zero snapshots write no file. Local timestamp collisions advance the filename by a second.
- `manifest.json`: version 1 with sorted `trades` and `candles` ticker arrays. Skip histories present locally or listed here; runners download only this manifest, never the history archive.

New files and refreshed catalogs use temporary files plus atomic rename. Only finalized/settled markets get histories; existing trade/candle files are never rewritten. Empty tapes with positive `volume_fp` (or `volume`) and empty candle lists report errors without writing files, allowing retries. Zero-volume empty tapes are saved as complete. Other markets continue after failures; failed catalogs skip that series. After collection, atomically rewrite the manifest as the union of its old entries and all local histories, including newly saved files. A missing manifest starts empty. `promval kalshi manifest` rebuilds it from local history files only, for seeding S3. Books are written atomically once per pass.

The standard-library client uses a repository User-Agent, 30-second timeout and at least 0.06 seconds between requests. HTTP 429/5xx, URL errors and timeouts retry up to five attempts with 1/2/4/8-second backoff. First-run estimate: about 10k final markets × two requests at ~0.06-second spacing plus latency, roughly an hour; pagination and retries can add time.

## VLR scraper

`uv run promval vlr events` refreshes all tier lists: 60 VCT, 61 VCL, 62 T3, 63 GC, 64 Collegiate, 67 Offseason. Pages stop at the first empty list; `raw/events/tier<T>_p<N>.html.gz` is overwritten each run, obsolete trailing pages removed. Cost: ≈63 pages ≈2 min at 2 s/request. `003_events.py` builds the union into `events` (event_id, slug, name, primary vlr_tier, section, JSON tiers, international, status, dates, region, prize); no cache creates an empty table. Primary priority: 60, 63, 61, 67, 62, 64; sections: vct, gc, vcl, offseason, t3, collegiate. International (`is_international`): a vct, gc or offseason event, not a qualifier, whose name matches Masters followed by a city, Valorant Champions <year>, Champions Tour <year>: Champions, LOCK//IN, Esports World Cup or a Game Changers Championship. Regional names ending in Masters and T3/collegiate "Masters" cups do not match. `promval/vlr/event_overrides.json` applies international/section overrides by event ID last.

`004_map_pool.py` builds `veto_pools` (match_id, start_utc, sorted comma-joined pool) from exactly seven distinct veto maps. `map_pool_periods` (pool, first_utc, last_utc, matches) merges consecutive pools in VCT start order (all matches only when events is empty). Runs shorter than three join the preceding stable pool, or the next at the start; without a stable run, use the longest run's pool. View `map_pool` merges each map's adjacent active spans. Endpoints are inclusive observed times, not patch dates.

Run `uv run promval vlr crawl --since 2021-01-01`; options: `--economy-since 2023-01-01`, `--max-matches N`, `--min-interval 2.0`, `--full` (walk back to `--since` past cached pages; use it to resume an interrupted backfill, since a normal run stops after 3 pages with nothing new). Build offline with `bash scripts/setup_db.sh`; it deletes and rebuilds `db/valorant.db` in numeric script order. Failures roll back one match, continue, and log to `db/parse_errors.txt`.

Cache: `${PROMVAL_DATA:-data}/vlr/raw/matches/<id>.html.gz` and `<id>_economy.html.gz`. Writes use atomic gzip replacement. Results listings are uncached. Never re-fetch cached match pages; missing economy tabs can be retried independently. Skip same-day matches until tomorrow (Eastern date). Stop at empty/older pages, three consecutive pages without new work, or the match limit.

Requests start at least 2 seconds apart. User-Agent: `valorant-model/0.1 (+https://github.com/thaiv28/valorant-model)`. Retry 429, 5xx, URL errors and timeouts up to five attempts, sleeping 5/10/20/40 seconds. Fetching is injectable; parsers never fetch.

Results parser extracts IDs, slugs and day headings. Match parser extracts event/stage, team IDs/names, best-of, patch, UTC start, series score/winner, ordered veto (short tags; “remains” is decider), played maps, picks, scores, side totals, duration, overtime beyond 24 rounds, players/agents/stats, and round winners/sides/types. Skip unplayed maps. Missing stats are null. Reject inconsistent round counts, round wins or series map wins. An 11–13 score is 24 regulation rounds, not overtime. Map order is taken from the numbered map tabs, not the order of the stat sections. A drawn series (1–1 Bo2) has a null winner. The economy tab omits overtime rounds, so its per-round rows cover regulation only.

Economy fixtures (2020–2026) show pistol/conversion/bonus won/played, eco (<10k), half buy (10–18k), full buy (18k+) matchup counts, plus per-round team equipment and bank amounts (displayed in thousands). Summary grids exclude each half’s first three rounds; aggregate their counts by own buy category. Preserve every round’s category/buy/bank. Separate semi-eco and semi-buy are absent, stored null; half buy stays separate. Unavailable values remain null.

Tables: `matches` (match_id), `vetoes` (match_id/step), `maps` (game_id), `rounds` (game_id/round), `player_maps` (game_id/player_id), `economy` (game_id/team); declared foreign keys connect them. Agents and economy round details use JSON text; other fields are scalar SQL columns.

Time gotcha: VLR `data-utc-ts` is America/New_York local time, despite its name. Convert with zoneinfo (EST/EDT) to ISO UTC ending Z.

Backfill estimate: roughly 590 results pages back to 2021, about 29k matches; approximately two requests per match from 2023 and one before, at 2 seconds, roughly a day of crawling. Not run against the live site.

## Kalshi ↔ VLR links

The numbered DB build loads `kalshi_markets` from `collect.data_dir()/markets/{KXVALORANTGAME,KXVALORANTMAP}.json`; missing catalogs load zero rows with a message. Rules supply scheduled EDT/EST times (UTC Z) and event names; ticker suffixes supply team codes and map numbers.

`team_aliases` maps consistent competitor UUIDs to VLR team IDs, with names, codes and confident-series evidence counts; conflicting UUIDs are permanently dropped. `kalshi_links` stores one row per event, match/game IDs, kind, method and failure reason.

Candidates start within ±30 hours of the advertised schedule (otherwise open time +24 hours), allowing a one-day slip. Exact → alias → anchor passes repeat until no new link is made, re-deriving aliases from every confident link. Exact matching accepts either the outside name or the alternate inside a trailing parenthetical. Alias matching requires both UUIDs. An anchor requires one exact/aliased team appearing in only one candidate match; the other name must share normalized tokens, match team-code initials/a token, or have difflib similarity ≥0.6. Prefer an exact other-side name present in the window over a looser subteam name; competing matches remain ambiguous. Finally both fuzzy name similarities must reach 0.8, without overriding that preference. Normalization removes accents and generic organization words and equates female/women/GC. Map events inherit their series match (map-only catalogs use a representative map event), then select the played map by order; missing rows are `unplayed`.

Cross-check each linked binary settled market against the series/map winner; skip scalar settlements and unknown winners. `db/link_report.txt` lists unlinked events/unplayed maps with team names, schedule, event name and reason; anchor name mappings; and mismatched tickers with VLR IDs. The linker prints linked/total series and maps, aliases, market agreements/checked and mismatches. Re-runs replace derived rows. The Aug 18–Oct 27, 2026 catalog window linked 194/252 series against 233 cached matches before anchor/variant improvements. Settlement checks agreed on 1256/1264; eight disagreements came from the subsequently fixed VLR map ordering bug. Updated coverage is pending.

## Ratings and benchmark

Built v1: `coin` (0.5) and `team_elo`, one global pool across all tiers. Teams start at 1500; map-win Elo uses scale 400 and binary outcomes, no margin. Predict before updating, replaying by (match start UTC, match_id, map order). Model factories in `ratings/models.py` accept keyword parameters; later increments add registry entries. Series probabilities use the first map's pre-update p and independent maps to first ceil(best_of/2) wins; skip missing/even best-of and unknown series winners.

2021–22 seed ratings only; score from 2023-01-01. Select K by all-section tuning map log loss from grid 16,24,32,40,48,64, strictly before `HOLDOUT_START = "2026-07-01"`. Holdout scores appear only with `--holdout`, never select K. Sequential holdout updates use only already played maps. Sections: all, events.section (vct/vcl/gc/t3/collegiate/offseason/unknown), international=0/1. Metrics: rows, log loss (clip 1e-6), Brier, accuracy (0.5 picks get half credit), 10-bin ECE. Prometheus's five evaluation helpers are ported with attribution. Paired log-loss differences use 2,000 resamples, seed 0, whole matches clustered by match_id; a 95% interval excluding zero is significant. Tuning comparisons are selection diagnostics.

Kalshi joins links to markets and competitor aliases; skip unresolved teams/missing candles. Read `collect.data_dir()/candles/<TICKER>.json.gz`: last valid hourly candle ending no later than VLR match start, midpoint of yes bid/ask closes (`close_dollars` or historical `close`, both dollars). Orient to VLR team1; one contract per event, prefer team1, otherwise complement team2. Compare Elo and market on identical series/map rows, clustered by match. Map rows use the model's pre-match chance (the first map's p), matching the market's pre-match quote. Missing Kalshi inputs report “no linked markets”. No fees/execution simulation.

Run `uv run python scripts/evaluate_elo.py --db db/valorant.db --out docs/elo_backtest.md`; optional `--k-grid 16,32`, `--score-from 2023-01-01`, `--holdout`, `--write-weights`. Weights save selected K and last tuning date to `promval/ratings/elo_weights.json`; real-DB evaluation has not run here.
