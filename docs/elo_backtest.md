# Elo variants benchmark

## Combined summary (validation, all sections)

| Model | Series Δ log loss | Series flat ROI | Series Kelly (LoL caps) $ | Series flat ROI depth-capped | Series Kelly depth-capped $ | Map Δ log loss | Map flat ROI | Map Kelly (LoL caps) $ | Map flat ROI depth-capped | Map Kelly depth-capped $ | Series blended Δ log loss | Series blended flat ROI | Series blended Kelly (LoL caps) $ | Series blended flat ROI depth-capped | Series blended Kelly depth-capped $ | Map blended Δ log loss | Map blended flat ROI | Map blended Kelly (LoL caps) $ | Map blended flat ROI depth-capped | Map blended Kelly depth-capped $ |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| team_elo | 0.026644 | -2.01% | $0.55 | 15.98% | $128.56 | 0.005994 | 12.02% | $480.61 | 52.76% | $203.47 | 0.000161 | -5.01% | $35.62 | 16.91% | $57.12 | 0.011243 | -8.06% | $7.27 | -5.79% | $38.70 |
| player_round_glicko_rookie | -0.010090 | 12.00% | $1320.48 | 21.43% | $853.50 | -0.010355 | 19.44% | $6405.08 | 57.11% | $240.23 | -0.013821 | 17.12% | $1040.06 | 19.75% | $297.46 | 0.003189 | 3.00% | $27.07 | 12.78% | $55.59 |
| team_elo+form | 0.021016 | -0.12% | $9.64 | 17.01% | $348.00 | 0.004624 | 13.90% | $1157.01 | 51.73% | $245.92 | 0.000875 | 14.50% | $24.84 | 19.83% | $44.03 | 0.008039 | -1.04% | $11.73 | -0.14% | $42.85 |
| team_elo+regional | 0.028115 | -1.10% | $0.52 | 17.38% | $164.74 | 0.005838 | 12.63% | $491.83 | 53.70% | $206.11 | 0.000104 | -11.63% | $42.09 | 10.04% | $51.28 | 0.011066 | -6.48% | $8.17 | -2.16% | $38.64 |
| team_elo+regional_form | 0.022052 | 1.64% | $9.24 | 19.43% | $465.94 | 0.004259 | 14.89% | $2338.43 | 54.00% | $251.63 | 0.000533 | 17.32% | $28.39 | 16.33% | $47.21 | 0.008507 | 6.55% | $15.40 | 2.20% | $43.19 |
| player_round_glicko_rookie+form | -0.010599 | 9.69% | $1418.44 | 19.32% | $894.82 | -0.010666 | 19.71% | $5136.77 | 50.61% | $238.02 | -0.012923 | 18.16% | $2043.39 | 21.44% | $386.49 | 0.000701 | 14.33% | $52.42 | 59.64% | $61.23 |
| player_round_glicko_rookie+regional | -0.010019 | 10.64% | $1060.65 | 19.31% | $780.09 | -0.010455 | 19.65% | $7163.79 | 57.56% | $249.12 | -0.013773 | 16.66% | $996.32 | 18.85% | $289.05 | 0.002338 | 1.82% | $23.87 | 10.07% | $54.12 |
| player_round_glicko_rookie+regional_form | -0.010617 | 9.09% | $1175.86 | 18.24% | $843.81 | -0.010748 | 19.70% | $5311.31 | 52.36% | $256.56 | -0.012900 | 18.06% | $1977.83 | 21.21% | $361.77 | 0.000028 | 17.97% | $71.82 | 90.22% | $77.55 |

Series temperatures (stage 1; p′ = σ(T·logit p), T < 1 pulls odds toward 50%): team_elo Bo3 0.70, Bo5 0.62; player_round_glicko_rookie Bo3 0.81, Bo5 0.77; team_elo+form Bo3 0.63, Bo5 0.56; team_elo+regional Bo3 0.72, Bo5 0.63; team_elo+regional_form Bo3 0.64, Bo5 0.57; player_round_glicko_rookie+form Bo3 0.75, Bo5 0.71; player_round_glicko_rookie+regional Bo3 0.82, Bo5 0.77; player_round_glicko_rookie+regional_form Bo3 0.75, Bo5 0.71

Parameters minimize tuning map log loss across all sections. Replay predicts before update; Replay starts 2021-01-01. Tuning: [2023-01-01, 2025-09-01); validation: [2025-09-01, 2026-07-01). Holdout is scored only with --holdout and never selects parameters. Series use the first map prediction and independent maps in an odd best-of; missing/even best-of or unknown results are skipped. Accuracy gives 0.5 predictions half credit; ECE uses 10 equal-width bins. Log loss clips probabilities at 1e-6. Paired bootstrap uses 2,000 resamples, seed 0, clustered by match_id. Differences are the named model minus its comparator; negative favors the model. Significance requires a 95% percentile interval excluding zero. Tuning scores are selection diagnostics, not independent evidence of improvement.

Fit through 2025-08-31. Unknown host-region map rows: 7142 (including missing/un).

## Stage 1 — tuning (outcomes)

### Leaderboard

| Model | Best params | Map log loss | Series log loss | Rows |
|---|---|---:|---:|---:|
| player_round_glicko_rookie | {"k": 32, "new_player": "teammates", "rd_info": 0.25, "rd_new": 280, "rookie_maps": 400, "rookie_penalty": 200, "tau": 0.5} | 0.622668 | 0.584466 | 25649 |
| team_elo | {"k": 32} | 0.651782 | 0.626711 | 25649 |

Kalshi uses the first hourly bid/ask (midpoint for log loss, ask/bid for bets) ending ≥30 min after the market opened and ≥2 h before the scheduled start, with a spread ≤ 0.06: a price a bot could trade before any veto. Markets without such a quote are skipped. oriented to team1 using aliases. One contract per event, preferring team1. Compare identical rows; map predictions use the first map's pre-match chance. Missing links, aliases or candles are skipped; unplayed maps are not in the rows. Returns use frozen stage-1 parameters. Each bet buys $1 of contracts, fees extra; order fees ceil to a cent (0.07 × contracts × price × (1−price)). Edge selection uses unrounded per-contract fees. ROI divides profit by stake plus fees; intervals resample matches 2,000 times. Unlimited depth and depth-capped returns are shown together. Depth uses 0.5 of acceptable-price tape volume in the 6 hours after the quote, missing tapes give zero fills. Partial Kelly fills are allowed; flat bets require the full $1 stake. Kelly uses LoL caps and rounded-fee affordability, from a $50 seed. Each slice runs independently. Tape volume is a fill proxy; no slippage is modeled.

## Quote-time robustness

| Quote rule | Model | Kind | Rows | Raw Δ log loss | Blended Δ log loss | Raw flat ROI depth-capped | Blended flat ROI depth-capped |
|---|---|---|---:|---:|---:|---:|---:|
| tradeable | team_elo | series | 677 | 0.026644 | 0.000161 | 15.98% | 16.91% |
| tradeable | team_elo | map | 1049 | 0.005994 | 0.011243 | 52.76% | -5.79% |
| tradeable | player_round_glicko_rookie | series | 677 | -0.010090 | -0.013821 | 21.43% | 19.75% |
| tradeable | player_round_glicko_rookie | map | 1049 | -0.010355 | 0.003189 | 57.11% | 12.78% |
| tradeable | team_elo+form | series | 677 | 0.021016 | 0.000875 | 17.01% | 19.83% |
| tradeable | team_elo+form | map | 1049 | 0.004624 | 0.008039 | 51.73% | -0.14% |
| tradeable | team_elo+regional | series | 677 | 0.028115 | 0.000104 | 17.38% | 10.04% |
| tradeable | team_elo+regional | map | 1049 | 0.005838 | 0.011066 | 53.70% | -2.16% |
| tradeable | team_elo+regional_form | series | 677 | 0.022052 | 0.000533 | 19.43% | 16.33% |
| tradeable | team_elo+regional_form | map | 1049 | 0.004259 | 0.008507 | 54.00% | 2.20% |
| tradeable | player_round_glicko_rookie+form | series | 677 | -0.010599 | -0.012923 | 19.32% | 21.44% |
| tradeable | player_round_glicko_rookie+form | map | 1049 | -0.010666 | 0.000701 | 50.61% | 59.64% |
| tradeable | player_round_glicko_rookie+regional | series | 677 | -0.010019 | -0.013773 | 19.31% | 18.85% |
| tradeable | player_round_glicko_rookie+regional | map | 1049 | -0.010455 | 0.002338 | 57.56% | 10.07% |
| tradeable | player_round_glicko_rookie+regional_form | series | 677 | -0.010617 | -0.012900 | 18.24% | 21.21% |
| tradeable | player_round_glicko_rookie+regional_form | map | 1049 | -0.010748 | 0.000028 | 52.36% | 90.22% |
| hours24 | team_elo | series | 375 | 0.037793 | 0.011799 | -8.26% | -39.74% |
| hours24 | team_elo | map | 608 | -0.007035 | 0.004756 | 139.73% | 3.02% |
| hours24 | player_round_glicko_rookie | series | 375 | 0.003343 | 0.001913 | 7.78% | 19.86% |
| hours24 | player_round_glicko_rookie | map | 608 | -0.021420 | 0.000060 | 174.71% | 4.55% |
| hours24 | team_elo+form | series | 375 | 0.030076 | 0.011312 | -2.31% | -18.98% |
| hours24 | team_elo+form | map | 608 | -0.006972 | 0.004052 | 137.00% | 19.13% |
| hours24 | team_elo+regional | series | 375 | 0.041865 | 0.008626 | -12.46% | -46.17% |
| hours24 | team_elo+regional | map | 608 | -0.006371 | 0.004536 | 171.73% | -19.86% |
| hours24 | team_elo+regional_form | series | 375 | 0.033416 | 0.009392 | -4.10% | -32.64% |
| hours24 | team_elo+regional_form | map | 608 | -0.006520 | 0.003820 | 164.36% | -23.62% |
| hours24 | player_round_glicko_rookie+form | series | 375 | 0.002011 | -0.000115 | 6.37% | 14.84% |
| hours24 | player_round_glicko_rookie+form | map | 608 | -0.021178 | -0.000301 | 171.15% | 22.26% |
| hours24 | player_round_glicko_rookie+regional | series | 375 | 0.003273 | 0.001870 | 7.59% | 16.48% |
| hours24 | player_round_glicko_rookie+regional | map | 608 | -0.021249 | -0.000040 | 157.97% | 11.62% |
| hours24 | player_round_glicko_rookie+regional_form | series | 375 | 0.001975 | -0.000152 | 5.77% | 6.62% |
| hours24 | player_round_glicko_rookie+regional_form | map | 608 | -0.020999 | -0.000391 | 171.42% | 11.62% |
| hours6 | team_elo | series | 644 | 0.038723 | 0.005797 | -8.59% | -9.29% |
| hours6 | team_elo | map | 983 | 0.011234 | 0.009681 | 15.59% | 7.92% |
| hours6 | player_round_glicko_rookie | series | 644 | -0.000229 | -0.005932 | 4.57% | 7.94% |
| hours6 | player_round_glicko_rookie | map | 983 | -0.006840 | 0.008854 | 18.54% | 3.34% |
| hours6 | team_elo+form | series | 644 | 0.031482 | 0.007417 | -2.24% | -11.12% |
| hours6 | team_elo+form | map | 983 | 0.010263 | 0.011864 | 17.85% | 4.84% |
| hours6 | team_elo+regional | series | 644 | 0.040066 | 0.005471 | -8.73% | -6.20% |
| hours6 | team_elo+regional | map | 983 | 0.010847 | 0.009285 | 18.14% | 2.39% |
| hours6 | team_elo+regional_form | series | 644 | 0.032407 | 0.006966 | -0.81% | -12.06% |
| hours6 | team_elo+regional_form | map | 983 | 0.009685 | 0.011493 | 20.66% | 2.34% |
| hours6 | player_round_glicko_rookie+form | series | 644 | -0.001216 | -0.006344 | 2.00% | 6.65% |
| hours6 | player_round_glicko_rookie+form | map | 983 | -0.006909 | 0.009071 | 16.82% | 4.35% |
| hours6 | player_round_glicko_rookie+regional | series | 644 | -0.000247 | -0.005963 | 3.95% | 7.72% |
| hours6 | player_round_glicko_rookie+regional | map | 983 | -0.006944 | 0.008786 | 19.82% | 2.06% |
| hours6 | player_round_glicko_rookie+regional_form | series | 644 | -0.001241 | -0.006378 | 1.70% | 6.30% |
| hours6 | player_round_glicko_rookie+regional_form | map | 983 | -0.006992 | 0.009020 | 18.52% | 4.99% |

## Series independence: team_elo

Series independence [2025-09-01, 2026-07-01): 2421 matches.

Bo3: 2218 series, log loss 0.655463.

Bo5: 203 series, log loss 0.662286.

Map 2 after map-1 win: win rate 0.6469, model 0.6052, residual 0.0417 [0.0159, 0.0680], n=1317.

Map 2 after map-1 loss: win rate 0.4303, model 0.4501, residual -0.0199 [-0.0478, 0.0083], n=1104.

Map-2 residual contrast (win minus loss): 95% [0.0232, 0.0983].

Bo3 1–1 decider: residual 0.0027 [-0.0320, 0.0366], n=852.

Intervals resample whole matches; residual = won − model pre-map chance.

| Best of | Probability bin | Rows | Predicted | Actual |
|---:|---|---:|---:|---:|
| 3 | 0.0–0.1 | 48 | 0.0657 | 0.2500 |
| 3 | 0.1–0.2 | 98 | 0.1547 | 0.2347 |
| 3 | 0.2–0.3 | 176 | 0.2548 | 0.3864 |
| 3 | 0.3–0.4 | 230 | 0.3530 | 0.4304 |
| 3 | 0.4–0.5 | 330 | 0.4550 | 0.4697 |
| 3 | 0.5–0.6 | 419 | 0.5443 | 0.5752 |
| 3 | 0.6–0.7 | 330 | 0.6473 | 0.6333 |
| 3 | 0.7–0.8 | 280 | 0.7497 | 0.6750 |
| 3 | 0.8–0.9 | 205 | 0.8483 | 0.7805 |
| 3 | 0.9–1.0 | 102 | 0.9333 | 0.8333 |
| 5 | 0.0–0.1 | 3 | 0.0664 | 0.0000 |
| 5 | 0.1–0.2 | 9 | 0.1494 | 0.2222 |
| 5 | 0.2–0.3 | 28 | 0.2555 | 0.3571 |
| 5 | 0.3–0.4 | 21 | 0.3468 | 0.6190 |
| 5 | 0.4–0.5 | 32 | 0.4489 | 0.4688 |
| 5 | 0.5–0.6 | 31 | 0.5525 | 0.5806 |
| 5 | 0.6–0.7 | 25 | 0.6478 | 0.6000 |
| 5 | 0.7–0.8 | 19 | 0.7583 | 0.7895 |
| 5 | 0.8–0.9 | 25 | 0.8488 | 0.6800 |
| 5 | 0.9–1.0 | 10 | 0.9301 | 0.9000 |

## Series independence: player_round_glicko_rookie

Series independence [2025-09-01, 2026-07-01): 2421 matches.

Bo3: 2218 series, log loss 0.610868.

Bo5: 203 series, log loss 0.600797.

Map 2 after map-1 win: win rate 0.6469, model 0.6169, residual 0.0300 [0.0036, 0.0568], n=1317.

Map 2 after map-1 loss: win rate 0.4303, model 0.4375, residual -0.0072 [-0.0354, 0.0213], n=1104.

Map-2 residual contrast (win minus loss): 95% [-0.0007, 0.0727].

Bo3 1–1 decider: residual 0.0119 [-0.0219, 0.0460], n=852.

Intervals resample whole matches; residual = won − model pre-map chance.

| Best of | Probability bin | Rows | Predicted | Actual |
|---:|---|---:|---:|---:|
| 3 | 0.0–0.1 | 81 | 0.0480 | 0.1235 |
| 3 | 0.1–0.2 | 111 | 0.1515 | 0.2432 |
| 3 | 0.2–0.3 | 193 | 0.2536 | 0.3523 |
| 3 | 0.3–0.4 | 264 | 0.3568 | 0.3902 |
| 3 | 0.4–0.5 | 271 | 0.4523 | 0.4465 |
| 3 | 0.5–0.6 | 327 | 0.5525 | 0.6147 |
| 3 | 0.6–0.7 | 321 | 0.6509 | 0.6106 |
| 3 | 0.7–0.8 | 272 | 0.7442 | 0.7463 |
| 3 | 0.8–0.9 | 204 | 0.8477 | 0.7549 |
| 3 | 0.9–1.0 | 174 | 0.9603 | 0.9080 |
| 5 | 0.0–0.1 | 6 | 0.0345 | 0.1667 |
| 5 | 0.1–0.2 | 8 | 0.1610 | 0.1250 |
| 5 | 0.2–0.3 | 17 | 0.2421 | 0.1765 |
| 5 | 0.3–0.4 | 23 | 0.3577 | 0.3478 |
| 5 | 0.4–0.5 | 32 | 0.4542 | 0.6250 |
| 5 | 0.5–0.6 | 38 | 0.5430 | 0.5526 |
| 5 | 0.6–0.7 | 32 | 0.6533 | 0.6250 |
| 5 | 0.7–0.8 | 27 | 0.7345 | 0.8148 |
| 5 | 0.8–0.9 | 13 | 0.8567 | 0.8462 |
| 5 | 0.9–1.0 | 7 | 0.9343 | 1.0000 |

## Series independence: team_elo+form

Series independence [2025-09-01, 2026-07-01): 2421 matches.

Bo3: 2218 series, log loss 0.649718.

Bo5: 203 series, log loss 0.657740.

Map 2 after map-1 win: win rate 0.6469, model 0.6328, residual 0.0141 [-0.0118, 0.0408], n=1317.

Map 2 after map-1 loss: win rate 0.4303, model 0.4326, residual -0.0024 [-0.0302, 0.0257], n=1104.

Map-2 residual contrast (win minus loss): 95% [-0.0209, 0.0525].

Bo3 1–1 decider: residual -0.0020 [-0.0358, 0.0315], n=852.

Intervals resample whole matches; residual = won − model pre-map chance.

| Best of | Probability bin | Rows | Predicted | Actual |
|---:|---|---:|---:|---:|
| 3 | 0.0–0.1 | 89 | 0.0574 | 0.2022 |
| 3 | 0.1–0.2 | 123 | 0.1512 | 0.3089 |
| 3 | 0.2–0.3 | 178 | 0.2511 | 0.3708 |
| 3 | 0.3–0.4 | 231 | 0.3526 | 0.4329 |
| 3 | 0.4–0.5 | 273 | 0.4499 | 0.4469 |
| 3 | 0.5–0.6 | 340 | 0.5480 | 0.5412 |
| 3 | 0.6–0.7 | 273 | 0.6472 | 0.6374 |
| 3 | 0.7–0.8 | 286 | 0.7498 | 0.7238 |
| 3 | 0.8–0.9 | 239 | 0.8486 | 0.7573 |
| 3 | 0.9–1.0 | 186 | 0.9461 | 0.8118 |
| 5 | 0.0–0.1 | 6 | 0.0639 | 0.1667 |
| 5 | 0.1–0.2 | 13 | 0.1530 | 0.1538 |
| 5 | 0.2–0.3 | 23 | 0.2550 | 0.4348 |
| 5 | 0.3–0.4 | 28 | 0.3587 | 0.4643 |
| 5 | 0.4–0.5 | 24 | 0.4489 | 0.6250 |
| 5 | 0.5–0.6 | 25 | 0.5643 | 0.6400 |
| 5 | 0.6–0.7 | 23 | 0.6410 | 0.4783 |
| 5 | 0.7–0.8 | 16 | 0.7479 | 0.6250 |
| 5 | 0.8–0.9 | 25 | 0.8514 | 0.7600 |
| 5 | 0.9–1.0 | 20 | 0.9476 | 0.8500 |

## Series independence: team_elo+regional

Series independence [2025-09-01, 2026-07-01): 2421 matches.

Bo3: 2218 series, log loss 0.655256.

Bo5: 203 series, log loss 0.654082.

Map 2 after map-1 win: win rate 0.6469, model 0.6035, residual 0.0434 [0.0174, 0.0697], n=1317.

Map 2 after map-1 loss: win rate 0.4303, model 0.4515, residual -0.0212 [-0.0491, 0.0070], n=1104.

Map-2 residual contrast (win minus loss): 95% [0.0266, 0.1016].

Bo3 1–1 decider: residual 0.0027 [-0.0318, 0.0366], n=852.

Intervals resample whole matches; residual = won − model pre-map chance.

| Best of | Probability bin | Rows | Predicted | Actual |
|---:|---|---:|---:|---:|
| 3 | 0.0–0.1 | 42 | 0.0658 | 0.2619 |
| 3 | 0.1–0.2 | 99 | 0.1573 | 0.2323 |
| 3 | 0.2–0.3 | 173 | 0.2544 | 0.3815 |
| 3 | 0.3–0.4 | 235 | 0.3529 | 0.4298 |
| 3 | 0.4–0.5 | 331 | 0.4545 | 0.4713 |
| 3 | 0.5–0.6 | 428 | 0.5447 | 0.5724 |
| 3 | 0.6–0.7 | 333 | 0.6471 | 0.6276 |
| 3 | 0.7–0.8 | 279 | 0.7489 | 0.6953 |
| 3 | 0.8–0.9 | 205 | 0.8478 | 0.7756 |
| 3 | 0.9–1.0 | 93 | 0.9329 | 0.8280 |
| 5 | 0.0–0.1 | 3 | 0.0664 | 0.0000 |
| 5 | 0.1–0.2 | 7 | 0.1480 | 0.1429 |
| 5 | 0.2–0.3 | 29 | 0.2543 | 0.3448 |
| 5 | 0.3–0.4 | 18 | 0.3435 | 0.6111 |
| 5 | 0.4–0.5 | 35 | 0.4498 | 0.5143 |
| 5 | 0.5–0.6 | 32 | 0.5497 | 0.5625 |
| 5 | 0.6–0.7 | 25 | 0.6444 | 0.6000 |
| 5 | 0.7–0.8 | 19 | 0.7583 | 0.7895 |
| 5 | 0.8–0.9 | 25 | 0.8488 | 0.6800 |
| 5 | 0.9–1.0 | 10 | 0.9301 | 0.9000 |

## Series independence: team_elo+regional_form

Series independence [2025-09-01, 2026-07-01): 2421 matches.

Bo3: 2218 series, log loss 0.649081.

Bo5: 203 series, log loss 0.649322.

Map 2 after map-1 win: win rate 0.6469, model 0.6315, residual 0.0154 [-0.0107, 0.0421], n=1317.

Map 2 after map-1 loss: win rate 0.4303, model 0.4337, residual -0.0034 [-0.0311, 0.0250], n=1104.

Map-2 residual contrast (win minus loss): 95% [-0.0189, 0.0547].

Bo3 1–1 decider: residual -0.0021 [-0.0360, 0.0314], n=852.

Intervals resample whole matches; residual = won − model pre-map chance.

| Best of | Probability bin | Rows | Predicted | Actual |
|---:|---|---:|---:|---:|
| 3 | 0.0–0.1 | 80 | 0.0563 | 0.2125 |
| 3 | 0.1–0.2 | 129 | 0.1510 | 0.3023 |
| 3 | 0.2–0.3 | 174 | 0.2510 | 0.3678 |
| 3 | 0.3–0.4 | 238 | 0.3521 | 0.4370 |
| 3 | 0.4–0.5 | 271 | 0.4495 | 0.4428 |
| 3 | 0.5–0.6 | 346 | 0.5481 | 0.5376 |
| 3 | 0.6–0.7 | 276 | 0.6472 | 0.6449 |
| 3 | 0.7–0.8 | 288 | 0.7500 | 0.7153 |
| 3 | 0.8–0.9 | 241 | 0.8497 | 0.7676 |
| 3 | 0.9–1.0 | 175 | 0.9461 | 0.8114 |
| 5 | 0.0–0.1 | 5 | 0.0630 | 0.0000 |
| 5 | 0.1–0.2 | 15 | 0.1564 | 0.2000 |
| 5 | 0.2–0.3 | 19 | 0.2552 | 0.4737 |
| 5 | 0.3–0.4 | 29 | 0.3561 | 0.4483 |
| 5 | 0.4–0.5 | 24 | 0.4481 | 0.5833 |
| 5 | 0.5–0.6 | 27 | 0.5610 | 0.6667 |
| 5 | 0.6–0.7 | 23 | 0.6383 | 0.4783 |
| 5 | 0.7–0.8 | 16 | 0.7483 | 0.6250 |
| 5 | 0.8–0.9 | 24 | 0.8498 | 0.7500 |
| 5 | 0.9–1.0 | 21 | 0.9456 | 0.8571 |

## Series independence: player_round_glicko_rookie+form

Series independence [2025-09-01, 2026-07-01): 2421 matches.

Bo3: 2218 series, log loss 0.612113.

Bo5: 203 series, log loss 0.599026.

Map 2 after map-1 win: win rate 0.6469, model 0.6264, residual 0.0205 [-0.0058, 0.0476], n=1317.

Map 2 after map-1 loss: win rate 0.4303, model 0.4317, residual -0.0014 [-0.0299, 0.0271], n=1104.

Map-2 residual contrast (win minus loss): 95% [-0.0153, 0.0578].

Bo3 1–1 decider: residual 0.0097 [-0.0241, 0.0437], n=852.

Intervals resample whole matches; residual = won − model pre-map chance.

| Best of | Probability bin | Rows | Predicted | Actual |
|---:|---|---:|---:|---:|
| 3 | 0.0–0.1 | 93 | 0.0449 | 0.0968 |
| 3 | 0.1–0.2 | 137 | 0.1521 | 0.2847 |
| 3 | 0.2–0.3 | 187 | 0.2534 | 0.3797 |
| 3 | 0.3–0.4 | 253 | 0.3573 | 0.3874 |
| 3 | 0.4–0.5 | 242 | 0.4507 | 0.4256 |
| 3 | 0.5–0.6 | 307 | 0.5508 | 0.6156 |
| 3 | 0.6–0.7 | 299 | 0.6503 | 0.5987 |
| 3 | 0.7–0.8 | 283 | 0.7464 | 0.7527 |
| 3 | 0.8–0.9 | 213 | 0.8506 | 0.7230 |
| 3 | 0.9–1.0 | 204 | 0.9589 | 0.9118 |
| 5 | 0.0–0.1 | 8 | 0.0462 | 0.2500 |
| 5 | 0.1–0.2 | 9 | 0.1678 | 0.1111 |
| 5 | 0.2–0.3 | 16 | 0.2416 | 0.1875 |
| 5 | 0.3–0.4 | 23 | 0.3512 | 0.4348 |
| 5 | 0.4–0.5 | 27 | 0.4530 | 0.5556 |
| 5 | 0.5–0.6 | 41 | 0.5456 | 0.5854 |
| 5 | 0.6–0.7 | 27 | 0.6582 | 0.5926 |
| 5 | 0.7–0.8 | 29 | 0.7468 | 0.7586 |
| 5 | 0.8–0.9 | 11 | 0.8430 | 0.8182 |
| 5 | 0.9–1.0 | 12 | 0.9396 | 1.0000 |

## Series independence: player_round_glicko_rookie+regional

Series independence [2025-09-01, 2026-07-01): 2421 matches.

Bo3: 2218 series, log loss 0.610749.

Bo5: 203 series, log loss 0.598240.

Map 2 after map-1 win: win rate 0.6469, model 0.6169, residual 0.0300 [0.0035, 0.0569], n=1317.

Map 2 after map-1 loss: win rate 0.4303, model 0.4373, residual -0.0071 [-0.0354, 0.0212], n=1104.

Map-2 residual contrast (win minus loss): 95% [-0.0005, 0.0725].

Bo3 1–1 decider: residual 0.0118 [-0.0221, 0.0459], n=852.

Intervals resample whole matches; residual = won − model pre-map chance.

| Best of | Probability bin | Rows | Predicted | Actual |
|---:|---|---:|---:|---:|
| 3 | 0.0–0.1 | 82 | 0.0487 | 0.1220 |
| 3 | 0.1–0.2 | 111 | 0.1523 | 0.2523 |
| 3 | 0.2–0.3 | 192 | 0.2527 | 0.3490 |
| 3 | 0.3–0.4 | 266 | 0.3571 | 0.3910 |
| 3 | 0.4–0.5 | 270 | 0.4524 | 0.4407 |
| 3 | 0.5–0.6 | 323 | 0.5518 | 0.6161 |
| 3 | 0.6–0.7 | 320 | 0.6501 | 0.6156 |
| 3 | 0.7–0.8 | 276 | 0.7440 | 0.7428 |
| 3 | 0.8–0.9 | 204 | 0.8475 | 0.7549 |
| 3 | 0.9–1.0 | 174 | 0.9600 | 0.9080 |
| 5 | 0.0–0.1 | 6 | 0.0345 | 0.1667 |
| 5 | 0.1–0.2 | 9 | 0.1673 | 0.1111 |
| 5 | 0.2–0.3 | 16 | 0.2442 | 0.1875 |
| 5 | 0.3–0.4 | 23 | 0.3579 | 0.3913 |
| 5 | 0.4–0.5 | 31 | 0.4554 | 0.6129 |
| 5 | 0.5–0.6 | 39 | 0.5424 | 0.5385 |
| 5 | 0.6–0.7 | 31 | 0.6522 | 0.6129 |
| 5 | 0.7–0.8 | 28 | 0.7340 | 0.8214 |
| 5 | 0.8–0.9 | 13 | 0.8567 | 0.8462 |
| 5 | 0.9–1.0 | 7 | 0.9343 | 1.0000 |

## Series independence: player_round_glicko_rookie+regional_form

Series independence [2025-09-01, 2026-07-01): 2421 matches.

Bo3: 2218 series, log loss 0.612047.

Bo5: 203 series, log loss 0.596415.

Map 2 after map-1 win: win rate 0.6469, model 0.6264, residual 0.0205 [-0.0059, 0.0476], n=1317.

Map 2 after map-1 loss: win rate 0.4303, model 0.4315, residual -0.0012 [-0.0295, 0.0273], n=1104.

Map-2 residual contrast (win minus loss): 95% [-0.0155, 0.0576].

Bo3 1–1 decider: residual 0.0097 [-0.0243, 0.0436], n=852.

Intervals resample whole matches; residual = won − model pre-map chance.

| Best of | Probability bin | Rows | Predicted | Actual |
|---:|---|---:|---:|---:|
| 3 | 0.0–0.1 | 93 | 0.0448 | 0.0968 |
| 3 | 0.1–0.2 | 138 | 0.1522 | 0.2826 |
| 3 | 0.2–0.3 | 185 | 0.2523 | 0.3838 |
| 3 | 0.3–0.4 | 256 | 0.3569 | 0.3828 |
| 3 | 0.4–0.5 | 241 | 0.4508 | 0.4315 |
| 3 | 0.5–0.6 | 304 | 0.5505 | 0.6118 |
| 3 | 0.6–0.7 | 296 | 0.6496 | 0.6014 |
| 3 | 0.7–0.8 | 287 | 0.7459 | 0.7561 |
| 3 | 0.8–0.9 | 213 | 0.8502 | 0.7136 |
| 3 | 0.9–1.0 | 205 | 0.9584 | 0.9122 |
| 5 | 0.0–0.1 | 7 | 0.0397 | 0.1429 |
| 5 | 0.1–0.2 | 10 | 0.1608 | 0.2000 |
| 5 | 0.2–0.3 | 16 | 0.2415 | 0.1875 |
| 5 | 0.3–0.4 | 23 | 0.3528 | 0.4348 |
| 5 | 0.4–0.5 | 25 | 0.4510 | 0.5600 |
| 5 | 0.5–0.6 | 43 | 0.5441 | 0.5814 |
| 5 | 0.6–0.7 | 27 | 0.6595 | 0.5926 |
| 5 | 0.7–0.8 | 29 | 0.7469 | 0.7586 |
| 5 | 0.8–0.9 | 11 | 0.8432 | 0.8182 |
| 5 | 0.9–1.0 | 12 | 0.9397 | 1.0000 |

### Maps

| Model | Section | Rows | Log loss | Brier | Accuracy | ECE |
|---|---|---:|---:|---:|---:|---:|
| coin | all | 25649 | 0.693147 | 0.250000 | 0.500000 | 0.042087 |
| coin | vct | 3333 | 0.693147 | 0.250000 | 0.500000 | 0.018152 |
| coin | vcl | 14263 | 0.693147 | 0.250000 | 0.500000 | 0.028150 |
| coin | gc | 4129 | 0.693147 | 0.250000 | 0.500000 | 0.084887 |
| coin | t3 | 1455 | 0.693147 | 0.250000 | 0.500000 | 0.071821 |
| coin | collegiate | 95 | 0.693147 | 0.250000 | 0.500000 | 0.089474 |
| coin | offseason | 2374 | 0.693147 | 0.250000 | 0.500000 | 0.064869 |
| coin | unknown | 0 | — | — | — | — |
| coin | international=1 | 751 | 0.693147 | 0.250000 | 0.500000 | 0.004660 |
| coin | international=0 | 24898 | 0.693147 | 0.250000 | 0.500000 | 0.043216 |

| Model | Section | Rows | Log loss | Brier | Accuracy | ECE |
|---|---|---:|---:|---:|---:|---:|
| team_elo | all | 25649 | 0.651782 | 0.229929 | 0.615989 | 0.023986 |
| team_elo | vct | 3333 | 0.677574 | 0.240943 | 0.581758 | 0.063446 |
| team_elo | vcl | 14263 | 0.650388 | 0.229421 | 0.618734 | 0.018886 |
| team_elo | gc | 4129 | 0.626845 | 0.218485 | 0.645193 | 0.051156 |
| team_elo | t3 | 1455 | 0.665545 | 0.236579 | 0.598969 | 0.059461 |
| team_elo | collegiate | 95 | 0.656779 | 0.233016 | 0.594737 | 0.079508 |
| team_elo | offseason | 2374 | 0.658675 | 0.233225 | 0.608045 | 0.032891 |
| team_elo | unknown | 0 | — | — | — | — |
| team_elo | international=1 | 751 | 0.679081 | 0.241826 | 0.585885 | 0.050186 |
| team_elo | international=0 | 24898 | 0.650958 | 0.229570 | 0.616897 | 0.024461 |

team_elo − coin (paired log loss):

| Section | Rows | team_elo log loss | coin log loss | Difference | 95% interval | Significant |
|---|---:|---:|---:|---:|---|---|
| all | 25649 | 0.651782 | 0.693147 | -0.041366 | [-0.046095, -0.037066] | yes |

| Model | Section | Rows | Log loss | Brier | Accuracy | ECE |
|---|---|---:|---:|---:|---:|---:|
| player_round_glicko_rookie | all | 25649 | 0.622668 | 0.217092 | 0.646399 | 0.009044 |
| player_round_glicko_rookie | vct | 3333 | 0.661363 | 0.234335 | 0.597960 | 0.017087 |
| player_round_glicko_rookie | vcl | 14263 | 0.625591 | 0.218209 | 0.645692 | 0.009913 |
| player_round_glicko_rookie | gc | 4129 | 0.577911 | 0.198295 | 0.695205 | 0.025630 |
| player_round_glicko_rookie | t3 | 1455 | 0.626518 | 0.217860 | 0.634021 | 0.042809 |
| player_round_glicko_rookie | collegiate | 95 | 0.606615 | 0.211588 | 0.657895 | 0.050834 |
| player_round_glicko_rookie | offseason | 2374 | 0.626908 | 0.218618 | 0.640901 | 0.018630 |
| player_round_glicko_rookie | unknown | 0 | — | — | — | — |
| player_round_glicko_rookie | international=1 | 751 | 0.661279 | 0.234584 | 0.604527 | 0.031240 |
| player_round_glicko_rookie | international=0 | 24898 | 0.621504 | 0.216565 | 0.647662 | 0.009878 |

player_round_glicko_rookie − coin (paired log loss):

| Section | Rows | player_round_glicko_rookie log loss | coin log loss | Difference | 95% interval | Significant |
|---|---:|---:|---:|---:|---|---|
| all | 25649 | 0.622668 | 0.693147 | -0.070479 | [-0.075322, -0.065707] | yes |

player_round_glicko_rookie − team_elo (paired log loss):

| Section | Rows | player_round_glicko_rookie log loss | team_elo log loss | Difference | 95% interval | Significant |
|---|---:|---:|---:|---:|---|---|
| all | 25649 | 0.622668 | 0.651782 | -0.029113 | [-0.032734, -0.025553] | yes |

### Series

| Model | Section | Rows | Log loss | Brier | Accuracy | ECE |
|---|---|---:|---:|---:|---:|---:|
| coin | all | 11288 | 0.693147 | 0.250000 | 0.500000 | 0.054128 |
| coin | vct | 1322 | 0.693147 | 0.250000 | 0.500000 | 0.037065 |
| coin | vcl | 6463 | 0.693147 | 0.250000 | 0.500000 | 0.035510 |
| coin | gc | 1698 | 0.693147 | 0.250000 | 0.500000 | 0.106007 |
| coin | t3 | 650 | 0.693147 | 0.250000 | 0.500000 | 0.092308 |
| coin | collegiate | 42 | 0.693147 | 0.250000 | 0.500000 | 0.095238 |
| coin | offseason | 1113 | 0.693147 | 0.250000 | 0.500000 | 0.079515 |
| coin | unknown | 0 | — | — | — | — |
| coin | international=1 | 310 | 0.693147 | 0.250000 | 0.500000 | 0.016129 |
| coin | international=0 | 10978 | 0.693147 | 0.250000 | 0.500000 | 0.055201 |

| Model | Section | Rows | Log loss | Brier | Accuracy | ECE |
|---|---|---:|---:|---:|---:|---:|
| team_elo | all | 11288 | 0.626711 | 0.218731 | 0.643692 | 0.027296 |
| team_elo | vct | 1322 | 0.641839 | 0.225179 | 0.627837 | 0.034264 |
| team_elo | vcl | 6463 | 0.624950 | 0.217878 | 0.650549 | 0.018614 |
| team_elo | gc | 1698 | 0.601043 | 0.207539 | 0.657833 | 0.070171 |
| team_elo | t3 | 650 | 0.656447 | 0.232376 | 0.603846 | 0.081441 |
| team_elo | collegiate | 42 | 0.643076 | 0.226759 | 0.630952 | 0.119004 |
| team_elo | offseason | 1113 | 0.640138 | 0.224827 | 0.624888 | 0.034341 |
| team_elo | unknown | 0 | — | — | — | — |
| team_elo | international=1 | 310 | 0.663269 | 0.234321 | 0.619355 | 0.046489 |
| team_elo | international=0 | 10978 | 0.625678 | 0.218291 | 0.644380 | 0.028178 |

team_elo − coin (paired log loss):

| Section | Rows | team_elo log loss | coin log loss | Difference | 95% interval | Significant |
|---|---:|---:|---:|---:|---|---|
| all | 11288 | 0.626711 | 0.693147 | -0.066437 | [-0.072453, -0.059803] | yes |

| Model | Section | Rows | Log loss | Brier | Accuracy | ECE |
|---|---|---:|---:|---:|---:|---:|
| player_round_glicko_rookie | all | 11288 | 0.584466 | 0.200032 | 0.685861 | 0.016459 |
| player_round_glicko_rookie | vct | 1322 | 0.625366 | 0.218607 | 0.641452 | 0.019528 |
| player_round_glicko_rookie | vcl | 6463 | 0.588342 | 0.201578 | 0.682268 | 0.014086 |
| player_round_glicko_rookie | gc | 1698 | 0.521406 | 0.173772 | 0.750000 | 0.044263 |
| player_round_glicko_rookie | t3 | 650 | 0.600497 | 0.203875 | 0.667692 | 0.060811 |
| player_round_glicko_rookie | collegiate | 42 | 0.620345 | 0.216045 | 0.678571 | 0.105528 |
| player_round_glicko_rookie | offseason | 1113 | 0.598862 | 0.206209 | 0.672507 | 0.028604 |
| player_round_glicko_rookie | unknown | 0 | — | — | — | — |
| player_round_glicko_rookie | international=1 | 310 | 0.635640 | 0.223061 | 0.629032 | 0.022102 |
| player_round_glicko_rookie | international=0 | 10978 | 0.583021 | 0.199382 | 0.687466 | 0.017327 |

player_round_glicko_rookie − coin (paired log loss):

| Section | Rows | player_round_glicko_rookie log loss | coin log loss | Difference | 95% interval | Significant |
|---|---:|---:|---:|---:|---|---|
| all | 11288 | 0.584466 | 0.693147 | -0.108681 | [-0.116419, -0.100538] | yes |

player_round_glicko_rookie − team_elo (paired log loss):

| Section | Rows | player_round_glicko_rookie log loss | team_elo log loss | Difference | 95% interval | Significant |
|---|---:|---:|---:|---:|---|---|
| all | 11288 | 0.584466 | 0.626711 | -0.042245 | [-0.048494, -0.036019] | yes |

## Stage 2 — validation (outcomes)

### Leaderboard (frozen stage-1 parameters)

| Model | Best params | Map log loss | Series log loss | Rows |
|---|---|---:|---:|---:|
| player_round_glicko_rookie+regional_form | {"k": 32, "new_player": "teammates", "rd_info": 0.25, "rd_new": 280, "rookie_maps": 400, "rookie_penalty": 200, "tau": 0.5} | 0.638461 | 0.603490 | 6337 |
| player_round_glicko_rookie+regional | {"k": 32, "new_player": "teammates", "rd_info": 0.25, "rd_new": 280, "rookie_maps": 400, "rookie_penalty": 200, "tau": 0.5} | 0.638530 | 0.606442 | 6337 |
| player_round_glicko_rookie+form | {"k": 32, "new_player": "teammates", "rd_info": 0.25, "rd_new": 280, "rookie_maps": 400, "rookie_penalty": 200, "tau": 0.5} | 0.638613 | 0.603856 | 6337 |
| player_round_glicko_rookie | {"k": 32, "new_player": "teammates", "rd_info": 0.25, "rd_new": 280, "rookie_maps": 400, "rookie_penalty": 200, "tau": 0.5} | 0.638693 | 0.606622 | 6337 |
| team_elo+regional_form | {"k": 32} | 0.657048 | 0.628785 | 6337 |
| team_elo+form | {"k": 32} | 0.657731 | 0.629253 | 6337 |
| team_elo+regional | {"k": 32} | 0.662588 | 0.643500 | 6337 |
| team_elo | {"k": 32} | 0.662947 | 0.643432 | 6337 |

### Maps

| Model | Section | Rows | Log loss | Brier | Accuracy | ECE |
|---|---|---:|---:|---:|---:|---:|
| coin | all | 6337 | 0.693147 | 0.250000 | 0.500000 | 0.043475 |
| coin | vct | 1080 | 0.693147 | 0.250000 | 0.500000 | 0.016667 |
| coin | vcl | 3374 | 0.693147 | 0.250000 | 0.500000 | 0.047125 |
| coin | gc | 1005 | 0.693147 | 0.250000 | 0.500000 | 0.103980 |
| coin | t3 | 16 | 0.693147 | 0.250000 | 0.500000 | 0.250000 |
| coin | collegiate | 7 | 0.693147 | 0.250000 | 0.500000 | 0.071429 |
| coin | offseason | 855 | 0.693147 | 0.250000 | 0.500000 | 0.030994 |
| coin | unknown | 0 | — | — | — | — |
| coin | international=1 | 268 | 0.693147 | 0.250000 | 0.500000 | 0.003731 |
| coin | international=0 | 6069 | 0.693147 | 0.250000 | 0.500000 | 0.045230 |

| Model | Section | Rows | Log loss | Brier | Accuracy | ECE |
|---|---|---:|---:|---:|---:|---:|
| team_elo | all | 6337 | 0.662947 | 0.234966 | 0.602730 | 0.031254 |
| team_elo | vct | 1080 | 0.685646 | 0.245671 | 0.564815 | 0.063606 |
| team_elo | vcl | 3374 | 0.666871 | 0.236503 | 0.604624 | 0.042181 |
| team_elo | gc | 1005 | 0.631112 | 0.221113 | 0.637313 | 0.043127 |
| team_elo | t3 | 16 | 0.458119 | 0.148245 | 0.750000 | 0.220932 |
| team_elo | collegiate | 7 | 0.735155 | 0.270941 | 0.285714 | 0.236280 |
| team_elo | offseason | 855 | 0.659448 | 0.232990 | 0.602339 | 0.029427 |
| team_elo | unknown | 0 | — | — | — | — |
| team_elo | international=1 | 268 | 0.672124 | 0.240160 | 0.589552 | 0.065781 |
| team_elo | international=0 | 6069 | 0.662541 | 0.234737 | 0.603312 | 0.030130 |

team_elo − coin (paired log loss):

| Section | Rows | team_elo log loss | coin log loss | Difference | 95% interval | Significant |
|---|---:|---:|---:|---:|---|---|
| all | 6337 | 0.662947 | 0.693147 | -0.030201 | [-0.038540, -0.021979] | yes |
| vct | 1080 | 0.685646 | 0.693147 | -0.007501 | [-0.027539, 0.011220] | no |
| vcl | 3374 | 0.666871 | 0.693147 | -0.026276 | [-0.037134, -0.014615] | yes |
| gc | 1005 | 0.631112 | 0.693147 | -0.062035 | [-0.085840, -0.039958] | yes |
| t3 | 16 | 0.458119 | 0.693147 | -0.235028 | [-0.504444, -0.062593] | yes |
| collegiate | 7 | 0.735155 | 0.693147 | 0.042008 | [0.035882, 0.046602] | yes |
| offseason | 855 | 0.659448 | 0.693147 | -0.033700 | [-0.057063, -0.010644] | yes |
| international=1 | 268 | 0.672124 | 0.693147 | -0.021024 | [-0.063385, 0.018346] | no |
| international=0 | 6069 | 0.662541 | 0.693147 | -0.030606 | [-0.039247, -0.021872] | yes |

| Model | Section | Rows | Log loss | Brier | Accuracy | ECE |
|---|---|---:|---:|---:|---:|---:|
| player_round_glicko_rookie | all | 6337 | 0.638693 | 0.223702 | 0.631687 | 0.015405 |
| player_round_glicko_rookie | vct | 1080 | 0.667241 | 0.237238 | 0.591667 | 0.034482 |
| player_round_glicko_rookie | vcl | 3374 | 0.643621 | 0.225550 | 0.628334 | 0.031249 |
| player_round_glicko_rookie | gc | 1005 | 0.593128 | 0.204091 | 0.679602 | 0.026907 |
| player_round_glicko_rookie | t3 | 16 | 0.536829 | 0.186297 | 0.687500 | 0.238687 |
| player_round_glicko_rookie | collegiate | 7 | 0.719943 | 0.263865 | 0.428571 | 0.161536 |
| player_round_glicko_rookie | offseason | 855 | 0.637983 | 0.222732 | 0.639766 | 0.021006 |
| player_round_glicko_rookie | unknown | 0 | — | — | — | — |
| player_round_glicko_rookie | international=1 | 268 | 0.667079 | 0.237581 | 0.597015 | 0.043891 |
| player_round_glicko_rookie | international=0 | 6069 | 0.637439 | 0.223089 | 0.633218 | 0.016391 |

player_round_glicko_rookie − coin (paired log loss):

| Section | Rows | player_round_glicko_rookie log loss | coin log loss | Difference | 95% interval | Significant |
|---|---:|---:|---:|---:|---|---|
| all | 6337 | 0.638693 | 0.693147 | -0.054454 | [-0.063703, -0.045388] | yes |
| vct | 1080 | 0.667241 | 0.693147 | -0.025906 | [-0.042020, -0.010591] | yes |
| vcl | 3374 | 0.643621 | 0.693147 | -0.049526 | [-0.062517, -0.036427] | yes |
| gc | 1005 | 0.593128 | 0.693147 | -0.100019 | [-0.126011, -0.075221] | yes |
| t3 | 16 | 0.536829 | 0.693147 | -0.156319 | [-0.492423, 0.064567] | no |
| collegiate | 7 | 0.719943 | 0.693147 | 0.026795 | [0.026330, 0.027145] | yes |
| offseason | 855 | 0.637983 | 0.693147 | -0.055164 | [-0.082896, -0.029099] | yes |
| international=1 | 268 | 0.667079 | 0.693147 | -0.026068 | [-0.055209, 0.000311] | no |
| international=0 | 6069 | 0.637439 | 0.693147 | -0.055708 | [-0.065270, -0.046598] | yes |

| Model | Section | Rows | Log loss | Brier | Accuracy | ECE |
|---|---|---:|---:|---:|---:|---:|
| team_elo+form | all | 6337 | 0.657731 | 0.231818 | 0.618747 | 0.032462 |
| team_elo+form | vct | 1080 | 0.685729 | 0.245335 | 0.582407 | 0.071589 |
| team_elo+form | vcl | 3374 | 0.664542 | 0.234134 | 0.616183 | 0.039915 |
| team_elo+form | gc | 1005 | 0.614125 | 0.213526 | 0.667164 | 0.043058 |
| team_elo+form | t3 | 16 | 0.431784 | 0.141729 | 0.750000 | 0.125212 |
| team_elo+form | collegiate | 7 | 0.793952 | 0.298100 | 0.285714 | 0.408248 |
| team_elo+form | offseason | 855 | 0.649859 | 0.228249 | 0.618129 | 0.035971 |
| team_elo+form | unknown | 0 | — | — | — | — |
| team_elo+form | international=1 | 268 | 0.673584 | 0.240436 | 0.593284 | 0.070586 |
| team_elo+form | international=0 | 6069 | 0.657031 | 0.231438 | 0.619871 | 0.031068 |

team_elo+form − coin (paired log loss):

| Section | Rows | team_elo+form log loss | coin log loss | Difference | 95% interval | Significant |
|---|---:|---:|---:|---:|---|---|
| all | 6337 | 0.657731 | 0.693147 | -0.035416 | [-0.045681, -0.025441] | yes |
| vct | 1080 | 0.685729 | 0.693147 | -0.007418 | [-0.029695, 0.013497] | no |
| vcl | 3374 | 0.664542 | 0.693147 | -0.028605 | [-0.042994, -0.014042] | yes |
| gc | 1005 | 0.614125 | 0.693147 | -0.079022 | [-0.108296, -0.051919] | yes |
| t3 | 16 | 0.431784 | 0.693147 | -0.261363 | [-0.567619, -0.069920] | yes |
| collegiate | 7 | 0.793952 | 0.693147 | 0.100804 | [0.083069, 0.124451] | yes |
| offseason | 855 | 0.649859 | 0.693147 | -0.043288 | [-0.071010, -0.016012] | yes |
| international=1 | 268 | 0.673584 | 0.693147 | -0.019563 | [-0.065645, 0.024981] | no |
| international=0 | 6069 | 0.657031 | 0.693147 | -0.036116 | [-0.046997, -0.026004] | yes |

| Model | Section | Rows | Log loss | Brier | Accuracy | ECE |
|---|---|---:|---:|---:|---:|---:|
| team_elo+regional | all | 6337 | 0.662588 | 0.234813 | 0.603046 | 0.027984 |
| team_elo+regional | vct | 1080 | 0.684610 | 0.245045 | 0.567593 | 0.053731 |
| team_elo+regional | vcl | 3374 | 0.666871 | 0.236503 | 0.604624 | 0.042181 |
| team_elo+regional | gc | 1005 | 0.630890 | 0.221018 | 0.636318 | 0.041574 |
| team_elo+regional | t3 | 16 | 0.458119 | 0.148245 | 0.750000 | 0.220932 |
| team_elo+regional | collegiate | 7 | 0.735155 | 0.270941 | 0.285714 | 0.236280 |
| team_elo+regional | offseason | 855 | 0.658357 | 0.232757 | 0.602339 | 0.030131 |
| team_elo+regional | unknown | 0 | — | — | — | — |
| team_elo+regional | international=1 | 268 | 0.663479 | 0.236079 | 0.593284 | 0.034255 |
| team_elo+regional | international=0 | 6069 | 0.662548 | 0.234757 | 0.603477 | 0.029081 |

team_elo+regional − coin (paired log loss):

| Section | Rows | team_elo+regional log loss | coin log loss | Difference | 95% interval | Significant |
|---|---:|---:|---:|---:|---|---|
| all | 6337 | 0.662588 | 0.693147 | -0.030559 | [-0.038621, -0.022630] | yes |
| vct | 1080 | 0.684610 | 0.693147 | -0.008538 | [-0.026921, 0.009760] | no |
| vcl | 3374 | 0.666871 | 0.693147 | -0.026276 | [-0.037134, -0.014615] | yes |
| gc | 1005 | 0.630890 | 0.693147 | -0.062257 | [-0.085485, -0.040702] | yes |
| t3 | 16 | 0.458119 | 0.693147 | -0.235028 | [-0.504444, -0.062593] | yes |
| collegiate | 7 | 0.735155 | 0.693147 | 0.042008 | [0.035882, 0.046602] | yes |
| offseason | 855 | 0.658357 | 0.693147 | -0.034790 | [-0.056762, -0.013302] | yes |
| international=1 | 268 | 0.663479 | 0.693147 | -0.029668 | [-0.062684, 0.000328] | no |
| international=0 | 6069 | 0.662548 | 0.693147 | -0.030599 | [-0.039133, -0.021945] | yes |

| Model | Section | Rows | Log loss | Brier | Accuracy | ECE |
|---|---|---:|---:|---:|---:|---:|
| team_elo+regional_form | all | 6337 | 0.657048 | 0.231547 | 0.618431 | 0.030834 |
| team_elo+regional_form | vct | 1080 | 0.683930 | 0.244464 | 0.581481 | 0.064437 |
| team_elo+regional_form | vcl | 3374 | 0.664608 | 0.234142 | 0.615886 | 0.040918 |
| team_elo+regional_form | gc | 1005 | 0.613256 | 0.213172 | 0.666169 | 0.041712 |
| team_elo+regional_form | t3 | 16 | 0.431583 | 0.141687 | 0.750000 | 0.098682 |
| team_elo+regional_form | collegiate | 7 | 0.794982 | 0.298541 | 0.285714 | 0.325608 |
| team_elo+regional_form | offseason | 855 | 0.647825 | 0.227722 | 0.619298 | 0.033947 |
| team_elo+regional_form | unknown | 0 | — | — | — | — |
| team_elo+regional_form | international=1 | 268 | 0.661266 | 0.235211 | 0.593284 | 0.078263 |
| team_elo+regional_form | international=0 | 6069 | 0.656862 | 0.231385 | 0.619542 | 0.030690 |

team_elo+regional_form − coin (paired log loss):

| Section | Rows | team_elo+regional_form log loss | coin log loss | Difference | 95% interval | Significant |
|---|---:|---:|---:|---:|---|---|
| all | 6337 | 0.657048 | 0.693147 | -0.036099 | [-0.046159, -0.026535] | yes |
| vct | 1080 | 0.683930 | 0.693147 | -0.009218 | [-0.029852, 0.011348] | no |
| vcl | 3374 | 0.664608 | 0.693147 | -0.028539 | [-0.042960, -0.013941] | yes |
| gc | 1005 | 0.613256 | 0.693147 | -0.079892 | [-0.108655, -0.053184] | yes |
| t3 | 16 | 0.431583 | 0.693147 | -0.261565 | [-0.568177, -0.069984] | yes |
| collegiate | 7 | 0.794982 | 0.693147 | 0.101835 | [0.083833, 0.125837] | yes |
| offseason | 855 | 0.647825 | 0.693147 | -0.045323 | [-0.071174, -0.019909] | yes |
| international=1 | 268 | 0.661266 | 0.693147 | -0.031882 | [-0.070909, 0.004896] | no |
| international=0 | 6069 | 0.656862 | 0.693147 | -0.036285 | [-0.047076, -0.026150] | yes |

| Model | Section | Rows | Log loss | Brier | Accuracy | ECE |
|---|---|---:|---:|---:|---:|---:|
| player_round_glicko_rookie+form | all | 6337 | 0.638613 | 0.223444 | 0.637683 | 0.022978 |
| player_round_glicko_rookie+form | vct | 1080 | 0.667071 | 0.237142 | 0.592593 | 0.036802 |
| player_round_glicko_rookie+form | vcl | 3374 | 0.645466 | 0.225977 | 0.631891 | 0.038048 |
| player_round_glicko_rookie+form | gc | 1005 | 0.587792 | 0.201763 | 0.694527 | 0.036813 |
| player_round_glicko_rookie+form | t3 | 16 | 0.519825 | 0.179991 | 0.687500 | 0.277736 |
| player_round_glicko_rookie+form | collegiate | 7 | 0.742520 | 0.274706 | 0.428571 | 0.413265 |
| player_round_glicko_rookie+form | offseason | 855 | 0.636728 | 0.222021 | 0.651462 | 0.033269 |
| player_round_glicko_rookie+form | unknown | 0 | — | — | — | — |
| player_round_glicko_rookie+form | international=1 | 268 | 0.664210 | 0.236190 | 0.623134 | 0.067325 |
| player_round_glicko_rookie+form | international=0 | 6069 | 0.637482 | 0.222881 | 0.638326 | 0.022634 |

player_round_glicko_rookie+form − coin (paired log loss):

| Section | Rows | player_round_glicko_rookie+form log loss | coin log loss | Difference | 95% interval | Significant |
|---|---:|---:|---:|---:|---|---|
| all | 6337 | 0.638613 | 0.693147 | -0.054535 | [-0.064449, -0.044704] | yes |
| vct | 1080 | 0.667071 | 0.693147 | -0.026076 | [-0.042764, -0.009923] | yes |
| vcl | 3374 | 0.645466 | 0.693147 | -0.047681 | [-0.061745, -0.033218] | yes |
| gc | 1005 | 0.587792 | 0.693147 | -0.105355 | [-0.133178, -0.078892] | yes |
| t3 | 16 | 0.519825 | 0.693147 | -0.173322 | [-0.513074, 0.043349] | no |
| collegiate | 7 | 0.742520 | 0.693147 | 0.049373 | [0.044790, 0.055484] | yes |
| offseason | 855 | 0.636728 | 0.693147 | -0.056420 | [-0.084935, -0.028512] | yes |
| international=1 | 268 | 0.664210 | 0.693147 | -0.028937 | [-0.059717, -0.000770] | yes |
| international=0 | 6069 | 0.637482 | 0.693147 | -0.055665 | [-0.065914, -0.045866] | yes |

| Model | Section | Rows | Log loss | Brier | Accuracy | ECE |
|---|---|---:|---:|---:|---:|---:|
| player_round_glicko_rookie+regional | all | 6337 | 0.638530 | 0.223624 | 0.632949 | 0.015387 |
| player_round_glicko_rookie+regional | vct | 1080 | 0.667022 | 0.237133 | 0.594444 | 0.034133 |
| player_round_glicko_rookie+regional | vcl | 3374 | 0.643621 | 0.225550 | 0.628334 | 0.031249 |
| player_round_glicko_rookie+regional | gc | 1005 | 0.592646 | 0.203815 | 0.681592 | 0.030864 |
| player_round_glicko_rookie+regional | t3 | 16 | 0.536829 | 0.186297 | 0.687500 | 0.238687 |
| player_round_glicko_rookie+regional | collegiate | 7 | 0.719943 | 0.263865 | 0.428571 | 0.161536 |
| player_round_glicko_rookie+regional | offseason | 855 | 0.637623 | 0.222608 | 0.643275 | 0.023699 |
| player_round_glicko_rookie+regional | unknown | 0 | — | — | — | — |
| player_round_glicko_rookie+regional | international=1 | 268 | 0.663896 | 0.236064 | 0.615672 | 0.064167 |
| player_round_glicko_rookie+regional | international=0 | 6069 | 0.637410 | 0.223074 | 0.633712 | 0.016311 |

player_round_glicko_rookie+regional − coin (paired log loss):

| Section | Rows | player_round_glicko_rookie+regional log loss | coin log loss | Difference | 95% interval | Significant |
|---|---:|---:|---:|---:|---|---|
| all | 6337 | 0.638530 | 0.693147 | -0.054617 | [-0.063856, -0.045556] | yes |
| vct | 1080 | 0.667022 | 0.693147 | -0.026125 | [-0.042252, -0.010443] | yes |
| vcl | 3374 | 0.643621 | 0.693147 | -0.049526 | [-0.062517, -0.036427] | yes |
| gc | 1005 | 0.592646 | 0.693147 | -0.100501 | [-0.126300, -0.075691] | yes |
| t3 | 16 | 0.536829 | 0.693147 | -0.156319 | [-0.492423, 0.064567] | no |
| collegiate | 7 | 0.719943 | 0.693147 | 0.026795 | [0.026330, 0.027145] | yes |
| offseason | 855 | 0.637623 | 0.693147 | -0.055524 | [-0.083395, -0.029531] | yes |
| international=1 | 268 | 0.663896 | 0.693147 | -0.029252 | [-0.059658, -0.001841] | yes |
| international=0 | 6069 | 0.637410 | 0.693147 | -0.055737 | [-0.065303, -0.046615] | yes |

| Model | Section | Rows | Log loss | Brier | Accuracy | ECE |
|---|---|---:|---:|---:|---:|---:|
| player_round_glicko_rookie+regional_form | all | 6337 | 0.638461 | 0.223372 | 0.637683 | 0.022692 |
| player_round_glicko_rookie+regional_form | vct | 1080 | 0.666900 | 0.237062 | 0.594444 | 0.036977 |
| player_round_glicko_rookie+regional_form | vcl | 3374 | 0.645483 | 0.225982 | 0.631891 | 0.038314 |
| player_round_glicko_rookie+regional_form | gc | 1005 | 0.587309 | 0.201496 | 0.693532 | 0.037714 |
| player_round_glicko_rookie+regional_form | t3 | 16 | 0.519732 | 0.179957 | 0.687500 | 0.277673 |
| player_round_glicko_rookie+regional_form | collegiate | 7 | 0.742680 | 0.274779 | 0.428571 | 0.413414 |
| player_round_glicko_rookie+regional_form | offseason | 855 | 0.636320 | 0.221883 | 0.650292 | 0.029805 |
| player_round_glicko_rookie+regional_form | unknown | 0 | — | — | — | — |
| player_round_glicko_rookie+regional_form | international=1 | 268 | 0.661497 | 0.234920 | 0.626866 | 0.079838 |
| player_round_glicko_rookie+regional_form | international=0 | 6069 | 0.637444 | 0.222862 | 0.638161 | 0.022301 |

player_round_glicko_rookie+regional_form − coin (paired log loss):

| Section | Rows | player_round_glicko_rookie+regional_form log loss | coin log loss | Difference | 95% interval | Significant |
|---|---:|---:|---:|---:|---|---|
| all | 6337 | 0.638461 | 0.693147 | -0.054686 | [-0.064674, -0.044811] | yes |
| vct | 1080 | 0.666900 | 0.693147 | -0.026247 | [-0.043135, -0.009827] | yes |
| vcl | 3374 | 0.645483 | 0.693147 | -0.047664 | [-0.061731, -0.033197] | yes |
| gc | 1005 | 0.587309 | 0.693147 | -0.105838 | [-0.133542, -0.079337] | yes |
| t3 | 16 | 0.519732 | 0.693147 | -0.173415 | [-0.513182, 0.043233] | no |
| collegiate | 7 | 0.742680 | 0.693147 | 0.049533 | [0.044920, 0.055683] | yes |
| offseason | 855 | 0.636320 | 0.693147 | -0.056827 | [-0.085334, -0.029152] | yes |
| international=1 | 268 | 0.661497 | 0.693147 | -0.031650 | [-0.063511, -0.002090] | yes |
| international=0 | 6069 | 0.637444 | 0.693147 | -0.055704 | [-0.065938, -0.045939] | yes |

player_round_glicko_rookie − team_elo (paired log loss):

| Section | Rows | player_round_glicko_rookie log loss | team_elo log loss | Difference | 95% interval | Significant |
|---|---:|---:|---:|---:|---|---|
| all | 6337 | 0.638693 | 0.662947 | -0.024254 | [-0.031251, -0.017380] | yes |

team_elo+form − team_elo (paired log loss):

| Section | Rows | team_elo+form log loss | team_elo log loss | Difference | 95% interval | Significant |
|---|---:|---:|---:|---:|---|---|
| all | 6337 | 0.657731 | 0.662947 | -0.005215 | [-0.008529, -0.002021] | yes |

team_elo+regional − team_elo (paired log loss):

| Section | Rows | team_elo+regional log loss | team_elo log loss | Difference | 95% interval | Significant |
|---|---:|---:|---:|---:|---|---|
| all | 6337 | 0.662588 | 0.662947 | -0.000359 | [-0.001205, 0.000447] | no |

team_elo+regional_form − team_elo (paired log loss):

| Section | Rows | team_elo+regional_form log loss | team_elo log loss | Difference | 95% interval | Significant |
|---|---:|---:|---:|---:|---|---|
| all | 6337 | 0.657048 | 0.662947 | -0.005899 | [-0.009166, -0.002726] | yes |

player_round_glicko_rookie+form − team_elo (paired log loss):

| Section | Rows | player_round_glicko_rookie+form log loss | team_elo log loss | Difference | 95% interval | Significant |
|---|---:|---:|---:|---:|---|---|
| all | 6337 | 0.638613 | 0.662947 | -0.024334 | [-0.031782, -0.017082] | yes |

player_round_glicko_rookie+regional − team_elo (paired log loss):

| Section | Rows | player_round_glicko_rookie+regional log loss | team_elo log loss | Difference | 95% interval | Significant |
|---|---:|---:|---:|---:|---|---|
| all | 6337 | 0.638530 | 0.662947 | -0.024416 | [-0.031469, -0.017491] | yes |

player_round_glicko_rookie+regional_form − team_elo (paired log loss):

| Section | Rows | player_round_glicko_rookie+regional_form log loss | team_elo log loss | Difference | 95% interval | Significant |
|---|---:|---:|---:|---:|---|---|
| all | 6337 | 0.638461 | 0.662947 | -0.024486 | [-0.031907, -0.017356] | yes |

### Series

| Model | Section | Rows | Log loss | Brier | Accuracy | ECE |
|---|---|---:|---:|---:|---:|---:|
| coin | all | 2618 | 0.693147 | 0.250000 | 0.500000 | 0.056532 |
| coin | vct | 415 | 0.693147 | 0.250000 | 0.500000 | 0.018072 |
| coin | vcl | 1351 | 0.693147 | 0.250000 | 0.500000 | 0.058105 |
| coin | gc | 409 | 0.693147 | 0.250000 | 0.500000 | 0.143032 |
| coin | t3 | 6 | 0.693147 | 0.250000 | 0.500000 | 0.333333 |
| coin | collegiate | 2 | 0.693147 | 0.250000 | 0.500000 | 0.000000 |
| coin | offseason | 435 | 0.693147 | 0.250000 | 0.500000 | 0.037931 |
| coin | unknown | 0 | — | — | — | — |
| coin | international=1 | 103 | 0.693147 | 0.250000 | 0.500000 | 0.024272 |
| coin | international=0 | 2515 | 0.693147 | 0.250000 | 0.500000 | 0.057853 |

| Model | Section | Rows | Log loss | Brier | Accuracy | ECE |
|---|---|---:|---:|---:|---:|---:|
| team_elo | all | 2618 | 0.643432 | 0.225839 | 0.630443 | 0.030124 |
| team_elo | vct | 415 | 0.664437 | 0.235728 | 0.612048 | 0.059909 |
| team_elo | vcl | 1351 | 0.649305 | 0.227962 | 0.633605 | 0.044519 |
| team_elo | gc | 409 | 0.596811 | 0.206447 | 0.658924 | 0.073475 |
| team_elo | t3 | 6 | 0.292563 | 0.076004 | 1.000000 | 0.240926 |
| team_elo | collegiate | 2 | 0.748653 | 0.277657 | 0.000000 | 0.526357 |
| team_elo | offseason | 435 | 0.653339 | 0.229875 | 0.609195 | 0.047433 |
| team_elo | unknown | 0 | — | — | — | — |
| team_elo | international=1 | 103 | 0.639781 | 0.225951 | 0.631068 | 0.069954 |
| team_elo | international=0 | 2515 | 0.643581 | 0.225835 | 0.630417 | 0.030105 |

team_elo − coin (paired log loss):

| Section | Rows | team_elo log loss | coin log loss | Difference | 95% interval | Significant |
|---|---:|---:|---:|---:|---|---|
| all | 2618 | 0.643432 | 0.693147 | -0.049716 | [-0.063008, -0.036807] | yes |
| vct | 415 | 0.664437 | 0.693147 | -0.028710 | [-0.062897, 0.006215] | no |
| vcl | 1351 | 0.649305 | 0.693147 | -0.043842 | [-0.061912, -0.025614] | yes |
| gc | 409 | 0.596811 | 0.693147 | -0.096336 | [-0.129011, -0.061504] | yes |
| t3 | 6 | 0.292563 | 0.693147 | -0.400584 | [-0.535592, -0.240596] | yes |
| collegiate | 2 | 0.748653 | 0.693147 | 0.055505 | [0.003500, 0.107511] | yes |
| offseason | 435 | 0.653339 | 0.693147 | -0.039808 | [-0.072346, -0.004089] | yes |
| international=1 | 103 | 0.639781 | 0.693147 | -0.053366 | [-0.121532, 0.013749] | no |
| international=0 | 2515 | 0.643581 | 0.693147 | -0.049566 | [-0.063305, -0.035982] | yes |

| Model | Section | Rows | Log loss | Brier | Accuracy | ECE |
|---|---|---:|---:|---:|---:|---:|
| player_round_glicko_rookie | all | 2618 | 0.606622 | 0.209441 | 0.671505 | 0.025923 |
| player_round_glicko_rookie | vct | 415 | 0.637085 | 0.224561 | 0.631325 | 0.036790 |
| player_round_glicko_rookie | vcl | 1351 | 0.613287 | 0.211041 | 0.667654 | 0.039104 |
| player_round_glicko_rookie | gc | 409 | 0.531225 | 0.180006 | 0.745721 | 0.062250 |
| player_round_glicko_rookie | t3 | 6 | 0.573765 | 0.208319 | 0.666667 | 0.147831 |
| player_round_glicko_rookie | collegiate | 2 | 0.468348 | 0.143217 | 1.000000 | 0.367453 |
| player_round_glicko_rookie | offseason | 435 | 0.628838 | 0.218039 | 0.650575 | 0.056037 |
| player_round_glicko_rookie | unknown | 0 | — | — | — | — |
| player_round_glicko_rookie | international=1 | 103 | 0.643461 | 0.226408 | 0.640777 | 0.077826 |
| player_round_glicko_rookie | international=0 | 2515 | 0.605113 | 0.208746 | 0.672763 | 0.026114 |

player_round_glicko_rookie − coin (paired log loss):

| Section | Rows | player_round_glicko_rookie log loss | coin log loss | Difference | 95% interval | Significant |
|---|---:|---:|---:|---:|---|---|
| all | 2618 | 0.606622 | 0.693147 | -0.086526 | [-0.102601, -0.070031] | yes |
| vct | 415 | 0.637085 | 0.693147 | -0.056062 | [-0.084666, -0.025764] | yes |
| vcl | 1351 | 0.613287 | 0.693147 | -0.079861 | [-0.104530, -0.056267] | yes |
| gc | 409 | 0.531225 | 0.693147 | -0.161922 | [-0.200002, -0.120935] | yes |
| t3 | 6 | 0.573765 | 0.693147 | -0.119382 | [-0.537065, 0.331489] | no |
| collegiate | 2 | 0.468348 | 0.693147 | -0.224799 | [-0.368899, -0.080700] | yes |
| offseason | 435 | 0.628838 | 0.693147 | -0.064309 | [-0.106971, -0.020208] | yes |
| international=1 | 103 | 0.643461 | 0.693147 | -0.049686 | [-0.107227, 0.004493] | no |
| international=0 | 2515 | 0.605113 | 0.693147 | -0.088034 | [-0.104511, -0.070465] | yes |

| Model | Section | Rows | Log loss | Brier | Accuracy | ECE |
|---|---|---:|---:|---:|---:|---:|
| team_elo+form | all | 2618 | 0.629253 | 0.219158 | 0.650879 | 0.029928 |
| team_elo+form | vct | 415 | 0.657629 | 0.232411 | 0.624096 | 0.051752 |
| team_elo+form | vcl | 1351 | 0.635732 | 0.221402 | 0.641747 | 0.046500 |
| team_elo+form | gc | 409 | 0.569081 | 0.194472 | 0.720049 | 0.071598 |
| team_elo+form | t3 | 6 | 0.256269 | 0.066914 | 1.000000 | 0.210086 |
| team_elo+form | collegiate | 2 | 0.743048 | 0.274880 | 0.000000 | 0.523818 |
| team_elo+form | offseason | 435 | 0.643256 | 0.224598 | 0.637931 | 0.046964 |
| team_elo+form | unknown | 0 | — | — | — | — |
| team_elo+form | international=1 | 103 | 0.630398 | 0.221663 | 0.631068 | 0.067842 |
| team_elo+form | international=0 | 2515 | 0.629206 | 0.219055 | 0.651690 | 0.030472 |

team_elo+form − coin (paired log loss):

| Section | Rows | team_elo+form log loss | coin log loss | Difference | 95% interval | Significant |
|---|---:|---:|---:|---:|---|---|
| all | 2618 | 0.629253 | 0.693147 | -0.063894 | [-0.078892, -0.049924] | yes |
| vct | 415 | 0.657629 | 0.693147 | -0.035518 | [-0.067563, -0.001762] | yes |
| vcl | 1351 | 0.635732 | 0.693147 | -0.057416 | [-0.077118, -0.037301] | yes |
| gc | 409 | 0.569081 | 0.693147 | -0.124066 | [-0.161297, -0.087381] | yes |
| t3 | 6 | 0.256269 | 0.693147 | -0.436878 | [-0.583539, -0.260288] | yes |
| collegiate | 2 | 0.743048 | 0.693147 | 0.049900 | [0.003149, 0.096652] | yes |
| offseason | 435 | 0.643256 | 0.693147 | -0.049891 | [-0.085553, -0.010719] | yes |
| international=1 | 103 | 0.630398 | 0.693147 | -0.062749 | [-0.132899, 0.004737] | no |
| international=0 | 2515 | 0.629206 | 0.693147 | -0.063941 | [-0.078740, -0.049281] | yes |

| Model | Section | Rows | Log loss | Brier | Accuracy | ECE |
|---|---|---:|---:|---:|---:|---:|
| team_elo+regional | all | 2618 | 0.643500 | 0.225870 | 0.629679 | 0.029295 |
| team_elo+regional | vct | 415 | 0.666209 | 0.236098 | 0.609639 | 0.059272 |
| team_elo+regional | vcl | 1351 | 0.649712 | 0.228044 | 0.633605 | 0.046233 |
| team_elo+regional | gc | 409 | 0.596735 | 0.206486 | 0.658924 | 0.071954 |
| team_elo+regional | t3 | 6 | 0.286795 | 0.074264 | 1.000000 | 0.236333 |
| team_elo+regional | collegiate | 2 | 0.749612 | 0.278132 | 0.000000 | 0.526790 |
| team_elo+regional | offseason | 435 | 0.650942 | 0.229439 | 0.606897 | 0.029580 |
| team_elo+regional | unknown | 0 | — | — | — | — |
| team_elo+regional | international=1 | 103 | 0.640354 | 0.225232 | 0.631068 | 0.065164 |
| team_elo+regional | international=0 | 2515 | 0.643629 | 0.225896 | 0.629622 | 0.029243 |

team_elo+regional − coin (paired log loss):

| Section | Rows | team_elo+regional log loss | coin log loss | Difference | 95% interval | Significant |
|---|---:|---:|---:|---:|---|---|
| all | 2618 | 0.643500 | 0.693147 | -0.049647 | [-0.062932, -0.036963] | yes |
| vct | 415 | 0.666209 | 0.693147 | -0.026938 | [-0.058975, 0.005593] | no |
| vcl | 1351 | 0.649712 | 0.693147 | -0.043435 | [-0.061908, -0.024693] | yes |
| gc | 409 | 0.596735 | 0.693147 | -0.096412 | [-0.129432, -0.061735] | yes |
| t3 | 6 | 0.286795 | 0.693147 | -0.406352 | [-0.542257, -0.243422] | yes |
| collegiate | 2 | 0.749612 | 0.693147 | 0.056465 | [0.003600, 0.109330] | yes |
| offseason | 435 | 0.650942 | 0.693147 | -0.042205 | [-0.072327, -0.010138] | yes |
| international=1 | 103 | 0.640354 | 0.693147 | -0.052793 | [-0.104288, -0.002160] | yes |
| international=0 | 2515 | 0.643629 | 0.693147 | -0.049518 | [-0.063390, -0.035867] | yes |

| Model | Section | Rows | Log loss | Brier | Accuracy | ECE |
|---|---|---:|---:|---:|---:|---:|
| team_elo+regional_form | all | 2618 | 0.628785 | 0.219014 | 0.650879 | 0.025913 |
| team_elo+regional_form | vct | 415 | 0.658801 | 0.232599 | 0.624096 | 0.039269 |
| team_elo+regional_form | vcl | 1351 | 0.635947 | 0.221407 | 0.641007 | 0.044874 |
| team_elo+regional_form | gc | 409 | 0.568510 | 0.194261 | 0.720049 | 0.074966 |
| team_elo+regional_form | t3 | 6 | 0.252808 | 0.065967 | 1.000000 | 0.207259 |
| team_elo+regional_form | collegiate | 2 | 0.743974 | 0.275340 | 0.000000 | 0.524239 |
| team_elo+regional_form | offseason | 435 | 0.639231 | 0.223750 | 0.640230 | 0.041941 |
| team_elo+regional_form | unknown | 0 | — | — | — | — |
| team_elo+regional_form | international=1 | 103 | 0.630280 | 0.220735 | 0.631068 | 0.064251 |
| team_elo+regional_form | international=0 | 2515 | 0.628723 | 0.218944 | 0.651690 | 0.027538 |

team_elo+regional_form − coin (paired log loss):

| Section | Rows | team_elo+regional_form log loss | coin log loss | Difference | 95% interval | Significant |
|---|---:|---:|---:|---:|---|---|
| all | 2618 | 0.628785 | 0.693147 | -0.064362 | [-0.079261, -0.050609] | yes |
| vct | 415 | 0.658801 | 0.693147 | -0.034346 | [-0.064944, -0.001914] | yes |
| vcl | 1351 | 0.635947 | 0.693147 | -0.057200 | [-0.077194, -0.036735] | yes |
| gc | 409 | 0.568510 | 0.693147 | -0.124637 | [-0.161890, -0.087113] | yes |
| t3 | 6 | 0.252808 | 0.693147 | -0.440339 | [-0.586973, -0.263787] | yes |
| collegiate | 2 | 0.743974 | 0.693147 | 0.050827 | [0.003199, 0.098455] | yes |
| offseason | 435 | 0.639231 | 0.693147 | -0.053916 | [-0.086618, -0.017872] | yes |
| international=1 | 103 | 0.630280 | 0.693147 | -0.062867 | [-0.117714, -0.009969] | yes |
| international=0 | 2515 | 0.628723 | 0.693147 | -0.064424 | [-0.079109, -0.049814] | yes |

| Model | Section | Rows | Log loss | Brier | Accuracy | ECE |
|---|---|---:|---:|---:|---:|---:|
| player_round_glicko_rookie+form | all | 2618 | 0.603856 | 0.208507 | 0.677235 | 0.029227 |
| player_round_glicko_rookie+form | vct | 415 | 0.635384 | 0.223680 | 0.633735 | 0.032456 |
| player_round_glicko_rookie+form | vcl | 1351 | 0.610927 | 0.210554 | 0.669134 | 0.037355 |
| player_round_glicko_rookie+form | gc | 409 | 0.524794 | 0.177311 | 0.757946 | 0.071313 |
| player_round_glicko_rookie+form | t3 | 6 | 0.534535 | 0.194096 | 0.666667 | 0.137103 |
| player_round_glicko_rookie+form | collegiate | 2 | 0.481464 | 0.148824 | 1.000000 | 0.376313 |
| player_round_glicko_rookie+form | offseason | 435 | 0.627672 | 0.217478 | 0.666667 | 0.055150 |
| player_round_glicko_rookie+form | unknown | 0 | — | — | — | — |
| player_round_glicko_rookie+form | international=1 | 103 | 0.637022 | 0.223281 | 0.650485 | 0.067096 |
| player_round_glicko_rookie+form | international=0 | 2515 | 0.602498 | 0.207902 | 0.678330 | 0.029591 |

player_round_glicko_rookie+form − coin (paired log loss):

| Section | Rows | player_round_glicko_rookie+form log loss | coin log loss | Difference | 95% interval | Significant |
|---|---:|---:|---:|---:|---|---|
| all | 2618 | 0.603856 | 0.693147 | -0.089291 | [-0.105695, -0.072381] | yes |
| vct | 415 | 0.635384 | 0.693147 | -0.057763 | [-0.086008, -0.029112] | yes |
| vcl | 1351 | 0.610927 | 0.693147 | -0.082221 | [-0.106689, -0.058633] | yes |
| gc | 409 | 0.524794 | 0.693147 | -0.168353 | [-0.206502, -0.127360] | yes |
| t3 | 6 | 0.534535 | 0.693147 | -0.158612 | [-0.544992, 0.242797] | no |
| collegiate | 2 | 0.481464 | 0.693147 | -0.211683 | [-0.348700, -0.074665] | yes |
| offseason | 435 | 0.627672 | 0.693147 | -0.065475 | [-0.107733, -0.021023] | yes |
| international=1 | 103 | 0.637022 | 0.693147 | -0.056125 | [-0.111989, -0.002722] | yes |
| international=0 | 2515 | 0.602498 | 0.693147 | -0.090650 | [-0.106933, -0.073465] | yes |

| Model | Section | Rows | Log loss | Brier | Accuracy | ECE |
|---|---|---:|---:|---:|---:|---:|
| player_round_glicko_rookie+regional | all | 2618 | 0.606442 | 0.209313 | 0.672651 | 0.026877 |
| player_round_glicko_rookie+regional | vct | 415 | 0.637117 | 0.224566 | 0.628916 | 0.036696 |
| player_round_glicko_rookie+regional | vcl | 1351 | 0.613687 | 0.211115 | 0.667654 | 0.037816 |
| player_round_glicko_rookie+regional | gc | 409 | 0.529480 | 0.179244 | 0.750611 | 0.059835 |
| player_round_glicko_rookie+regional | t3 | 6 | 0.574644 | 0.208571 | 0.666667 | 0.147304 |
| player_round_glicko_rookie+regional | collegiate | 2 | 0.466714 | 0.142564 | 1.000000 | 0.366270 |
| player_round_glicko_rookie+regional | offseason | 435 | 0.628122 | 0.217754 | 0.655172 | 0.056235 |
| player_round_glicko_rookie+regional | unknown | 0 | — | — | — | — |
| player_round_glicko_rookie+regional | international=1 | 103 | 0.638024 | 0.223756 | 0.650485 | 0.079424 |
| player_round_glicko_rookie+regional | international=0 | 2515 | 0.605149 | 0.208722 | 0.673559 | 0.026837 |

player_round_glicko_rookie+regional − coin (paired log loss):

| Section | Rows | player_round_glicko_rookie+regional log loss | coin log loss | Difference | 95% interval | Significant |
|---|---:|---:|---:|---:|---|---|
| all | 2618 | 0.606442 | 0.693147 | -0.086705 | [-0.102827, -0.069985] | yes |
| vct | 415 | 0.637117 | 0.693147 | -0.056030 | [-0.085337, -0.025133] | yes |
| vcl | 1351 | 0.613687 | 0.693147 | -0.079460 | [-0.104485, -0.055553] | yes |
| gc | 409 | 0.529480 | 0.693147 | -0.163667 | [-0.201729, -0.123080] | yes |
| t3 | 6 | 0.574644 | 0.693147 | -0.118503 | [-0.538740, 0.335908] | no |
| collegiate | 2 | 0.466714 | 0.693147 | -0.226433 | [-0.372166, -0.080700] | yes |
| offseason | 435 | 0.628122 | 0.693147 | -0.065025 | [-0.107551, -0.020782] | yes |
| international=1 | 103 | 0.638024 | 0.693147 | -0.055123 | [-0.114856, 0.002015] | no |
| international=0 | 2515 | 0.605149 | 0.693147 | -0.087998 | [-0.104735, -0.070544] | yes |

| Model | Section | Rows | Log loss | Brier | Accuracy | ECE |
|---|---|---:|---:|---:|---:|---:|
| player_round_glicko_rookie+regional_form | all | 2618 | 0.603490 | 0.208356 | 0.676853 | 0.028624 |
| player_round_glicko_rookie+regional_form | vct | 415 | 0.635322 | 0.223642 | 0.631325 | 0.037430 |
| player_round_glicko_rookie+regional_form | vcl | 1351 | 0.610932 | 0.210555 | 0.669134 | 0.037415 |
| player_round_glicko_rookie+regional_form | gc | 409 | 0.523442 | 0.176707 | 0.757946 | 0.073489 |
| player_round_glicko_rookie+regional_form | t3 | 6 | 0.534371 | 0.194037 | 0.666667 | 0.137016 |
| player_round_glicko_rookie+regional_form | collegiate | 2 | 0.481464 | 0.148824 | 1.000000 | 0.376313 |
| player_round_glicko_rookie+regional_form | offseason | 435 | 0.626784 | 0.217172 | 0.666667 | 0.053402 |
| player_round_glicko_rookie+regional_form | unknown | 0 | — | — | — | — |
| player_round_glicko_rookie+regional_form | international=1 | 103 | 0.632377 | 0.221079 | 0.640777 | 0.078419 |
| player_round_glicko_rookie+regional_form | international=0 | 2515 | 0.602307 | 0.207835 | 0.678330 | 0.029912 |

player_round_glicko_rookie+regional_form − coin (paired log loss):

| Section | Rows | player_round_glicko_rookie+regional_form log loss | coin log loss | Difference | 95% interval | Significant |
|---|---:|---:|---:|---:|---|---|
| all | 2618 | 0.603490 | 0.693147 | -0.089657 | [-0.105954, -0.072607] | yes |
| vct | 415 | 0.635322 | 0.693147 | -0.057826 | [-0.086564, -0.028572] | yes |
| vcl | 1351 | 0.610932 | 0.693147 | -0.082215 | [-0.106693, -0.058623] | yes |
| gc | 409 | 0.523442 | 0.693147 | -0.169705 | [-0.207796, -0.128720] | yes |
| t3 | 6 | 0.534371 | 0.693147 | -0.158776 | [-0.545089, 0.242476] | no |
| collegiate | 2 | 0.481464 | 0.693147 | -0.211683 | [-0.348700, -0.074665] | yes |
| offseason | 435 | 0.626784 | 0.693147 | -0.066363 | [-0.108513, -0.022310] | yes |
| international=1 | 103 | 0.632377 | 0.693147 | -0.060770 | [-0.118121, -0.004931] | yes |
| international=0 | 2515 | 0.602307 | 0.693147 | -0.090840 | [-0.107062, -0.073801] | yes |

player_round_glicko_rookie − team_elo (paired log loss):

| Section | Rows | player_round_glicko_rookie log loss | team_elo log loss | Difference | 95% interval | Significant |
|---|---:|---:|---:|---:|---|---|
| all | 2618 | 0.606622 | 0.643432 | -0.036810 | [-0.050837, -0.022530] | yes |

team_elo+form − team_elo (paired log loss):

| Section | Rows | team_elo+form log loss | team_elo log loss | Difference | 95% interval | Significant |
|---|---:|---:|---:|---:|---|---|
| all | 2618 | 0.629253 | 0.643432 | -0.014179 | [-0.018629, -0.009937] | yes |

team_elo+regional − team_elo (paired log loss):

| Section | Rows | team_elo+regional log loss | team_elo log loss | Difference | 95% interval | Significant |
|---|---:|---:|---:|---:|---|---|
| all | 2618 | 0.643500 | 0.643432 | 0.000068 | [-0.001653, 0.001623] | no |

team_elo+regional_form − team_elo (paired log loss):

| Section | Rows | team_elo+regional_form log loss | team_elo log loss | Difference | 95% interval | Significant |
|---|---:|---:|---:|---:|---|---|
| all | 2618 | 0.628785 | 0.643432 | -0.014647 | [-0.019485, -0.010146] | yes |

player_round_glicko_rookie+form − team_elo (paired log loss):

| Section | Rows | player_round_glicko_rookie+form log loss | team_elo log loss | Difference | 95% interval | Significant |
|---|---:|---:|---:|---:|---|---|
| all | 2618 | 0.603856 | 0.643432 | -0.039576 | [-0.053266, -0.025569] | yes |

player_round_glicko_rookie+regional − team_elo (paired log loss):

| Section | Rows | player_round_glicko_rookie+regional log loss | team_elo log loss | Difference | 95% interval | Significant |
|---|---:|---:|---:|---:|---|---|
| all | 2618 | 0.606442 | 0.643432 | -0.036989 | [-0.051028, -0.022683] | yes |

player_round_glicko_rookie+regional_form − team_elo (paired log loss):

| Section | Rows | player_round_glicko_rookie+regional_form log loss | team_elo log loss | Difference | 95% interval | Significant |
|---|---:|---:|---:|---:|---|---|
| all | 2618 | 0.603490 | 0.643432 | -0.039942 | [-0.053652, -0.025891] | yes |

## Stage 2 — validation vs Kalshi

### team_elo: Kalshi comparison and returns



#### Log loss vs Kalshi

| Kind | Slice | Rows | Model log loss | Kalshi log loss | Difference [95% interval] | Significant |
|---|---|---:|---:|---:|---|---|
| series | all | 677 | 0.659884 | 0.633240 | 0.026644 [0.005070, 0.049198] | yes |
| series | vct | 278 | 0.656875 | 0.634755 | 0.022120 [-0.008080, 0.052332] | no |
| series | vcl | 340 | 0.653448 | 0.619968 | 0.033480 [-0.002273, 0.068144] | no |
| series | gc | 0 | — | — | — | — |
| series | t3 | 0 | — | — | — | — |
| series | collegiate | 0 | — | — | — | — |
| series | offseason | 59 | 0.711150 | 0.702587 | 0.008563 [-0.038647, 0.057958] | no |
| series | international=1 | 41 | 0.651212 | 0.653397 | -0.002184 [-0.046947, 0.045515] | no |
| series | international=0 | 636 | 0.660443 | 0.631941 | 0.028502 [0.005725, 0.053222] | yes |
| map | all | 1049 | 0.674219 | 0.668225 | 0.005994 [-0.016072, 0.025667] | no |
| map | vct | 461 | 0.678620 | 0.665762 | 0.012858 [-0.012004, 0.036805] | no |
| map | vcl | 490 | 0.669823 | 0.668365 | 0.001458 [-0.038888, 0.036008] | no |
| map | gc | 0 | — | — | — | — |
| map | t3 | 0 | — | — | — | — |
| map | collegiate | 0 | — | — | — | — |
| map | offseason | 98 | 0.675493 | 0.679111 | -0.003618 [-0.033834, 0.028482] | no |
| map | international=1 | 59 | 0.669039 | 0.649653 | 0.019386 [-0.020368, 0.061334] | no |
| map | international=0 | 990 | 0.674527 | 0.669332 | 0.005196 [-0.018272, 0.026420] | no |

#### Full-Kelly returns

| Kind | Slice | Bets | Matches | Mean edge | Flat ROI [95% interval] | Kelly, LoL caps ($50 start) | Multiple | Max drawdown | Largest stake | Bets filled | Flat ROI depth-capped [95% interval] | Kelly depth-capped final |
|---|---|---:|---:|---:|---|---:|---:|---:|---:|---:|---|---:|
| series | all | 473 | 473 | 0.0894 | -2.01% [-15.18%, 11.35%] | $0.55 | 0.011× | 99.52% | $9.89 | 260 (213 unfilled) | 15.98% [-1.36%, 35.27%] | $128.56 |
| series | vct | 180 | 180 | 0.0796 | -2.47% [-21.83%, 19.63%] | $17.90 | 0.358× | 72.48% | $5.29 | 107 (73 unfilled) | 15.75% [-9.72%, 43.70%] | $93.96 |
| series | vcl | 257 | 257 | 0.1004 | -3.13% [-20.74%, 15.40%] | $2.78 | 0.056× | 97.26% | $8.12 | 126 (131 unfilled) | 20.99% [-5.94%, 48.89%] | $127.28 |
| series | gc | 0 | 0 | — | — | $50.00 | 1.000× | 0.00% | $0.00 | 0 (0 unfilled) | — | $50.00 |
| series | t3 | 0 | 0 | — | — | $50.00 | 1.000× | 0.00% | $0.00 | 0 (0 unfilled) | — | $50.00 |
| series | collegiate | 0 | 0 | — | — | $50.00 | 1.000× | 0.00% | $0.00 | 0 (0 unfilled) | — | $50.00 |
| series | offseason | 36 | 36 | 0.0591 | 8.33% [-29.51%, 48.08%] | $43.23 | 0.865× | 59.45% | $7.21 | 27 (9 unfilled) | -6.59% [-46.54%, 37.00%] | $37.07 |
| series | international=1 | 32 | 32 | 0.0514 | 5.76% [-27.15%, 40.29%] | $45.99 | 0.920× | 41.06% | $6.36 | 31 (1 unfilled) | 4.29% [-31.31%, 39.31%] | $44.04 |
| series | international=0 | 441 | 441 | 0.0921 | -2.57% [-15.72%, 11.09%] | $0.62 | 0.012× | 99.31% | $7.62 | 229 (212 unfilled) | 17.55% [-1.89%, 37.48%] | $152.11 |
| map | all | 698 | 372 | 0.0762 | 12.02% [-4.33%, 32.11%] | $480.61 | 9.612× | 80.53% | $143.37 | 108 (590 unfilled) | 52.76% [3.09%, 115.44%] | $203.47 |
| map | vct | 286 | 151 | 0.0699 | 3.93% [-12.79%, 27.90%] | $62.89 | 1.258× | 50.73% | $7.89 | 42 (244 unfilled) | 70.04% [-9.28%, 197.74%] | $93.56 |
| map | vcl | 350 | 190 | 0.0874 | 19.95% [-7.26%, 52.36%] | $366.07 | 7.321× | 72.37% | $80.85 | 57 (293 unfilled) | 48.44% [-12.85%, 131.95%] | $117.23 |
| map | gc | 0 | 0 | — | — | $50.00 | 1.000× | 0.00% | $0.00 | 0 (0 unfilled) | — | $50.00 |
| map | t3 | 0 | 0 | — | — | $50.00 | 1.000× | 0.00% | $0.00 | 0 (0 unfilled) | — | $50.00 |
| map | collegiate | 0 | 0 | — | — | $50.00 | 1.000× | 0.00% | $0.00 | 0 (0 unfilled) | — | $50.00 |
| map | offseason | 62 | 31 | 0.0420 | 4.29% [-20.29%, 28.35%] | $43.32 | 0.866× | 27.84% | $3.31 | 9 (53 unfilled) | -0.67% [-57.18%, 35.88%] | $47.13 |
| map | international=1 | 42 | 23 | 0.0572 | -9.87% [-32.61%, 11.40%] | $38.60 | 0.772× | 30.42% | $2.84 | 11 (31 unfilled) | 19.70% [-26.58%, 56.05%] | $52.92 |
| map | international=0 | 656 | 349 | 0.0775 | 13.41% [-3.61%, 34.83%] | $622.19 | 12.444× | 74.78% | $143.30 | 97 (559 unfilled) | 56.48% [-0.76%, 129.18%] | $198.48 |
| series+map | all | 1171 | 544 | 0.0815 | 6.33% [-5.87%, 19.78%] | $48.89 | 0.978× | 97.29% | $123.59 | 368 (803 unfilled) | 26.77% [7.20%, 49.68%] | $202.77 |

#### Monthly market blend fits

UTC monthly fits use earlier rows of the same kind from 2025-09-01, excluding holdout; minimum 100 rows. logit(p_blend) = a·logit(mid) + b·(logit(p_model) − logit(mid)); inputs clipped to [0.01, 0.99], no intercept, ridge 1e-6. Unfitted rows use mid unchanged; excluded from blended tables: 240 rows. Rating parameters remain selected on the tuning window.

| Month | Kind | n | a | b | Status |
|---|---|---:|---:|---:|---|
| 2026-01 | series | 0 | 1.000000 | 0.000000 | unfitted |
| 2026-02 | series | 21 | 1.000000 | 0.000000 | unfitted |
| 2026-02 | map | 0 | 1.000000 | 0.000000 | unfitted |
| 2026-03 | series | 72 | 1.000000 | 0.000000 | unfitted |
| 2026-03 | map | 48 | 1.000000 | 0.000000 | unfitted |
| 2026-04 | series | 136 | 1.042825 | 0.215516 | fitted |
| 2026-04 | map | 104 | 1.439410 | 0.208235 | fitted |
| 2026-05 | series | 357 | 0.942242 | 0.232480 | fitted |
| 2026-05 | map | 456 | 0.879130 | 0.568385 | fitted |
| 2026-06 | series | 556 | 0.860932 | 0.124059 | fitted |
| 2026-06 | map | 833 | 0.763049 | 0.405197 | fitted |

#### Log loss vs Kalshi (blended)

| Kind | Slice | Rows | Model log loss | Kalshi log loss | Difference [95% interval] | Significant |
|---|---|---:|---:|---:|---|---|
| series | all | 541 | 0.634508 | 0.634347 | 0.000161 [-0.005143, 0.005135] | no |
| series | vct | 201 | 0.643137 | 0.644147 | -0.001010 [-0.009242, 0.007156] | no |
| series | vcl | 291 | 0.622082 | 0.621829 | 0.000253 [-0.007141, 0.007684] | no |
| series | gc | 0 | — | — | — | — |
| series | t3 | 0 | — | — | — | — |
| series | collegiate | 0 | — | — | — | — |
| series | offseason | 49 | 0.672904 | 0.668490 | 0.004414 [-0.008452, 0.016494] | no |
| series | international=1 | 24 | 0.680037 | 0.682705 | -0.002669 [-0.027187, 0.017497] | no |
| series | international=0 | 517 | 0.632394 | 0.632102 | 0.000292 [-0.005051, 0.005662] | no |
| map | all | 945 | 0.684435 | 0.673192 | 0.011243 [0.002676, 0.019848] | yes |
| map | vct | 392 | 0.675770 | 0.667249 | 0.008520 [-0.004749, 0.022586] | no |
| map | vcl | 456 | 0.693354 | 0.676303 | 0.017051 [0.003772, 0.030048] | yes |
| map | gc | 0 | — | — | — | — |
| map | t3 | 0 | — | — | — | — |
| map | collegiate | 0 | — | — | — | — |
| map | offseason | 97 | 0.677523 | 0.682581 | -0.005057 [-0.019598, 0.009568] | no |
| map | international=1 | 50 | 0.658711 | 0.651359 | 0.007353 [-0.007823, 0.021042] | no |
| map | international=0 | 895 | 0.685872 | 0.674412 | 0.011460 [0.001858, 0.020438] | yes |

#### Full-Kelly returns (blended)

| Kind | Slice | Bets | Matches | Mean edge | Flat ROI [95% interval] | Kelly, LoL caps ($50 start) | Multiple | Max drawdown | Largest stake | Bets filled | Flat ROI depth-capped [95% interval] | Kelly depth-capped final |
|---|---|---:|---:|---:|---|---:|---:|---:|---:|---:|---|---:|
| series | all | 82 | 82 | 0.0152 | -5.01% [-38.32%, 28.44%] | $35.62 | 0.712× | 43.57% | $5.46 | 49 (33 unfilled) | 16.91% [-25.46%, 65.25%] | $57.12 |
| series | vct | 28 | 28 | 0.0196 | 14.92% [-47.96%, 87.75%] | $45.59 | 0.912× | 34.31% | $4.96 | 18 (10 unfilled) | 63.04% [-26.71%, 163.05%] | $62.32 |
| series | vcl | 50 | 50 | 0.0135 | -8.62% [-45.61%, 31.17%] | $40.94 | 0.819× | 19.74% | $4.61 | 27 (23 unfilled) | 3.28% [-40.89%, 50.22%] | $47.76 |
| series | gc | 0 | 0 | — | — | $50.00 | 1.000× | 0.00% | $0.00 | 0 (0 unfilled) | — | $50.00 |
| series | t3 | 0 | 0 | — | — | $50.00 | 1.000× | 0.00% | $0.00 | 0 (0 unfilled) | — | $50.00 |
| series | collegiate | 0 | 0 | — | — | $50.00 | 1.000× | 0.00% | $0.00 | 0 (0 unfilled) | — | $50.00 |
| series | offseason | 4 | 4 | 0.0065 | -100.00% [-100.00%, -100.00%] | $47.79 | 0.956× | 4.42% | $1.19 | 4 (0 unfilled) | -100.00% [-100.00%, -100.00%] | $47.79 |
| series | international=1 | 5 | 5 | 0.0076 | 128.58% [-40.93%, 298.09%] | $54.96 | 1.099× | 1.20% | $0.70 | 5 (0 unfilled) | 128.58% [-40.93%, 298.09%] | $54.96 |
| series | international=0 | 77 | 77 | 0.0157 | -13.74% [-45.15%, 22.22%] | $32.39 | 0.648× | 44.19% | $5.46 | 44 (33 unfilled) | 4.13% [-38.95%, 48.31%] | $51.92 |
| map | all | 435 | 244 | 0.0302 | -8.06% [-17.18%, 1.76%] | $7.27 | 0.145× | 88.32% | $5.68 | 69 (366 unfilled) | -5.79% [-25.63%, 15.35%] | $38.70 |
| map | vct | 184 | 100 | 0.0327 | -5.21% [-18.93%, 9.43%] | $28.54 | 0.571× | 50.48% | $5.13 | 30 (154 unfilled) | 1.27% [-36.69%, 39.63%] | $52.39 |
| map | vcl | 222 | 129 | 0.0296 | -11.48% [-23.80%, 1.98%] | $13.80 | 0.276× | 75.99% | $5.19 | 36 (186 unfilled) | -8.56% [-34.11%, 13.90%] | $40.07 |
| map | gc | 0 | 0 | — | — | $50.00 | 1.000× | 0.00% | $0.00 | 0 (0 unfilled) | — | $50.00 |
| map | t3 | 0 | 0 | — | — | $50.00 | 1.000× | 0.00% | $0.00 | 0 (0 unfilled) | — | $50.00 |
| map | collegiate | 0 | 0 | — | — | $50.00 | 1.000× | 0.00% | $0.00 | 0 (0 unfilled) | — | $50.00 |
| map | offseason | 29 | 15 | 0.0195 | 0.15% [-31.48%, 32.90%] | $48.32 | 0.966× | 9.94% | $2.85 | 3 (26 unfilled) | -42.95% [-100.00%, -14.15%] | $46.34 |
| map | international=1 | 16 | 10 | 0.0119 | -21.91% [-67.31%, 29.28%] | $46.48 | 0.930× | 7.05% | $2.46 | 4 (12 unfilled) | -59.26% [-100.00%, 64.55%] | $48.87 |
| map | international=0 | 419 | 234 | 0.0309 | -7.52% [-16.46%, 2.12%] | $7.90 | 0.158× | 87.34% | $5.68 | 65 (354 unfilled) | -2.49% [-23.23%, 18.34%] | $39.58 |
| series+map | all | 517 | 268 | 0.0278 | -7.57% [-18.34%, 3.94%] | $5.97 | 0.119× | 90.40% | $5.67 | 118 (399 unfilled) | 3.72% [-17.74%, 27.80%] | $39.19 |

#### Monthly breakdown

All metrics use identical linked rows within each kind/month. Unfitted blend months show —; counts include all rows.

| Kind | Month | Rows | Model log loss | Blended log loss | Kalshi log loss | Raw flat ROI (bets), unlimited Kelly final | Blended flat ROI (bets), unlimited Kelly final | Raw bets filled | Raw Flat ROI depth-capped [95% interval] | Raw Kelly depth-capped final | Blended bets filled | Blended Flat ROI depth-capped [95% interval] | Blended Kelly depth-capped final |
|---|---|---:|---:|---:|---:|---|---|---:|---|---:|---:|---|---:|
| map | 2026-02 | 48 | 0.701058 | — | 0.690786 | -19.10% (25), $33.55 | — | 9 (16 unfilled) | -1.84% [-100.00%, 65.78%] | $45.89 | — | — | — |
| map | 2026-03 | 56 | 0.637862 | — | 0.565065 | -31.56% (35), $21.54 | — | 10 (25 unfilled) | -27.24% [-81.79%, 41.92%] | $37.51 | — | — | — |
| map | 2026-04 | 352 | 0.660671 | 0.707440 | 0.690793 | 49.03% (241), $6279.98 | -9.38% (188), $17.46 | 29 (212 unfilled) | 183.25% [4.69%, 428.45%] | $242.59 | 33 (155 unfilled) | -12.13% [-31.69%, 6.10%] | $41.36 |
| map | 2026-05 | 377 | 0.704442 | 0.690344 | 0.687018 | -1.28% (249), $26.14 | -0.66% (155), $42.94 | 36 (213 unfilled) | 10.12% [-22.78%, 41.28%] | $54.33 | 25 (130 unfilled) | 11.32% [-34.86%, 53.52%] | $53.62 |
| map | 2026-06 | 216 | 0.647007 | 0.636631 | 0.620377 | -10.26% (148), $16.82 | -17.81% (92), $25.67 | 24 (124 unfilled) | 12.50% [-21.08%, 41.11%] | $46.58 | 11 (81 unfilled) | -26.18% [-100.00%, 29.50%] | $44.04 |
| series | 2026-01 | 21 | 0.684822 | — | 0.661069 | 4.92% (16), $45.78 | — | 9 (7 unfilled) | -25.46% [-81.66%, 48.91%] | $36.49 | — | — | — |
| series | 2026-02 | 51 | 0.659130 | — | 0.694525 | 25.18% (34), $95.24 | — | 22 (12 unfilled) | 49.18% [-13.77%, 132.77%] | $129.91 | — | — | — |
| series | 2026-03 | 64 | 0.662527 | — | 0.565917 | -31.86% (49), $10.02 | — | 37 (12 unfilled) | -19.68% [-50.47%, 13.73%] | $18.83 | — | — | — |
| series | 2026-04 | 221 | 0.645922 | 0.624471 | 0.627690 | 3.92% (146), $67.65 | 5.82% (25), $48.53 | 59 (87 unfilled) | 58.07% [8.98%, 114.67%] | $210.98 | 16 (9 unfilled) | 27.95% [-31.97%, 85.50%] | $58.32 |
| series | 2026-05 | 199 | 0.690980 | 0.663840 | 0.663719 | 0.07% (133), $9.78 | -33.91% (33), $36.72 | 83 (50 unfilled) | -1.88% [-27.64%, 26.71%] | $36.33 | 22 (11 unfilled) | -11.15% [-73.62%, 72.74%] | $50.32 |
| series | 2026-06 | 121 | 0.628835 | 0.604598 | 0.598199 | -9.59% (95), $9.03 | 23.37% (24), $50.00 | 50 (45 unfilled) | 14.89% [-15.83%, 48.34%] | $44.61 | 11 (13 unfilled) | 56.86% [-46.08%, 168.60%] | $48.32 |

### player_round_glicko_rookie: Kalshi comparison and returns



#### Log loss vs Kalshi

| Kind | Slice | Rows | Model log loss | Kalshi log loss | Difference [95% interval] | Significant |
|---|---|---:|---:|---:|---|---|
| series | all | 677 | 0.623150 | 0.633240 | -0.010090 [-0.032692, 0.012225] | no |
| series | vct | 278 | 0.624632 | 0.634755 | -0.010123 [-0.040594, 0.018729] | no |
| series | vcl | 340 | 0.611400 | 0.619968 | -0.008568 [-0.046862, 0.030177] | no |
| series | gc | 0 | — | — | — | — |
| series | t3 | 0 | — | — | — | — |
| series | collegiate | 0 | — | — | — | — |
| series | offseason | 59 | 0.683883 | 0.702587 | -0.018704 [-0.076671, 0.036333] | no |
| series | international=1 | 41 | 0.619698 | 0.653397 | -0.033699 [-0.082145, 0.013847] | no |
| series | international=0 | 636 | 0.623373 | 0.631941 | -0.008568 [-0.033414, 0.015130] | no |
| map | all | 1049 | 0.657869 | 0.668225 | -0.010355 [-0.032093, 0.008133] | no |
| map | vct | 461 | 0.659841 | 0.665762 | -0.005921 [-0.026354, 0.012261] | no |
| map | vcl | 490 | 0.650736 | 0.668365 | -0.017628 [-0.060518, 0.017599] | no |
| map | gc | 0 | — | — | — | — |
| map | t3 | 0 | — | — | — | — |
| map | collegiate | 0 | — | — | — | — |
| map | offseason | 98 | 0.684259 | 0.679111 | 0.005148 [-0.025952, 0.036273] | no |
| map | international=1 | 59 | 0.667005 | 0.649653 | 0.017353 [-0.012325, 0.050561] | no |
| map | international=0 | 990 | 0.657325 | 0.669332 | -0.012007 [-0.034084, 0.008115] | no |

#### Full-Kelly returns

| Kind | Slice | Bets | Matches | Mean edge | Flat ROI [95% interval] | Kelly, LoL caps ($50 start) | Multiple | Max drawdown | Largest stake | Bets filled | Flat ROI depth-capped [95% interval] | Kelly depth-capped final |
|---|---|---:|---:|---:|---|---:|---:|---:|---:|---:|---|---:|
| series | all | 502 | 502 | 0.0895 | 12.00% [-0.34%, 24.82%] | $1320.48 | 26.410× | 83.28% | $188.73 | 289 (213 unfilled) | 21.43% [5.36%, 38.42%] | $853.50 |
| series | vct | 202 | 202 | 0.0750 | 7.42% [-10.91%, 28.33%] | $50.99 | 1.020× | 76.61% | $5.59 | 126 (76 unfilled) | 22.90% [-0.30%, 49.36%] | $223.86 |
| series | vcl | 256 | 256 | 0.1052 | 16.55% [-0.18%, 34.94%] | $535.40 | 10.708× | 64.15% | $115.41 | 129 (127 unfilled) | 25.26% [1.33%, 51.62%] | $242.82 |
| series | gc | 0 | 0 | — | — | $50.00 | 1.000× | 0.00% | $0.00 | 0 (0 unfilled) | — | $50.00 |
| series | t3 | 0 | 0 | — | — | $50.00 | 1.000× | 0.00% | $0.00 | 0 (0 unfilled) | — | $50.00 |
| series | collegiate | 0 | 0 | — | — | $50.00 | 1.000× | 0.00% | $0.00 | 0 (0 unfilled) | — | $50.00 |
| series | offseason | 44 | 44 | 0.0649 | 6.55% [-29.26%, 42.64%] | $74.75 | 1.495× | 40.20% | $9.22 | 34 (10 unfilled) | 1.44% [-38.32%, 43.95%] | $57.76 |
| series | international=1 | 28 | 28 | 0.0468 | 33.11% [-12.73%, 82.91%] | $85.13 | 1.703× | 24.63% | $6.78 | 28 (0 unfilled) | 33.11% [-12.73%, 82.91%] | $88.28 |
| series | international=0 | 474 | 474 | 0.0920 | 10.75% [-1.80%, 23.97%] | $531.11 | 10.622× | 83.28% | $108.10 | 261 (213 unfilled) | 20.17% [3.24%, 38.89%] | $492.03 |
| map | all | 676 | 361 | 0.0693 | 19.44% [3.25%, 39.05%] | $6405.08 | 128.102× | 36.48% | $245.53 | 98 (578 unfilled) | 57.11% [2.56%, 131.34%] | $240.23 |
| map | vct | 286 | 148 | 0.0564 | 8.60% [-9.16%, 30.25%] | $162.05 | 3.241× | 40.17% | $20.35 | 55 (231 unfilled) | 47.47% [-14.71%, 147.52%] | $102.47 |
| map | vcl | 336 | 186 | 0.0847 | 31.30% [3.15%, 67.76%] | $1447.32 | 28.946× | 59.77% | $245.53 | 39 (297 unfilled) | 66.60% [-23.57%, 198.57%] | $140.02 |
| map | gc | 0 | 0 | — | — | $50.00 | 1.000× | 0.00% | $0.00 | 0 (0 unfilled) | — | $50.00 |
| map | t3 | 0 | 0 | — | — | $50.00 | 1.000× | 0.00% | $0.00 | 0 (0 unfilled) | — | $50.00 |
| map | collegiate | 0 | 0 | — | — | $50.00 | 1.000× | 0.00% | $0.00 | 0 (0 unfilled) | — | $50.00 |
| map | offseason | 54 | 27 | 0.0416 | 2.86% [-27.55%, 33.38%] | $54.82 | 1.096× | 18.51% | $3.98 | 4 (50 unfilled) | 95.88% [13.38%, 262.84%] | $58.92 |
| map | international=1 | 32 | 17 | 0.0487 | -17.50% [-45.66%, 9.44%] | $37.23 | 0.745× | 28.34% | $4.62 | 13 (19 unfilled) | 3.89% [-28.83%, 46.71%] | $50.74 |
| map | international=0 | 644 | 344 | 0.0703 | 21.27% [4.15%, 41.52%] | $7325.13 | 146.503× | 33.66% | $245.53 | 85 (559 unfilled) | 65.17% [0.95%, 150.71%] | $239.87 |
| series+map | all | 1178 | 536 | 0.0779 | 16.27% [3.84%, 29.53%] | $3903.30 | 78.066× | 50.47% | $247.91 | 387 (791 unfilled) | 30.46% [11.66%, 53.18%] | $450.30 |

#### Monthly market blend fits

UTC monthly fits use earlier rows of the same kind from 2025-09-01, excluding holdout; minimum 100 rows. logit(p_blend) = a·logit(mid) + b·(logit(p_model) − logit(mid)); inputs clipped to [0.01, 0.99], no intercept, ridge 1e-6. Unfitted rows use mid unchanged; excluded from blended tables: 240 rows. Rating parameters remain selected on the tuning window.

| Month | Kind | n | a | b | Status |
|---|---|---:|---:|---:|---|
| 2026-01 | series | 0 | 1.000000 | 0.000000 | unfitted |
| 2026-02 | series | 21 | 1.000000 | 0.000000 | unfitted |
| 2026-02 | map | 0 | 1.000000 | 0.000000 | unfitted |
| 2026-03 | series | 72 | 1.000000 | 0.000000 | unfitted |
| 2026-03 | map | 48 | 1.000000 | 0.000000 | unfitted |
| 2026-04 | series | 136 | 1.279942 | 0.782399 | fitted |
| 2026-04 | map | 104 | 1.456725 | 0.380201 | fitted |
| 2026-05 | series | 357 | 1.074314 | 0.678349 | fitted |
| 2026-05 | map | 456 | 1.050436 | 0.867487 | fitted |
| 2026-06 | series | 556 | 1.019323 | 0.649238 | fitted |
| 2026-06 | map | 833 | 0.913242 | 0.739875 | fitted |

#### Log loss vs Kalshi (blended)

| Kind | Slice | Rows | Model log loss | Kalshi log loss | Difference [95% interval] | Significant |
|---|---|---:|---:|---:|---|---|
| series | all | 541 | 0.620526 | 0.634347 | -0.013821 [-0.030707, 0.003857] | no |
| series | vct | 201 | 0.633359 | 0.644147 | -0.010788 [-0.033171, 0.011681] | no |
| series | vcl | 291 | 0.601829 | 0.621829 | -0.020000 [-0.045178, 0.008558] | no |
| series | gc | 0 | — | — | — | — |
| series | t3 | 0 | — | — | — | — |
| series | collegiate | 0 | — | — | — | — |
| series | offseason | 49 | 0.678920 | 0.668490 | 0.010430 [-0.028051, 0.045189] | no |
| series | international=1 | 24 | 0.658652 | 0.682705 | -0.024053 [-0.069236, 0.022505] | no |
| series | international=0 | 517 | 0.618756 | 0.632102 | -0.013346 [-0.029767, 0.004333] | no |
| map | all | 945 | 0.676380 | 0.673192 | 0.003189 [-0.006601, 0.013743] | no |
| map | vct | 392 | 0.666609 | 0.667249 | -0.000640 [-0.014723, 0.012856] | no |
| map | vcl | 456 | 0.682449 | 0.676303 | 0.006146 [-0.009352, 0.021912] | no |
| map | gc | 0 | — | — | — | — |
| map | t3 | 0 | — | — | — | — |
| map | collegiate | 0 | — | — | — | — |
| map | offseason | 97 | 0.687340 | 0.682581 | 0.004759 [-0.023637, 0.033587] | no |
| map | international=1 | 50 | 0.664657 | 0.651359 | 0.013298 [-0.010105, 0.037913] | no |
| map | international=0 | 895 | 0.677035 | 0.674412 | 0.002624 [-0.008266, 0.012805] | no |

#### Full-Kelly returns (blended)

| Kind | Slice | Bets | Matches | Mean edge | Flat ROI [95% interval] | Kelly, LoL caps ($50 start) | Multiple | Max drawdown | Largest stake | Bets filled | Flat ROI depth-capped [95% interval] | Kelly depth-capped final |
|---|---|---:|---:|---:|---|---:|---:|---:|---:|---:|---|---:|
| series | all | 330 | 330 | 0.0549 | 17.12% [3.19%, 31.74%] | $1040.06 | 20.801× | 42.79% | $136.82 | 174 (156 unfilled) | 19.75% [0.91%, 39.64%] | $297.46 |
| series | vct | 123 | 123 | 0.0447 | 8.58% [-13.31%, 32.79%] | $101.54 | 2.031× | 34.06% | $9.03 | 70 (53 unfilled) | 23.03% [-6.99%, 55.28%] | $144.00 |
| series | vcl | 183 | 183 | 0.0638 | 25.77% [6.09%, 45.53%] | $498.81 | 9.976× | 40.07% | $65.63 | 86 (97 unfilled) | 27.56% [1.59%, 57.56%] | $151.63 |
| series | gc | 0 | 0 | — | — | $50.00 | 1.000× | 0.00% | $0.00 | 0 (0 unfilled) | — | $50.00 |
| series | t3 | 0 | 0 | — | — | $50.00 | 1.000× | 0.00% | $0.00 | 0 (0 unfilled) | — | $50.00 |
| series | collegiate | 0 | 0 | — | — | $50.00 | 1.000× | 0.00% | $0.00 | 0 (0 unfilled) | — | $50.00 |
| series | offseason | 24 | 24 | 0.0400 | -5.06% [-52.08%, 45.92%] | $52.94 | 1.059× | 20.01% | $5.10 | 18 (6 unfilled) | -30.23% [-75.94%, 18.63%] | $36.93 |
| series | international=1 | 12 | 12 | 0.0366 | 38.07% [-40.32%, 122.50%] | $65.91 | 1.318× | 14.00% | $5.27 | 12 (0 unfilled) | 38.07% [-40.32%, 122.50%] | $65.91 |
| series | international=0 | 318 | 318 | 0.0556 | 16.32% [2.34%, 31.17%] | $789.46 | 15.789× | 42.79% | $103.85 | 162 (156 unfilled) | 18.39% [-1.76%, 38.36%] | $214.87 |
| map | all | 512 | 275 | 0.0402 | 3.00% [-8.80%, 16.21%] | $27.07 | 0.541× | 70.83% | $7.71 | 66 (446 unfilled) | 12.78% [-9.92%, 38.10%] | $55.59 |
| map | vct | 200 | 105 | 0.0392 | -2.98% [-16.60%, 10.96%] | $43.46 | 0.869× | 44.90% | $5.43 | 29 (171 unfilled) | 27.83% [-8.28%, 66.27%] | $68.13 |
| map | vcl | 267 | 147 | 0.0418 | 7.52% [-11.12%, 31.20%] | $26.04 | 0.521× | 69.34% | $7.20 | 32 (235 unfilled) | -12.31% [-40.70%, 16.15%] | $36.93 |
| map | gc | 0 | 0 | — | — | $50.00 | 1.000× | 0.00% | $0.00 | 0 (0 unfilled) | — | $50.00 |
| map | t3 | 0 | 0 | — | — | $50.00 | 1.000× | 0.00% | $0.00 | 0 (0 unfilled) | — | $50.00 |
| map | collegiate | 0 | 0 | — | — | $50.00 | 1.000× | 0.00% | $0.00 | 0 (0 unfilled) | — | $50.00 |
| map | offseason | 45 | 23 | 0.0359 | 2.71% [-28.59%, 34.84%] | $54.15 | 1.083× | 12.79% | $4.21 | 5 (40 unfilled) | 85.42% [23.05%, 209.00%] | $54.98 |
| map | international=1 | 26 | 12 | 0.0342 | -16.79% [-49.43%, 15.49%] | $42.14 | 0.843× | 16.08% | $2.39 | 8 (18 unfilled) | 9.16% [-36.34%, 63.48%] | $51.45 |
| map | international=0 | 486 | 263 | 0.0405 | 4.06% [-7.33%, 17.39%] | $32.14 | 0.643× | 65.38% | $7.71 | 58 (428 unfilled) | 13.28% [-11.53%, 39.95%] | $54.07 |
| series+map | all | 842 | 380 | 0.0460 | 8.54% [-2.26%, 20.26%] | $247.49 | 4.950× | 54.12% | $39.27 | 240 (602 unfilled) | 17.84% [2.15%, 33.63%] | $193.30 |

#### Monthly breakdown

All metrics use identical linked rows within each kind/month. Unfitted blend months show —; counts include all rows.

| Kind | Month | Rows | Model log loss | Blended log loss | Kalshi log loss | Raw flat ROI (bets), unlimited Kelly final | Blended flat ROI (bets), unlimited Kelly final | Raw bets filled | Raw Flat ROI depth-capped [95% interval] | Raw Kelly depth-capped final | Blended bets filled | Blended Flat ROI depth-capped [95% interval] | Blended Kelly depth-capped final |
|---|---|---:|---:|---:|---:|---|---|---:|---|---:|---:|---|---:|
| map | 2026-02 | 48 | 0.701317 | — | 0.690786 | 0.54% (36), $44.66 | — | 12 (24 unfilled) | 1.41% [-66.85%, 52.25%] | $48.88 | — | — | — |
| map | 2026-03 | 56 | 0.595514 | — | 0.565065 | -11.68% (39), $39.74 | — | 11 (28 unfilled) | 3.06% [-46.55%, 49.04%] | $52.33 | — | — | — |
| map | 2026-04 | 352 | 0.637459 | 0.688528 | 0.690793 | 57.00% (249), $7795.97 | 10.45% (201), $49.57 | 29 (220 unfilled) | 170.74% [5.32%, 407.56%] | $232.37 | 23 (178 unfilled) | 9.21% [-11.50%, 28.42%] | $54.69 |
| map | 2026-05 | 377 | 0.684941 | 0.684282 | 0.687018 | 7.02% (216), $77.67 | 5.84% (188), $78.71 | 26 (190 unfilled) | 29.69% [-16.99%, 85.45%] | $65.27 | 26 (162 unfilled) | 31.94% [-14.69%, 83.84%] | $62.30 |
| map | 2026-06 | 216 | 0.650391 | 0.642793 | 0.620377 | -15.62% (136), $15.94 | -13.34% (123), $17.24 | 20 (116 unfilled) | -10.38% [-44.77%, 26.04%] | $39.76 | 17 (106 unfilled) | -11.75% [-54.05%, 36.07%] | $40.87 |
| series | 2026-01 | 21 | 0.635271 | — | 0.661069 | 26.04% (19), $54.00 | — | 11 (8 unfilled) | 7.12% [-53.39%, 68.22%] | $43.96 | — | — | — |
| series | 2026-02 | 51 | 0.650791 | — | 0.694525 | 33.18% (40), $103.11 | — | 29 (11 unfilled) | 48.21% [-8.07%, 115.74%] | $103.15 | — | — | — |
| series | 2026-03 | 64 | 0.590399 | — | 0.565917 | -3.95% (49), $38.98 | — | 37 (12 unfilled) | 1.60% [-29.72%, 32.22%] | $49.13 | — | — | — |
| series | 2026-04 | 221 | 0.611446 | 0.610052 | 0.627690 | 15.23% (164), $226.84 | 19.35% (149), $279.60 | 68 (96 unfilled) | 53.35% [13.27%, 100.55%] | $298.31 | 62 (87 unfilled) | 36.67% [4.03%, 71.94%] | $164.32 |
| series | 2026-05 | 199 | 0.653669 | 0.651147 | 0.663719 | 10.41% (142), $74.55 | 15.89% (114), $127.21 | 96 (46 unfilled) | 0.33% [-23.50%, 25.37%] | $44.95 | 74 (40 unfilled) | 3.14% [-23.54%, 31.97%] | $55.27 |
| series | 2026-06 | 121 | 0.597906 | 0.589295 | 0.598199 | 4.72% (88), $76.90 | 14.27% (67), $72.21 | 48 (40 unfilled) | 20.64% [-12.91%, 56.05%] | $130.95 | 38 (29 unfilled) | 24.58% [-15.31%, 67.81%] | $84.40 |

### team_elo+form: Kalshi comparison and returns

form: rows=25380, H=80, w=3.29584

#### Log loss vs Kalshi

| Kind | Slice | Rows | Model log loss | Kalshi log loss | Difference [95% interval] | Significant |
|---|---|---:|---:|---:|---|---|
| series | all | 677 | 0.654256 | 0.633240 | 0.021016 [-0.001783, 0.044713] | no |
| series | vct | 278 | 0.650998 | 0.634755 | 0.016243 [-0.014265, 0.046872] | no |
| series | vcl | 340 | 0.650803 | 0.619968 | 0.030835 [-0.005137, 0.068035] | no |
| series | gc | 0 | — | — | — | — |
| series | t3 | 0 | — | — | — | — |
| series | collegiate | 0 | — | — | — | — |
| series | offseason | 59 | 0.689505 | 0.702587 | -0.013081 [-0.060679, 0.036007] | no |
| series | international=1 | 41 | 0.636524 | 0.653397 | -0.016873 [-0.060411, 0.030930] | no |
| series | international=0 | 636 | 0.655399 | 0.631941 | 0.023458 [0.000021, 0.048564] | yes |
| map | all | 1049 | 0.672849 | 0.668225 | 0.004624 [-0.018747, 0.026281] | no |
| map | vct | 461 | 0.679540 | 0.665762 | 0.013778 [-0.013947, 0.041008] | no |
| map | vcl | 490 | 0.666581 | 0.668365 | -0.001784 [-0.042863, 0.035204] | no |
| map | gc | 0 | — | — | — | — |
| map | t3 | 0 | — | — | — | — |
| map | collegiate | 0 | — | — | — | — |
| map | offseason | 98 | 0.672713 | 0.679111 | -0.006397 [-0.040522, 0.028462] | no |
| map | international=1 | 59 | 0.664526 | 0.649653 | 0.014874 [-0.035684, 0.069348] | no |
| map | international=0 | 990 | 0.673345 | 0.669332 | 0.004013 [-0.020485, 0.025924] | no |

#### Full-Kelly returns

| Kind | Slice | Bets | Matches | Mean edge | Flat ROI [95% interval] | Kelly, LoL caps ($50 start) | Multiple | Max drawdown | Largest stake | Bets filled | Flat ROI depth-capped [95% interval] | Kelly depth-capped final |
|---|---|---:|---:|---:|---|---:|---:|---:|---:|---:|---|---:|
| series | all | 485 | 485 | 0.0861 | -0.12% [-12.80%, 13.40%] | $9.64 | 0.193× | 95.18% | $15.72 | 272 (213 unfilled) | 17.01% [0.49%, 35.62%] | $348.00 |
| series | vct | 188 | 188 | 0.0776 | -2.44% [-21.22%, 17.63%] | $33.01 | 0.660× | 66.72% | $7.51 | 112 (76 unfilled) | 19.44% [-6.22%, 46.04%] | $151.82 |
| series | vcl | 257 | 257 | 0.0971 | -0.46% [-17.92%, 17.97%] | $8.09 | 0.162× | 92.46% | $8.42 | 130 (127 unfilled) | 20.11% [-5.07%, 46.20%] | $157.37 |
| series | gc | 0 | 0 | — | — | $50.00 | 1.000× | 0.00% | $0.00 | 0 (0 unfilled) | — | $50.00 |
| series | t3 | 0 | 0 | — | — | $50.00 | 1.000× | 0.00% | $0.00 | 0 (0 unfilled) | — | $50.00 |
| series | collegiate | 0 | 0 | — | — | $50.00 | 1.000× | 0.00% | $0.00 | 0 (0 unfilled) | — | $50.00 |
| series | offseason | 40 | 40 | 0.0552 | 13.04% [-24.51%, 50.21%] | $84.39 | 1.688× | 42.14% | $7.99 | 30 (10 unfilled) | -5.47% [-45.84%, 36.23%] | $55.13 |
| series | international=1 | 33 | 33 | 0.0477 | 6.72% [-24.50%, 39.72%] | $66.69 | 1.334× | 26.37% | $6.96 | 32 (1 unfilled) | 5.32% [-27.71%, 38.76%] | $63.90 |
| series | international=0 | 452 | 452 | 0.0889 | -0.61% [-13.52%, 12.82%] | $7.04 | 0.141× | 95.04% | $11.15 | 240 (212 unfilled) | 18.56% [0.66%, 38.87%] | $305.84 |
| map | all | 739 | 392 | 0.0813 | 13.90% [-1.73%, 32.09%] | $1157.01 | 23.140× | 68.34% | $242.07 | 114 (625 unfilled) | 51.73% [3.92%, 116.64%] | $245.92 |
| map | vct | 330 | 173 | 0.0718 | 6.22% [-7.81%, 25.57%] | $62.45 | 1.249× | 42.14% | $8.81 | 51 (279 unfilled) | 68.71% [3.33%, 174.46%] | $117.17 |
| map | vcl | 345 | 189 | 0.0964 | 23.96% [-3.79%, 59.15%] | $786.80 | 15.736× | 64.22% | $140.48 | 52 (293 unfilled) | 46.95% [-20.14%, 138.26%] | $127.10 |
| map | gc | 0 | 0 | — | — | $50.00 | 1.000× | 0.00% | $0.00 | 0 (0 unfilled) | — | $50.00 |
| map | t3 | 0 | 0 | — | — | $50.00 | 1.000× | 0.00% | $0.00 | 0 (0 unfilled) | — | $50.00 |
| map | collegiate | 0 | 0 | — | — | $50.00 | 1.000× | 0.00% | $0.00 | 0 (0 unfilled) | — | $50.00 |
| map | offseason | 64 | 30 | 0.0480 | -0.95% [-23.42%, 21.08%] | $48.72 | 0.974× | 19.04% | $3.67 | 11 (53 unfilled) | -4.63% [-44.12%, 27.77%] | $45.86 |
| map | international=1 | 49 | 26 | 0.0649 | -0.22% [-22.06%, 20.40%] | $43.60 | 0.872× | 25.39% | $4.73 | 17 (32 unfilled) | 22.88% [-10.66%, 53.88%] | $57.22 |
| map | international=0 | 690 | 366 | 0.0824 | 14.90% [-1.50%, 34.99%] | $1292.89 | 25.858× | 63.34% | $229.07 | 97 (593 unfilled) | 56.74% [1.62%, 133.92%] | $226.53 |
| series+map | all | 1224 | 577 | 0.0832 | 8.33% [-2.87%, 21.57%] | $2370.90 | 47.418× | 90.20% | $246.03 | 386 (838 unfilled) | 27.25% [7.63%, 50.62%] | $423.35 |

#### Monthly market blend fits

UTC monthly fits use earlier rows of the same kind from 2025-09-01, excluding holdout; minimum 100 rows. logit(p_blend) = a·logit(mid) + b·(logit(p_model) − logit(mid)); inputs clipped to [0.01, 0.99], no intercept, ridge 1e-6. Unfitted rows use mid unchanged; excluded from blended tables: 240 rows. Rating parameters remain selected on the tuning window.

| Month | Kind | n | a | b | Status |
|---|---|---:|---:|---:|---|
| 2026-01 | series | 0 | 1.000000 | 0.000000 | unfitted |
| 2026-02 | series | 21 | 1.000000 | 0.000000 | unfitted |
| 2026-02 | map | 0 | 1.000000 | 0.000000 | unfitted |
| 2026-03 | series | 72 | 1.000000 | 0.000000 | unfitted |
| 2026-03 | map | 48 | 1.000000 | 0.000000 | unfitted |
| 2026-04 | series | 136 | 1.151951 | 0.442278 | fitted |
| 2026-04 | map | 104 | 1.539189 | 0.497671 | fitted |
| 2026-05 | series | 357 | 0.958513 | 0.297586 | fitted |
| 2026-05 | map | 456 | 0.865108 | 0.612669 | fitted |
| 2026-06 | series | 556 | 0.894094 | 0.226557 | fitted |
| 2026-06 | map | 833 | 0.743905 | 0.440648 | fitted |

#### Log loss vs Kalshi (blended)

| Kind | Slice | Rows | Model log loss | Kalshi log loss | Difference [95% interval] | Significant |
|---|---|---:|---:|---:|---|---|
| series | all | 541 | 0.635222 | 0.634347 | 0.000875 [-0.007253, 0.009086] | no |
| series | vct | 201 | 0.644503 | 0.644147 | 0.000356 [-0.012238, 0.013532] | no |
| series | vcl | 291 | 0.622943 | 0.621829 | 0.001114 [-0.010713, 0.013959] | no |
| series | gc | 0 | — | — | — | — |
| series | t3 | 0 | — | — | — | — |
| series | collegiate | 0 | — | — | — | — |
| series | offseason | 49 | 0.670075 | 0.668490 | 0.001585 [-0.014477, 0.016490] | no |
| series | international=1 | 24 | 0.678377 | 0.682705 | -0.004328 [-0.028051, 0.015470] | no |
| series | international=0 | 517 | 0.633219 | 0.632102 | 0.001116 [-0.007349, 0.010341] | no |
| map | all | 945 | 0.681231 | 0.673192 | 0.008039 [-0.003406, 0.019444] | no |
| map | vct | 392 | 0.679006 | 0.667249 | 0.011757 [-0.007144, 0.030994] | no |
| map | vcl | 456 | 0.684405 | 0.676303 | 0.008102 [-0.008395, 0.024910] | no |
| map | gc | 0 | — | — | — | — |
| map | t3 | 0 | — | — | — | — |
| map | collegiate | 0 | — | — | — | — |
| map | offseason | 97 | 0.675303 | 0.682581 | -0.007278 [-0.025524, 0.011423] | no |
| map | international=1 | 50 | 0.654324 | 0.651359 | 0.002966 [-0.016625, 0.021581] | no |
| map | international=0 | 895 | 0.682735 | 0.674412 | 0.008323 [-0.003758, 0.020177] | no |

#### Full-Kelly returns (blended)

| Kind | Slice | Bets | Matches | Mean edge | Flat ROI [95% interval] | Kelly, LoL caps ($50 start) | Multiple | Max drawdown | Largest stake | Bets filled | Flat ROI depth-capped [95% interval] | Kelly depth-capped final |
|---|---|---:|---:|---:|---|---:|---:|---:|---:|---:|---|---:|
| series | all | 162 | 162 | 0.0255 | 14.50% [-8.75%, 39.31%] | $24.84 | 0.497× | 55.20% | $5.22 | 92 (70 unfilled) | 19.83% [-6.58%, 49.79%] | $44.03 |
| series | vct | 59 | 59 | 0.0290 | 14.31% [-24.87%, 59.11%] | $25.05 | 0.501× | 55.19% | $5.06 | 35 (24 unfilled) | 31.54% [-18.13%, 89.96%] | $41.41 |
| series | vcl | 94 | 94 | 0.0249 | 13.90% [-14.01%, 46.54%] | $53.19 | 1.064× | 19.43% | $6.01 | 50 (44 unfilled) | 18.44% [-15.33%, 52.43%] | $56.92 |
| series | gc | 0 | 0 | — | — | $50.00 | 1.000× | 0.00% | $0.00 | 0 (0 unfilled) | — | $50.00 |
| series | t3 | 0 | 0 | — | — | $50.00 | 1.000× | 0.00% | $0.00 | 0 (0 unfilled) | — | $50.00 |
| series | collegiate | 0 | 0 | — | — | $50.00 | 1.000× | 0.00% | $0.00 | 0 (0 unfilled) | — | $50.00 |
| series | offseason | 9 | 9 | 0.0082 | 21.99% [-77.79%, 125.74%] | $46.88 | 0.938× | 8.83% | $1.61 | 7 (2 unfilled) | -28.75% [-100.00%, 56.75%] | $46.24 |
| series | international=1 | 6 | 6 | 0.0058 | 122.62% [-18.78%, 264.28%] | $53.43 | 1.069× | 1.61% | $0.82 | 6 (0 unfilled) | 122.62% [-18.78%, 264.28%] | $53.43 |
| series | international=0 | 156 | 156 | 0.0262 | 10.29% [-12.86%, 35.49%] | $23.26 | 0.465× | 58.04% | $5.22 | 86 (70 unfilled) | 12.59% [-13.98%, 42.63%] | $41.19 |
| map | all | 511 | 272 | 0.0470 | -1.04% [-11.87%, 12.94%] | $11.73 | 0.235× | 82.85% | $6.15 | 69 (442 unfilled) | -0.14% [-20.66%, 20.22%] | $42.85 |
| map | vct | 224 | 115 | 0.0510 | -4.81% [-17.56%, 8.09%] | $26.45 | 0.529× | 53.28% | $4.91 | 32 (192 unfilled) | 16.99% [-16.06%, 53.23%] | $64.93 |
| map | vcl | 257 | 141 | 0.0453 | 2.36% [-16.28%, 26.81%] | $21.27 | 0.425× | 73.80% | $7.03 | 34 (223 unfilled) | -12.45% [-37.04%, 12.36%] | $35.65 |
| map | gc | 0 | 0 | — | — | $50.00 | 1.000× | 0.00% | $0.00 | 0 (0 unfilled) | — | $50.00 |
| map | t3 | 0 | 0 | — | — | $50.00 | 1.000× | 0.00% | $0.00 | 0 (0 unfilled) | — | $50.00 |
| map | collegiate | 0 | 0 | — | — | $50.00 | 1.000× | 0.00% | $0.00 | 0 (0 unfilled) | — | $50.00 |
| map | offseason | 30 | 16 | 0.0320 | -2.11% [-33.24%, 28.96%] | $50.88 | 1.018× | 11.56% | $2.99 | 3 (27 unfilled) | -42.95% [-100.00%, -14.15%] | $46.23 |
| map | international=1 | 25 | 12 | 0.0147 | -19.35% [-54.44%, 15.43%] | $45.29 | 0.906× | 13.04% | $2.99 | 6 (19 unfilled) | -18.25% [-100.00%, 64.55%] | $48.26 |
| map | international=0 | 486 | 260 | 0.0487 | -0.09% [-11.81%, 14.40%] | $13.02 | 0.260× | 81.02% | $6.15 | 63 (423 unfilled) | 1.58% [-18.98%, 24.00%] | $44.35 |
| series+map | all | 673 | 313 | 0.0418 | 2.72% [-9.17%, 15.82%] | $12.05 | 0.241× | 85.08% | $6.71 | 161 (512 unfilled) | 11.31% [-6.54%, 29.93%] | $47.95 |

#### Monthly breakdown

All metrics use identical linked rows within each kind/month. Unfitted blend months show —; counts include all rows.

| Kind | Month | Rows | Model log loss | Blended log loss | Kalshi log loss | Raw flat ROI (bets), unlimited Kelly final | Blended flat ROI (bets), unlimited Kelly final | Raw bets filled | Raw Flat ROI depth-capped [95% interval] | Raw Kelly depth-capped final | Blended bets filled | Blended Flat ROI depth-capped [95% interval] | Blended Kelly depth-capped final |
|---|---|---:|---:|---:|---:|---|---|---:|---|---:|---:|---|---:|
| map | 2026-02 | 48 | 0.699857 | — | 0.690786 | -7.69% (27), $36.28 | — | 11 (16 unfilled) | -0.32% [-85.05%, 62.58%] | $43.26 | — | — | — |
| map | 2026-03 | 56 | 0.597898 | — | 0.565065 | -2.16% (39), $39.44 | — | 11 (28 unfilled) | 9.67% [-43.87%, 60.63%] | $50.17 | — | — | — |
| map | 2026-04 | 352 | 0.657308 | 0.696545 | 0.690793 | 45.91% (261), $4455.68 | 3.56% (240), $30.80 | 29 (232 unfilled) | 174.51% [-4.54%, 421.92%] | $234.45 | 29 (211 unfilled) | -5.31% [-25.16%, 14.40%] | $45.11 |
| map | 2026-05 | 377 | 0.709549 | 0.692876 | 0.687018 | -1.37% (261), $29.15 | -0.86% (172), $39.91 | 32 (229 unfilled) | 14.10% [-19.65%, 50.59%] | $56.62 | 28 (144 unfilled) | 14.04% [-25.61%, 54.46%] | $58.55 |
| map | 2026-06 | 216 | 0.647550 | 0.635951 | 0.620377 | -7.01% (151), $26.81 | -12.33% (99), $24.49 | 31 (120 unfilled) | 8.49% [-19.64%, 33.88%] | $48.34 | 12 (87 unfilled) | -21.04% [-78.34%, 32.75%] | $40.80 |
| series | 2026-01 | 21 | 0.667656 | — | 0.661069 | -1.29% (17), $42.40 | — | 10 (7 unfilled) | -32.98% [-83.50%, 35.50%] | $32.27 | — | — | — |
| series | 2026-02 | 51 | 0.642121 | — | 0.694525 | 29.33% (40), $139.85 | — | 26 (14 unfilled) | 56.16% [-0.85%, 124.93%] | $153.05 | — | — | — |
| series | 2026-03 | 64 | 0.642835 | — | 0.565917 | -21.94% (50), $14.24 | — | 36 (14 unfilled) | -10.93% [-40.81%, 19.59%] | $25.99 | — | — | — |
| series | 2026-04 | 221 | 0.647345 | 0.627895 | 0.627690 | 5.99% (153), $82.52 | 7.21% (76), $42.88 | 64 (89 unfilled) | 54.10% [8.12%, 104.46%] | $232.04 | 38 (38 unfilled) | 14.10% [-20.99%, 51.79%] | $46.76 |
| series | 2026-05 | 199 | 0.682843 | 0.662314 | 0.663719 | 0.29% (133), $22.77 | 15.29% (51), $31.09 | 85 (48 unfilled) | -1.40% [-26.42%, 24.64%] | $54.96 | 34 (17 unfilled) | 5.63% [-42.08%, 61.30%] | $51.29 |
| series | 2026-06 | 121 | 0.628694 | 0.604048 | 0.598199 | -11.65% (92), $19.23 | 28.94% (35), $46.67 | 51 (41 unfilled) | 10.49% [-17.94%, 39.48%] | $73.75 | 20 (15 unfilled) | 54.73% [-8.04%, 119.50%] | $46.24 |

### team_elo+regional: Kalshi comparison and returns

regional: rows=1069, ridge=4, s=0.539114, effects: Americas=0.134853, EMEA=0.0358544, Pacific=-0.0300089, China=-0.140699

#### Log loss vs Kalshi

| Kind | Slice | Rows | Model log loss | Kalshi log loss | Difference [95% interval] | Significant |
|---|---|---:|---:|---:|---|---|
| series | all | 677 | 0.661355 | 0.633240 | 0.028115 [0.006594, 0.050545] | yes |
| series | vct | 278 | 0.659421 | 0.634755 | 0.024666 [-0.005961, 0.056484] | no |
| series | vcl | 340 | 0.653983 | 0.619968 | 0.034015 [-0.001907, 0.069170] | no |
| series | gc | 0 | — | — | — | — |
| series | t3 | 0 | — | — | — | — |
| series | collegiate | 0 | — | — | — | — |
| series | offseason | 59 | 0.712948 | 0.702587 | 0.010361 [-0.037856, 0.060383] | no |
| series | international=1 | 41 | 0.644569 | 0.653397 | -0.008828 [-0.059366, 0.041234] | no |
| series | international=0 | 636 | 0.662437 | 0.631941 | 0.030496 [0.007402, 0.055149] | yes |
| map | all | 1049 | 0.674062 | 0.668225 | 0.005838 [-0.015884, 0.024931] | no |
| map | vct | 461 | 0.678264 | 0.665762 | 0.012502 [-0.011432, 0.035669] | no |
| map | vcl | 490 | 0.669823 | 0.668365 | 0.001458 [-0.038888, 0.036008] | no |
| map | gc | 0 | — | — | — | — |
| map | t3 | 0 | — | — | — | — |
| map | collegiate | 0 | — | — | — | — |
| map | offseason | 98 | 0.675493 | 0.679111 | -0.003618 [-0.033834, 0.028482] | no |
| map | international=1 | 59 | 0.651353 | 0.649653 | 0.001701 [-0.022880, 0.025591] | no |
| map | international=0 | 990 | 0.675416 | 0.669332 | 0.006084 [-0.016907, 0.027155] | no |

#### Full-Kelly returns

| Kind | Slice | Bets | Matches | Mean edge | Flat ROI [95% interval] | Kelly, LoL caps ($50 start) | Multiple | Max drawdown | Largest stake | Bets filled | Flat ROI depth-capped [95% interval] | Kelly depth-capped final |
|---|---|---:|---:|---:|---|---:|---:|---:|---:|---:|---|---:|
| series | all | 465 | 465 | 0.0901 | -1.10% [-13.92%, 13.31%] | $0.52 | 0.010× | 99.50% | $8.85 | 255 (210 unfilled) | 17.38% [-0.47%, 36.57%] | $164.74 |
| series | vct | 173 | 173 | 0.0798 | -0.62% [-20.58%, 22.46%] | $18.81 | 0.376× | 77.70% | $5.25 | 103 (70 unfilled) | 19.24% [-9.92%, 50.01%] | $140.24 |
| series | vcl | 257 | 257 | 0.1008 | -3.13% [-21.46%, 16.27%] | $3.01 | 0.060× | 97.13% | $8.48 | 126 (131 unfilled) | 20.05% [-6.42%, 48.56%] | $121.69 |
| series | gc | 0 | 0 | — | — | $50.00 | 1.000× | 0.00% | $0.00 | 0 (0 unfilled) | — | $50.00 |
| series | t3 | 0 | 0 | — | — | $50.00 | 1.000× | 0.00% | $0.00 | 0 (0 unfilled) | — | $50.00 |
| series | collegiate | 0 | 0 | — | — | $50.00 | 1.000× | 0.00% | $0.00 | 0 (0 unfilled) | — | $50.00 |
| series | offseason | 35 | 35 | 0.0621 | 11.45% [-25.64%, 52.12%] | $41.63 | 0.833× | 60.29% | $7.27 | 26 (9 unfilled) | -2.97% [-47.04%, 42.40%] | $36.62 |
| series | international=1 | 25 | 25 | 0.0498 | 18.98% [-34.16%, 81.79%] | $63.30 | 1.266× | 34.30% | $5.73 | 25 (0 unfilled) | 18.98% [-34.16%, 81.79%] | $68.20 |
| series | international=0 | 440 | 440 | 0.0924 | -2.24% [-15.57%, 11.64%] | $0.34 | 0.007× | 99.58% | $7.34 | 230 (210 unfilled) | 17.21% [-1.29%, 38.26%] | $121.05 |
| map | all | 681 | 362 | 0.0753 | 12.63% [-4.11%, 33.66%] | $491.83 | 9.837× | 79.38% | $138.51 | 107 (574 unfilled) | 53.70% [2.63%, 119.81%] | $206.11 |
| map | vct | 269 | 141 | 0.0671 | 4.98% [-12.14%, 28.24%] | $69.50 | 1.390× | 47.78% | $8.36 | 41 (228 unfilled) | 72.89% [-7.88%, 214.63%] | $92.97 |
| map | vcl | 350 | 190 | 0.0874 | 19.95% [-7.26%, 52.36%] | $366.07 | 7.321× | 72.37% | $80.85 | 57 (293 unfilled) | 48.44% [-12.85%, 131.95%] | $117.23 |
| map | gc | 0 | 0 | — | — | $50.00 | 1.000× | 0.00% | $0.00 | 0 (0 unfilled) | — | $50.00 |
| map | t3 | 0 | 0 | — | — | $50.00 | 1.000× | 0.00% | $0.00 | 0 (0 unfilled) | — | $50.00 |
| map | collegiate | 0 | 0 | — | — | $50.00 | 1.000× | 0.00% | $0.00 | 0 (0 unfilled) | — | $50.00 |
| map | offseason | 62 | 31 | 0.0420 | 4.29% [-20.29%, 28.35%] | $43.32 | 0.866× | 27.84% | $3.31 | 9 (53 unfilled) | -0.67% [-57.18%, 35.88%] | $47.13 |
| map | international=1 | 29 | 15 | 0.0419 | -2.90% [-28.72%, 25.59%] | $45.46 | 0.909× | 17.47% | $3.04 | 10 (19 unfilled) | 26.65% [-17.50%, 76.61%] | $53.01 |
| map | international=0 | 652 | 347 | 0.0768 | 13.32% [-4.03%, 33.49%] | $530.49 | 10.610× | 76.11% | $129.00 | 97 (555 unfilled) | 56.48% [-0.76%, 129.18%] | $198.48 |
| series+map | all | 1146 | 533 | 0.0813 | 7.04% [-5.25%, 20.44%] | $50.39 | 1.008× | 96.67% | $100.42 | 362 (784 unfilled) | 28.12% [7.18%, 51.83%] | $262.82 |

#### Monthly market blend fits

UTC monthly fits use earlier rows of the same kind from 2025-09-01, excluding holdout; minimum 100 rows. logit(p_blend) = a·logit(mid) + b·(logit(p_model) − logit(mid)); inputs clipped to [0.01, 0.99], no intercept, ridge 1e-6. Unfitted rows use mid unchanged; excluded from blended tables: 240 rows. Rating parameters remain selected on the tuning window.

| Month | Kind | n | a | b | Status |
|---|---|---:|---:|---:|---|
| 2026-01 | series | 0 | 1.000000 | 0.000000 | unfitted |
| 2026-02 | series | 21 | 1.000000 | 0.000000 | unfitted |
| 2026-02 | map | 0 | 1.000000 | 0.000000 | unfitted |
| 2026-03 | series | 72 | 1.000000 | 0.000000 | unfitted |
| 2026-03 | map | 48 | 1.000000 | 0.000000 | unfitted |
| 2026-04 | series | 136 | 0.994869 | 0.111337 | fitted |
| 2026-04 | map | 104 | 1.480508 | 0.269254 | fitted |
| 2026-05 | series | 357 | 0.916291 | 0.167028 | fitted |
| 2026-05 | map | 456 | 0.881870 | 0.559636 | fitted |
| 2026-06 | series | 556 | 0.838973 | 0.065782 | fitted |
| 2026-06 | map | 833 | 0.763016 | 0.394094 | fitted |

#### Log loss vs Kalshi (blended)

| Kind | Slice | Rows | Model log loss | Kalshi log loss | Difference [95% interval] | Significant |
|---|---|---:|---:|---:|---|---|
| series | all | 541 | 0.634451 | 0.634347 | 0.000104 [-0.004282, 0.004217] | no |
| series | vct | 201 | 0.642946 | 0.644147 | -0.001201 [-0.007993, 0.005565] | no |
| series | vcl | 291 | 0.622370 | 0.621829 | 0.000541 [-0.005427, 0.006616] | no |
| series | gc | 0 | — | — | — | — |
| series | t3 | 0 | — | — | — | — |
| series | collegiate | 0 | — | — | — | — |
| series | offseason | 49 | 0.671347 | 0.668490 | 0.002857 [-0.009293, 0.013351] | no |
| series | international=1 | 24 | 0.675815 | 0.682705 | -0.006891 [-0.035772, 0.016794] | no |
| series | international=0 | 517 | 0.632530 | 0.632102 | 0.000428 [-0.003786, 0.004558] | no |
| map | all | 945 | 0.684258 | 0.673192 | 0.011066 [0.002438, 0.019682] | yes |
| map | vct | 392 | 0.676563 | 0.667249 | 0.009313 [-0.004246, 0.023732] | no |
| map | vcl | 456 | 0.692286 | 0.676303 | 0.015983 [0.002915, 0.028957] | yes |
| map | gc | 0 | — | — | — | — |
| map | t3 | 0 | — | — | — | — |
| map | collegiate | 0 | — | — | — | — |
| map | offseason | 97 | 0.677615 | 0.682581 | -0.004966 [-0.019240, 0.009479] | no |
| map | international=1 | 50 | 0.657412 | 0.651359 | 0.006054 [-0.007257, 0.020738] | no |
| map | international=0 | 895 | 0.685757 | 0.674412 | 0.011346 [0.001892, 0.020337] | yes |

#### Full-Kelly returns (blended)

| Kind | Slice | Bets | Matches | Mean edge | Flat ROI [95% interval] | Kelly, LoL caps ($50 start) | Multiple | Max drawdown | Largest stake | Bets filled | Flat ROI depth-capped [95% interval] | Kelly depth-capped final |
|---|---|---:|---:|---:|---|---:|---:|---:|---:|---:|---|---:|
| series | all | 60 | 60 | 0.0102 | -11.63% [-52.14%, 30.72%] | $42.09 | 0.842× | 30.23% | $3.36 | 37 (23 unfilled) | 10.04% [-42.76%, 69.85%] | $51.28 |
| series | vct | 21 | 21 | 0.0136 | 25.36% [-53.63%, 114.43%] | $48.27 | 0.965× | 23.90% | $2.96 | 15 (6 unfilled) | 75.45% [-25.20%, 198.38%] | $57.17 |
| series | vcl | 38 | 38 | 0.0083 | -29.73% [-70.06%, 18.52%] | $44.25 | 0.885× | 14.57% | $3.28 | 21 (17 unfilled) | -31.52% [-75.86%, 22.41%] | $45.61 |
| series | gc | 0 | 0 | — | — | $50.00 | 1.000× | 0.00% | $0.00 | 0 (0 unfilled) | — | $50.00 |
| series | t3 | 0 | 0 | — | — | $50.00 | 1.000× | 0.00% | $0.00 | 0 (0 unfilled) | — | $50.00 |
| series | collegiate | 0 | 0 | — | — | $50.00 | 1.000× | 0.00% | $0.00 | 0 (0 unfilled) | — | $50.00 |
| series | offseason | 1 | 1 | 0.0111 | -100.00% [-100.00%, -100.00%] | $49.20 | 0.984× | 1.60% | $0.76 | 1 (0 unfilled) | -100.00% [-100.00%, -100.00%] | $49.20 |
| series | international=1 | 8 | 8 | 0.0091 | 43.10% [-63.06%, 185.87%] | $58.18 | 1.164× | 2.52% | $1.12 | 8 (0 unfilled) | 43.10% [-63.06%, 185.87%] | $58.18 |
| series | international=0 | 52 | 52 | 0.0104 | -20.04% [-62.15%, 25.80%] | $36.14 | 0.723× | 30.23% | $3.36 | 29 (23 unfilled) | 0.91% [-52.88%, 69.89%] | $43.98 |
| map | all | 437 | 242 | 0.0326 | -6.48% [-15.38%, 3.15%] | $8.17 | 0.163× | 86.67% | $5.55 | 66 (371 unfilled) | -2.16% [-22.85%, 18.97%] | $38.64 |
| map | vct | 187 | 99 | 0.0363 | -2.21% [-16.09%, 11.93%] | $27.55 | 0.551× | 50.09% | $5.04 | 29 (158 unfilled) | 6.81% [-29.86%, 45.52%] | $51.41 |
| map | vcl | 223 | 128 | 0.0310 | -10.85% [-23.15%, 2.11%] | $15.72 | 0.314× | 74.75% | $5.67 | 34 (189 unfilled) | -6.18% [-31.54%, 19.23%] | $40.57 |
| map | gc | 0 | 0 | — | — | $50.00 | 1.000× | 0.00% | $0.00 | 0 (0 unfilled) | — | $50.00 |
| map | t3 | 0 | 0 | — | — | $50.00 | 1.000× | 0.00% | $0.00 | 0 (0 unfilled) | — | $50.00 |
| map | collegiate | 0 | 0 | — | — | $50.00 | 1.000× | 0.00% | $0.00 | 0 (0 unfilled) | — | $50.00 |
| map | offseason | 27 | 15 | 0.0199 | 0.15% [-30.93%, 31.29%] | $48.48 | 0.970× | 9.63% | $2.86 | 3 (24 unfilled) | -42.95% [-100.00%, -14.15%] | $46.45 |
| map | international=1 | 12 | 7 | 0.0270 | 2.75% [-51.24%, 59.76%] | $45.91 | 0.918× | 10.00% | $2.37 | 3 (9 unfilled) | -25.94% [-25.94%, -25.94%] | $47.44 |
| map | international=0 | 425 | 235 | 0.0328 | -6.74% [-15.82%, 2.65%] | $8.91 | 0.178× | 85.46% | $5.55 | 63 (362 unfilled) | -1.02% [-23.80%, 20.51%] | $40.59 |
| series+map | all | 497 | 266 | 0.0299 | -7.11% [-17.77%, 5.00%] | $7.64 | 0.153× | 87.46% | $5.55 | 103 (394 unfilled) | 2.27% [-21.36%, 28.51%] | $38.59 |

#### Monthly breakdown

All metrics use identical linked rows within each kind/month. Unfitted blend months show —; counts include all rows.

| Kind | Month | Rows | Model log loss | Blended log loss | Kalshi log loss | Raw flat ROI (bets), unlimited Kelly final | Blended flat ROI (bets), unlimited Kelly final | Raw bets filled | Raw Flat ROI depth-capped [95% interval] | Raw Kelly depth-capped final | Blended bets filled | Blended Flat ROI depth-capped [95% interval] | Blended Kelly depth-capped final |
|---|---|---:|---:|---:|---:|---|---|---:|---|---:|---:|---|---:|
| map | 2026-02 | 48 | 0.703819 | — | 0.690786 | -19.10% (25), $33.55 | — | 9 (16 unfilled) | -1.84% [-100.00%, 65.78%] | $45.89 | — | — | — |
| map | 2026-03 | 56 | 0.631331 | — | 0.565065 | -28.91% (32), $23.70 | — | 9 (23 unfilled) | -32.37% [-83.38%, 41.61%] | $38.71 | — | — | — |
| map | 2026-04 | 352 | 0.663126 | 0.707600 | 0.690793 | 49.37% (237), $6058.42 | -8.72% (204), $19.04 | 29 (208 unfilled) | 183.25% [4.69%, 428.45%] | $242.59 | 31 (173 unfilled) | -9.72% [-29.68%, 10.26%] | $42.09 |
| map | 2026-05 | 377 | 0.704131 | 0.690060 | 0.687018 | -1.28% (249), $26.14 | 0.56% (148), $44.06 | 36 (213 unfilled) | 10.12% [-22.78%, 41.28%] | $54.33 | 25 (123 unfilled) | 11.32% [-34.86%, 53.52%] | $53.92 |
| map | 2026-06 | 216 | 0.643869 | 0.636092 | 0.620377 | -9.92% (138), $18.03 | -13.38% (85), $25.39 | 24 (114 unfilled) | 15.43% [-17.05%, 43.88%] | $45.29 | 10 (75 unfilled) | -12.96% [-72.35%, 38.43%] | $42.75 |
| series | 2026-01 | 21 | 0.692233 | — | 0.661069 | 4.92% (16), $45.54 | — | 9 (7 unfilled) | -25.46% [-81.66%, 48.91%] | $36.24 | — | — | — |
| series | 2026-02 | 51 | 0.664482 | — | 0.694525 | 25.39% (34), $87.45 | — | 23 (11 unfilled) | 49.61% [-13.35%, 131.25%] | $128.01 | — | — | — |
| series | 2026-03 | 64 | 0.671104 | — | 0.565917 | -33.05% (45), $8.57 | — | 33 (12 unfilled) | -19.86% [-57.18%, 21.15%] | $15.88 | — | — | — |
| series | 2026-04 | 221 | 0.648713 | 0.625256 | 0.627690 | 3.79% (149), $60.55 | -19.15% (10), $44.66 | 61 (88 unfilled) | 57.55% [9.23%, 113.13%] | $203.58 | 6 (4 unfilled) | 35.52% [-65.71%, 149.01%] | $47.29 |
| series | 2026-05 | 199 | 0.692929 | 0.662930 | 0.663719 | 1.68% (131), $7.83 | -26.91% (21), $42.02 | 83 (48 unfilled) | -1.77% [-26.49%, 26.40%] | $32.93 | 14 (7 unfilled) | 9.58% [-81.24%, 124.19%] | $50.31 |
| series | 2026-06 | 121 | 0.620683 | 0.604407 | 0.598199 | -8.36% (90), $16.68 | 2.01% (29), $56.07 | 46 (44 unfilled) | 17.40% [-17.81%, 52.00%] | $79.29 | 17 (12 unfilled) | 1.49% [-68.34%, 83.56%] | $54.03 |

### team_elo+regional_form: Kalshi comparison and returns

regional_form: regional: rows=1069, ridge=4, s=0.539114, effects: Americas=0.134853, EMEA=0.0358544, Pacific=-0.0300089, China=-0.140699; form: rows=25380, H=80, w=3.33271

#### Log loss vs Kalshi

| Kind | Slice | Rows | Model log loss | Kalshi log loss | Difference [95% interval] | Significant |
|---|---|---:|---:|---:|---|---|
| series | all | 677 | 0.655292 | 0.633240 | 0.022052 [-0.001172, 0.045787] | no |
| series | vct | 278 | 0.652884 | 0.634755 | 0.018129 [-0.013038, 0.049103] | no |
| series | vcl | 340 | 0.651250 | 0.619968 | 0.031283 [-0.005126, 0.068821] | no |
| series | gc | 0 | — | — | — | — |
| series | t3 | 0 | — | — | — | — |
| series | collegiate | 0 | — | — | — | — |
| series | offseason | 59 | 0.689935 | 0.702587 | -0.012652 [-0.060058, 0.036940] | no |
| series | international=1 | 41 | 0.629933 | 0.653397 | -0.023463 [-0.070419, 0.023565] | no |
| series | international=0 | 636 | 0.656927 | 0.631941 | 0.024986 [0.001579, 0.050053] | yes |
| map | all | 1049 | 0.672483 | 0.668225 | 0.004259 [-0.019043, 0.025369] | no |
| map | vct | 461 | 0.678695 | 0.665762 | 0.012934 [-0.013695, 0.039437] | no |
| map | vcl | 490 | 0.666597 | 0.668365 | -0.001768 [-0.042881, 0.035284] | no |
| map | gc | 0 | — | — | — | — |
| map | t3 | 0 | — | — | — | — |
| map | collegiate | 0 | — | — | — | — |
| map | offseason | 98 | 0.672695 | 0.679111 | -0.006416 [-0.040603, 0.028501] | no |
| map | international=1 | 59 | 0.643914 | 0.649653 | -0.005739 [-0.039326, 0.028210] | no |
| map | international=0 | 990 | 0.674186 | 0.669332 | 0.004855 [-0.019657, 0.026752] | no |

#### Full-Kelly returns

| Kind | Slice | Bets | Matches | Mean edge | Flat ROI [95% interval] | Kelly, LoL caps ($50 start) | Multiple | Max drawdown | Largest stake | Bets filled | Flat ROI depth-capped [95% interval] | Kelly depth-capped final |
|---|---|---:|---:|---:|---|---:|---:|---:|---:|---:|---|---:|
| series | all | 474 | 474 | 0.0874 | 1.64% [-11.50%, 14.99%] | $9.24 | 0.185× | 94.39% | $12.30 | 263 (211 unfilled) | 19.43% [1.62%, 37.64%] | $465.94 |
| series | vct | 182 | 182 | 0.0776 | -1.04% [-20.68%, 20.44%] | $30.84 | 0.617× | 67.14% | $5.04 | 107 (75 unfilled) | 22.96% [-4.19%, 53.44%] | $191.09 |
| series | vcl | 253 | 253 | 0.0990 | 1.37% [-15.34%, 20.96%] | $8.71 | 0.174× | 92.00% | $8.51 | 127 (126 unfilled) | 21.38% [-4.65%, 47.48%] | $159.79 |
| series | gc | 0 | 0 | — | — | $50.00 | 1.000× | 0.00% | $0.00 | 0 (0 unfilled) | — | $50.00 |
| series | t3 | 0 | 0 | — | — | $50.00 | 1.000× | 0.00% | $0.00 | 0 (0 unfilled) | — | $50.00 |
| series | collegiate | 0 | 0 | — | — | $50.00 | 1.000× | 0.00% | $0.00 | 0 (0 unfilled) | — | $50.00 |
| series | offseason | 39 | 39 | 0.0575 | 15.96% [-19.88%, 54.17%] | $83.41 | 1.668× | 42.36% | $8.00 | 29 (10 unfilled) | -2.18% [-42.56%, 40.18%] | $54.66 |
| series | international=1 | 28 | 28 | 0.0449 | 22.77% [-26.07%, 79.64%] | $71.49 | 1.430× | 28.49% | $5.69 | 27 (1 unfilled) | 21.71% [-31.65%, 81.37%] | $72.92 |
| series | international=0 | 446 | 446 | 0.0901 | 0.32% [-12.97%, 14.19%] | $6.40 | 0.128× | 95.52% | $11.23 | 236 (210 unfilled) | 19.16% [1.18%, 38.46%] | $303.56 |
| map | all | 726 | 384 | 0.0800 | 14.89% [-0.36%, 33.45%] | $2338.43 | 46.769× | 43.70% | $245.70 | 111 (615 unfilled) | 54.00% [5.68%, 123.67%] | $251.63 |
| map | vct | 317 | 165 | 0.0684 | 8.17% [-6.95%, 28.28%] | $82.35 | 1.647× | 43.52% | $9.66 | 48 (269 unfilled) | 74.98% [7.54%, 186.19%] | $122.58 |
| map | vcl | 345 | 189 | 0.0966 | 23.96% [-3.79%, 59.15%] | $788.95 | 15.779× | 64.11% | $140.28 | 52 (293 unfilled) | 46.95% [-20.14%, 138.26%] | $126.54 |
| map | gc | 0 | 0 | — | — | $50.00 | 1.000× | 0.00% | $0.00 | 0 (0 unfilled) | — | $50.00 |
| map | t3 | 0 | 0 | — | — | $50.00 | 1.000× | 0.00% | $0.00 | 0 (0 unfilled) | — | $50.00 |
| map | collegiate | 0 | 0 | — | — | $50.00 | 1.000× | 0.00% | $0.00 | 0 (0 unfilled) | — | $50.00 |
| map | offseason | 64 | 30 | 0.0481 | -0.95% [-23.42%, 21.08%] | $48.56 | 0.971× | 19.08% | $3.68 | 11 (53 unfilled) | -4.63% [-44.12%, 27.77%] | $45.85 |
| map | international=1 | 37 | 19 | 0.0514 | 13.57% [-8.15%, 35.61%] | $60.23 | 1.205× | 12.01% | $3.95 | 14 (23 unfilled) | 34.88% [1.62%, 70.11%] | $61.37 |
| map | international=0 | 689 | 365 | 0.0815 | 14.96% [-1.29%, 35.07%] | $1297.19 | 25.944× | 62.94% | $226.94 | 97 (592 unfilled) | 56.74% [1.62%, 133.92%] | $226.14 |
| series+map | all | 1200 | 566 | 0.0829 | 9.64% [-1.93%, 23.10%] | $3196.51 | 63.930× | 89.73% | $246.03 | 374 (826 unfilled) | 29.67% [10.03%, 53.31%] | $502.09 |

#### Monthly market blend fits

UTC monthly fits use earlier rows of the same kind from 2025-09-01, excluding holdout; minimum 100 rows. logit(p_blend) = a·logit(mid) + b·(logit(p_model) − logit(mid)); inputs clipped to [0.01, 0.99], no intercept, ridge 1e-6. Unfitted rows use mid unchanged; excluded from blended tables: 240 rows. Rating parameters remain selected on the tuning window.

| Month | Kind | n | a | b | Status |
|---|---|---:|---:|---:|---|
| 2026-01 | series | 0 | 1.000000 | 0.000000 | unfitted |
| 2026-02 | series | 21 | 1.000000 | 0.000000 | unfitted |
| 2026-02 | map | 0 | 1.000000 | 0.000000 | unfitted |
| 2026-03 | series | 72 | 1.000000 | 0.000000 | unfitted |
| 2026-03 | map | 48 | 1.000000 | 0.000000 | unfitted |
| 2026-04 | series | 136 | 1.129934 | 0.379571 | fitted |
| 2026-04 | map | 104 | 1.591109 | 0.579571 | fitted |
| 2026-05 | series | 357 | 0.940595 | 0.245232 | fitted |
| 2026-05 | map | 456 | 0.870934 | 0.609540 | fitted |
| 2026-06 | series | 556 | 0.878831 | 0.182407 | fitted |
| 2026-06 | map | 833 | 0.746078 | 0.434052 | fitted |

#### Log loss vs Kalshi (blended)

| Kind | Slice | Rows | Model log loss | Kalshi log loss | Difference [95% interval] | Significant |
|---|---|---:|---:|---:|---|---|
| series | all | 541 | 0.634880 | 0.634347 | 0.000533 [-0.006734, 0.007737] | no |
| series | vct | 201 | 0.643914 | 0.644147 | -0.000232 [-0.011538, 0.011600] | no |
| series | vcl | 291 | 0.622820 | 0.621829 | 0.000992 [-0.009155, 0.012075] | no |
| series | gc | 0 | — | — | — | — |
| series | t3 | 0 | — | — | — | — |
| series | collegiate | 0 | — | — | — | — |
| series | offseason | 49 | 0.669440 | 0.668490 | 0.000950 [-0.013459, 0.014140] | no |
| series | international=1 | 24 | 0.672189 | 0.682705 | -0.010517 [-0.039115, 0.013132] | no |
| series | international=0 | 517 | 0.633148 | 0.632102 | 0.001046 [-0.006430, 0.009054] | no |
| map | all | 945 | 0.681699 | 0.673192 | 0.008507 [-0.003841, 0.020783] | no |
| map | vct | 392 | 0.681501 | 0.667249 | 0.014252 [-0.005805, 0.035179] | no |
| map | vcl | 456 | 0.683208 | 0.676303 | 0.006905 [-0.011255, 0.024673] | no |
| map | gc | 0 | — | — | — | — |
| map | t3 | 0 | — | — | — | — |
| map | collegiate | 0 | — | — | — | — |
| map | offseason | 97 | 0.675401 | 0.682581 | -0.007180 [-0.025460, 0.011386] | no |
| map | international=1 | 50 | 0.652355 | 0.651359 | 0.000996 [-0.015029, 0.016737] | no |
| map | international=0 | 895 | 0.683338 | 0.674412 | 0.008926 [-0.004033, 0.021967] | no |

#### Full-Kelly returns (blended)

| Kind | Slice | Bets | Matches | Mean edge | Flat ROI [95% interval] | Kelly, LoL caps ($50 start) | Multiple | Max drawdown | Largest stake | Bets filled | Flat ROI depth-capped [95% interval] | Kelly depth-capped final |
|---|---|---:|---:|---:|---|---:|---:|---:|---:|---:|---|---:|
| series | all | 133 | 133 | 0.0225 | 17.32% [-9.96%, 47.37%] | $28.39 | 0.568× | 50.12% | $4.50 | 76 (57 unfilled) | 16.33% [-17.51%, 52.41%] | $47.21 |
| series | vct | 47 | 47 | 0.0270 | 11.81% [-36.32%, 68.66%] | $33.94 | 0.679× | 48.12% | $5.21 | 29 (18 unfilled) | 19.51% [-38.61%, 89.54%] | $49.76 |
| series | vcl | 80 | 80 | 0.0212 | 17.94% [-15.53%, 54.94%] | $43.23 | 0.865× | 21.27% | $5.04 | 42 (38 unfilled) | 16.09% [-20.27%, 54.75%] | $48.56 |
| series | gc | 0 | 0 | — | — | $50.00 | 1.000× | 0.00% | $0.00 | 0 (0 unfilled) | — | $50.00 |
| series | t3 | 0 | 0 | — | — | $50.00 | 1.000× | 0.00% | $0.00 | 0 (0 unfilled) | — | $50.00 |
| series | collegiate | 0 | 0 | — | — | $50.00 | 1.000× | 0.00% | $0.00 | 0 (0 unfilled) | — | $50.00 |
| series | offseason | 6 | 6 | 0.0056 | 52.17% [-66.72%, 189.25%] | $48.59 | 0.972× | 4.01% | $1.27 | 5 (1 unfilled) | -0.22% [-100.00%, 119.09%] | $48.11 |
| series | international=1 | 6 | 6 | 0.0142 | 90.72% [-50.71%, 256.75%] | $60.27 | 1.205× | 2.08% | $2.13 | 6 (0 unfilled) | 90.72% [-50.71%, 256.75%] | $60.27 |
| series | international=0 | 127 | 127 | 0.0229 | 13.82% [-12.09%, 42.36%] | $23.55 | 0.471× | 55.31% | $4.50 | 70 (57 unfilled) | 9.88% [-22.16%, 43.55%] | $39.07 |
| map | all | 512 | 274 | 0.0509 | 6.55% [-8.37%, 25.14%] | $15.40 | 0.308× | 81.69% | $7.30 | 68 (444 unfilled) | 2.20% [-16.94%, 23.12%] | $43.19 |
| map | vct | 220 | 113 | 0.0563 | -2.73% [-15.43%, 10.51%] | $29.38 | 0.588× | 51.54% | $4.91 | 31 (189 unfilled) | 22.66% [-8.98%, 58.34%] | $66.97 |
| map | vcl | 262 | 145 | 0.0485 | 15.31% [-10.95%, 53.51%] | $22.63 | 0.453× | 74.52% | $7.77 | 34 (228 unfilled) | -12.45% [-37.04%, 12.36%] | $34.52 |
| map | gc | 0 | 0 | — | — | $50.00 | 1.000× | 0.00% | $0.00 | 0 (0 unfilled) | — | $50.00 |
| map | t3 | 0 | 0 | — | — | $50.00 | 1.000× | 0.00% | $0.00 | 0 (0 unfilled) | — | $50.00 |
| map | collegiate | 0 | 0 | — | — | $50.00 | 1.000× | 0.00% | $0.00 | 0 (0 unfilled) | — | $50.00 |
| map | offseason | 30 | 16 | 0.0317 | -2.11% [-33.24%, 28.96%] | $51.12 | 1.022× | 11.56% | $3.00 | 3 (27 unfilled) | -42.95% [-100.00%, -14.15%] | $46.34 |
| map | international=1 | 18 | 8 | 0.0215 | 6.88% [-29.39%, 42.08%] | $49.04 | 0.981× | 10.00% | $2.37 | 5 (13 unfilled) | 9.91% [-25.94%, 64.55%] | $49.72 |
| map | international=0 | 494 | 266 | 0.0519 | 6.54% [-9.28%, 26.05%] | $15.76 | 0.315× | 81.29% | $7.30 | 63 (431 unfilled) | 1.58% [-18.98%, 24.00%] | $43.44 |
| series+map | all | 645 | 308 | 0.0450 | 8.79% [-5.57%, 25.58%] | $14.48 | 0.290× | 83.42% | $7.61 | 144 (501 unfilled) | 9.69% [-9.88%, 30.99%] | $48.40 |

#### Monthly breakdown

All metrics use identical linked rows within each kind/month. Unfitted blend months show —; counts include all rows.

| Kind | Month | Rows | Model log loss | Blended log loss | Kalshi log loss | Raw flat ROI (bets), unlimited Kelly final | Blended flat ROI (bets), unlimited Kelly final | Raw bets filled | Raw Flat ROI depth-capped [95% interval] | Raw Kelly depth-capped final | Blended bets filled | Blended Flat ROI depth-capped [95% interval] | Blended Kelly depth-capped final |
|---|---|---:|---:|---:|---:|---|---|---:|---|---:|---:|---|---:|
| map | 2026-02 | 48 | 0.702747 | — | 0.690786 | -7.69% (27), $36.36 | — | 11 (16 unfilled) | -0.32% [-85.05%, 62.58%] | $43.36 | — | — | — |
| map | 2026-03 | 56 | 0.590099 | — | 0.565065 | -0.81% (37), $44.25 | — | 10 (27 unfilled) | 6.19% [-50.57%, 63.65%] | $53.48 | — | — | — |
| map | 2026-04 | 352 | 0.659563 | 0.698398 | 0.690793 | 46.14% (258), $4277.24 | 16.42% (250), $36.78 | 29 (229 unfilled) | 174.51% [-4.54%, 421.92%] | $234.30 | 29 (221 unfilled) | -5.31% [-25.16%, 14.40%] | $43.80 |
| map | 2026-05 | 377 | 0.709306 | 0.692734 | 0.687018 | -0.97% (263), $28.99 | -0.61% (170), $40.16 | 32 (231 unfilled) | 14.10% [-19.65%, 50.59%] | $56.65 | 28 (142 unfilled) | 14.04% [-25.61%, 54.46%] | $58.94 |
| map | 2026-06 | 216 | 0.643903 | 0.635224 | 0.620377 | -4.26% (141), $33.21 | -6.69% (92), $26.54 | 29 (112 unfilled) | 14.07% [-15.12%, 38.40%] | $48.70 | 11 (81 unfilled) | -8.54% [-59.52%, 35.54%] | $42.11 |
| series | 2026-01 | 21 | 0.673017 | — | 0.661069 | -1.29% (17), $42.55 | — | 10 (7 unfilled) | -32.98% [-83.50%, 35.50%] | $32.19 | — | — | — |
| series | 2026-02 | 51 | 0.646635 | — | 0.694525 | 32.08% (38), $137.67 | — | 25 (13 unfilled) | 56.14% [-0.29%, 124.95%] | $149.58 | — | — | — |
| series | 2026-03 | 64 | 0.649758 | — | 0.565917 | -21.71% (46), $11.43 | — | 32 (14 unfilled) | -9.25% [-47.57%, 33.24%] | $20.28 | — | — | — |
| series | 2026-04 | 221 | 0.649853 | 0.628074 | 0.627690 | 7.09% (153), $73.71 | 10.42% (61), $39.38 | 64 (89 unfilled) | 54.40% [9.33%, 105.43%] | $226.41 | 31 (30 unfilled) | 12.79% [-28.76%, 56.62%] | $45.50 |
| series | 2026-05 | 199 | 0.683908 | 0.661901 | 0.663719 | 0.31% (133), $21.35 | 26.29% (42), $34.34 | 85 (48 unfilled) | -1.36% [-26.12%, 24.77%] | $55.51 | 29 (13 unfilled) | 10.44% [-42.55%, 69.76%] | $50.76 |
| series | 2026-06 | 121 | 0.621666 | 0.602872 | 0.598199 | -6.30% (87), $28.06 | 18.64% (30), $52.67 | 47 (40 unfilled) | 20.35% [-12.68%, 55.47%] | $112.25 | 16 (14 unfilled) | 33.72% [-41.62%, 115.98%] | $51.61 |

### player_round_glicko_rookie+form: Kalshi comparison and returns

form: rows=25380, H=80, w=1.32932

#### Log loss vs Kalshi

| Kind | Slice | Rows | Model log loss | Kalshi log loss | Difference [95% interval] | Significant |
|---|---|---:|---:|---:|---|---|
| series | all | 677 | 0.622641 | 0.633240 | -0.010599 [-0.033331, 0.012083] | no |
| series | vct | 278 | 0.623918 | 0.634755 | -0.010836 [-0.042316, 0.017655] | no |
| series | vcl | 340 | 0.612489 | 0.619968 | -0.007479 [-0.045906, 0.031458] | no |
| series | gc | 0 | — | — | — | — |
| series | t3 | 0 | — | — | — | — |
| series | collegiate | 0 | — | — | — | — |
| series | offseason | 59 | 0.675133 | 0.702587 | -0.027453 [-0.086596, 0.028587] | no |
| series | international=1 | 41 | 0.614991 | 0.653397 | -0.038406 [-0.086315, 0.009544] | no |
| series | international=0 | 636 | 0.623135 | 0.631941 | -0.008806 [-0.034087, 0.015856] | no |
| map | all | 1049 | 0.657559 | 0.668225 | -0.010666 [-0.032954, 0.008263] | no |
| map | vct | 461 | 0.660165 | 0.665762 | -0.005597 [-0.026303, 0.013389] | no |
| map | vcl | 490 | 0.650091 | 0.668365 | -0.018274 [-0.061162, 0.017768] | no |
| map | gc | 0 | — | — | — | — |
| map | t3 | 0 | — | — | — | — |
| map | collegiate | 0 | — | — | — | — |
| map | offseason | 98 | 0.682635 | 0.679111 | 0.003524 [-0.030305, 0.036203] | no |
| map | international=1 | 59 | 0.664228 | 0.649653 | 0.014576 [-0.019023, 0.051465] | no |
| map | international=0 | 990 | 0.657161 | 0.669332 | -0.012170 [-0.034912, 0.008286] | no |

#### Full-Kelly returns

| Kind | Slice | Bets | Matches | Mean edge | Flat ROI [95% interval] | Kelly, LoL caps ($50 start) | Multiple | Max drawdown | Largest stake | Bets filled | Flat ROI depth-capped [95% interval] | Kelly depth-capped final |
|---|---|---:|---:|---:|---|---:|---:|---:|---:|---:|---|---:|
| series | all | 490 | 490 | 0.0912 | 9.69% [-2.56%, 22.26%] | $1418.44 | 28.369× | 78.26% | $242.03 | 278 (212 unfilled) | 19.32% [2.98%, 37.11%] | $894.82 |
| series | vct | 198 | 198 | 0.0767 | 7.52% [-12.19%, 28.79%] | $60.09 | 1.202× | 72.32% | $5.45 | 123 (75 unfilled) | 22.57% [-2.08%, 50.71%] | $228.89 |
| series | vcl | 253 | 253 | 0.1055 | 12.98% [-4.30%, 31.62%] | $693.83 | 13.877× | 59.50% | $131.12 | 125 (128 unfilled) | 21.96% [-3.30%, 47.94%] | $263.28 |
| series | gc | 0 | 0 | — | — | $50.00 | 1.000× | 0.00% | $0.00 | 0 (0 unfilled) | — | $50.00 |
| series | t3 | 0 | 0 | — | — | $50.00 | 1.000× | 0.00% | $0.00 | 0 (0 unfilled) | — | $50.00 |
| series | collegiate | 0 | 0 | — | — | $50.00 | 1.000× | 0.00% | $0.00 | 0 (0 unfilled) | — | $50.00 |
| series | offseason | 39 | 39 | 0.0719 | -0.66% [-39.45%, 41.58%] | $89.62 | 1.792× | 35.61% | $10.24 | 30 (9 unfilled) | -4.89% [-46.92%, 40.67%] | $59.23 |
| series | international=1 | 28 | 28 | 0.0467 | 33.20% [-12.64%, 82.96%] | $93.09 | 1.862× | 23.81% | $7.41 | 28 (0 unfilled) | 33.20% [-12.64%, 82.96%] | $95.87 |
| series | international=0 | 462 | 462 | 0.0939 | 8.26% [-4.64%, 21.68%] | $1348.32 | 26.966× | 78.26% | $190.15 | 250 (212 unfilled) | 17.77% [0.76%, 36.56%] | $493.87 |
| map | all | 704 | 374 | 0.0713 | 19.71% [2.81%, 38.78%] | $5136.77 | 102.735× | 30.79% | $245.53 | 104 (600 unfilled) | 50.61% [-3.00%, 121.15%] | $238.02 |
| map | vct | 292 | 152 | 0.0601 | 11.53% [-5.75%, 33.68%] | $220.59 | 4.412× | 31.55% | $18.30 | 55 (237 unfilled) | 50.92% [-11.06%, 156.21%] | $115.67 |
| map | vcl | 356 | 195 | 0.0852 | 28.31% [1.03%, 61.78%] | $1600.72 | 32.014× | 60.89% | $245.53 | 44 (312 unfilled) | 46.26% [-30.63%, 157.85%] | $133.29 |
| map | gc | 0 | 0 | — | — | $50.00 | 1.000× | 0.00% | $0.00 | 0 (0 unfilled) | — | $50.00 |
| map | t3 | 0 | 0 | — | — | $50.00 | 1.000× | 0.00% | $0.00 | 0 (0 unfilled) | — | $50.00 |
| map | collegiate | 0 | 0 | — | — | $50.00 | 1.000× | 0.00% | $0.00 | 0 (0 unfilled) | — | $50.00 |
| map | offseason | 56 | 27 | 0.0414 | 7.49% [-22.56%, 36.85%] | $57.92 | 1.158× | 15.48% | $3.95 | 5 (51 unfilled) | 85.42% [23.05%, 209.00%] | $56.52 |
| map | international=1 | 34 | 19 | 0.0518 | -5.37% [-32.61%, 23.32%] | $43.17 | 0.863× | 17.73% | $4.43 | 14 (20 unfilled) | 9.97% [-25.39%, 51.07%] | $52.23 |
| map | international=0 | 670 | 355 | 0.0723 | 20.98% [4.14%, 40.67%] | $5304.62 | 106.092× | 31.30% | $245.53 | 90 (580 unfilled) | 56.88% [-4.11%, 138.84%] | $235.09 |
| series+map | all | 1194 | 547 | 0.0795 | 15.59% [3.68%, 29.32%] | $3849.11 | 76.982× | 52.96% | $247.91 | 382 (812 unfilled) | 27.83% [7.25%, 50.77%] | $418.39 |

#### Monthly market blend fits

UTC monthly fits use earlier rows of the same kind from 2025-09-01, excluding holdout; minimum 100 rows. logit(p_blend) = a·logit(mid) + b·(logit(p_model) − logit(mid)); inputs clipped to [0.01, 0.99], no intercept, ridge 1e-6. Unfitted rows use mid unchanged; excluded from blended tables: 240 rows. Rating parameters remain selected on the tuning window.

| Month | Kind | n | a | b | Status |
|---|---|---:|---:|---:|---|
| 2026-01 | series | 0 | 1.000000 | 0.000000 | unfitted |
| 2026-02 | series | 21 | 1.000000 | 0.000000 | unfitted |
| 2026-02 | map | 0 | 1.000000 | 0.000000 | unfitted |
| 2026-03 | series | 72 | 1.000000 | 0.000000 | unfitted |
| 2026-03 | map | 48 | 1.000000 | 0.000000 | unfitted |
| 2026-04 | series | 136 | 1.315300 | 0.836933 | fitted |
| 2026-04 | map | 104 | 1.462638 | 0.457650 | fitted |
| 2026-05 | series | 357 | 1.075859 | 0.673803 | fitted |
| 2026-05 | map | 456 | 1.012439 | 0.835572 | fitted |
| 2026-06 | series | 556 | 1.032380 | 0.670412 | fitted |
| 2026-06 | map | 833 | 0.879213 | 0.712852 | fitted |

#### Log loss vs Kalshi (blended)

| Kind | Slice | Rows | Model log loss | Kalshi log loss | Difference [95% interval] | Significant |
|---|---|---:|---:|---:|---|---|
| series | all | 541 | 0.621424 | 0.634347 | -0.012923 [-0.030669, 0.005382] | no |
| series | vct | 201 | 0.634379 | 0.644147 | -0.009768 [-0.033004, 0.013564] | no |
| series | vcl | 291 | 0.603631 | 0.621829 | -0.018198 [-0.045130, 0.012831] | no |
| series | gc | 0 | — | — | — | — |
| series | t3 | 0 | — | — | — | — |
| series | collegiate | 0 | — | — | — | — |
| series | offseason | 49 | 0.673946 | 0.668490 | 0.005456 [-0.032610, 0.039571] | no |
| series | international=1 | 24 | 0.653013 | 0.682705 | -0.029693 [-0.074593, 0.017583] | no |
| series | international=0 | 517 | 0.619957 | 0.632102 | -0.012145 [-0.029410, 0.006700] | no |
| map | all | 945 | 0.673893 | 0.673192 | 0.000701 [-0.010454, 0.012084] | no |
| map | vct | 392 | 0.666061 | 0.667249 | -0.001189 [-0.016140, 0.013245] | no |
| map | vcl | 456 | 0.678145 | 0.676303 | 0.001842 [-0.015635, 0.019580] | no |
| map | gc | 0 | — | — | — | — |
| map | t3 | 0 | — | — | — | — |
| map | collegiate | 0 | — | — | — | — |
| map | offseason | 97 | 0.685560 | 0.682581 | 0.002979 [-0.025513, 0.031786] | no |
| map | international=1 | 50 | 0.661782 | 0.651359 | 0.010424 [-0.015227, 0.036364] | no |
| map | international=0 | 895 | 0.674570 | 0.674412 | 0.000158 [-0.011495, 0.011041] | no |

#### Full-Kelly returns (blended)

| Kind | Slice | Bets | Matches | Mean edge | Flat ROI [95% interval] | Kelly, LoL caps ($50 start) | Multiple | Max drawdown | Largest stake | Bets filled | Flat ROI depth-capped [95% interval] | Kelly depth-capped final |
|---|---|---:|---:|---:|---|---:|---:|---:|---:|---:|---|---:|
| series | all | 327 | 327 | 0.0576 | 18.16% [4.03%, 33.04%] | $2043.39 | 40.868× | 39.66% | $228.71 | 172 (155 unfilled) | 21.44% [2.74%, 41.32%] | $386.49 |
| series | vct | 120 | 120 | 0.0481 | 9.55% [-13.53%, 34.83%] | $114.89 | 2.298× | 42.45% | $9.10 | 69 (51 unfilled) | 23.85% [-5.33%, 56.29%] | $153.44 |
| series | vcl | 186 | 186 | 0.0655 | 24.82% [5.80%, 45.20%] | $777.38 | 15.548× | 30.34% | $86.22 | 87 (99 unfilled) | 27.45% [1.23%, 57.10%] | $175.20 |
| series | gc | 0 | 0 | — | — | $50.00 | 1.000× | 0.00% | $0.00 | 0 (0 unfilled) | — | $50.00 |
| series | t3 | 0 | 0 | — | — | $50.00 | 1.000× | 0.00% | $0.00 | 0 (0 unfilled) | — | $50.00 |
| series | collegiate | 0 | 0 | — | — | $50.00 | 1.000× | 0.00% | $0.00 | 0 (0 unfilled) | — | $50.00 |
| series | offseason | 21 | 21 | 0.0429 | 8.50% [-44.07%, 61.52%] | $58.70 | 1.174× | 17.46% | $5.59 | 16 (5 unfilled) | -21.46% [-72.15%, 32.42%] | $39.74 |
| series | international=1 | 13 | 13 | 0.0372 | 43.17% [-30.36%, 128.15%] | $70.98 | 1.420× | 12.68% | $5.60 | 13 (0 unfilled) | 43.17% [-30.36%, 128.15%] | $70.98 |
| series | international=0 | 314 | 314 | 0.0585 | 17.12% [2.71%, 32.91%] | $1578.71 | 31.574× | 39.66% | $175.09 | 159 (155 unfilled) | 19.66% [0.46%, 40.41%] | $259.09 |
| map | all | 543 | 288 | 0.0429 | 14.33% [-2.51%, 37.50%] | $52.42 | 1.048× | 61.82% | $9.00 | 65 (478 unfilled) | 59.64% [4.39%, 147.26%] | $61.23 |
| map | vct | 213 | 110 | 0.0419 | -1.33% [-13.85%, 11.53%] | $41.92 | 0.838× | 53.53% | $5.30 | 27 (186 unfilled) | 37.46% [3.22%, 74.66%] | $71.96 |
| map | vcl | 285 | 154 | 0.0449 | 27.50% [-3.09%, 68.49%] | $53.84 | 1.077× | 59.53% | $10.58 | 34 (251 unfilled) | 72.83% [-26.64%, 217.17%] | $39.05 |
| map | gc | 0 | 0 | — | — | $50.00 | 1.000× | 0.00% | $0.00 | 0 (0 unfilled) | — | $50.00 |
| map | t3 | 0 | 0 | — | — | $50.00 | 1.000× | 0.00% | $0.00 | 0 (0 unfilled) | — | $50.00 |
| map | collegiate | 0 | 0 | — | — | $50.00 | 1.000× | 0.00% | $0.00 | 0 (0 unfilled) | — | $50.00 |
| map | offseason | 45 | 24 | 0.0350 | 4.87% [-25.42%, 36.22%] | $52.93 | 1.059× | 13.29% | $4.21 | 4 (41 unfilled) | 95.88% [13.38%, 262.84%] | $54.30 |
| map | international=1 | 28 | 13 | 0.0344 | -8.99% [-42.54%, 26.09%] | $41.83 | 0.837× | 16.33% | $2.37 | 8 (20 unfilled) | 9.16% [-36.34%, 63.48%] | $50.74 |
| map | international=0 | 515 | 275 | 0.0434 | 15.60% [-2.66%, 37.79%] | $62.73 | 1.255× | 54.31% | $10.76 | 57 (458 unfilled) | 66.72% [4.05%, 152.54%] | $60.25 |
| series+map | all | 870 | 384 | 0.0485 | 15.77% [2.31%, 31.96%] | $861.33 | 17.227× | 50.01% | $105.20 | 237 (633 unfilled) | 31.89% [10.75%, 57.77%] | $268.30 |

#### Monthly breakdown

All metrics use identical linked rows within each kind/month. Unfitted blend months show —; counts include all rows.

| Kind | Month | Rows | Model log loss | Blended log loss | Kalshi log loss | Raw flat ROI (bets), unlimited Kelly final | Blended flat ROI (bets), unlimited Kelly final | Raw bets filled | Raw Flat ROI depth-capped [95% interval] | Raw Kelly depth-capped final | Blended bets filled | Blended Flat ROI depth-capped [95% interval] | Blended Kelly depth-capped final |
|---|---|---:|---:|---:|---:|---|---|---:|---|---:|---:|---|---:|
| map | 2026-02 | 48 | 0.703306 | — | 0.690786 | -8.46% (35), $40.05 | — | 11 (24 unfilled) | -19.43% [-100.00%, 38.35%] | $45.24 | — | — | — |
| map | 2026-03 | 56 | 0.584067 | — | 0.565065 | -2.21% (42), $47.10 | — | 12 (30 unfilled) | 10.20% [-37.83%, 54.20%] | $53.95 | — | — | — |
| map | 2026-04 | 352 | 0.636775 | 0.681852 | 0.690793 | 57.47% (255), $5794.88 | 37.15% (220), $58.89 | 29 (226 unfilled) | 170.92% [-4.61%, 416.98%] | $233.41 | 23 (197 unfilled) | 136.25% [2.56%, 341.45%] | $60.19 |
| map | 2026-05 | 377 | 0.686359 | 0.684532 | 0.687018 | 5.52% (236), $93.96 | 5.69% (199), $103.72 | 30 (206 unfilled) | 25.77% [-14.90%, 70.29%] | $68.44 | 25 (174 unfilled) | 38.58% [-7.04%, 91.60%] | $65.13 |
| map | 2026-06 | 216 | 0.650047 | 0.642354 | 0.620377 | -12.42% (136), $19.53 | -11.86% (124), $21.25 | 22 (114 unfilled) | -18.50% [-52.34%, 17.32%] | $36.03 | 17 (107 unfilled) | -11.75% [-54.05%, 36.07%] | $39.06 |
| series | 2026-01 | 21 | 0.630380 | — | 0.661069 | 23.78% (18), $57.41 | — | 10 (8 unfilled) | 1.19% [-65.23%, 69.94%] | $44.76 | — | — | — |
| series | 2026-02 | 51 | 0.644799 | — | 0.694525 | 29.11% (38), $101.10 | — | 27 (11 unfilled) | 43.57% [-15.63%, 113.51%] | $100.49 | — | — | — |
| series | 2026-03 | 64 | 0.588521 | — | 0.565917 | -3.95% (49), $36.12 | — | 36 (13 unfilled) | 4.45% [-27.20%, 37.18%] | $47.17 | — | — | — |
| series | 2026-04 | 221 | 0.614712 | 0.614041 | 0.627690 | 13.68% (160), $295.53 | 17.08% (151), $319.86 | 66 (94 unfilled) | 51.26% [8.01%, 95.79%] | $323.56 | 65 (86 unfilled) | 32.70% [0.19%, 66.63%] | $164.96 |
| series | 2026-05 | 199 | 0.649850 | 0.648689 | 0.663719 | 8.62% (138), $107.55 | 21.76% (106), $189.62 | 91 (47 unfilled) | -1.96% [-25.71%, 23.19%] | $44.12 | 68 (38 unfilled) | 7.76% [-21.34%, 38.17%] | $62.78 |
| series | 2026-06 | 121 | 0.599741 | 0.590065 | 0.598199 | 0.26% (87), $90.82 | 15.04% (70), $91.23 | 48 (39 unfilled) | 16.94% [-17.14%, 53.00%] | $149.16 | 39 (31 unfilled) | 26.62% [-13.03%, 67.66%] | $103.39 |

### player_round_glicko_rookie+regional: Kalshi comparison and returns

regional: rows=1069, ridge=4, s=0.886184, effects: Americas=0.0959955, EMEA=-0.0333152, Pacific=0.0359274, China=-0.0986076

#### Log loss vs Kalshi

| Kind | Slice | Rows | Model log loss | Kalshi log loss | Difference [95% interval] | Significant |
|---|---|---:|---:|---:|---|---|
| series | all | 677 | 0.623221 | 0.633240 | -0.010019 [-0.032517, 0.012464] | no |
| series | vct | 278 | 0.624562 | 0.634755 | -0.010193 [-0.040328, 0.018412] | no |
| series | vcl | 340 | 0.611548 | 0.619968 | -0.008420 [-0.047124, 0.030337] | no |
| series | gc | 0 | — | — | — | — |
| series | t3 | 0 | — | — | — | — |
| series | collegiate | 0 | — | — | — | — |
| series | offseason | 59 | 0.684167 | 0.702587 | -0.018420 [-0.076766, 0.036899] | no |
| series | international=1 | 41 | 0.617464 | 0.653397 | -0.035932 [-0.083595, 0.013321] | no |
| series | international=0 | 636 | 0.623592 | 0.631941 | -0.008349 [-0.033261, 0.015582] | no |
| map | all | 1049 | 0.657770 | 0.668225 | -0.010455 [-0.032139, 0.008049] | no |
| map | vct | 461 | 0.659615 | 0.665762 | -0.006147 [-0.026490, 0.012064] | no |
| map | vcl | 490 | 0.650736 | 0.668365 | -0.017628 [-0.060518, 0.017599] | no |
| map | gc | 0 | — | — | — | — |
| map | t3 | 0 | — | — | — | — |
| map | collegiate | 0 | — | — | — | — |
| map | offseason | 98 | 0.684259 | 0.679111 | 0.005148 [-0.025952, 0.036273] | no |
| map | international=1 | 59 | 0.663266 | 0.649653 | 0.013613 [-0.020365, 0.051181] | no |
| map | international=0 | 990 | 0.657442 | 0.669332 | -0.011889 [-0.034000, 0.008239] | no |

#### Full-Kelly returns

| Kind | Slice | Bets | Matches | Mean edge | Flat ROI [95% interval] | Kelly, LoL caps ($50 start) | Multiple | Max drawdown | Largest stake | Bets filled | Flat ROI depth-capped [95% interval] | Kelly depth-capped final |
|---|---|---:|---:|---:|---|---:|---:|---:|---:|---:|---|---:|
| series | all | 504 | 504 | 0.0899 | 10.64% [-1.39%, 22.74%] | $1060.65 | 21.213× | 83.02% | $163.67 | 289 (215 unfilled) | 19.31% [3.30%, 36.22%] | $780.09 |
| series | vct | 204 | 204 | 0.0754 | 4.71% [-12.88%, 24.37%] | $45.91 | 0.918× | 76.99% | $6.01 | 128 (76 unfilled) | 18.33% [-5.40%, 45.51%] | $204.27 |
| series | vcl | 257 | 257 | 0.1053 | 15.61% [-0.78%, 33.60%] | $548.68 | 10.974× | 63.96% | $117.39 | 128 (129 unfilled) | 24.11% [-1.43%, 52.09%] | $244.27 |
| series | gc | 0 | 0 | — | — | $50.00 | 1.000× | 0.00% | $0.00 | 0 (0 unfilled) | — | $50.00 |
| series | t3 | 0 | 0 | — | — | $50.00 | 1.000× | 0.00% | $0.00 | 0 (0 unfilled) | — | $50.00 |
| series | collegiate | 0 | 0 | — | — | $50.00 | 1.000× | 0.00% | $0.00 | 0 (0 unfilled) | — | $50.00 |
| series | offseason | 43 | 43 | 0.0666 | 9.05% [-27.85%, 47.26%] | $73.89 | 1.478× | 40.31% | $9.17 | 33 (10 unfilled) | 4.53% [-35.70%, 46.97%] | $57.56 |
| series | international=1 | 31 | 31 | 0.0482 | 17.62% [-22.72%, 60.01%] | $78.69 | 1.574× | 20.90% | $6.27 | 31 (0 unfilled) | 17.62% [-22.72%, 60.01%] | $82.74 |
| series | international=0 | 473 | 473 | 0.0926 | 10.18% [-2.03%, 23.38%] | $538.95 | 10.779× | 83.02% | $105.10 | 258 (215 unfilled) | 19.51% [2.14%, 37.10%] | $486.98 |
| map | all | 680 | 364 | 0.0691 | 19.65% [1.89%, 40.38%] | $7163.79 | 143.276× | 29.59% | $245.53 | 102 (578 unfilled) | 57.56% [2.11%, 125.23%] | $249.12 |
| map | vct | 290 | 151 | 0.0561 | 9.24% [-7.83%, 33.04%] | $169.77 | 3.395× | 40.94% | $22.17 | 59 (231 unfilled) | 48.90% [-10.41%, 153.72%] | $109.13 |
| map | vcl | 336 | 186 | 0.0847 | 31.30% [3.15%, 67.76%] | $1447.32 | 28.946× | 59.77% | $245.53 | 39 (297 unfilled) | 66.60% [-23.57%, 198.57%] | $140.02 |
| map | gc | 0 | 0 | — | — | $50.00 | 1.000× | 0.00% | $0.00 | 0 (0 unfilled) | — | $50.00 |
| map | t3 | 0 | 0 | — | — | $50.00 | 1.000× | 0.00% | $0.00 | 0 (0 unfilled) | — | $50.00 |
| map | collegiate | 0 | 0 | — | — | $50.00 | 1.000× | 0.00% | $0.00 | 0 (0 unfilled) | — | $50.00 |
| map | offseason | 54 | 27 | 0.0416 | 2.86% [-27.55%, 33.38%] | $54.82 | 1.096× | 18.51% | $3.98 | 4 (50 unfilled) | 95.88% [13.38%, 262.84%] | $58.92 |
| map | international=1 | 38 | 21 | 0.0466 | -7.79% [-35.38%, 19.06%] | $40.51 | 0.810× | 24.05% | $4.86 | 17 (21 unfilled) | 19.16% [-13.28%, 53.72%] | $55.11 |
| map | international=0 | 642 | 343 | 0.0704 | 21.27% [3.62%, 42.31%] | $7148.02 | 142.960× | 33.66% | $245.53 | 85 (557 unfilled) | 65.17% [0.95%, 150.71%] | $239.87 |
| series+map | all | 1184 | 538 | 0.0780 | 15.81% [3.68%, 29.45%] | $4120.80 | 82.416× | 46.64% | $247.91 | 391 (793 unfilled) | 29.29% [9.21%, 51.38%] | $479.29 |

#### Monthly market blend fits

UTC monthly fits use earlier rows of the same kind from 2025-09-01, excluding holdout; minimum 100 rows. logit(p_blend) = a·logit(mid) + b·(logit(p_model) − logit(mid)); inputs clipped to [0.01, 0.99], no intercept, ridge 1e-6. Unfitted rows use mid unchanged; excluded from blended tables: 240 rows. Rating parameters remain selected on the tuning window.

| Month | Kind | n | a | b | Status |
|---|---|---:|---:|---:|---|
| 2026-01 | series | 0 | 1.000000 | 0.000000 | unfitted |
| 2026-02 | series | 21 | 1.000000 | 0.000000 | unfitted |
| 2026-02 | map | 0 | 1.000000 | 0.000000 | unfitted |
| 2026-03 | series | 72 | 1.000000 | 0.000000 | unfitted |
| 2026-03 | map | 48 | 1.000000 | 0.000000 | unfitted |
| 2026-04 | series | 136 | 1.269244 | 0.774284 | fitted |
| 2026-04 | map | 104 | 1.475157 | 0.426116 | fitted |
| 2026-05 | series | 357 | 1.066051 | 0.669604 | fitted |
| 2026-05 | map | 456 | 1.053916 | 0.870997 | fitted |
| 2026-06 | series | 556 | 1.011582 | 0.640910 | fitted |
| 2026-06 | map | 833 | 0.915080 | 0.741665 | fitted |

#### Log loss vs Kalshi (blended)

| Kind | Slice | Rows | Model log loss | Kalshi log loss | Difference [95% interval] | Significant |
|---|---|---:|---:|---:|---|---|
| series | all | 541 | 0.620574 | 0.634347 | -0.013773 [-0.030694, 0.003777] | no |
| series | vct | 201 | 0.633482 | 0.644147 | -0.010664 [-0.033364, 0.011738] | no |
| series | vcl | 291 | 0.601839 | 0.621829 | -0.019989 [-0.045181, 0.008528] | no |
| series | gc | 0 | — | — | — | — |
| series | t3 | 0 | — | — | — | — |
| series | collegiate | 0 | — | — | — | — |
| series | offseason | 49 | 0.678882 | 0.668490 | 0.010392 [-0.028027, 0.045101] | no |
| series | international=1 | 24 | 0.657976 | 0.682705 | -0.024730 [-0.068865, 0.022587] | no |
| series | international=0 | 517 | 0.618838 | 0.632102 | -0.013264 [-0.029656, 0.004365] | no |
| map | all | 945 | 0.675530 | 0.673192 | 0.002338 [-0.008202, 0.013307] | no |
| map | vct | 392 | 0.666454 | 0.667249 | -0.000795 [-0.015247, 0.013234] | no |
| map | vcl | 456 | 0.680804 | 0.676303 | 0.004501 [-0.011767, 0.020909] | no |
| map | gc | 0 | — | — | — | — |
| map | t3 | 0 | — | — | — | — |
| map | collegiate | 0 | — | — | — | — |
| map | offseason | 97 | 0.687413 | 0.682581 | 0.004832 [-0.023611, 0.033735] | no |
| map | international=1 | 50 | 0.663375 | 0.651359 | 0.012016 [-0.015904, 0.040430] | no |
| map | international=0 | 895 | 0.676209 | 0.674412 | 0.001797 [-0.009321, 0.012202] | no |

#### Full-Kelly returns (blended)

| Kind | Slice | Bets | Matches | Mean edge | Flat ROI [95% interval] | Kelly, LoL caps ($50 start) | Multiple | Max drawdown | Largest stake | Bets filled | Flat ROI depth-capped [95% interval] | Kelly depth-capped final |
|---|---|---:|---:|---:|---|---:|---:|---:|---:|---:|---|---:|
| series | all | 333 | 333 | 0.0545 | 16.66% [2.10%, 31.23%] | $996.32 | 19.926× | 42.73% | $131.29 | 177 (156 unfilled) | 18.85% [0.68%, 38.10%] | $289.05 |
| series | vct | 126 | 126 | 0.0439 | 7.59% [-14.57%, 31.47%] | $97.72 | 1.954× | 34.01% | $8.95 | 73 (53 unfilled) | 20.72% [-7.84%, 50.64%] | $141.04 |
| series | vcl | 183 | 183 | 0.0638 | 25.77% [6.09%, 45.53%] | $498.24 | 9.965× | 40.16% | $65.65 | 86 (97 unfilled) | 27.56% [1.59%, 57.56%] | $151.50 |
| series | gc | 0 | 0 | — | — | $50.00 | 1.000× | 0.00% | $0.00 | 0 (0 unfilled) | — | $50.00 |
| series | t3 | 0 | 0 | — | — | $50.00 | 1.000× | 0.00% | $0.00 | 0 (0 unfilled) | — | $50.00 |
| series | collegiate | 0 | 0 | — | — | $50.00 | 1.000× | 0.00% | $0.00 | 0 (0 unfilled) | — | $50.00 |
| series | offseason | 24 | 24 | 0.0398 | -5.06% [-52.08%, 45.92%] | $52.85 | 1.057× | 20.04% | $5.10 | 18 (6 unfilled) | -30.23% [-75.94%, 18.63%] | $36.88 |
| series | international=1 | 15 | 15 | 0.0336 | 23.85% [-41.92%, 98.14%] | $64.01 | 1.280× | 12.96% | $5.09 | 15 (0 unfilled) | 23.85% [-41.92%, 98.14%] | $64.01 |
| series | international=0 | 318 | 318 | 0.0555 | 16.32% [2.34%, 31.17%] | $780.86 | 15.617× | 42.73% | $102.90 | 162 (156 unfilled) | 18.39% [-1.76%, 38.36%] | $214.64 |
| map | all | 522 | 276 | 0.0414 | 1.82% [-8.81%, 14.61%] | $23.87 | 0.477× | 73.86% | $7.76 | 69 (453 unfilled) | 10.07% [-12.35%, 33.35%] | $54.12 |
| map | vct | 208 | 107 | 0.0404 | -4.36% [-16.26%, 9.48%] | $37.87 | 0.757× | 46.30% | $5.46 | 32 (176 unfilled) | 20.61% [-13.17%, 55.81%] | $66.51 |
| map | vcl | 269 | 146 | 0.0431 | 6.43% [-11.30%, 30.42%] | $26.51 | 0.530× | 69.16% | $7.65 | 32 (237 unfilled) | -12.33% [-40.72%, 16.12%] | $36.98 |
| map | gc | 0 | 0 | — | — | $50.00 | 1.000× | 0.00% | $0.00 | 0 (0 unfilled) | — | $50.00 |
| map | t3 | 0 | 0 | — | — | $50.00 | 1.000× | 0.00% | $0.00 | 0 (0 unfilled) | — | $50.00 |
| map | collegiate | 0 | 0 | — | — | $50.00 | 1.000× | 0.00% | $0.00 | 0 (0 unfilled) | — | $50.00 |
| map | offseason | 45 | 23 | 0.0361 | 2.71% [-28.59%, 34.84%] | $53.90 | 1.078× | 12.73% | $4.18 | 5 (40 unfilled) | 85.42% [23.05%, 209.00%] | $54.89 |
| map | international=1 | 28 | 13 | 0.0362 | -17.31% [-48.85%, 12.57%] | $37.65 | 0.753× | 24.70% | $2.25 | 10 (18 unfilled) | 2.53% [-38.68%, 45.73%] | $50.31 |
| map | international=0 | 494 | 263 | 0.0417 | 2.91% [-8.93%, 15.73%] | $31.73 | 0.635× | 65.25% | $7.76 | 59 (435 unfilled) | 11.35% [-13.16%, 37.56%] | $54.04 |
| series+map | all | 855 | 382 | 0.0465 | 7.61% [-2.81%, 19.30%] | $246.87 | 4.937× | 54.13% | $39.13 | 246 (609 unfilled) | 16.40% [0.96%, 32.82%] | $196.56 |

#### Monthly breakdown

All metrics use identical linked rows within each kind/month. Unfitted blend months show —; counts include all rows.

| Kind | Month | Rows | Model log loss | Blended log loss | Kalshi log loss | Raw flat ROI (bets), unlimited Kelly final | Blended flat ROI (bets), unlimited Kelly final | Raw bets filled | Raw Flat ROI depth-capped [95% interval] | Raw Kelly depth-capped final | Blended bets filled | Blended Flat ROI depth-capped [95% interval] | Blended Kelly depth-capped final |
|---|---|---:|---:|---:|---:|---|---|---:|---|---:|---:|---|---:|
| map | 2026-02 | 48 | 0.701272 | — | 0.690786 | 0.54% (36), $44.66 | — | 12 (24 unfilled) | 1.41% [-66.85%, 52.25%] | $48.88 | — | — | — |
| map | 2026-03 | 56 | 0.592550 | — | 0.565065 | -9.20% (40), $44.03 | — | 12 (28 unfilled) | 10.11% [-40.05%, 52.87%] | $54.96 | — | — | — |
| map | 2026-04 | 352 | 0.637791 | 0.686349 | 0.690793 | 57.28% (247), $7677.91 | 8.68% (208), $49.16 | 29 (218 unfilled) | 170.74% [5.32%, 407.56%] | $232.37 | 23 (185 unfilled) | 9.16% [-11.56%, 28.42%] | $54.76 |
| map | 2026-05 | 377 | 0.684945 | 0.684367 | 0.687018 | 7.02% (216), $77.67 | 5.50% (190), $77.99 | 26 (190 unfilled) | 29.69% [-16.99%, 85.45%] | $65.27 | 27 (163 unfilled) | 27.10% [-18.00%, 76.89%] | $62.13 |
| map | 2026-06 | 216 | 0.650139 | 0.642475 | 0.620377 | -13.83% (141), $15.60 | -15.15% (124), $15.41 | 23 (118 unfilled) | -0.93% [-37.39%, 34.97%] | $41.20 | 19 (105 unfilled) | -13.05% [-49.10%, 27.54%] | $40.01 |
| series | 2026-01 | 21 | 0.635683 | — | 0.661069 | 26.04% (19), $53.59 | — | 11 (8 unfilled) | 7.12% [-53.39%, 68.22%] | $44.08 | — | — | — |
| series | 2026-02 | 51 | 0.649820 | — | 0.694525 | 33.17% (41), $104.26 | — | 30 (11 unfilled) | 47.70% [-5.62%, 110.22%] | $104.30 | — | — | — |
| series | 2026-03 | 64 | 0.589992 | — | 0.565917 | -6.89% (52), $41.21 | — | 40 (12 unfilled) | -2.63% [-32.22%, 28.98%] | $51.83 | — | — | — |
| series | 2026-04 | 221 | 0.611924 | 0.610186 | 0.627690 | 14.75% (166), $221.30 | 19.35% (149), $279.66 | 68 (98 unfilled) | 53.35% [13.27%, 100.55%] | $294.14 | 62 (87 unfilled) | 36.67% [4.03%, 71.94%] | $165.68 |
| series | 2026-05 | 199 | 0.653944 | 0.651201 | 0.663719 | 8.97% (139), $72.98 | 15.89% (114), $126.22 | 93 (46 unfilled) | -2.15% [-25.53%, 23.62%] | $44.33 | 74 (40 unfilled) | 3.14% [-23.54%, 31.97%] | $54.80 |
| series | 2026-06 | 121 | 0.597527 | 0.589177 | 0.598199 | 1.90% (87), $69.15 | 12.24% (70), $69.79 | 47 (40 unfilled) | 15.76% [-19.18%, 49.35%] | $117.56 | 41 (29 unfilled) | 20.36% [-16.84%, 59.20%] | $80.94 |

### player_round_glicko_rookie+regional_form: Kalshi comparison and returns

regional_form: regional: rows=1069, ridge=4, s=0.886184, effects: Americas=0.0959955, EMEA=-0.0333152, Pacific=0.0359274, China=-0.0986076; form: rows=25380, H=80, w=1.3369

#### Log loss vs Kalshi

| Kind | Slice | Rows | Model log loss | Kalshi log loss | Difference [95% interval] | Significant |
|---|---|---:|---:|---:|---|---|
| series | all | 677 | 0.622623 | 0.633240 | -0.010617 [-0.033468, 0.012225] | no |
| series | vct | 278 | 0.623867 | 0.634755 | -0.010888 [-0.042074, 0.017935] | no |
| series | vcl | 340 | 0.612501 | 0.619968 | -0.007467 [-0.045911, 0.031476] | no |
| series | gc | 0 | — | — | — | — |
| series | t3 | 0 | — | — | — | — |
| series | collegiate | 0 | — | — | — | — |
| series | offseason | 59 | 0.675095 | 0.702587 | -0.027491 [-0.086631, 0.028554] | no |
| series | international=1 | 41 | 0.613043 | 0.653397 | -0.040354 [-0.088361, 0.007909] | no |
| series | international=0 | 636 | 0.623241 | 0.631941 | -0.008700 [-0.034025, 0.015872] | no |
| map | all | 1049 | 0.657477 | 0.668225 | -0.010748 [-0.033235, 0.008261] | no |
| map | vct | 461 | 0.659981 | 0.665762 | -0.005781 [-0.026512, 0.013164] | no |
| map | vcl | 490 | 0.650092 | 0.668365 | -0.018273 [-0.061166, 0.017756] | no |
| map | gc | 0 | — | — | — | — |
| map | t3 | 0 | — | — | — | — |
| map | collegiate | 0 | — | — | — | — |
| map | offseason | 98 | 0.682627 | 0.679111 | 0.003516 [-0.030299, 0.036215] | no |
| map | international=1 | 59 | 0.660840 | 0.649653 | 0.011188 [-0.026676, 0.052249] | no |
| map | international=0 | 990 | 0.657277 | 0.669332 | -0.012055 [-0.034784, 0.008428] | no |

#### Full-Kelly returns

| Kind | Slice | Bets | Matches | Mean edge | Flat ROI [95% interval] | Kelly, LoL caps ($50 start) | Multiple | Max drawdown | Largest stake | Bets filled | Flat ROI depth-capped [95% interval] | Kelly depth-capped final |
|---|---|---:|---:|---:|---|---:|---:|---:|---:|---:|---|---:|
| series | all | 491 | 491 | 0.0913 | 9.09% [-3.77%, 21.88%] | $1175.86 | 23.517× | 78.20% | $236.60 | 279 (212 unfilled) | 18.24% [1.30%, 36.16%] | $843.81 |
| series | vct | 199 | 199 | 0.0770 | 6.07% [-12.22%, 26.31%] | $52.51 | 1.050× | 72.33% | $5.41 | 124 (75 unfilled) | 20.11% [-4.92%, 46.50%] | $206.10 |
| series | vcl | 253 | 253 | 0.1055 | 12.98% [-4.30%, 31.62%] | $694.94 | 13.899× | 59.48% | $131.24 | 125 (128 unfilled) | 21.96% [-3.30%, 47.94%] | $263.11 |
| series | gc | 0 | 0 | — | — | $50.00 | 1.000× | 0.00% | $0.00 | 0 (0 unfilled) | — | $50.00 |
| series | t3 | 0 | 0 | — | — | $50.00 | 1.000× | 0.00% | $0.00 | 0 (0 unfilled) | — | $50.00 |
| series | collegiate | 0 | 0 | — | — | $50.00 | 1.000× | 0.00% | $0.00 | 0 (0 unfilled) | — | $50.00 |
| series | offseason | 39 | 39 | 0.0719 | -0.66% [-39.45%, 41.58%] | $89.67 | 1.793× | 35.59% | $10.24 | 30 (9 unfilled) | -4.89% [-46.92%, 40.67%] | $59.23 |
| series | international=1 | 29 | 29 | 0.0503 | 22.34% [-20.61%, 73.10%] | $82.93 | 1.659× | 20.46% | $6.60 | 29 (0 unfilled) | 22.34% [-20.61%, 73.10%] | $86.74 |
| series | international=0 | 462 | 462 | 0.0938 | 8.26% [-4.64%, 21.68%] | $1290.61 | 25.812× | 78.20% | $184.98 | 250 (212 unfilled) | 17.77% [0.76%, 36.56%] | $493.75 |
| map | all | 710 | 377 | 0.0710 | 19.70% [3.63%, 38.87%] | $5311.31 | 106.226× | 30.79% | $245.53 | 106 (604 unfilled) | 52.36% [-0.03%, 119.46%] | $256.56 |
| map | vct | 298 | 155 | 0.0595 | 11.68% [-4.82%, 33.40%] | $240.69 | 4.814× | 31.51% | $19.65 | 57 (241 unfilled) | 54.18% [-6.09%, 147.08%] | $126.70 |
| map | vcl | 356 | 195 | 0.0852 | 28.31% [1.03%, 61.78%] | $1609.46 | 32.189× | 60.70% | $245.53 | 44 (312 unfilled) | 46.26% [-30.63%, 157.85%] | $133.31 |
| map | gc | 0 | 0 | — | — | $50.00 | 1.000× | 0.00% | $0.00 | 0 (0 unfilled) | — | $50.00 |
| map | t3 | 0 | 0 | — | — | $50.00 | 1.000× | 0.00% | $0.00 | 0 (0 unfilled) | — | $50.00 |
| map | collegiate | 0 | 0 | — | — | $50.00 | 1.000× | 0.00% | $0.00 | 0 (0 unfilled) | — | $50.00 |
| map | offseason | 56 | 27 | 0.0414 | 7.49% [-22.56%, 36.85%] | $57.95 | 1.159× | 15.47% | $3.95 | 5 (51 unfilled) | 85.42% [23.05%, 209.00%] | $56.50 |
| map | international=1 | 41 | 22 | 0.0490 | -0.88% [-26.69%, 25.82%] | $47.80 | 0.956× | 16.20% | $5.04 | 16 (25 unfilled) | 26.72% [-4.48%, 60.92%] | $58.34 |
| map | international=0 | 669 | 355 | 0.0723 | 20.96% [4.10%, 40.70%] | $5375.57 | 107.511× | 31.29% | $245.53 | 90 (579 unfilled) | 56.88% [-4.11%, 138.84%] | $235.09 |
| series+map | all | 1201 | 548 | 0.0793 | 15.35% [3.71%, 28.91%] | $4394.43 | 87.889× | 51.28% | $247.91 | 385 (816 unfilled) | 27.63% [7.66%, 49.24%] | $475.19 |

#### Monthly market blend fits

UTC monthly fits use earlier rows of the same kind from 2025-09-01, excluding holdout; minimum 100 rows. logit(p_blend) = a·logit(mid) + b·(logit(p_model) − logit(mid)); inputs clipped to [0.01, 0.99], no intercept, ridge 1e-6. Unfitted rows use mid unchanged; excluded from blended tables: 240 rows. Rating parameters remain selected on the tuning window.

| Month | Kind | n | a | b | Status |
|---|---|---:|---:|---:|---|
| 2026-01 | series | 0 | 1.000000 | 0.000000 | unfitted |
| 2026-02 | series | 21 | 1.000000 | 0.000000 | unfitted |
| 2026-02 | map | 0 | 1.000000 | 0.000000 | unfitted |
| 2026-03 | series | 72 | 1.000000 | 0.000000 | unfitted |
| 2026-03 | map | 48 | 1.000000 | 0.000000 | unfitted |
| 2026-04 | series | 136 | 1.313639 | 0.838732 | fitted |
| 2026-04 | map | 104 | 1.477320 | 0.496567 | fitted |
| 2026-05 | series | 357 | 1.075564 | 0.673437 | fitted |
| 2026-05 | map | 456 | 1.015335 | 0.838479 | fitted |
| 2026-06 | series | 556 | 1.032178 | 0.670252 | fitted |
| 2026-06 | map | 833 | 0.880664 | 0.714249 | fitted |

#### Log loss vs Kalshi (blended)

| Kind | Slice | Rows | Model log loss | Kalshi log loss | Difference [95% interval] | Significant |
|---|---|---:|---:|---:|---|---|
| series | all | 541 | 0.621447 | 0.634347 | -0.012900 [-0.030681, 0.005304] | no |
| series | vct | 201 | 0.634498 | 0.644147 | -0.009649 [-0.032896, 0.013499] | no |
| series | vcl | 291 | 0.603597 | 0.621829 | -0.018232 [-0.045305, 0.012838] | no |
| series | gc | 0 | — | — | — | — |
| series | t3 | 0 | — | — | — | — |
| series | collegiate | 0 | — | — | — | — |
| series | offseason | 49 | 0.673920 | 0.668490 | 0.005430 [-0.032656, 0.039527] | no |
| series | international=1 | 24 | 0.652393 | 0.682705 | -0.030313 [-0.076320, 0.018861] | no |
| series | international=0 | 517 | 0.620011 | 0.632102 | -0.012091 [-0.029457, 0.006805] | no |
| map | all | 945 | 0.673220 | 0.673192 | 0.000028 [-0.011599, 0.011745] | no |
| map | vct | 392 | 0.666054 | 0.667249 | -0.001195 [-0.016249, 0.013565] | no |
| map | vcl | 456 | 0.676745 | 0.676303 | 0.000442 [-0.018002, 0.019119] | no |
| map | gc | 0 | — | — | — | — |
| map | t3 | 0 | — | — | — | — |
| map | collegiate | 0 | — | — | — | — |
| map | offseason | 97 | 0.685609 | 0.682581 | 0.003028 [-0.025605, 0.031884] | no |
| map | international=1 | 50 | 0.660676 | 0.651359 | 0.009318 [-0.020248, 0.038923] | no |
| map | international=0 | 895 | 0.673921 | 0.674412 | -0.000491 [-0.012652, 0.010783] | no |

#### Full-Kelly returns (blended)

| Kind | Slice | Bets | Matches | Mean edge | Flat ROI [95% interval] | Kelly, LoL caps ($50 start) | Multiple | Max drawdown | Largest stake | Bets filled | Flat ROI depth-capped [95% interval] | Kelly depth-capped final |
|---|---|---:|---:|---:|---|---:|---:|---:|---:|---:|---|---:|
| series | all | 329 | 329 | 0.0575 | 18.06% [3.84%, 33.21%] | $1977.83 | 39.557× | 39.76% | $219.22 | 174 (155 unfilled) | 21.21% [3.03%, 40.88%] | $361.77 |
| series | vct | 122 | 122 | 0.0477 | 9.40% [-13.23%, 35.21%] | $106.43 | 2.129× | 42.38% | $9.08 | 71 (51 unfilled) | 23.20% [-6.45%, 55.74%] | $143.31 |
| series | vcl | 186 | 186 | 0.0656 | 24.82% [5.80%, 45.20%] | $786.60 | 15.732× | 30.31% | $87.20 | 87 (99 unfilled) | 27.45% [1.23%, 57.10%] | $176.96 |
| series | gc | 0 | 0 | — | — | $50.00 | 1.000× | 0.00% | $0.00 | 0 (0 unfilled) | — | $50.00 |
| series | t3 | 0 | 0 | — | — | $50.00 | 1.000× | 0.00% | $0.00 | 0 (0 unfilled) | — | $50.00 |
| series | collegiate | 0 | 0 | — | — | $50.00 | 1.000× | 0.00% | $0.00 | 0 (0 unfilled) | — | $50.00 |
| series | offseason | 21 | 21 | 0.0429 | 8.50% [-44.07%, 61.52%] | $58.72 | 1.174× | 17.45% | $5.59 | 16 (5 unfilled) | -21.46% [-72.15%, 32.42%] | $39.75 |
| series | international=1 | 15 | 15 | 0.0371 | 37.54% [-26.73%, 111.10%] | $65.85 | 1.317× | 11.88% | $5.25 | 15 (0 unfilled) | 37.54% [-26.73%, 111.10%] | $65.85 |
| series | international=0 | 314 | 314 | 0.0585 | 17.12% [2.71%, 32.91%] | $1597.75 | 31.955× | 39.76% | $177.10 | 159 (155 unfilled) | 19.66% [0.46%, 40.41%] | $262.16 |
| map | all | 548 | 289 | 0.0445 | 17.97% [-0.15%, 43.83%] | $71.82 | 1.436× | 65.00% | $12.30 | 68 (480 unfilled) | 90.22% [11.22%, 190.76%] | $77.55 |
| map | vct | 217 | 111 | 0.0436 | 8.67% [-12.64%, 36.90%] | $40.79 | 0.816× | 50.55% | $5.32 | 30 (187 unfilled) | 109.27% [6.05%, 296.14%] | $77.51 |
| map | vcl | 287 | 155 | 0.0464 | 26.62% [-4.04%, 67.54%] | $75.10 | 1.502× | 59.25% | $13.84 | 34 (253 unfilled) | 72.83% [-26.64%, 217.17%] | $45.79 |
| map | gc | 0 | 0 | — | — | $50.00 | 1.000× | 0.00% | $0.00 | 0 (0 unfilled) | — | $50.00 |
| map | t3 | 0 | 0 | — | — | $50.00 | 1.000× | 0.00% | $0.00 | 0 (0 unfilled) | — | $50.00 |
| map | collegiate | 0 | 0 | — | — | $50.00 | 1.000× | 0.00% | $0.00 | 0 (0 unfilled) | — | $50.00 |
| map | offseason | 44 | 23 | 0.0360 | 7.27% [-22.04%, 39.37%] | $52.74 | 1.055× | 13.34% | $4.20 | 4 (40 unfilled) | 95.88% [13.38%, 262.84%] | $54.20 |
| map | international=1 | 30 | 14 | 0.0361 | -9.99% [-43.21%, 19.51%] | $38.05 | 0.761× | 23.91% | $2.24 | 10 (20 unfilled) | 2.53% [-38.68%, 45.73%] | $50.03 |
| map | international=0 | 518 | 275 | 0.0450 | 19.59% [-1.21%, 43.56%] | $94.34 | 1.887× | 54.03% | $16.13 | 58 (460 unfilled) | 105.31% [13.61%, 221.33%] | $77.24 |
| series+map | all | 877 | 387 | 0.0494 | 18.00% [3.23%, 33.98%] | $919.46 | 18.389× | 45.20% | $112.18 | 242 (635 unfilled) | 40.56% [12.93%, 72.56%] | $285.23 |

#### Monthly breakdown

All metrics use identical linked rows within each kind/month. Unfitted blend months show —; counts include all rows.

| Kind | Month | Rows | Model log loss | Blended log loss | Kalshi log loss | Raw flat ROI (bets), unlimited Kelly final | Blended flat ROI (bets), unlimited Kelly final | Raw bets filled | Raw Flat ROI depth-capped [95% interval] | Raw Kelly depth-capped final | Blended bets filled | Blended Flat ROI depth-capped [95% interval] | Blended Kelly depth-capped final |
|---|---|---:|---:|---:|---:|---|---|---:|---|---:|---:|---|---:|
| map | 2026-02 | 48 | 0.703275 | — | 0.690786 | -8.46% (35), $40.05 | — | 11 (24 unfilled) | -19.43% [-100.00%, 38.35%] | $45.25 | — | — | — |
| map | 2026-03 | 56 | 0.581018 | — | 0.565065 | 0.18% (41), $51.35 | — | 11 (30 unfilled) | 20.24% [-28.91%, 64.65%] | $56.35 | — | — | — |
| map | 2026-04 | 352 | 0.637095 | 0.680122 | 0.690793 | 57.57% (254), $5778.94 | 46.82% (222), $88.10 | 29 (225 unfilled) | 170.92% [-4.61%, 416.98%] | $233.42 | 24 (198 unfilled) | 227.12% [16.53%, 515.56%] | $77.37 |
| map | 2026-05 | 377 | 0.686374 | 0.684617 | 0.687018 | 5.52% (236), $94.09 | 5.18% (200), $103.13 | 30 (206 unfilled) | 25.77% [-14.90%, 70.29%] | $68.47 | 25 (175 unfilled) | 38.58% [-7.04%, 91.60%] | $65.02 |
| map | 2026-06 | 216 | 0.649902 | 0.642081 | 0.620377 | -11.41% (144), $19.81 | -12.06% (126), $19.46 | 25 (119 unfilled) | -8.83% [-40.72%, 26.02%] | $38.46 | 19 (107 unfilled) | -13.05% [-49.10%, 27.54%] | $38.55 |
| series | 2026-01 | 21 | 0.630925 | — | 0.661069 | 23.78% (18), $56.93 | — | 10 (8 unfilled) | 1.19% [-65.23%, 69.94%] | $44.76 | — | — | — |
| series | 2026-02 | 51 | 0.643896 | — | 0.694525 | 29.11% (38), $101.12 | — | 27 (11 unfilled) | 43.57% [-15.63%, 113.51%] | $100.51 | — | — | — |
| series | 2026-03 | 64 | 0.588060 | — | 0.565917 | -7.72% (51), $36.53 | — | 38 (13 unfilled) | -1.05% [-31.98%, 32.72%] | $47.78 | — | — | — |
| series | 2026-04 | 221 | 0.615006 | 0.614178 | 0.627690 | 13.68% (160), $292.50 | 17.08% (151), $323.14 | 66 (94 unfilled) | 51.26% [8.01%, 95.79%] | $323.50 | 65 (86 unfilled) | 32.70% [0.19%, 66.63%] | $166.77 |
| series | 2026-05 | 199 | 0.649826 | 0.648670 | 0.663719 | 8.62% (138), $107.74 | 21.76% (106), $189.86 | 91 (47 unfilled) | -1.96% [-25.71%, 23.19%] | $44.09 | 68 (38 unfilled) | 7.76% [-21.34%, 38.17%] | $62.82 |
| series | 2026-06 | 121 | 0.599672 | 0.589954 | 0.598199 | -0.71% (86), $79.68 | 14.65% (72), $84.44 | 47 (39 unfilled) | 15.54% [-17.48%, 53.22%] | $131.93 | 41 (31 unfilled) | 25.37% [-11.35%, 63.50%] | $95.63 |
