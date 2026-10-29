# Work log

Newest first. Each entry: what changed, the checks run, remaining limits. At most 150 words.

## 2026-10-28 — VLR crawler and parsers

Branch `vlr-scraper`, base `main` (156e8f7). Added a polite VLR fetcher (2 s, retries), a permanent gzip raw cache, an incremental results crawl (`--full` walks past cached pages to resume a backfill), pure parsers for results, match and economy pages, and `scripts/setup_db.sh` building `db/valorant.db` (matches, vetoes, maps, rounds, player_maps, economy). Drawn series (1–1 Bo2) store a null winner; the economy tab omits overtime rounds, so economy checks regulation rounds only (regression fixtures 29754, 582286). Checks: pytest (41 passed), ruff format/check; a live sample of 27 matches across 2021–2026 built with 0 parse errors (68 veto steps, every round with side and win type, 70 of 560 player rows without a rating). Limits: backfill not run; no event tiers, team aliases or bo3.gg check yet.

## 2026-10-28 — Kalshi collector

Branch: `kalshi-collector`; base: `main` (`156e8f7`). Added public HTTP pacing/retries/pagination, merged catalogs, atomic final trade/candle files, append-only active books, collector and timed-book CLI commands, and offline fixture tests. Historical-catalog markets use `/historical/trades` and `/historical/markets/{T}/candlesticks`; `/markets` wins overlaps and retains recent endpoints. Empty tapes for positive-volume markets and empty candles report errors without saving files, allowing retries; zero-volume empty tapes are complete. Raw fields are preserved. Updated layout, usage and status docs. Checks: pytest (26 passed), ruff format/check; live `collect --limit 12` saved 2025 historical tapes (20–277 trades) and candles with no errors, and 36 open books. Limits: full backfill not run; not scheduled.

## 2026-10-28 — Repo skeleton

Base: new repo. Created `valorant-model` with Prometheus's conventions: AGENTS.md, steering docs, work-log tooling and hook, steering test (budgets scaled down), ruff config, CI (ruff + pytest), Typer CLI `promval` with empty `kalshi` and `vlr` groups, the design plan PDF, and fixtures: Kalshi API responses and gzipped VLR pages (results pages 1/300/600/1500; matches 773441 Bo3, 654971 and 610432 Bo5, 163803 Bo1 2023, 6805 Bo1 2020, each with its economy tab), fetched 2026-10-28. Checks: `uv run pytest -q`, `uv run ruff format --check`, `uv run ruff check`.
