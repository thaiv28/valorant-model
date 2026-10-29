# Work log

Newest first. Each entry: what changed, the checks run, remaining limits. At most 150 words.

## 2026-10-28 — Prometheus-style Kelly caps in the backtest

Branch `lol-sizing`, base `main`. Returns tables now size like Prometheus's pregame executor (`LOL_SIZING` in `promval/backtest.py`): full Kelly, at most 10% of capital per fixture, $250 per order and per fixture, $1k exposure and $2k per UTC day, all of a day's bets sized from that day's opening capital, nothing once capital is $0; `summarize(..., sizing="full")` keeps the uncapped path. Reports add a series+map row so the fixture cap spans both kinds. Parser now stores `maps.picked_by` (1/2, from VLR's `picked mod-1/2` badge); `PARSER_VERSION` 2. Checks: pytest, ruff.

## 2026-10-28 — Kalshi quotes a bot could trade before the veto

Branch `quote-time`, base `main`. The benchmark priced Kalshi at the last hourly candle before VLR's scheduled start, which can already reflect the veto and late news. Default is now `--quote tradeable`: the first hourly bid/ask ending ≥ 30 min after listing and ≥ 2 h before start with spread ≤ 6¢ (`--max-spread`); `--quote prestart` keeps the old rule. Measured on Feb–Jun 2026 linked markets: 30 min after listing books are empty (median spread 13¢, quarter ≥ 93¢); the tradeable rule covers 83% of markets at a median 40 h before start. Rerun (Feb–Jun 2026, in-sample): Kalshi's early price is much less sharp (series log loss 0.632 vs 0.604 pre-start); player_round_glicko raw vs Kalshi series +0.009, maps −0.003 (not significant), flat ROI +6.7%/+14.9% (intervals include 0), full Kelly still goes broke; blended series −0.006, flat ROI +5.9%, Kelly $50→$77; blended maps worse (+0.011, significant). Checks: pytest (193), ruff.

## 2026-10-28 — Walk-forward market blend; wider RD grid

Branch `blend`, base `main`. `promval/blend.py`: logit p = a·logit(mid) + b·(logit model − logit mid), no intercept, fitted by month on earlier rows only (series and maps separately; ≥100 rows, else mid). Reports add blended log-loss and full-Kelly tables. RD grid widened (rd_new to 600, rd_info to 1.0; chosen 280/0.25, inside). Checks: pytest (192), ruff. Run on VLR from Sep 2025, tuning Feb–Jun 2026 (4,237 maps, in-sample params): player_round_glicko vs Kalshi raw series +0.037 (significant), maps +0.008; blended series +0.003, maps +0.004 (not significant); blended flat ROI series −3%, maps −9%. Blend fits a ≈ 1.06–1.41 (> 1: Kalshi mids underconfident) and b ≈ 0.11 series, 0.52 maps. 113 s wall.

## 2026-10-28 — Player RD, combined variants, Kalshi Kelly backtest

Branch `glicko`, base `main`. Ported Prometheus's player RD (new 280→grid, floor 140, growth 10/√day; moves scale by RD²/floor²), added `player_round_glicko` and `player_round_region_glicko`, and `promval/backtest.py`: after-fee edge against the pre-match hourly ask, full Kelly per match from $50, flat-stake ROI with match bootstrap. Reports now show log loss vs Kalshi and returns by tier. Checks: pytest (188), ruff. Rough run (VLR from Dec 2025; tuning June, in-sample): player_round_glicko maps 0.6389 (v1 0.6614; significant), series 0.6034 (v1 0.6530; significant); vs Kalshi series +0.042, maps +0.009 (not significant); flat ROI ≈ 0%, full Kelly $50 → $0.37. Limits: rd_new and rd_info at grid edges; raw model edges are overconfident.

## 2026-10-28 — Elo variants: margin, round, player, region

Branch `elo-variants`, base `main`. One composable Elo: credit (binary, margin 0.5 + 0.5·tanh(diff/c), round share with an exact first-to-13 map DP and temperature τ), unit (team, or players with the side = starters' mean), and region offsets (host country → Americas/EMEA/Pacific/China; homes from earlier non-international maps; offsets move only on cross-region maps); 12 variants, grids widened after edge hits. Checks: pytest (169), ruff. Rough run (VLR from Feb 2026; tuning = June, 549 maps): player_round 0.6487, player_margin 0.6502, team_round 0.6512, team_margin 0.6521, v1 0.6627; margin and round beat v1 significantly on maps; player ≈ team; region offsets pick the smallest weight (no gain yet). Limits: cold start; rerun on full data.

## 2026-10-28 — Parallel parse and parsed cache

Branch `fast-build`, base `main` (31a140a). Added versioned atomic parsed caches with raw-mtime invalidation, bounded process-pool parsing, configurable jobs, and batched SQLite inserts in numeric match order. Five-match fixture loader timings: original serial 1.135 s; cold jobs=1 0.991 s, cold jobs=8 0.851 s, warm jobs=8 0.023 s (cold jobs=4 0.897 s). All six tables matched exactly across these runs. Tests cover warm-cache parser avoidance, both raw-file mtimes, parser-version invalidation, serial/parallel equality, uncached parse errors, and transaction rollback. Checks: pytest (160 passed, 20.61 s), ruff format/check, and diff whitespace check passed. Used `UV_NO_SYNC=true` because plain uv dependency sync crashes in macOS system configuration. Limit: no 30k-match benchmark; fixture timings include worker startup. Real cache (1,129 matches): cold 93 s with 8 jobs (serial ≈ 0.31 s/match), warm 9 s.

## 2026-10-28 — Elo v1 and benchmark harness

Branch `elo-v1`, base `main` (e5d0f2d). Added `team_elo` (one rating per VLR team, map win = 1, loss = 0, K from a grid by tuning log loss), a coin baseline, chronological replay, Prometheus's scoring and series-clustered bootstrap helpers, series odds from map odds, an opt-in holdout (from 2026-07-01), and a comparison with Kalshi's last hourly pre-match midpoint on linked markets (maps use the model's pre-match chance). Added numpy and pandas. Checks: pytest (152 passed), ruff format/check; `scripts/evaluate_elo.py` ran end to end on a partial DB (VLR crawled back to 2026-06-25: 141 tuning maps), too little data to judge. Limits: rerun after the VLR backfill.

## 2026-10-28 — Kalshi–VLR linking

Branch `kalshi-link`, base `main`. `005_load_kalshi.py` loads the catalog into `kalshi_markets`; `006_link_kalshi.py` links Kalshi series and map events to VLR matches and maps (exact, VLR parenthetical names, learned competitor-UUID aliases, an anchor pass on one confirmed team with a plausible opponent, then fuzzy), and cross-checks settled results. Checks: pytest (142 passed), ruff format/check; on the real catalog with VLR cached from Aug 9 to Oct 27 2026: 288/335 series and 629/724 map events in that window linked (first version: 194/252), 1,840/1,840 settled results agree with VLR. Limits: unlinked are mostly events VLR lacks (Monsters Reloaded qualifier) or academy rosters Kalshi names after the main org ("Natus Vincere" = VLR "Natus Vincere Junior"); see `db/link_report.txt`.

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
