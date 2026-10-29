# Work log

Newest first. Each entry: what changed, the checks run, remaining limits. At most 150 words.

## 2026-10-28 — Two-stage benchmark and layer hook

Branch `two-stage`, base `main`. Split outcome tuning (2023-01-01 to 2025-09-01 exclusive) from frozen validation against Kalshi (2025-09-01 to 2026-07-01 exclusive). Added ISO date controls, context-aware layer hooks with identity default, validation summaries, monthly identical-row breakdowns, and synthetic separation/layer tests. Holdout remains optional and excluded from selection/blend fitting. Checks: offline `uv run pytest -q` (201 passed, 17.46s), `uv run ruff format --check`, and `uv run ruff check`, with `UV_NO_SYNC=1` to avoid sandbox sync startup panic; direct virtualenv checks also passed. Limits: no full-data benchmark or network; baseline CI timing unavailable after initial uv startup failure. Monthly ROI avoids unnecessary bootstrap work.

## 2026-10-28 — Rookie discount and tier moves

Branch `rookie-moves`, base `main`. Added optional player-only logarithmic rookie discounts and linearly fading tier-move adjustments to prediction/update strengths, with update-only map counts and majority tier homes. Registered three narrowed-grid Glicko variants; existing defaults retain exact predictions. Tests cover decay, promotions/demotions, ties, excluded sections, update expectations, leakage and registry grids. Checks: offline `uv run --no-sync pytest -q` (221 passed, 14.40 s; baseline 198 in 21.52 s), `ruff format --check`, `ruff check`, and `git diff --check` passed. Plain `uv run` panicked locally; used the existing environment with `--no-sync`. Limits: not yet benchmarked; no holdout tuning or network access.

## 2026-10-28 — Parallel VLR crawl

Branch `crawl-workers`, base `main`. `promval vlr crawl --workers N` fetches each results page's missing match and economy pages in N threads. The fetcher is thread-safe: one shared request slot per `--min-interval` (the total rate cap), and a 429/5xx pauses every worker for the backoff, not only the one that hit it. Default stays 1 worker. Checks: pytest, ruff.

## 2026-10-28 — Pick advantage check; capped-Kelly rerun

Docs only. On Feb–Jun 2026 picked maps (2,409), the picking team won 52.5% vs 50.0% predicted by player_round_glicko (+2.5 pts, 95% [+0.5, +4.4]); a constant picker bonus of 0.11 logit improves picked-map log loss 0.6457 → 0.6443 (in-sample). Pre-veto the picker of map 1 isn't predictable in Bo3 (VLR team1 picks it 46%) but is in Bo5 (70%), so a full map model is deferred. Capped-Kelly rerun (tradeable quotes, in-sample): player_round_glicko raw series+map flat ROI +13.4% [+1.5, +27.0], $50 → $3,622; blended series +9.6%, $50 → $158; blended maps −3.4%. Limits: in-sample parameters; fills at hourly quotes with no depth.

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
