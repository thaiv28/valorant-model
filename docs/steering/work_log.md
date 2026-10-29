# Work log

Newest first. Each entry: what changed, the checks run, remaining limits. At most 150 words.

## 2026-10-29 — Map strength offsets and pick bonus

Branch `map-strength`, base `main`. Added optional centred per-player/team map offsets, picker strength bonuses, and `predict_maps` without history mutation. Replay loads picked_by; two registry variants fix the adopted rookie/RD base and vary map/pick parameters. Tests cover centring, keys, update expectations, missing context, prediction state, exact default predictions, registry grids and SQL loading. Checks: 293 tests passed (24.14 s); `uv run --no-sync pytest -q`, Ruff format/check and `git diff --check` passed. Plain `uv run` crashed in macOS configuration; offline/no-sync runs passed. Grids rescaled after a first run (round-level points amplify ~3× into map odds): map_k {0.5,1,2,4}, pick_bonus {1,2,3,5,8}. Verdict: both rejected (gains below 0.0005); left off.

## 2026-10-29 — Full-crawl two-stage benchmark

Branch `full-rerun`, base `main`. Rebuilt the DB from the complete crawl (28,770 matches from 2021; 12 min) and reran the two-stage benchmark (stage 1 2023 – Aug 2025, 25,649 maps). Widened grids where choices hit edges: rookie_penalty {50,100,150,200,300}, rookie_maps {100,200,400,800}, form H {3,…,80}. Adopted rookie 200/400 (stage 2 −0.0044, significant). Dropped form (H drifts to 80; stage 2 flat, VCL significantly worse) and regional (no gain). Wrote `elo_weights.json`. Vs Kalshi: depth-capped series+map flat ROI +30.5% [+11.7, +53.2], Kelly $50 → $450. Report and ledger updated. Checks: pytest, ruff, `evaluate_elo.py` (3.7 min). Limits: holdout unopened; weights omit the series temperature.

## 2026-10-29 — Retry dropped VLR connections

Branch `crawl-retry`, base `main`. The 4-worker crawl stopped at 18,147 match pages on `RemoteDisconnected` (VLR closed a connection), which the fetcher didn't retry. It now retries `ConnectionError` and `http.client.HTTPException` with the same shared backoff as 429/5xx. Checks: pytest, ruff.

## 2026-10-29 — Stage-1 series temperature

Branch `series-temp`, base `main`. The series check showed independent-map series odds are too extreme (Bo3: 5% predicted → 10% won, 96% → 90%). `evaluate_elo.py` now fits, per model and best-of (Bo3, Bo5; ≥ 30 rows, grid 0.40–1.50), a temperature T on stage-1 series log loss and applies p′ = σ(T·logit p) to every series probability (series metrics, Kalshi series comparison, returns); Bo1 unchanged. Layer variants fit their own T on layered stage-1 rows. `--no-series-temperature` restores the old odds. Result (`rookie+form`): T = 0.79 Bo3, 0.68 Bo5; stage-2 series log loss −0.0050 [−0.0088, −0.0011]. Checks: pytest (261), ruff.

## 2026-10-29 — Realism and grid results (partial crawl)

Data and docs only. Second two-stage run on 10,027 matches (stage 1 Mar 2024 – Aug 2025). Adopted rookie discount 150 / 200 maps (stage 1 −0.0046, stage 2 −0.0069); kept form (weaker: −0.0015 / −0.0007); rejected multi-stat form (VCT worse). Depth caps leave 307/534 series and 99/675 map bets fillable; filled bets keep positive ROI but Kelly drops from $4,637 to $298. Kalshi's series price sharpens toward the start (model edge only at the early quote). Series odds from independent maps are too extreme (5% → 10%, 96% → 90%). Report committed; ledger updated. Checks: pytest.

## 2026-10-29 — Wider rookie/form grids; multi-stat form layer

Branch `form-grid`, base `main`. Expanded rookie penalty/map grids while fixing K=32 and rd_new=280 for rookie variants; moves-only unchanged. Form half-lives now {2,3,5,8,12}. Added `form_multi` and ordered `regional_form_multi`: causal starter means of rating, ACS, KAST, ADR and fk−fd, stage-1 standard deviations, ridge-1 logistic weights and stage-1 half-life selection. Shared cached history skips null observations per stat. Tests cover grids, recovery, selection, frozen scales, missing/constant data, causality, composition and registration. Checks: `uv run pytest -q` (243 passed, 18.99s; prior recorded 235 in 18.08s), `uv run ruff format --check`, `uv run ruff check`, `git diff --check` passed. Used `UV_OFFLINE=1 UV_NO_SYNC=1` after plain uv hit its local startup panic. Limits: not benchmarked; no network or holdout access.

## 2026-10-29 — Backtest realism: rounded fees, depth caps, quote robustness, series check

Branch `realism`, base `main`. Added cent-ceiling order fees, $1 contract stakes with fee-inclusive flat ROI, rounded-fee Kelly cash sizing, and tape-volume depth caps (6 hours, 50%; missing tapes unfilled). Returns pair unlimited and capped fills. Added 24/6-hour quote rules, frozen-model quote robustness, and standalone/in-report series calibration, conditional map-2 and decider residual checks. Tests cover fees, depth/orientation, cash caps, quote cutoffs, report assembly without retuning, planted dependence and calibration counts. Baseline: 235 tests in 26.19s. Checks: `uv run pytest -q` (252 passed, 22.38s), `uv run ruff format --check`, `uv run ruff check`, and `git diff --check` passed. Plain offline `uv run` hits the local startup panic; checks use `UV_OFFLINE=1 UV_NO_SYNC=1`. Limits: no network, real-data benchmark or holdout evaluation; tape volume is a fill proxy without queue position/slippage. Changes uncommitted as requested.

## 2026-10-28 — First two-stage benchmark (partial crawl)

Data and docs only. Rebuilt on the crawl so far (7,597 matches from 2024-06) and ran the two-stage benchmark: stage 1 Oct 2024 – Aug 2025, stage 2 Sep 2025 – Jun 2026. Adopted (candidates, to rerun on full history): rookie discount (stage 1 −0.0046, stage 2 −0.0070, both significant) and the form layer (−0.0030 / −0.0027). Rejected: tier moves (no effect). Regional calibration not significant on 327 cross-region maps. Best, `player_round_glicko_rookie+form`: blended series vs Kalshi −0.017 (significant). Committed `docs/elo_backtest.md`; ledger updated. Checks: pytest.

## 2026-10-28 — Regional calibration and form layers

Branch `layers`, base `main`. Added ridge-shrunk zero-sum regional calibration, player-rating recent form with stage-1 half-life selection, and their ordered combination. A shared causal history pass records pre-map homes/form, caches per instance, and ignores international hosts for home counts. Reports include fitted parameters and row counts. Synthetic tests cover causality, decay, missing ratings, regional shrinkage/thresholds, parameter recovery, stage separation, composition and report integration. Checks: `UV_NO_SYNC=1 uv run pytest -q` (235 passed, 18.08s; baseline 224 in 24.95s), `uv run ruff format --check`, `uv run ruff check` (both with `UV_NO_SYNC=1`), and `git diff --check` passed. Plain offline `uv run` hit the local startup panic; `UV_NO_SYNC=1` uses the existing environment without network. Limits: not yet benchmarked on full data.

## 2026-10-28 — Model change rules and research ledger

Docs only. Added tech.md "Model change rules" (two stages: tune on outcomes 2023-01 to 2025-09, validate frozen models against outcomes and Kalshi 2025-09 to 2026-07, holdout opened once; adopt only on a significant stage-1 gain with no guarded regression and ≥ 0.0005 for additions; confirm on stage 2; removals non-inferior; data fixes lighter), `docs/research/README.md` (ledger, backfilled with every variant tested so far and its partial-crawl numbers), and AGENTS.md pointers: ledger entries for every test, commit `docs/elo_backtest.md` with each model change (first full-data report pending the crawl). Checks: pytest.

## 2026-10-28 — Two-stage benchmark and layer hook

Branch `two-stage`, base `main`. Split outcome tuning (2023-01-01 to 2025-09-01 exclusive) from frozen validation against Kalshi (2025-09-01 to 2026-07-01 exclusive). Added ISO date controls, context-aware layer hooks with identity default, validation summaries, monthly identical-row breakdowns, and synthetic separation/layer tests. Holdout remains optional and excluded from selection/blend fitting. Checks: offline `uv run pytest -q` (201 passed, 17.46s), `uv run ruff format --check`, and `uv run ruff check`, with `UV_NO_SYNC=1` to avoid sandbox sync startup panic; direct virtualenv checks also passed. Limits: no full-data benchmark or network; baseline CI timing unavailable after initial uv startup failure. Monthly ROI avoids unnecessary bootstrap work.
