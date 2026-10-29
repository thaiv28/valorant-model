# Work log

Newest first. Each entry: what changed, the checks run, remaining limits. At most 150 words.

## 2026-10-29 — Game execution inputs

Branch `game-candidates`, base `main`. Added frozen `promval/blend_artifact.json` and atomic private `data/feed/candidates.json`, uploaded to private `valorant-model/feed/candidates.json` for Prometheus's execution Lambda. Shared benchmark row construction preserves quote rules, stage-1 temperatures and orientation. Candidates validate paired rules, names and starts; export both international and domestic groups. Artifact: 7 snapshots; latest November 1, 2026, a=1.069742465, b=0.535410478, n=1263. Checks (UV_OFFLINE=1 UV_NO_SYNC=1; plain uv startup panics): pytest 390 passed in 25.56s versus existing 373 in 27.69s; 16 new trading tests 0.18s; Ruff format/check and diff check passed. Real blend-artifact, feed-state and offline snapshot export passed (5 upcoming, 2,457 finals, 1,287 prices, zero candidates). No network or commits; Prometheus packaging/deployment remains external.

## 2026-10-29 — refresh-db: save the raw cache before the DB build

Branch `game-feed`, base `main`. The first `refresh-db` run spent 35 min seeding ~1 GB from S3, then timed out (45 min) in the DB build, so the Actions cache was never saved. The raw cache is now saved right after the crawl; on a cache miss, parsed pickles are touched after the S3 download (S3 sets mtimes to upload time, which made valid pickles look older than their raw pages and forced a full reparse); timeout 90 min. Checks: workflow tests (new order guard), YAML parse. Run timing to follow on GitHub.

## 2026-10-29 — Snapshot site feed workflows

Branch `game-feed`, base phase-1 commit `45b5ba5`. Split DB replay/closing quotes into an atomic, versioned gzip-pickle snapshot; exports load it without SQLite. Added hourly refresh-db and 10-minute feed dispatch workflows (GitHub schedules are backups), raw Actions cache and conditional S3 prediction-log persistence. S3: `valorant-model/{vlr/,kalshi/,feed/{state.pkl.gz,predictions.json,valorant.json.gz,upcoming/}}`. Checks: offline/no-sync uv pytest (369 passed, 27.81 s), Ruff format/check, shell syntax, diff check and real-DB snapshot/export passed; 1,890,179-byte state built in 3.83 s; export 0.54 s versus DB 4.68 s, identical after removing generated. Plain uv startup panics on macOS. Limits: workflows not yet run on GitHub; runner times unmeasured; raw cache must be seeded in S3 once. No network or commits. Merged main: the feed now replays the adopted `player_round_glicko_rookie_tier_revert`; its stage-1 series temperatures (Bo3 0.91, Bo5 0.84, from docs/elo_backtest.md) are stored in elo_weights.json.

## 2026-10-29 — Website prediction feed

Branch `game-feed`, base `main`. Added `promval export` for the Prometheus feed: upcoming/live matches, replayed results, section filters and oriented Kalshi current/closing prices. Future calls refresh in `data/predictions.json`, then freeze at start; missing future listings are removed. Upcoming pages use a separate cache; `--no-fetch` is offline. Stored existing series temperatures and retained them on refits; shared candle helpers preserve benchmark behavior. Checks (UV_OFFLINE=1 UV_NO_SYNC=1; plain uv startup panics): pytest 363 passed, Ruff format/check, diff check, real-DB offline export (2,457 finals; 1,287 prices). Observed suite timing: 347 existing tests 66.17s → 363 tests 76.04s; 16 feed tests alone 2.38s. Limits: DB only as fresh as the last crawl + `setup_db`; VLR skips same-day results, so finished matches await a result until ingested; TBD sides omitted. No commits.

## 2026-10-29 — Holdout opened

Branch `holdout`, base `main`. Pulled Kalshi from S3, rebuilt the DB, and ran `evaluate_elo.py --holdout` once (July 1 – Oct 28, 2026; 1,663 maps) with frozen stage-1 parameters. `tier_revert` beats team Elo (0.650 vs 0.670 map log loss) but matches Kalshi raw (series +0.009, maps +0.0005, n.s.); blended −0.005 / −0.004 (n.s.), VCL significant. Depth-capped blended series +17.0% [+1.0, +33.7]; maps −3.6%; international series negative. Report `docs/elo_holdout.md`; ledger and current state updated. Checks: pytest. Limit: the holdout is spent; later ideas need a new forward window.

## 2026-10-29 — Tier-mean reversion adopted

Branch `tier-revert`, base `main`. `revert_target="tier"` pulls a player toward the running mean rating of their latest tier (vct, vcl, gc, t3, collegiate; offseason/unknown keep the previous tier), kept as O(1) per-tier sums. New variant `player_round_glicko_rookie_tier_revert`. Stage 1 chose 0.2 at Nov 1: −0.0007 [−0.0014, −0.0001], no section worse; stage 2 −0.0015 (n.s.; VCL −0.0021 significant; GC +0.0029 n.s.); blended vs Kalshi within 0.0005 of the old model. Adopted; series T now Bo3 0.91, Bo5 0.84. Report and weights rewritten. Caveat: sixth candidate tested on stage 2, proposed after the global version's stage-2 GC result. Checks: pytest, ruff, `evaluate_elo.py`.

## 2026-10-29 — Rating reversion toward the mean

Branch `revert`, base `main`. Added off-by-default player season/inactivity reversion toward the initial rating, separate update dates, non-mutating prediction calculations, and the fixed-base `player_round_glicko_rookie_revert` grid (40 candidates). Existing defaults retain exact synthetic predictions; RD behavior is unchanged. Tests cover boundaries, UTC offsets, multiplicative decay, teammate initialization, prediction/update agreement, validation and registry parameters with RD on/off. Documented formulas/defaults/grid. Checks: full suite passed (347 tests, 26.20 s); Ruff format/check passed. Benchmark: stage 1 chose a 0.2 pull at Jan 1, no inactivity pull (−0.0006 [−0.0013, −0.0000]); stage 2 −0.0007 (n.s.) with GC significantly worse (+0.0040). Not adopted; left off.

## 2026-10-29 — Map strength offsets and pick bonus

Branch `map-strength`, base `main`. Added optional centred per-player/team map offsets, picker strength bonuses, and `predict_maps` without history mutation. Replay loads picked_by; two registry variants fix the adopted rookie/RD base and vary map/pick parameters. Tests cover centring, keys, update expectations, missing context, prediction state, exact default predictions, registry grids and SQL loading. Checks: 293 tests passed (24.14 s); `uv run --no-sync pytest -q`, Ruff format/check and `git diff --check` passed. Plain `uv run` crashed in macOS configuration; offline/no-sync runs passed. Grids rescaled after a first run (round-level points amplify ~3× into map odds): map_k {0.5,1,2,4}, pick_bonus {1,2,3,5,8}. Verdict: both rejected (gains below 0.0005); left off.

## 2026-10-29 — Series momentum chain

Branch `momentum`, base `main`. Added exact two-state series/slot odds and stage-1 momentum MLE using first-map probabilities. The optional benchmark flag fits each model/layer separately, then refits temperatures; Kalshi map markets use slot chances conditional on being played. Added `series_odds.py` for frozen stage comparisons, clustered intervals and calibration. Real DB: m=0.196441; m+T versus T series log-loss Δ +0.000005 stage 1, +0.000162 [+0.000028,+0.000299] stage 2; later-map slot Δ +0.001640. Checks: pytest, ruff format/check, diff check, real-DB report. Observed CI timing: 262 existing tests 24.42s → 270 tests 24.57s; 8 added tests alone 1.57s. Used `UV_OFFLINE=1 UV_NO_SYNC=1` after uv's local startup panic. Verdict: rejected (no gain over the temperature; slot odds worse); flag stays off. Limits: holdout unopened.

## 2026-10-29 — Full-crawl two-stage benchmark

Branch `full-rerun`, base `main`. Rebuilt the DB from the complete crawl (28,770 matches from 2021; 12 min) and reran the two-stage benchmark (stage 1 2023 – Aug 2025, 25,649 maps). Widened grids where choices hit edges: rookie_penalty {50,100,150,200,300}, rookie_maps {100,200,400,800}, form H {3,…,80}. Adopted rookie 200/400 (stage 2 −0.0044, significant). Dropped form (H drifts to 80; stage 2 flat, VCL significantly worse) and regional (no gain). Wrote `elo_weights.json`. Vs Kalshi: depth-capped series+map flat ROI +30.5% [+11.7, +53.2], Kelly $50 → $450. Report and ledger updated. Checks: pytest, ruff, `evaluate_elo.py` (3.7 min). Limits: holdout unopened; weights omit the series temperature.

## 2026-10-29 — Retry dropped VLR connections

Branch `crawl-retry`, base `main`. The 4-worker crawl stopped at 18,147 match pages on `RemoteDisconnected` (VLR closed a connection), which the fetcher didn't retry. It now retries `ConnectionError` and `http.client.HTTPException` with the same shared backoff as 429/5xx. Checks: pytest, ruff.

## 2026-10-29 — Stage-1 series temperature

Branch `series-temp`, base `main`. The series check showed independent-map series odds are too extreme (Bo3: 5% predicted → 10% won, 96% → 90%). `evaluate_elo.py` now fits, per model and best-of (Bo3, Bo5; ≥ 30 rows, grid 0.40–1.50), a temperature T on stage-1 series log loss and applies p′ = σ(T·logit p) to every series probability (series metrics, Kalshi series comparison, returns); Bo1 unchanged. Layer variants fit their own T on layered stage-1 rows. `--no-series-temperature` restores the old odds. Result (`rookie+form`): T = 0.79 Bo3, 0.68 Bo5; stage-2 series log loss −0.0050 [−0.0088, −0.0011]. Checks: pytest (261), ruff.
