# Work log

Newest first. Each entry: what changed, the checks run, remaining limits. At most 150 words.

## 2026-10-28 — Kalshi–VLR linking

Branch `kalshi-link`, base `main` (56b502a). Added offline catalog loading, schedule parsing, three-pass series matching, consistent UUID aliases, inherited map links and binary settlement checks. Rebuild writes `kalshi_markets`, `team_aliases`, `kalshi_links` and `db/link_report.txt`; missing catalogs remain empty, absent maps are unplayed, scalar settlements are skipped. Tests cover normalization, Eastern offsets, renames, fuzzy/ambiguous candidates, slip boundaries, alias conflicts, map order, results and fixture DB rebuilds. Checks: `UV_NO_SYNC=1 uv run pytest -q` (85 passed, 3.11 s; existing suite: 63 passed, 3.07 s), ruff format/check and `git diff --check` passed. Limits: not run on the real catalog. Plain `uv run` panics in sandbox initialization; `UV_NO_SYNC=1` works. Existing tracked egg-info changes were left untouched.

## 2026-10-28 — VLR map order from the map tabs

Branch `vlr-map-order`, base `main` (89aa707). Map order now comes from VLR's numbered map tabs ("1 Ascent"), which follow the veto and play order; the stat sections can be listed differently. Found by the Kalshi–VLR cross-check: all 8 map-result mismatches (3 matches) were maps in the wrong order. Regression fixture 730547. Checks: pytest, ruff format/check.

## 2026-10-28 — VLR event tiers and map pool

Branch `vlr-events`, base `main` (56b502a). Added `promval vlr events` (VLR's event lists by tier: VCT, VCL, T3, GC, collegiate, offseason; refreshable cache), an `events` table with a primary tier, an international flag (VCT/GC/offseason names, qualifiers excluded) and JSON overrides, and map-pool history from seven-map vetoes (`veto_pools`, smoothed `map_pool_periods`, `map_pool` view). Checks: pytest (95 passed), ruff format/check; live crawl: 69 pages, 3,050 events; a DB build on the 403 cached matches joined every match to an event, flagged 30 events international (no T3 "Masters" cups) and found the Aug 2026 Breeze→Abyss pool change. Limits: VLR's VCT tier includes some tier-2 events (China Evolution Series, 2021 Challengers); refine with overrides.

## 2026-10-28 — Scheduled Kalshi collector

Branch `kalshi-schedule`, base `main` (56b502a). Added a sorted, atomic history manifest and local rebuild command, immutable gzip book files per pass, an S3 pull/push helper, and a six-hour GitHub Actions collector that downloads only the manifest, guards missing seeds, and uploads partial progress. Updated offline collector/workflow checks and deployment guidance. Checks: `UV_NO_SYNC=true uv run pytest -q` (72 passed, 3.74 s), ruff format/check and `bash -n scripts/kalshi_data.sh`. Plain `uv run` crashed in macOS system configuration; disabling dependency sync used the existing environment. Limits: workflow not run; secrets/variable not yet set. Actions runtime is estimated until the first live runs; no CI runtime baseline measured.

## 2026-10-28 — Edge comes from the model

Docs only. Recorded the decision that the edge must come from a better rating model (as in Prometheus), not from trading on the veto faster than Kalshi: map prices react to the veto immediately. Removed the veto-window timing task from Future work. Checks: pytest.

## 2026-10-28 — VLR crawler and parsers

Branch `vlr-scraper`, base `main` (156e8f7). Added a polite VLR fetcher (2 s, retries), a permanent gzip raw cache, an incremental results crawl (`--full` walks past cached pages to resume a backfill), pure parsers for results, match and economy pages, and `scripts/setup_db.sh` building `db/valorant.db` (matches, vetoes, maps, rounds, player_maps, economy). Drawn series (1–1 Bo2) store a null winner; the economy tab omits overtime rounds, so economy checks regulation rounds only (regression fixtures 29754, 582286). Checks: pytest (41 passed), ruff format/check; a live sample of 27 matches across 2021–2026 built with 0 parse errors (68 veto steps, every round with side and win type, 70 of 560 player rows without a rating). Limits: backfill not run; no event tiers, team aliases or bo3.gg check yet.

## 2026-10-28 — Kalshi collector

Branch: `kalshi-collector`; base: `main` (`156e8f7`). Added public HTTP pacing/retries/pagination, merged catalogs, atomic final trade/candle files, append-only active books, collector and timed-book CLI commands, and offline fixture tests. Historical-catalog markets use `/historical/trades` and `/historical/markets/{T}/candlesticks`; `/markets` wins overlaps and retains recent endpoints. Empty tapes for positive-volume markets and empty candles report errors without saving files, allowing retries; zero-volume empty tapes are complete. Raw fields are preserved. Updated layout, usage and status docs. Checks: pytest (26 passed), ruff format/check; live `collect --limit 12` saved 2025 historical tapes (20–277 trades) and candles with no errors, and 36 open books. Limits: full backfill not run; not scheduled.

## 2026-10-28 — Repo skeleton

Base: new repo. Created `valorant-model` with Prometheus's conventions: AGENTS.md, steering docs, work-log tooling and hook, steering test (budgets scaled down), ruff config, CI (ruff + pytest), Typer CLI `promval` with empty `kalshi` and `vlr` groups, the design plan PDF, and fixtures: Kalshi API responses and gzipped VLR pages (results pages 1/300/600/1500; matches 773441 Bo3, 654971 and 610432 Bo5, 163803 Bo1 2023, 6805 Bo1 2020, each with its economy tab), fetched 2026-10-28. Checks: `uv run pytest -q`, `uv run ruff format --check`, `uv run ruff check`.
