# Work log

Newest first. Each entry: what changed, the checks run, remaining limits. At most 150 words.

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
