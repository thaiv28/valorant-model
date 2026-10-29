# Elo variants benchmark

## Combined summary (validation, all sections)

| Model | Series Δ log loss | Series flat ROI | Series Kelly (LoL caps) $ | Series flat ROI depth-capped | Series Kelly depth-capped $ | Map Δ log loss | Map flat ROI | Map Kelly (LoL caps) $ | Map flat ROI depth-capped | Map Kelly depth-capped $ | Series blended Δ log loss | Series blended flat ROI | Series blended Kelly (LoL caps) $ | Series blended flat ROI depth-capped | Series blended Kelly depth-capped $ | Map blended Δ log loss | Map blended flat ROI | Map blended Kelly (LoL caps) $ | Map blended flat ROI depth-capped | Map blended Kelly depth-capped $ |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| team_elo | 0.026644 | -2.01% | $0.55 | 15.98% | $128.56 | 0.005994 | 12.02% | $480.61 | 52.76% | $203.47 | 0.000161 | -5.01% | $35.62 | 16.91% | $57.12 | 0.011243 | -8.06% | $7.27 | -5.79% | $38.70 |
| player_round_glicko_rookie | -0.010090 | 12.00% | $1320.48 | 21.43% | $853.50 | -0.010355 | 19.44% | $6405.08 | 57.11% | $240.23 | -0.013821 | 17.12% | $1040.06 | 19.75% | $297.46 | 0.003189 | 3.00% | $27.07 | 12.78% | $55.59 |
| player_round_glicko_rookie_tier_revert | -0.009337 | 12.84% | $1331.19 | 21.40% | $809.50 | -0.010796 | 20.01% | $6645.34 | 58.73% | $254.51 | -0.013355 | 16.51% | $837.70 | 16.10% | $291.76 | 0.003717 | 2.26% | $27.59 | 7.74% | $54.56 |
| team_elo+none | 0.026644 | -2.01% | $0.55 | 15.98% | $128.56 | 0.005994 | 12.02% | $480.61 | 52.76% | $203.47 | 0.000161 | -5.01% | $35.62 | 16.91% | $57.12 | 0.011243 | -8.06% | $7.27 | -5.79% | $38.70 |
| player_round_glicko_rookie+none | -0.010090 | 12.00% | $1320.48 | 21.43% | $853.50 | -0.010355 | 19.44% | $6405.08 | 57.11% | $240.23 | -0.013821 | 17.12% | $1040.06 | 19.75% | $297.46 | 0.003189 | 3.00% | $27.07 | 12.78% | $55.59 |
| player_round_glicko_rookie_tier_revert+none | -0.009337 | 12.84% | $1331.19 | 21.40% | $809.50 | -0.010796 | 20.01% | $6645.34 | 58.73% | $254.51 | -0.013355 | 16.51% | $837.70 | 16.10% | $291.76 | 0.003717 | 2.26% | $27.59 | 7.74% | $54.56 |

Series momentum: off.

Series temperatures (stage 1; p′ = σ(T·logit p), T < 1 pulls odds toward 50%): team_elo Bo3 0.70, Bo5 0.62; player_round_glicko_rookie Bo3 0.81, Bo5 0.77; player_round_glicko_rookie_tier_revert Bo3 0.91, Bo5 0.84; team_elo+none Bo3 0.70, Bo5 0.62; player_round_glicko_rookie+none Bo3 0.81, Bo5 0.77; player_round_glicko_rookie_tier_revert+none Bo3 0.91, Bo5 0.84

Parameters minimize tuning map log loss across all sections. Replay predicts before update; Replay starts 2021-01-01. Tuning: [2023-01-01, 2025-09-01); validation: [2025-09-01, 2026-07-01). Holdout is scored only with --holdout and never selects parameters. Series use the first map prediction and an odd best-of map chain (independent when m=0); missing/even best-of or unknown results are skipped. Accuracy gives 0.5 predictions half credit; ECE uses 10 equal-width bins. Log loss clips probabilities at 1e-6. Paired bootstrap uses 2,000 resamples, seed 0, clustered by match_id. Differences are the named model minus its comparator; negative favors the model. Significance requires a 95% percentile interval excluding zero. Tuning scores are selection diagnostics, not independent evidence of improvement.

Fit through 2025-08-31. Unknown host-region map rows: 7261 (including missing/un).

## Stage 1 — tuning (outcomes)

### Leaderboard

| Model | Best params | Map log loss | Series log loss | Rows |
|---|---|---:|---:|---:|
| player_round_glicko_rookie_tier_revert | {"inactive_half_life": 0, "k": 32, "new_player": "teammates", "rd_info": 0.25, "rd_new": 280, "rookie_maps": 400, "rookie_penalty": 200, "season_month": 11, "season_revert": 0.2, "tau": 0.5} | 0.621941 | 0.582554 | 25649 |
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
| tradeable | player_round_glicko_rookie_tier_revert | series | 677 | -0.009337 | -0.013355 | 21.40% | 16.10% |
| tradeable | player_round_glicko_rookie_tier_revert | map | 1049 | -0.010796 | 0.003717 | 58.73% | 7.74% |
| tradeable | team_elo+none | series | 677 | 0.026644 | 0.000161 | 15.98% | 16.91% |
| tradeable | team_elo+none | map | 1049 | 0.005994 | 0.011243 | 52.76% | -5.79% |
| tradeable | player_round_glicko_rookie+none | series | 677 | -0.010090 | -0.013821 | 21.43% | 19.75% |
| tradeable | player_round_glicko_rookie+none | map | 1049 | -0.010355 | 0.003189 | 57.11% | 12.78% |
| tradeable | player_round_glicko_rookie_tier_revert+none | series | 677 | -0.009337 | -0.013355 | 21.40% | 16.10% |
| tradeable | player_round_glicko_rookie_tier_revert+none | map | 1049 | -0.010796 | 0.003717 | 58.73% | 7.74% |
| hours24 | team_elo | series | 375 | 0.037793 | 0.011799 | -8.26% | -39.74% |
| hours24 | team_elo | map | 608 | -0.007035 | 0.004756 | 139.73% | 3.02% |
| hours24 | player_round_glicko_rookie | series | 375 | 0.003343 | 0.001913 | 7.78% | 19.86% |
| hours24 | player_round_glicko_rookie | map | 608 | -0.021420 | 0.000060 | 174.71% | 4.55% |
| hours24 | player_round_glicko_rookie_tier_revert | series | 375 | 0.006331 | 0.002812 | 7.60% | 7.64% |
| hours24 | player_round_glicko_rookie_tier_revert | map | 608 | -0.021267 | -0.000717 | 174.71% | 4.05% |
| hours24 | team_elo+none | series | 375 | 0.037793 | 0.011799 | -8.26% | -39.74% |
| hours24 | team_elo+none | map | 608 | -0.007035 | 0.004756 | 139.73% | 3.02% |
| hours24 | player_round_glicko_rookie+none | series | 375 | 0.003343 | 0.001913 | 7.78% | 19.86% |
| hours24 | player_round_glicko_rookie+none | map | 608 | -0.021420 | 0.000060 | 174.71% | 4.55% |
| hours24 | player_round_glicko_rookie_tier_revert+none | series | 375 | 0.006331 | 0.002812 | 7.60% | 7.64% |
| hours24 | player_round_glicko_rookie_tier_revert+none | map | 608 | -0.021267 | -0.000717 | 174.71% | 4.05% |
| hours6 | team_elo | series | 644 | 0.038723 | 0.005797 | -8.59% | -9.29% |
| hours6 | team_elo | map | 983 | 0.011234 | 0.009681 | 15.59% | 7.92% |
| hours6 | player_round_glicko_rookie | series | 644 | -0.000229 | -0.005932 | 4.57% | 7.94% |
| hours6 | player_round_glicko_rookie | map | 983 | -0.006840 | 0.008854 | 18.54% | 3.34% |
| hours6 | player_round_glicko_rookie_tier_revert | series | 644 | 0.001278 | -0.004457 | 3.30% | 2.33% |
| hours6 | player_round_glicko_rookie_tier_revert | map | 983 | -0.007223 | 0.008525 | 15.02% | 5.35% |
| hours6 | team_elo+none | series | 644 | 0.038723 | 0.005797 | -8.59% | -9.29% |
| hours6 | team_elo+none | map | 983 | 0.011234 | 0.009681 | 15.59% | 7.92% |
| hours6 | player_round_glicko_rookie+none | series | 644 | -0.000229 | -0.005932 | 4.57% | 7.94% |
| hours6 | player_round_glicko_rookie+none | map | 983 | -0.006840 | 0.008854 | 18.54% | 3.34% |
| hours6 | player_round_glicko_rookie_tier_revert+none | series | 644 | 0.001278 | -0.004457 | 3.30% | 2.33% |
| hours6 | player_round_glicko_rookie_tier_revert+none | map | 983 | -0.007223 | 0.008525 | 15.02% | 5.35% |

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

| Model | Section | Rows | Log loss | Brier | Accuracy | ECE |
|---|---|---:|---:|---:|---:|---:|
| player_round_glicko_rookie_tier_revert | all | 25649 | 0.621941 | 0.216932 | 0.645366 | 0.014006 |
| player_round_glicko_rookie_tier_revert | vct | 3333 | 0.660314 | 0.234046 | 0.599160 | 0.008149 |
| player_round_glicko_rookie_tier_revert | vcl | 14263 | 0.624890 | 0.218067 | 0.643834 | 0.013490 |
| player_round_glicko_rookie_tier_revert | gc | 4129 | 0.578285 | 0.198366 | 0.694236 | 0.033087 |
| player_round_glicko_rookie_tier_revert | t3 | 1455 | 0.622763 | 0.216766 | 0.637801 | 0.043748 |
| player_round_glicko_rookie_tier_revert | collegiate | 95 | 0.607913 | 0.211375 | 0.657895 | 0.060784 |
| player_round_glicko_rookie_tier_revert | offseason | 2374 | 0.626343 | 0.218695 | 0.638585 | 0.021806 |
| player_round_glicko_rookie_tier_revert | unknown | 0 | — | — | — | — |
| player_round_glicko_rookie_tier_revert | international=1 | 751 | 0.659290 | 0.233650 | 0.607856 | 0.034980 |
| player_round_glicko_rookie_tier_revert | international=0 | 24898 | 0.620815 | 0.216427 | 0.646498 | 0.014571 |

player_round_glicko_rookie_tier_revert − coin (paired log loss):

| Section | Rows | player_round_glicko_rookie_tier_revert log loss | coin log loss | Difference | 95% interval | Significant |
|---|---:|---:|---:|---:|---|---|
| all | 25649 | 0.621941 | 0.693147 | -0.071206 | [-0.075758, -0.066868] | yes |

player_round_glicko_rookie − team_elo (paired log loss):

| Section | Rows | player_round_glicko_rookie log loss | team_elo log loss | Difference | 95% interval | Significant |
|---|---:|---:|---:|---:|---|---|
| all | 25649 | 0.622668 | 0.651782 | -0.029113 | [-0.032734, -0.025553] | yes |

player_round_glicko_rookie_tier_revert − team_elo (paired log loss):

| Section | Rows | player_round_glicko_rookie_tier_revert log loss | team_elo log loss | Difference | 95% interval | Significant |
|---|---:|---:|---:|---:|---|---|
| all | 25649 | 0.621941 | 0.651782 | -0.029840 | [-0.033182, -0.026520] | yes |

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

| Model | Section | Rows | Log loss | Brier | Accuracy | ECE |
|---|---|---:|---:|---:|---:|---:|
| player_round_glicko_rookie_tier_revert | all | 11288 | 0.582554 | 0.199538 | 0.686083 | 0.017473 |
| player_round_glicko_rookie_tier_revert | vct | 1322 | 0.625876 | 0.218848 | 0.645991 | 0.027340 |
| player_round_glicko_rookie_tier_revert | vcl | 6463 | 0.586340 | 0.201083 | 0.683661 | 0.009880 |
| player_round_glicko_rookie_tier_revert | gc | 1698 | 0.518702 | 0.172837 | 0.747055 | 0.043422 |
| player_round_glicko_rookie_tier_revert | t3 | 650 | 0.593181 | 0.201856 | 0.669231 | 0.062109 |
| player_round_glicko_rookie_tier_revert | collegiate | 42 | 0.631909 | 0.219161 | 0.654762 | 0.097407 |
| player_round_glicko_rookie_tier_revert | offseason | 1113 | 0.598459 | 0.206279 | 0.665768 | 0.028096 |
| player_round_glicko_rookie_tier_revert | unknown | 0 | — | — | — | — |
| player_round_glicko_rookie_tier_revert | international=1 | 310 | 0.633968 | 0.222341 | 0.641935 | 0.037469 |
| player_round_glicko_rookie_tier_revert | international=0 | 10978 | 0.581102 | 0.198895 | 0.687329 | 0.017869 |

player_round_glicko_rookie_tier_revert − coin (paired log loss):

| Section | Rows | player_round_glicko_rookie_tier_revert log loss | coin log loss | Difference | 95% interval | Significant |
|---|---:|---:|---:|---:|---|---|
| all | 11288 | 0.582554 | 0.693147 | -0.110593 | [-0.118455, -0.102513] | yes |

player_round_glicko_rookie − team_elo (paired log loss):

| Section | Rows | player_round_glicko_rookie log loss | team_elo log loss | Difference | 95% interval | Significant |
|---|---:|---:|---:|---:|---|---|
| all | 11288 | 0.584466 | 0.626711 | -0.042245 | [-0.048494, -0.036019] | yes |

player_round_glicko_rookie_tier_revert − team_elo (paired log loss):

| Section | Rows | player_round_glicko_rookie_tier_revert log loss | team_elo log loss | Difference | 95% interval | Significant |
|---|---:|---:|---:|---:|---|---|
| all | 11288 | 0.582554 | 0.626711 | -0.044157 | [-0.050092, -0.038130] | yes |

## Stage 2 — validation (outcomes)

### Leaderboard (frozen stage-1 parameters)

| Model | Best params | Map log loss | Series log loss | Rows |
|---|---|---:|---:|---:|
| player_round_glicko_rookie_tier_revert | {"inactive_half_life": 0, "k": 32, "new_player": "teammates", "rd_info": 0.25, "rd_new": 280, "rookie_maps": 400, "rookie_penalty": 200, "season_month": 11, "season_revert": 0.2, "tau": 0.5} | 0.637176 | 0.604421 | 6337 |
| player_round_glicko_rookie_tier_revert+none | {"inactive_half_life": 0, "k": 32, "new_player": "teammates", "rd_info": 0.25, "rd_new": 280, "rookie_maps": 400, "rookie_penalty": 200, "season_month": 11, "season_revert": 0.2, "tau": 0.5} | 0.637176 | 0.604421 | 6337 |
| player_round_glicko_rookie | {"k": 32, "new_player": "teammates", "rd_info": 0.25, "rd_new": 280, "rookie_maps": 400, "rookie_penalty": 200, "tau": 0.5} | 0.638693 | 0.606622 | 6337 |
| player_round_glicko_rookie+none | {"k": 32, "new_player": "teammates", "rd_info": 0.25, "rd_new": 280, "rookie_maps": 400, "rookie_penalty": 200, "tau": 0.5} | 0.638693 | 0.606622 | 6337 |
| team_elo | {"k": 32} | 0.662947 | 0.643432 | 6337 |
| team_elo+none | {"k": 32} | 0.662947 | 0.643432 | 6337 |

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
| player_round_glicko_rookie_tier_revert | all | 6337 | 0.637176 | 0.223510 | 0.629635 | 0.017829 |
| player_round_glicko_rookie_tier_revert | vct | 1080 | 0.667500 | 0.237597 | 0.584259 | 0.034351 |
| player_round_glicko_rookie_tier_revert | vcl | 3374 | 0.641489 | 0.225150 | 0.628631 | 0.029627 |
| player_round_glicko_rookie_tier_revert | gc | 1005 | 0.596066 | 0.205581 | 0.670647 | 0.034332 |
| player_round_glicko_rookie_tier_revert | t3 | 16 | 0.535758 | 0.184281 | 0.687500 | 0.142031 |
| player_round_glicko_rookie_tier_revert | collegiate | 7 | 0.741900 | 0.274684 | 0.285714 | 0.295353 |
| player_round_glicko_rookie_tier_revert | offseason | 855 | 0.631212 | 0.220637 | 0.644444 | 0.032012 |
| player_round_glicko_rookie_tier_revert | unknown | 0 | — | — | — | — |
| player_round_glicko_rookie_tier_revert | international=1 | 268 | 0.664654 | 0.236293 | 0.608209 | 0.052828 |
| player_round_glicko_rookie_tier_revert | international=0 | 6069 | 0.635962 | 0.222946 | 0.630582 | 0.018708 |

player_round_glicko_rookie_tier_revert − coin (paired log loss):

| Section | Rows | player_round_glicko_rookie_tier_revert log loss | coin log loss | Difference | 95% interval | Significant |
|---|---:|---:|---:|---:|---|---|
| all | 6337 | 0.637176 | 0.693147 | -0.055972 | [-0.064254, -0.048032] | yes |
| vct | 1080 | 0.667500 | 0.693147 | -0.025647 | [-0.040447, -0.012088] | yes |
| vcl | 3374 | 0.641489 | 0.693147 | -0.051658 | [-0.063263, -0.039670] | yes |
| gc | 1005 | 0.596066 | 0.693147 | -0.097081 | [-0.120771, -0.074071] | yes |
| t3 | 16 | 0.535758 | 0.693147 | -0.157389 | [-0.439823, 0.012072] | no |
| collegiate | 7 | 0.741900 | 0.693147 | 0.048753 | [0.030387, 0.062528] | yes |
| offseason | 855 | 0.631212 | 0.693147 | -0.061936 | [-0.084855, -0.039339] | yes |
| international=1 | 268 | 0.664654 | 0.693147 | -0.028493 | [-0.054463, -0.004607] | yes |
| international=0 | 6069 | 0.635962 | 0.693147 | -0.057185 | [-0.065871, -0.049042] | yes |

| Model | Section | Rows | Log loss | Brier | Accuracy | ECE |
|---|---|---:|---:|---:|---:|---:|
| team_elo+none | all | 6337 | 0.662947 | 0.234966 | 0.602730 | 0.031254 |
| team_elo+none | vct | 1080 | 0.685646 | 0.245671 | 0.564815 | 0.063606 |
| team_elo+none | vcl | 3374 | 0.666871 | 0.236503 | 0.604624 | 0.042181 |
| team_elo+none | gc | 1005 | 0.631112 | 0.221113 | 0.637313 | 0.043127 |
| team_elo+none | t3 | 16 | 0.458119 | 0.148245 | 0.750000 | 0.220932 |
| team_elo+none | collegiate | 7 | 0.735155 | 0.270941 | 0.285714 | 0.236280 |
| team_elo+none | offseason | 855 | 0.659448 | 0.232990 | 0.602339 | 0.029427 |
| team_elo+none | unknown | 0 | — | — | — | — |
| team_elo+none | international=1 | 268 | 0.672124 | 0.240160 | 0.589552 | 0.065781 |
| team_elo+none | international=0 | 6069 | 0.662541 | 0.234737 | 0.603312 | 0.030130 |

team_elo+none − coin (paired log loss):

| Section | Rows | team_elo+none log loss | coin log loss | Difference | 95% interval | Significant |
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
| player_round_glicko_rookie+none | all | 6337 | 0.638693 | 0.223702 | 0.631687 | 0.015405 |
| player_round_glicko_rookie+none | vct | 1080 | 0.667241 | 0.237238 | 0.591667 | 0.034482 |
| player_round_glicko_rookie+none | vcl | 3374 | 0.643621 | 0.225550 | 0.628334 | 0.031249 |
| player_round_glicko_rookie+none | gc | 1005 | 0.593128 | 0.204091 | 0.679602 | 0.026907 |
| player_round_glicko_rookie+none | t3 | 16 | 0.536829 | 0.186297 | 0.687500 | 0.238687 |
| player_round_glicko_rookie+none | collegiate | 7 | 0.719943 | 0.263865 | 0.428571 | 0.161536 |
| player_round_glicko_rookie+none | offseason | 855 | 0.637983 | 0.222732 | 0.639766 | 0.021006 |
| player_round_glicko_rookie+none | unknown | 0 | — | — | — | — |
| player_round_glicko_rookie+none | international=1 | 268 | 0.667079 | 0.237581 | 0.597015 | 0.043891 |
| player_round_glicko_rookie+none | international=0 | 6069 | 0.637439 | 0.223089 | 0.633218 | 0.016391 |

player_round_glicko_rookie+none − coin (paired log loss):

| Section | Rows | player_round_glicko_rookie+none log loss | coin log loss | Difference | 95% interval | Significant |
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
| player_round_glicko_rookie_tier_revert+none | all | 6337 | 0.637176 | 0.223510 | 0.629635 | 0.017829 |
| player_round_glicko_rookie_tier_revert+none | vct | 1080 | 0.667500 | 0.237597 | 0.584259 | 0.034351 |
| player_round_glicko_rookie_tier_revert+none | vcl | 3374 | 0.641489 | 0.225150 | 0.628631 | 0.029627 |
| player_round_glicko_rookie_tier_revert+none | gc | 1005 | 0.596066 | 0.205581 | 0.670647 | 0.034332 |
| player_round_glicko_rookie_tier_revert+none | t3 | 16 | 0.535758 | 0.184281 | 0.687500 | 0.142031 |
| player_round_glicko_rookie_tier_revert+none | collegiate | 7 | 0.741900 | 0.274684 | 0.285714 | 0.295353 |
| player_round_glicko_rookie_tier_revert+none | offseason | 855 | 0.631212 | 0.220637 | 0.644444 | 0.032012 |
| player_round_glicko_rookie_tier_revert+none | unknown | 0 | — | — | — | — |
| player_round_glicko_rookie_tier_revert+none | international=1 | 268 | 0.664654 | 0.236293 | 0.608209 | 0.052828 |
| player_round_glicko_rookie_tier_revert+none | international=0 | 6069 | 0.635962 | 0.222946 | 0.630582 | 0.018708 |

player_round_glicko_rookie_tier_revert+none − coin (paired log loss):

| Section | Rows | player_round_glicko_rookie_tier_revert+none log loss | coin log loss | Difference | 95% interval | Significant |
|---|---:|---:|---:|---:|---|---|
| all | 6337 | 0.637176 | 0.693147 | -0.055972 | [-0.064254, -0.048032] | yes |
| vct | 1080 | 0.667500 | 0.693147 | -0.025647 | [-0.040447, -0.012088] | yes |
| vcl | 3374 | 0.641489 | 0.693147 | -0.051658 | [-0.063263, -0.039670] | yes |
| gc | 1005 | 0.596066 | 0.693147 | -0.097081 | [-0.120771, -0.074071] | yes |
| t3 | 16 | 0.535758 | 0.693147 | -0.157389 | [-0.439823, 0.012072] | no |
| collegiate | 7 | 0.741900 | 0.693147 | 0.048753 | [0.030387, 0.062528] | yes |
| offseason | 855 | 0.631212 | 0.693147 | -0.061936 | [-0.084855, -0.039339] | yes |
| international=1 | 268 | 0.664654 | 0.693147 | -0.028493 | [-0.054463, -0.004607] | yes |
| international=0 | 6069 | 0.635962 | 0.693147 | -0.057185 | [-0.065871, -0.049042] | yes |

player_round_glicko_rookie − team_elo (paired log loss):

| Section | Rows | player_round_glicko_rookie log loss | team_elo log loss | Difference | 95% interval | Significant |
|---|---:|---:|---:|---:|---|---|
| all | 6337 | 0.638693 | 0.662947 | -0.024254 | [-0.031251, -0.017380] | yes |

player_round_glicko_rookie_tier_revert − team_elo (paired log loss):

| Section | Rows | player_round_glicko_rookie_tier_revert log loss | team_elo log loss | Difference | 95% interval | Significant |
|---|---:|---:|---:|---:|---|---|
| all | 6337 | 0.637176 | 0.662947 | -0.025771 | [-0.032120, -0.019646] | yes |

team_elo+none − team_elo (paired log loss):

| Section | Rows | team_elo+none log loss | team_elo log loss | Difference | 95% interval | Significant |
|---|---:|---:|---:|---:|---|---|
| all | 6337 | 0.662947 | 0.662947 | 0.000000 | [0.000000, 0.000000] | no |

player_round_glicko_rookie+none − team_elo (paired log loss):

| Section | Rows | player_round_glicko_rookie+none log loss | team_elo log loss | Difference | 95% interval | Significant |
|---|---:|---:|---:|---:|---|---|
| all | 6337 | 0.638693 | 0.662947 | -0.024254 | [-0.031251, -0.017380] | yes |

player_round_glicko_rookie_tier_revert+none − team_elo (paired log loss):

| Section | Rows | player_round_glicko_rookie_tier_revert+none log loss | team_elo log loss | Difference | 95% interval | Significant |
|---|---:|---:|---:|---:|---|---|
| all | 6337 | 0.637176 | 0.662947 | -0.025771 | [-0.032120, -0.019646] | yes |

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
| player_round_glicko_rookie_tier_revert | all | 2618 | 0.604421 | 0.209077 | 0.668067 | 0.019484 |
| player_round_glicko_rookie_tier_revert | vct | 415 | 0.639741 | 0.225637 | 0.636145 | 0.044141 |
| player_round_glicko_rookie_tier_revert | vcl | 1351 | 0.611871 | 0.211222 | 0.663953 | 0.038416 |
| player_round_glicko_rookie_tier_revert | gc | 409 | 0.535326 | 0.181381 | 0.733496 | 0.056317 |
| player_round_glicko_rookie_tier_revert | t3 | 6 | 0.518719 | 0.186424 | 0.666667 | 0.354131 |
| player_round_glicko_rookie_tier_revert | collegiate | 2 | 0.541715 | 0.180151 | 0.500000 | 0.403605 |
| player_round_glicko_rookie_tier_revert | offseason | 435 | 0.614020 | 0.213101 | 0.650575 | 0.040707 |
| player_round_glicko_rookie_tier_revert | unknown | 0 | — | — | — | — |
| player_round_glicko_rookie_tier_revert | international=1 | 103 | 0.636141 | 0.222869 | 0.650485 | 0.052314 |
| player_round_glicko_rookie_tier_revert | international=0 | 2515 | 0.603122 | 0.208512 | 0.668787 | 0.019690 |

player_round_glicko_rookie_tier_revert − coin (paired log loss):

| Section | Rows | player_round_glicko_rookie_tier_revert log loss | coin log loss | Difference | 95% interval | Significant |
|---|---:|---:|---:|---:|---|---|
| all | 2618 | 0.604421 | 0.693147 | -0.088726 | [-0.104087, -0.072887] | yes |
| vct | 415 | 0.639741 | 0.693147 | -0.053406 | [-0.082590, -0.023645] | yes |
| vcl | 1351 | 0.611871 | 0.693147 | -0.081276 | [-0.104592, -0.057906] | yes |
| gc | 409 | 0.535326 | 0.693147 | -0.157821 | [-0.196390, -0.117015] | yes |
| t3 | 6 | 0.518719 | 0.693147 | -0.174428 | [-0.505810, 0.156954] | no |
| collegiate | 2 | 0.541715 | 0.693147 | -0.151432 | [-0.375348, 0.072484] | no |
| offseason | 435 | 0.614020 | 0.693147 | -0.079127 | [-0.115476, -0.042093] | yes |
| international=1 | 103 | 0.636141 | 0.693147 | -0.057006 | [-0.111696, -0.004786] | yes |
| international=0 | 2515 | 0.603122 | 0.693147 | -0.090025 | [-0.105618, -0.073290] | yes |

| Model | Section | Rows | Log loss | Brier | Accuracy | ECE |
|---|---|---:|---:|---:|---:|---:|
| team_elo+none | all | 2618 | 0.643432 | 0.225839 | 0.630443 | 0.030124 |
| team_elo+none | vct | 415 | 0.664437 | 0.235728 | 0.612048 | 0.059909 |
| team_elo+none | vcl | 1351 | 0.649305 | 0.227962 | 0.633605 | 0.044519 |
| team_elo+none | gc | 409 | 0.596811 | 0.206447 | 0.658924 | 0.073475 |
| team_elo+none | t3 | 6 | 0.292563 | 0.076004 | 1.000000 | 0.240926 |
| team_elo+none | collegiate | 2 | 0.748653 | 0.277657 | 0.000000 | 0.526357 |
| team_elo+none | offseason | 435 | 0.653339 | 0.229875 | 0.609195 | 0.047433 |
| team_elo+none | unknown | 0 | — | — | — | — |
| team_elo+none | international=1 | 103 | 0.639781 | 0.225951 | 0.631068 | 0.069954 |
| team_elo+none | international=0 | 2515 | 0.643581 | 0.225835 | 0.630417 | 0.030105 |

team_elo+none − coin (paired log loss):

| Section | Rows | team_elo+none log loss | coin log loss | Difference | 95% interval | Significant |
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
| player_round_glicko_rookie+none | all | 2618 | 0.606622 | 0.209441 | 0.671505 | 0.025923 |
| player_round_glicko_rookie+none | vct | 415 | 0.637085 | 0.224561 | 0.631325 | 0.036790 |
| player_round_glicko_rookie+none | vcl | 1351 | 0.613287 | 0.211041 | 0.667654 | 0.039104 |
| player_round_glicko_rookie+none | gc | 409 | 0.531225 | 0.180006 | 0.745721 | 0.062250 |
| player_round_glicko_rookie+none | t3 | 6 | 0.573765 | 0.208319 | 0.666667 | 0.147831 |
| player_round_glicko_rookie+none | collegiate | 2 | 0.468348 | 0.143217 | 1.000000 | 0.367453 |
| player_round_glicko_rookie+none | offseason | 435 | 0.628838 | 0.218039 | 0.650575 | 0.056037 |
| player_round_glicko_rookie+none | unknown | 0 | — | — | — | — |
| player_round_glicko_rookie+none | international=1 | 103 | 0.643461 | 0.226408 | 0.640777 | 0.077826 |
| player_round_glicko_rookie+none | international=0 | 2515 | 0.605113 | 0.208746 | 0.672763 | 0.026114 |

player_round_glicko_rookie+none − coin (paired log loss):

| Section | Rows | player_round_glicko_rookie+none log loss | coin log loss | Difference | 95% interval | Significant |
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
| player_round_glicko_rookie_tier_revert+none | all | 2618 | 0.604421 | 0.209077 | 0.668067 | 0.019484 |
| player_round_glicko_rookie_tier_revert+none | vct | 415 | 0.639741 | 0.225637 | 0.636145 | 0.044141 |
| player_round_glicko_rookie_tier_revert+none | vcl | 1351 | 0.611871 | 0.211222 | 0.663953 | 0.038416 |
| player_round_glicko_rookie_tier_revert+none | gc | 409 | 0.535326 | 0.181381 | 0.733496 | 0.056317 |
| player_round_glicko_rookie_tier_revert+none | t3 | 6 | 0.518719 | 0.186424 | 0.666667 | 0.354131 |
| player_round_glicko_rookie_tier_revert+none | collegiate | 2 | 0.541715 | 0.180151 | 0.500000 | 0.403605 |
| player_round_glicko_rookie_tier_revert+none | offseason | 435 | 0.614020 | 0.213101 | 0.650575 | 0.040707 |
| player_round_glicko_rookie_tier_revert+none | unknown | 0 | — | — | — | — |
| player_round_glicko_rookie_tier_revert+none | international=1 | 103 | 0.636141 | 0.222869 | 0.650485 | 0.052314 |
| player_round_glicko_rookie_tier_revert+none | international=0 | 2515 | 0.603122 | 0.208512 | 0.668787 | 0.019690 |

player_round_glicko_rookie_tier_revert+none − coin (paired log loss):

| Section | Rows | player_round_glicko_rookie_tier_revert+none log loss | coin log loss | Difference | 95% interval | Significant |
|---|---:|---:|---:|---:|---|---|
| all | 2618 | 0.604421 | 0.693147 | -0.088726 | [-0.104087, -0.072887] | yes |
| vct | 415 | 0.639741 | 0.693147 | -0.053406 | [-0.082590, -0.023645] | yes |
| vcl | 1351 | 0.611871 | 0.693147 | -0.081276 | [-0.104592, -0.057906] | yes |
| gc | 409 | 0.535326 | 0.693147 | -0.157821 | [-0.196390, -0.117015] | yes |
| t3 | 6 | 0.518719 | 0.693147 | -0.174428 | [-0.505810, 0.156954] | no |
| collegiate | 2 | 0.541715 | 0.693147 | -0.151432 | [-0.375348, 0.072484] | no |
| offseason | 435 | 0.614020 | 0.693147 | -0.079127 | [-0.115476, -0.042093] | yes |
| international=1 | 103 | 0.636141 | 0.693147 | -0.057006 | [-0.111696, -0.004786] | yes |
| international=0 | 2515 | 0.603122 | 0.693147 | -0.090025 | [-0.105618, -0.073290] | yes |

player_round_glicko_rookie − team_elo (paired log loss):

| Section | Rows | player_round_glicko_rookie log loss | team_elo log loss | Difference | 95% interval | Significant |
|---|---:|---:|---:|---:|---|---|
| all | 2618 | 0.606622 | 0.643432 | -0.036810 | [-0.050837, -0.022530] | yes |

player_round_glicko_rookie_tier_revert − team_elo (paired log loss):

| Section | Rows | player_round_glicko_rookie_tier_revert log loss | team_elo log loss | Difference | 95% interval | Significant |
|---|---:|---:|---:|---:|---|---|
| all | 2618 | 0.604421 | 0.643432 | -0.039011 | [-0.052011, -0.026106] | yes |

team_elo+none − team_elo (paired log loss):

| Section | Rows | team_elo+none log loss | team_elo log loss | Difference | 95% interval | Significant |
|---|---:|---:|---:|---:|---|---|
| all | 2618 | 0.643432 | 0.643432 | 0.000000 | [0.000000, 0.000000] | no |

player_round_glicko_rookie+none − team_elo (paired log loss):

| Section | Rows | player_round_glicko_rookie+none log loss | team_elo log loss | Difference | 95% interval | Significant |
|---|---:|---:|---:|---:|---|---|
| all | 2618 | 0.606622 | 0.643432 | -0.036810 | [-0.050837, -0.022530] | yes |

player_round_glicko_rookie_tier_revert+none − team_elo (paired log loss):

| Section | Rows | player_round_glicko_rookie_tier_revert+none log loss | team_elo log loss | Difference | 95% interval | Significant |
|---|---:|---:|---:|---:|---|---|
| all | 2618 | 0.604421 | 0.643432 | -0.039011 | [-0.052011, -0.026106] | yes |

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

### player_round_glicko_rookie_tier_revert: Kalshi comparison and returns



#### Log loss vs Kalshi

| Kind | Slice | Rows | Model log loss | Kalshi log loss | Difference [95% interval] | Significant |
|---|---|---:|---:|---:|---|---|
| series | all | 677 | 0.623904 | 0.633240 | -0.009337 [-0.031885, 0.013364] | no |
| series | vct | 278 | 0.625343 | 0.634755 | -0.009412 [-0.039740, 0.019976] | no |
| series | vcl | 340 | 0.612711 | 0.619968 | -0.007257 [-0.046014, 0.030851] | no |
| series | gc | 0 | — | — | — | — |
| series | t3 | 0 | — | — | — | — |
| series | collegiate | 0 | — | — | — | — |
| series | offseason | 59 | 0.681622 | 0.702587 | -0.020965 [-0.081422, 0.037164] | no |
| series | international=1 | 41 | 0.615210 | 0.653397 | -0.038187 [-0.084915, 0.008950] | no |
| series | international=0 | 636 | 0.624464 | 0.631941 | -0.007477 [-0.032948, 0.016806] | no |
| map | all | 1049 | 0.657429 | 0.668225 | -0.010796 [-0.031967, 0.007441] | no |
| map | vct | 461 | 0.659632 | 0.665762 | -0.006130 [-0.025716, 0.011253] | no |
| map | vcl | 490 | 0.649981 | 0.668365 | -0.018383 [-0.059907, 0.016929] | no |
| map | gc | 0 | — | — | — | — |
| map | t3 | 0 | — | — | — | — |
| map | collegiate | 0 | — | — | — | — |
| map | offseason | 98 | 0.684308 | 0.679111 | 0.005198 [-0.024239, 0.035566] | no |
| map | international=1 | 59 | 0.662662 | 0.649653 | 0.013010 [-0.009799, 0.036385] | no |
| map | international=0 | 990 | 0.657117 | 0.669332 | -0.012214 [-0.033478, 0.007376] | no |

#### Full-Kelly returns

| Kind | Slice | Bets | Matches | Mean edge | Flat ROI [95% interval] | Kelly, LoL caps ($50 start) | Multiple | Max drawdown | Largest stake | Bets filled | Flat ROI depth-capped [95% interval] | Kelly depth-capped final |
|---|---|---:|---:|---:|---|---:|---:|---:|---:|---:|---|---:|
| series | all | 478 | 478 | 0.0954 | 12.84% [0.39%, 26.08%] | $1331.19 | 26.624× | 77.75% | $183.18 | 270 (208 unfilled) | 21.40% [4.53%, 39.39%] | $809.50 |
| series | vct | 190 | 190 | 0.0798 | 10.39% [-9.28%, 31.84%] | $68.22 | 1.364× | 73.96% | $6.62 | 116 (74 unfilled) | 25.57% [-0.04%, 54.12%] | $224.42 |
| series | vcl | 254 | 254 | 0.1085 | 14.42% [-1.69%, 33.26%] | $445.01 | 8.900× | 53.73% | $77.41 | 128 (126 unfilled) | 19.79% [-4.27%, 47.44%] | $164.49 |
| series | gc | 0 | 0 | — | — | $50.00 | 1.000× | 0.00% | $0.00 | 0 (0 unfilled) | — | $50.00 |
| series | t3 | 0 | 0 | — | — | $50.00 | 1.000× | 0.00% | $0.00 | 0 (0 unfilled) | — | $50.00 |
| series | collegiate | 0 | 0 | — | — | $50.00 | 1.000× | 0.00% | $0.00 | 0 (0 unfilled) | — | $50.00 |
| series | offseason | 34 | 34 | 0.0844 | 14.77% [-28.30%, 58.49%] | $75.87 | 1.517× | 35.70% | $8.93 | 26 (8 unfilled) | 10.78% [-32.86%, 57.56%] | $59.18 |
| series | international=1 | 25 | 25 | 0.0519 | 35.62% [-14.22%, 91.69%] | $83.36 | 1.667× | 28.06% | $6.64 | 25 (0 unfilled) | 35.62% [-14.22%, 91.69%] | $83.44 |
| series | international=0 | 453 | 453 | 0.0978 | 11.58% [-1.61%, 25.23%] | $641.63 | 12.833× | 77.76% | $111.50 | 245 (208 unfilled) | 19.95% [2.36%, 38.60%] | $465.20 |
| map | all | 651 | 348 | 0.0663 | 20.01% [2.44%, 41.22%] | $6645.34 | 132.907× | 36.85% | $245.53 | 92 (559 unfilled) | 58.73% [-1.26%, 133.26%] | $254.51 |
| map | vct | 269 | 140 | 0.0514 | 8.56% [-9.26%, 33.70%] | $158.80 | 3.176× | 36.41% | $10.03 | 45 (224 unfilled) | 61.59% [-16.07%, 187.28%] | $111.75 |
| map | vcl | 330 | 182 | 0.0830 | 31.86% [3.25%, 68.67%] | $1711.05 | 34.221× | 54.92% | $245.53 | 43 (287 unfilled) | 52.30% [-28.13%, 167.82%] | $127.98 |
| map | gc | 0 | 0 | — | — | $50.00 | 1.000× | 0.00% | $0.00 | 0 (0 unfilled) | — | $50.00 |
| map | t3 | 0 | 0 | — | — | $50.00 | 1.000× | 0.00% | $0.00 | 0 (0 unfilled) | — | $50.00 |
| map | collegiate | 0 | 0 | — | — | $50.00 | 1.000× | 0.00% | $0.00 | 0 (0 unfilled) | — | $50.00 |
| map | offseason | 52 | 26 | 0.0370 | 3.80% [-28.45%, 35.70%] | $61.44 | 1.229× | 14.49% | $4.16 | 4 (48 unfilled) | 95.88% [13.38%, 262.84%] | $60.43 |
| map | international=1 | 29 | 15 | 0.0405 | -19.00% [-52.60%, 11.58%] | $38.88 | 0.778× | 25.58% | $4.81 | 9 (20 unfilled) | 17.88% [-28.86%, 70.60%] | $51.00 |
| map | international=0 | 622 | 333 | 0.0675 | 21.82% [4.00%, 44.55%] | $7359.14 | 147.183× | 29.12% | $245.53 | 83 (539 unfilled) | 63.12% [-3.08%, 150.25%] | $241.63 |
| series+map | all | 1129 | 502 | 0.0786 | 16.97% [4.50%, 30.64%] | $5489.87 | 109.797× | 47.44% | $247.91 | 362 (767 unfilled) | 30.91% [10.20%, 54.20%] | $495.49 |

#### Monthly market blend fits

UTC monthly fits use earlier rows of the same kind from 2025-09-01, excluding holdout; minimum 100 rows. logit(p_blend) = a·logit(mid) + b·(logit(p_model) − logit(mid)); inputs clipped to [0.01, 0.99], no intercept, ridge 1e-6. Unfitted rows use mid unchanged; excluded from blended tables: 240 rows. Rating parameters remain selected on the tuning window.

| Month | Kind | n | a | b | Status |
|---|---|---:|---:|---:|---|
| 2026-01 | series | 0 | 1.000000 | 0.000000 | unfitted |
| 2026-02 | series | 21 | 1.000000 | 0.000000 | unfitted |
| 2026-02 | map | 0 | 1.000000 | 0.000000 | unfitted |
| 2026-03 | series | 72 | 1.000000 | 0.000000 | unfitted |
| 2026-03 | map | 48 | 1.000000 | 0.000000 | unfitted |
| 2026-04 | series | 136 | 1.298754 | 0.740539 | fitted |
| 2026-04 | map | 104 | 1.520663 | 0.423387 | fitted |
| 2026-05 | series | 357 | 1.078883 | 0.660530 | fitted |
| 2026-05 | map | 456 | 1.150388 | 0.957750 | fitted |
| 2026-06 | series | 556 | 1.020380 | 0.644239 | fitted |
| 2026-06 | map | 833 | 0.991260 | 0.813707 | fitted |

#### Log loss vs Kalshi (blended)

| Kind | Slice | Rows | Model log loss | Kalshi log loss | Difference [95% interval] | Significant |
|---|---|---:|---:|---:|---|---|
| series | all | 541 | 0.620992 | 0.634347 | -0.013355 [-0.029071, 0.003393] | no |
| series | vct | 201 | 0.633328 | 0.644147 | -0.010819 [-0.031948, 0.010939] | no |
| series | vcl | 291 | 0.602564 | 0.621829 | -0.019264 [-0.043749, 0.009091] | no |
| series | gc | 0 | — | — | — | — |
| series | t3 | 0 | — | — | — | — |
| series | collegiate | 0 | — | — | — | — |
| series | offseason | 49 | 0.679823 | 0.668490 | 0.011333 [-0.024502, 0.044154] | no |
| series | international=1 | 24 | 0.652144 | 0.682705 | -0.030561 [-0.074229, 0.010768] | no |
| series | international=0 | 517 | 0.619546 | 0.632102 | -0.012557 [-0.028672, 0.005036] | no |
| map | all | 945 | 0.676909 | 0.673192 | 0.003717 [-0.005960, 0.014521] | no |
| map | vct | 392 | 0.666334 | 0.667249 | -0.000915 [-0.014284, 0.012368] | no |
| map | vcl | 456 | 0.683550 | 0.676303 | 0.007247 [-0.008173, 0.023421] | no |
| map | gc | 0 | — | — | — | — |
| map | t3 | 0 | — | — | — | — |
| map | collegiate | 0 | — | — | — | — |
| map | offseason | 97 | 0.688425 | 0.682581 | 0.005844 [-0.022953, 0.035970] | no |
| map | international=1 | 50 | 0.659974 | 0.651359 | 0.008616 [-0.011120, 0.028770] | no |
| map | international=0 | 895 | 0.677855 | 0.674412 | 0.003443 [-0.007262, 0.013401] | no |

#### Full-Kelly returns (blended)

| Kind | Slice | Bets | Matches | Mean edge | Flat ROI [95% interval] | Kelly, LoL caps ($50 start) | Multiple | Max drawdown | Largest stake | Bets filled | Flat ROI depth-capped [95% interval] | Kelly depth-capped final |
|---|---|---:|---:|---:|---|---:|---:|---:|---:|---:|---|---:|
| series | all | 325 | 325 | 0.0527 | 16.51% [2.06%, 30.89%] | $837.70 | 16.754× | 39.30% | $101.60 | 177 (148 unfilled) | 16.10% [-2.45%, 35.60%] | $291.76 |
| series | vct | 120 | 120 | 0.0416 | 8.46% [-14.42%, 34.61%] | $78.85 | 1.577× | 45.14% | $6.53 | 70 (50 unfilled) | 19.35% [-8.73%, 50.89%] | $120.72 |
| series | vcl | 179 | 179 | 0.0630 | 24.43% [5.72%, 44.45%] | $505.98 | 10.120× | 36.09% | $61.38 | 87 (92 unfilled) | 22.35% [-5.39%, 52.89%] | $129.40 |
| series | gc | 0 | 0 | — | — | $50.00 | 1.000× | 0.00% | $0.00 | 0 (0 unfilled) | — | $50.00 |
| series | t3 | 0 | 0 | — | — | $50.00 | 1.000× | 0.00% | $0.00 | 0 (0 unfilled) | — | $50.00 |
| series | collegiate | 0 | 0 | — | — | $50.00 | 1.000× | 0.00% | $0.00 | 0 (0 unfilled) | — | $50.00 |
| series | offseason | 26 | 26 | 0.0331 | -0.93% [-42.77%, 47.23%] | $52.06 | 1.041× | 14.17% | $4.85 | 20 (6 unfilled) | -22.36% [-65.16%, 22.81%] | $42.45 |
| series | international=1 | 12 | 12 | 0.0312 | 38.18% [-40.22%, 122.84%] | $75.67 | 1.513× | 6.70% | $5.90 | 12 (0 unfilled) | 38.18% [-40.22%, 122.84%] | $75.67 |
| series | international=0 | 313 | 313 | 0.0535 | 15.67% [1.14%, 30.83%] | $554.25 | 11.085× | 39.30% | $67.22 | 165 (148 unfilled) | 14.49% [-4.22%, 34.08%] | $180.05 |
| map | all | 527 | 283 | 0.0397 | 2.26% [-8.51%, 15.49%] | $27.59 | 0.552× | 67.07% | $7.45 | 63 (464 unfilled) | 7.74% [-14.61%, 31.87%] | $54.56 |
| map | vct | 216 | 113 | 0.0357 | -1.65% [-14.40%, 11.08%] | $48.63 | 0.973× | 41.23% | $5.40 | 28 (188 unfilled) | 32.38% [-6.22%, 73.35%] | $66.61 |
| map | vcl | 267 | 147 | 0.0435 | 4.72% [-12.87%, 27.59%] | $25.78 | 0.516× | 68.28% | $7.14 | 32 (235 unfilled) | -16.81% [-43.84%, 11.33%] | $38.62 |
| map | gc | 0 | 0 | — | — | $50.00 | 1.000× | 0.00% | $0.00 | 0 (0 unfilled) | — | $50.00 |
| map | t3 | 0 | 0 | — | — | $50.00 | 1.000× | 0.00% | $0.00 | 0 (0 unfilled) | — | $50.00 |
| map | collegiate | 0 | 0 | — | — | $50.00 | 1.000× | 0.00% | $0.00 | 0 (0 unfilled) | — | $50.00 |
| map | offseason | 44 | 23 | 0.0362 | 6.47% [-21.89%, 35.52%] | $51.02 | 1.020× | 12.75% | $4.25 | 3 (41 unfilled) | 39.52% [13.38%, 92.31%] | $52.98 |
| map | international=1 | 25 | 12 | 0.0298 | -13.62% [-49.54%, 20.00%] | $45.10 | 0.902× | 13.09% | $2.33 | 7 (18 unfilled) | 24.65% [-17.02%, 64.55%] | $50.81 |
| map | international=0 | 502 | 271 | 0.0402 | 3.05% [-8.07%, 16.45%] | $30.64 | 0.613× | 63.43% | $7.45 | 56 (446 unfilled) | 5.62% [-20.33%, 32.51%] | $53.80 |
| series+map | all | 852 | 379 | 0.0446 | 7.70% [-3.09%, 18.29%] | $177.27 | 3.545× | 57.48% | $23.88 | 240 (612 unfilled) | 13.91% [-0.87%, 30.28%] | $130.51 |

#### Monthly breakdown

All metrics use identical linked rows within each kind/month. Unfitted blend months show —; counts include all rows.

| Kind | Month | Rows | Model log loss | Blended log loss | Kalshi log loss | Raw flat ROI (bets), unlimited Kelly final | Blended flat ROI (bets), unlimited Kelly final | Raw bets filled | Raw Flat ROI depth-capped [95% interval] | Raw Kelly depth-capped final | Blended bets filled | Blended Flat ROI depth-capped [95% interval] | Blended Kelly depth-capped final |
|---|---|---:|---:|---:|---:|---|---|---:|---|---:|---:|---|---:|
| map | 2026-02 | 48 | 0.702986 | — | 0.690786 | 1.89% (40), $46.09 | — | 12 (28 unfilled) | 1.41% [-66.85%, 52.25%] | $50.04 | — | — | — |
| map | 2026-03 | 56 | 0.602229 | — | 0.565065 | -16.09% (37), $36.80 | — | 10 (27 unfilled) | -42.81% [-100.00%, 27.38%] | $48.12 | — | — | — |
| map | 2026-04 | 352 | 0.638290 | 0.690906 | 0.690793 | 56.31% (236), $6773.69 | 6.06% (213), $44.23 | 28 (208 unfilled) | 182.88% [3.68%, 412.27%] | $239.49 | 24 (189 unfilled) | 4.63% [-16.91%, 24.13%] | $56.12 |
| map | 2026-05 | 377 | 0.682663 | 0.684397 | 0.687018 | 8.18% (209), $87.23 | 5.42% (196), $68.91 | 26 (183 unfilled) | 29.55% [-20.37%, 83.42%] | $65.09 | 23 (173 unfilled) | 20.70% [-27.24%, 73.57%] | $61.18 |
| map | 2026-06 | 216 | 0.648763 | 0.641029 | 0.620377 | -11.25% (129), $22.69 | -9.75% (118), $22.58 | 16 (113 unfilled) | -6.30% [-48.66%, 40.83%] | $41.57 | 16 (102 unfilled) | -6.30% [-48.66%, 40.83%] | $39.94 |
| series | 2026-01 | 21 | 0.622178 | — | 0.661069 | 28.56% (16), $69.72 | — | 8 (8 unfilled) | 5.12% [-73.61%, 84.67%] | $51.59 | — | — | — |
| series | 2026-02 | 51 | 0.666973 | — | 0.694525 | 22.67% (38), $71.84 | — | 26 (12 unfilled) | 39.68% [-20.35%, 112.10%] | $83.96 | — | — | — |
| series | 2026-03 | 64 | 0.591078 | — | 0.565917 | -6.21% (49), $32.08 | — | 36 (13 unfilled) | 4.78% [-25.93%, 39.35%] | $47.08 | — | — | — |
| series | 2026-04 | 221 | 0.612039 | 0.611697 | 0.627690 | 18.20% (158), $249.59 | 16.90% (143), $227.09 | 70 (88 unfilled) | 49.40% [10.63%, 96.23%] | $253.28 | 62 (81 unfilled) | 29.73% [-2.11%, 67.79%] | $119.92 |
| series | 2026-05 | 199 | 0.651325 | 0.650080 | 0.663719 | 16.36% (132), $109.77 | 17.83% (117), $112.95 | 86 (46 unfilled) | 5.53% [-19.47%, 31.27%] | $50.76 | 78 (39 unfilled) | 3.47% [-22.12%, 31.60%] | $59.40 |
| series | 2026-06 | 121 | 0.599983 | 0.590128 | 0.598199 | 1.00% (85), $74.62 | 13.26% (65), $80.70 | 44 (41 unfilled) | 13.51% [-21.53%, 52.41%] | $106.48 | 37 (28 unfilled) | 20.00% [-20.18%, 61.44%] | $95.72 |

### team_elo+none: Kalshi comparison and returns

none

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

### player_round_glicko_rookie+none: Kalshi comparison and returns

none

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

### player_round_glicko_rookie_tier_revert+none: Kalshi comparison and returns

none

#### Log loss vs Kalshi

| Kind | Slice | Rows | Model log loss | Kalshi log loss | Difference [95% interval] | Significant |
|---|---|---:|---:|---:|---|---|
| series | all | 677 | 0.623904 | 0.633240 | -0.009337 [-0.031885, 0.013364] | no |
| series | vct | 278 | 0.625343 | 0.634755 | -0.009412 [-0.039740, 0.019976] | no |
| series | vcl | 340 | 0.612711 | 0.619968 | -0.007257 [-0.046014, 0.030851] | no |
| series | gc | 0 | — | — | — | — |
| series | t3 | 0 | — | — | — | — |
| series | collegiate | 0 | — | — | — | — |
| series | offseason | 59 | 0.681622 | 0.702587 | -0.020965 [-0.081422, 0.037164] | no |
| series | international=1 | 41 | 0.615210 | 0.653397 | -0.038187 [-0.084915, 0.008950] | no |
| series | international=0 | 636 | 0.624464 | 0.631941 | -0.007477 [-0.032948, 0.016806] | no |
| map | all | 1049 | 0.657429 | 0.668225 | -0.010796 [-0.031967, 0.007441] | no |
| map | vct | 461 | 0.659632 | 0.665762 | -0.006130 [-0.025716, 0.011253] | no |
| map | vcl | 490 | 0.649981 | 0.668365 | -0.018383 [-0.059907, 0.016929] | no |
| map | gc | 0 | — | — | — | — |
| map | t3 | 0 | — | — | — | — |
| map | collegiate | 0 | — | — | — | — |
| map | offseason | 98 | 0.684308 | 0.679111 | 0.005198 [-0.024239, 0.035566] | no |
| map | international=1 | 59 | 0.662662 | 0.649653 | 0.013010 [-0.009799, 0.036385] | no |
| map | international=0 | 990 | 0.657117 | 0.669332 | -0.012214 [-0.033478, 0.007376] | no |

#### Full-Kelly returns

| Kind | Slice | Bets | Matches | Mean edge | Flat ROI [95% interval] | Kelly, LoL caps ($50 start) | Multiple | Max drawdown | Largest stake | Bets filled | Flat ROI depth-capped [95% interval] | Kelly depth-capped final |
|---|---|---:|---:|---:|---|---:|---:|---:|---:|---:|---|---:|
| series | all | 478 | 478 | 0.0954 | 12.84% [0.39%, 26.08%] | $1331.19 | 26.624× | 77.75% | $183.18 | 270 (208 unfilled) | 21.40% [4.53%, 39.39%] | $809.50 |
| series | vct | 190 | 190 | 0.0798 | 10.39% [-9.28%, 31.84%] | $68.22 | 1.364× | 73.96% | $6.62 | 116 (74 unfilled) | 25.57% [-0.04%, 54.12%] | $224.42 |
| series | vcl | 254 | 254 | 0.1085 | 14.42% [-1.69%, 33.26%] | $445.01 | 8.900× | 53.73% | $77.41 | 128 (126 unfilled) | 19.79% [-4.27%, 47.44%] | $164.49 |
| series | gc | 0 | 0 | — | — | $50.00 | 1.000× | 0.00% | $0.00 | 0 (0 unfilled) | — | $50.00 |
| series | t3 | 0 | 0 | — | — | $50.00 | 1.000× | 0.00% | $0.00 | 0 (0 unfilled) | — | $50.00 |
| series | collegiate | 0 | 0 | — | — | $50.00 | 1.000× | 0.00% | $0.00 | 0 (0 unfilled) | — | $50.00 |
| series | offseason | 34 | 34 | 0.0844 | 14.77% [-28.30%, 58.49%] | $75.87 | 1.517× | 35.70% | $8.93 | 26 (8 unfilled) | 10.78% [-32.86%, 57.56%] | $59.18 |
| series | international=1 | 25 | 25 | 0.0519 | 35.62% [-14.22%, 91.69%] | $83.36 | 1.667× | 28.06% | $6.64 | 25 (0 unfilled) | 35.62% [-14.22%, 91.69%] | $83.44 |
| series | international=0 | 453 | 453 | 0.0978 | 11.58% [-1.61%, 25.23%] | $641.63 | 12.833× | 77.76% | $111.50 | 245 (208 unfilled) | 19.95% [2.36%, 38.60%] | $465.20 |
| map | all | 651 | 348 | 0.0663 | 20.01% [2.44%, 41.22%] | $6645.34 | 132.907× | 36.85% | $245.53 | 92 (559 unfilled) | 58.73% [-1.26%, 133.26%] | $254.51 |
| map | vct | 269 | 140 | 0.0514 | 8.56% [-9.26%, 33.70%] | $158.80 | 3.176× | 36.41% | $10.03 | 45 (224 unfilled) | 61.59% [-16.07%, 187.28%] | $111.75 |
| map | vcl | 330 | 182 | 0.0830 | 31.86% [3.25%, 68.67%] | $1711.05 | 34.221× | 54.92% | $245.53 | 43 (287 unfilled) | 52.30% [-28.13%, 167.82%] | $127.98 |
| map | gc | 0 | 0 | — | — | $50.00 | 1.000× | 0.00% | $0.00 | 0 (0 unfilled) | — | $50.00 |
| map | t3 | 0 | 0 | — | — | $50.00 | 1.000× | 0.00% | $0.00 | 0 (0 unfilled) | — | $50.00 |
| map | collegiate | 0 | 0 | — | — | $50.00 | 1.000× | 0.00% | $0.00 | 0 (0 unfilled) | — | $50.00 |
| map | offseason | 52 | 26 | 0.0370 | 3.80% [-28.45%, 35.70%] | $61.44 | 1.229× | 14.49% | $4.16 | 4 (48 unfilled) | 95.88% [13.38%, 262.84%] | $60.43 |
| map | international=1 | 29 | 15 | 0.0405 | -19.00% [-52.60%, 11.58%] | $38.88 | 0.778× | 25.58% | $4.81 | 9 (20 unfilled) | 17.88% [-28.86%, 70.60%] | $51.00 |
| map | international=0 | 622 | 333 | 0.0675 | 21.82% [4.00%, 44.55%] | $7359.14 | 147.183× | 29.12% | $245.53 | 83 (539 unfilled) | 63.12% [-3.08%, 150.25%] | $241.63 |
| series+map | all | 1129 | 502 | 0.0786 | 16.97% [4.50%, 30.64%] | $5489.87 | 109.797× | 47.44% | $247.91 | 362 (767 unfilled) | 30.91% [10.20%, 54.20%] | $495.49 |

#### Monthly market blend fits

UTC monthly fits use earlier rows of the same kind from 2025-09-01, excluding holdout; minimum 100 rows. logit(p_blend) = a·logit(mid) + b·(logit(p_model) − logit(mid)); inputs clipped to [0.01, 0.99], no intercept, ridge 1e-6. Unfitted rows use mid unchanged; excluded from blended tables: 240 rows. Rating parameters remain selected on the tuning window.

| Month | Kind | n | a | b | Status |
|---|---|---:|---:|---:|---|
| 2026-01 | series | 0 | 1.000000 | 0.000000 | unfitted |
| 2026-02 | series | 21 | 1.000000 | 0.000000 | unfitted |
| 2026-02 | map | 0 | 1.000000 | 0.000000 | unfitted |
| 2026-03 | series | 72 | 1.000000 | 0.000000 | unfitted |
| 2026-03 | map | 48 | 1.000000 | 0.000000 | unfitted |
| 2026-04 | series | 136 | 1.298754 | 0.740539 | fitted |
| 2026-04 | map | 104 | 1.520663 | 0.423387 | fitted |
| 2026-05 | series | 357 | 1.078883 | 0.660530 | fitted |
| 2026-05 | map | 456 | 1.150388 | 0.957750 | fitted |
| 2026-06 | series | 556 | 1.020380 | 0.644239 | fitted |
| 2026-06 | map | 833 | 0.991260 | 0.813707 | fitted |

#### Log loss vs Kalshi (blended)

| Kind | Slice | Rows | Model log loss | Kalshi log loss | Difference [95% interval] | Significant |
|---|---|---:|---:|---:|---|---|
| series | all | 541 | 0.620992 | 0.634347 | -0.013355 [-0.029071, 0.003393] | no |
| series | vct | 201 | 0.633328 | 0.644147 | -0.010819 [-0.031948, 0.010939] | no |
| series | vcl | 291 | 0.602564 | 0.621829 | -0.019264 [-0.043749, 0.009091] | no |
| series | gc | 0 | — | — | — | — |
| series | t3 | 0 | — | — | — | — |
| series | collegiate | 0 | — | — | — | — |
| series | offseason | 49 | 0.679823 | 0.668490 | 0.011333 [-0.024502, 0.044154] | no |
| series | international=1 | 24 | 0.652144 | 0.682705 | -0.030561 [-0.074229, 0.010768] | no |
| series | international=0 | 517 | 0.619546 | 0.632102 | -0.012557 [-0.028672, 0.005036] | no |
| map | all | 945 | 0.676909 | 0.673192 | 0.003717 [-0.005960, 0.014521] | no |
| map | vct | 392 | 0.666334 | 0.667249 | -0.000915 [-0.014284, 0.012368] | no |
| map | vcl | 456 | 0.683550 | 0.676303 | 0.007247 [-0.008173, 0.023421] | no |
| map | gc | 0 | — | — | — | — |
| map | t3 | 0 | — | — | — | — |
| map | collegiate | 0 | — | — | — | — |
| map | offseason | 97 | 0.688425 | 0.682581 | 0.005844 [-0.022953, 0.035970] | no |
| map | international=1 | 50 | 0.659974 | 0.651359 | 0.008616 [-0.011120, 0.028770] | no |
| map | international=0 | 895 | 0.677855 | 0.674412 | 0.003443 [-0.007262, 0.013401] | no |

#### Full-Kelly returns (blended)

| Kind | Slice | Bets | Matches | Mean edge | Flat ROI [95% interval] | Kelly, LoL caps ($50 start) | Multiple | Max drawdown | Largest stake | Bets filled | Flat ROI depth-capped [95% interval] | Kelly depth-capped final |
|---|---|---:|---:|---:|---|---:|---:|---:|---:|---:|---|---:|
| series | all | 325 | 325 | 0.0527 | 16.51% [2.06%, 30.89%] | $837.70 | 16.754× | 39.30% | $101.60 | 177 (148 unfilled) | 16.10% [-2.45%, 35.60%] | $291.76 |
| series | vct | 120 | 120 | 0.0416 | 8.46% [-14.42%, 34.61%] | $78.85 | 1.577× | 45.14% | $6.53 | 70 (50 unfilled) | 19.35% [-8.73%, 50.89%] | $120.72 |
| series | vcl | 179 | 179 | 0.0630 | 24.43% [5.72%, 44.45%] | $505.98 | 10.120× | 36.09% | $61.38 | 87 (92 unfilled) | 22.35% [-5.39%, 52.89%] | $129.40 |
| series | gc | 0 | 0 | — | — | $50.00 | 1.000× | 0.00% | $0.00 | 0 (0 unfilled) | — | $50.00 |
| series | t3 | 0 | 0 | — | — | $50.00 | 1.000× | 0.00% | $0.00 | 0 (0 unfilled) | — | $50.00 |
| series | collegiate | 0 | 0 | — | — | $50.00 | 1.000× | 0.00% | $0.00 | 0 (0 unfilled) | — | $50.00 |
| series | offseason | 26 | 26 | 0.0331 | -0.93% [-42.77%, 47.23%] | $52.06 | 1.041× | 14.17% | $4.85 | 20 (6 unfilled) | -22.36% [-65.16%, 22.81%] | $42.45 |
| series | international=1 | 12 | 12 | 0.0312 | 38.18% [-40.22%, 122.84%] | $75.67 | 1.513× | 6.70% | $5.90 | 12 (0 unfilled) | 38.18% [-40.22%, 122.84%] | $75.67 |
| series | international=0 | 313 | 313 | 0.0535 | 15.67% [1.14%, 30.83%] | $554.25 | 11.085× | 39.30% | $67.22 | 165 (148 unfilled) | 14.49% [-4.22%, 34.08%] | $180.05 |
| map | all | 527 | 283 | 0.0397 | 2.26% [-8.51%, 15.49%] | $27.59 | 0.552× | 67.07% | $7.45 | 63 (464 unfilled) | 7.74% [-14.61%, 31.87%] | $54.56 |
| map | vct | 216 | 113 | 0.0357 | -1.65% [-14.40%, 11.08%] | $48.63 | 0.973× | 41.23% | $5.40 | 28 (188 unfilled) | 32.38% [-6.22%, 73.35%] | $66.61 |
| map | vcl | 267 | 147 | 0.0435 | 4.72% [-12.87%, 27.59%] | $25.78 | 0.516× | 68.28% | $7.14 | 32 (235 unfilled) | -16.81% [-43.84%, 11.33%] | $38.62 |
| map | gc | 0 | 0 | — | — | $50.00 | 1.000× | 0.00% | $0.00 | 0 (0 unfilled) | — | $50.00 |
| map | t3 | 0 | 0 | — | — | $50.00 | 1.000× | 0.00% | $0.00 | 0 (0 unfilled) | — | $50.00 |
| map | collegiate | 0 | 0 | — | — | $50.00 | 1.000× | 0.00% | $0.00 | 0 (0 unfilled) | — | $50.00 |
| map | offseason | 44 | 23 | 0.0362 | 6.47% [-21.89%, 35.52%] | $51.02 | 1.020× | 12.75% | $4.25 | 3 (41 unfilled) | 39.52% [13.38%, 92.31%] | $52.98 |
| map | international=1 | 25 | 12 | 0.0298 | -13.62% [-49.54%, 20.00%] | $45.10 | 0.902× | 13.09% | $2.33 | 7 (18 unfilled) | 24.65% [-17.02%, 64.55%] | $50.81 |
| map | international=0 | 502 | 271 | 0.0402 | 3.05% [-8.07%, 16.45%] | $30.64 | 0.613× | 63.43% | $7.45 | 56 (446 unfilled) | 5.62% [-20.33%, 32.51%] | $53.80 |
| series+map | all | 852 | 379 | 0.0446 | 7.70% [-3.09%, 18.29%] | $177.27 | 3.545× | 57.48% | $23.88 | 240 (612 unfilled) | 13.91% [-0.87%, 30.28%] | $130.51 |

#### Monthly breakdown

All metrics use identical linked rows within each kind/month. Unfitted blend months show —; counts include all rows.

| Kind | Month | Rows | Model log loss | Blended log loss | Kalshi log loss | Raw flat ROI (bets), unlimited Kelly final | Blended flat ROI (bets), unlimited Kelly final | Raw bets filled | Raw Flat ROI depth-capped [95% interval] | Raw Kelly depth-capped final | Blended bets filled | Blended Flat ROI depth-capped [95% interval] | Blended Kelly depth-capped final |
|---|---|---:|---:|---:|---:|---|---|---:|---|---:|---:|---|---:|
| map | 2026-02 | 48 | 0.702986 | — | 0.690786 | 1.89% (40), $46.09 | — | 12 (28 unfilled) | 1.41% [-66.85%, 52.25%] | $50.04 | — | — | — |
| map | 2026-03 | 56 | 0.602229 | — | 0.565065 | -16.09% (37), $36.80 | — | 10 (27 unfilled) | -42.81% [-100.00%, 27.38%] | $48.12 | — | — | — |
| map | 2026-04 | 352 | 0.638290 | 0.690906 | 0.690793 | 56.31% (236), $6773.69 | 6.06% (213), $44.23 | 28 (208 unfilled) | 182.88% [3.68%, 412.27%] | $239.49 | 24 (189 unfilled) | 4.63% [-16.91%, 24.13%] | $56.12 |
| map | 2026-05 | 377 | 0.682663 | 0.684397 | 0.687018 | 8.18% (209), $87.23 | 5.42% (196), $68.91 | 26 (183 unfilled) | 29.55% [-20.37%, 83.42%] | $65.09 | 23 (173 unfilled) | 20.70% [-27.24%, 73.57%] | $61.18 |
| map | 2026-06 | 216 | 0.648763 | 0.641029 | 0.620377 | -11.25% (129), $22.69 | -9.75% (118), $22.58 | 16 (113 unfilled) | -6.30% [-48.66%, 40.83%] | $41.57 | 16 (102 unfilled) | -6.30% [-48.66%, 40.83%] | $39.94 |
| series | 2026-01 | 21 | 0.622178 | — | 0.661069 | 28.56% (16), $69.72 | — | 8 (8 unfilled) | 5.12% [-73.61%, 84.67%] | $51.59 | — | — | — |
| series | 2026-02 | 51 | 0.666973 | — | 0.694525 | 22.67% (38), $71.84 | — | 26 (12 unfilled) | 39.68% [-20.35%, 112.10%] | $83.96 | — | — | — |
| series | 2026-03 | 64 | 0.591078 | — | 0.565917 | -6.21% (49), $32.08 | — | 36 (13 unfilled) | 4.78% [-25.93%, 39.35%] | $47.08 | — | — | — |
| series | 2026-04 | 221 | 0.612039 | 0.611697 | 0.627690 | 18.20% (158), $249.59 | 16.90% (143), $227.09 | 70 (88 unfilled) | 49.40% [10.63%, 96.23%] | $253.28 | 62 (81 unfilled) | 29.73% [-2.11%, 67.79%] | $119.92 |
| series | 2026-05 | 199 | 0.651325 | 0.650080 | 0.663719 | 16.36% (132), $109.77 | 17.83% (117), $112.95 | 86 (46 unfilled) | 5.53% [-19.47%, 31.27%] | $50.76 | 78 (39 unfilled) | 3.47% [-22.12%, 31.60%] | $59.40 |
| series | 2026-06 | 121 | 0.599983 | 0.590128 | 0.598199 | 1.00% (85), $74.62 | 13.26% (65), $80.70 | 44 (41 unfilled) | 13.51% [-21.53%, 52.41%] | $106.48 | 37 (28 unfilled) | 20.00% [-20.18%, 61.44%] | $95.72 |

## Holdout

### Leaderboard (frozen stage-1 parameters)

| Model | Best params | Map log loss | Series log loss | Rows |
|---|---|---:|---:|---:|
| player_round_glicko_rookie_tier_revert | {"inactive_half_life": 0, "k": 32, "new_player": "teammates", "rd_info": 0.25, "rd_new": 280, "rookie_maps": 400, "rookie_penalty": 200, "season_month": 11, "season_revert": 0.2, "tau": 0.5} | 0.650324 | 0.626858 | 1663 |
| player_round_glicko_rookie_tier_revert+none | {"inactive_half_life": 0, "k": 32, "new_player": "teammates", "rd_info": 0.25, "rd_new": 280, "rookie_maps": 400, "rookie_penalty": 200, "season_month": 11, "season_revert": 0.2, "tau": 0.5} | 0.650324 | 0.626858 | 1663 |
| player_round_glicko_rookie | {"k": 32, "new_player": "teammates", "rd_info": 0.25, "rd_new": 280, "rookie_maps": 400, "rookie_penalty": 200, "tau": 0.5} | 0.650792 | 0.625738 | 1663 |
| player_round_glicko_rookie+none | {"k": 32, "new_player": "teammates", "rd_info": 0.25, "rd_new": 280, "rookie_maps": 400, "rookie_penalty": 200, "tau": 0.5} | 0.650792 | 0.625738 | 1663 |
| team_elo | {"k": 32} | 0.669703 | 0.652743 | 1663 |
| team_elo+none | {"k": 32} | 0.669703 | 0.652743 | 1663 |

### Maps

| Model | Section | Rows | Log loss | Brier | Accuracy | ECE |
|---|---|---:|---:|---:|---:|---:|
| coin | all | 1663 | 0.693147 | 0.250000 | 0.500000 | 0.023752 |
| coin | vct | 768 | 0.693147 | 0.250000 | 0.500000 | 0.011719 |
| coin | vcl | 304 | 0.693147 | 0.250000 | 0.500000 | 0.016447 |
| coin | gc | 503 | 0.693147 | 0.250000 | 0.500000 | 0.080517 |
| coin | t3 | 0 | — | — | — | — |
| coin | collegiate | 0 | — | — | — | — |
| coin | offseason | 88 | 0.693147 | 0.250000 | 0.500000 | 0.034091 |
| coin | unknown | 0 | — | — | — | — |
| coin | international=1 | 192 | 0.693147 | 0.250000 | 0.500000 | 0.036458 |
| coin | international=0 | 1471 | 0.693147 | 0.250000 | 0.500000 | 0.022094 |

| Model | Section | Rows | Log loss | Brier | Accuracy | ECE |
|---|---|---:|---:|---:|---:|---:|
| team_elo | all | 1663 | 0.669703 | 0.238501 | 0.588094 | 0.040042 |
| team_elo | vct | 768 | 0.696330 | 0.250289 | 0.567708 | 0.069755 |
| team_elo | vcl | 304 | 0.640572 | 0.224792 | 0.628289 | 0.032689 |
| team_elo | gc | 503 | 0.645442 | 0.228285 | 0.600398 | 0.037631 |
| team_elo | t3 | 0 | — | — | — | — |
| team_elo | collegiate | 0 | — | — | — | — |
| team_elo | offseason | 88 | 0.676643 | 0.241368 | 0.556818 | 0.064361 |
| team_elo | unknown | 0 | — | — | — | — |
| team_elo | international=1 | 192 | 0.668318 | 0.238425 | 0.562500 | 0.040337 |
| team_elo | international=0 | 1471 | 0.669884 | 0.238510 | 0.591434 | 0.043242 |

team_elo − coin (paired log loss):

| Section | Rows | team_elo log loss | coin log loss | Difference | 95% interval | Significant |
|---|---:|---:|---:|---:|---|---|
| all | 1663 | 0.669703 | 0.693147 | -0.023444 | [-0.039982, -0.007173] | yes |
| vct | 768 | 0.696330 | 0.693147 | 0.003182 | [-0.022855, 0.029499] | no |
| vcl | 304 | 0.640572 | 0.693147 | -0.052575 | [-0.088452, -0.019559] | yes |
| gc | 503 | 0.645442 | 0.693147 | -0.047706 | [-0.080473, -0.015830] | yes |
| offseason | 88 | 0.676643 | 0.693147 | -0.016504 | [-0.070347, 0.035394] | no |
| international=1 | 192 | 0.668318 | 0.693147 | -0.024829 | [-0.062118, 0.011643] | no |
| international=0 | 1471 | 0.669884 | 0.693147 | -0.023263 | [-0.041809, -0.005241] | yes |

| Model | Section | Rows | Log loss | Brier | Accuracy | ECE |
|---|---|---:|---:|---:|---:|---:|
| player_round_glicko_rookie | all | 1663 | 0.650792 | 0.230300 | 0.595911 | 0.036093 |
| player_round_glicko_rookie | vct | 768 | 0.673543 | 0.239903 | 0.567708 | 0.054850 |
| player_round_glicko_rookie | vcl | 304 | 0.628863 | 0.219897 | 0.628289 | 0.078673 |
| player_round_glicko_rookie | gc | 503 | 0.624781 | 0.219690 | 0.626243 | 0.042600 |
| player_round_glicko_rookie | t3 | 0 | — | — | — | — |
| player_round_glicko_rookie | collegiate | 0 | — | — | — | — |
| player_round_glicko_rookie | offseason | 88 | 0.676672 | 0.243073 | 0.556818 | 0.050799 |
| player_round_glicko_rookie | unknown | 0 | — | — | — | — |
| player_round_glicko_rookie | international=1 | 192 | 0.676881 | 0.242343 | 0.541667 | 0.056111 |
| player_round_glicko_rookie | international=0 | 1471 | 0.647387 | 0.228728 | 0.602991 | 0.036377 |

player_round_glicko_rookie − coin (paired log loss):

| Section | Rows | player_round_glicko_rookie log loss | coin log loss | Difference | 95% interval | Significant |
|---|---:|---:|---:|---:|---|---|
| all | 1663 | 0.650792 | 0.693147 | -0.042355 | [-0.058849, -0.025999] | yes |
| vct | 768 | 0.673543 | 0.693147 | -0.019604 | [-0.040567, 0.001208] | no |
| vcl | 304 | 0.628863 | 0.693147 | -0.064284 | [-0.097015, -0.033125] | yes |
| gc | 503 | 0.624781 | 0.693147 | -0.068366 | [-0.107265, -0.030088] | yes |
| offseason | 88 | 0.676672 | 0.693147 | -0.016476 | [-0.076716, 0.035489] | no |
| international=1 | 192 | 0.676881 | 0.693147 | -0.016266 | [-0.048851, 0.015536] | no |
| international=0 | 1471 | 0.647387 | 0.693147 | -0.045760 | [-0.063422, -0.028261] | yes |

| Model | Section | Rows | Log loss | Brier | Accuracy | ECE |
|---|---|---:|---:|---:|---:|---:|
| player_round_glicko_rookie_tier_revert | all | 1663 | 0.650324 | 0.230253 | 0.594408 | 0.037163 |
| player_round_glicko_rookie_tier_revert | vct | 768 | 0.673665 | 0.240183 | 0.563802 | 0.049037 |
| player_round_glicko_rookie_tier_revert | vcl | 304 | 0.627411 | 0.219529 | 0.639803 | 0.076997 |
| player_round_glicko_rookie_tier_revert | gc | 503 | 0.624335 | 0.219552 | 0.622266 | 0.039874 |
| player_round_glicko_rookie_tier_revert | t3 | 0 | — | — | — | — |
| player_round_glicko_rookie_tier_revert | collegiate | 0 | — | — | — | — |
| player_round_glicko_rookie_tier_revert | offseason | 88 | 0.674320 | 0.241805 | 0.545455 | 0.059252 |
| player_round_glicko_rookie_tier_revert | unknown | 0 | — | — | — | — |
| player_round_glicko_rookie_tier_revert | international=1 | 192 | 0.670585 | 0.239469 | 0.510417 | 0.101056 |
| player_round_glicko_rookie_tier_revert | international=0 | 1471 | 0.647679 | 0.229050 | 0.605370 | 0.034004 |

player_round_glicko_rookie_tier_revert − coin (paired log loss):

| Section | Rows | player_round_glicko_rookie_tier_revert log loss | coin log loss | Difference | 95% interval | Significant |
|---|---:|---:|---:|---:|---|---|
| all | 1663 | 0.650324 | 0.693147 | -0.042824 | [-0.058412, -0.027504] | yes |
| vct | 768 | 0.673665 | 0.693147 | -0.019483 | [-0.039074, -0.000243] | yes |
| vcl | 304 | 0.627411 | 0.693147 | -0.065736 | [-0.096978, -0.036063] | yes |
| gc | 503 | 0.624335 | 0.693147 | -0.068812 | [-0.105428, -0.033303] | yes |
| offseason | 88 | 0.674320 | 0.693147 | -0.018827 | [-0.074716, 0.028555] | no |
| international=1 | 192 | 0.670585 | 0.693147 | -0.022562 | [-0.052061, 0.007195] | no |
| international=0 | 1471 | 0.647679 | 0.693147 | -0.045468 | [-0.062615, -0.029149] | yes |

| Model | Section | Rows | Log loss | Brier | Accuracy | ECE |
|---|---|---:|---:|---:|---:|---:|
| team_elo+none | all | 1663 | 0.669703 | 0.238501 | 0.588094 | 0.040042 |
| team_elo+none | vct | 768 | 0.696330 | 0.250289 | 0.567708 | 0.069755 |
| team_elo+none | vcl | 304 | 0.640572 | 0.224792 | 0.628289 | 0.032689 |
| team_elo+none | gc | 503 | 0.645442 | 0.228285 | 0.600398 | 0.037631 |
| team_elo+none | t3 | 0 | — | — | — | — |
| team_elo+none | collegiate | 0 | — | — | — | — |
| team_elo+none | offseason | 88 | 0.676643 | 0.241368 | 0.556818 | 0.064361 |
| team_elo+none | unknown | 0 | — | — | — | — |
| team_elo+none | international=1 | 192 | 0.668318 | 0.238425 | 0.562500 | 0.040337 |
| team_elo+none | international=0 | 1471 | 0.669884 | 0.238510 | 0.591434 | 0.043242 |

team_elo+none − coin (paired log loss):

| Section | Rows | team_elo+none log loss | coin log loss | Difference | 95% interval | Significant |
|---|---:|---:|---:|---:|---|---|
| all | 1663 | 0.669703 | 0.693147 | -0.023444 | [-0.039982, -0.007173] | yes |
| vct | 768 | 0.696330 | 0.693147 | 0.003182 | [-0.022855, 0.029499] | no |
| vcl | 304 | 0.640572 | 0.693147 | -0.052575 | [-0.088452, -0.019559] | yes |
| gc | 503 | 0.645442 | 0.693147 | -0.047706 | [-0.080473, -0.015830] | yes |
| offseason | 88 | 0.676643 | 0.693147 | -0.016504 | [-0.070347, 0.035394] | no |
| international=1 | 192 | 0.668318 | 0.693147 | -0.024829 | [-0.062118, 0.011643] | no |
| international=0 | 1471 | 0.669884 | 0.693147 | -0.023263 | [-0.041809, -0.005241] | yes |

| Model | Section | Rows | Log loss | Brier | Accuracy | ECE |
|---|---|---:|---:|---:|---:|---:|
| player_round_glicko_rookie+none | all | 1663 | 0.650792 | 0.230300 | 0.595911 | 0.036093 |
| player_round_glicko_rookie+none | vct | 768 | 0.673543 | 0.239903 | 0.567708 | 0.054850 |
| player_round_glicko_rookie+none | vcl | 304 | 0.628863 | 0.219897 | 0.628289 | 0.078673 |
| player_round_glicko_rookie+none | gc | 503 | 0.624781 | 0.219690 | 0.626243 | 0.042600 |
| player_round_glicko_rookie+none | t3 | 0 | — | — | — | — |
| player_round_glicko_rookie+none | collegiate | 0 | — | — | — | — |
| player_round_glicko_rookie+none | offseason | 88 | 0.676672 | 0.243073 | 0.556818 | 0.050799 |
| player_round_glicko_rookie+none | unknown | 0 | — | — | — | — |
| player_round_glicko_rookie+none | international=1 | 192 | 0.676881 | 0.242343 | 0.541667 | 0.056111 |
| player_round_glicko_rookie+none | international=0 | 1471 | 0.647387 | 0.228728 | 0.602991 | 0.036377 |

player_round_glicko_rookie+none − coin (paired log loss):

| Section | Rows | player_round_glicko_rookie+none log loss | coin log loss | Difference | 95% interval | Significant |
|---|---:|---:|---:|---:|---|---|
| all | 1663 | 0.650792 | 0.693147 | -0.042355 | [-0.058849, -0.025999] | yes |
| vct | 768 | 0.673543 | 0.693147 | -0.019604 | [-0.040567, 0.001208] | no |
| vcl | 304 | 0.628863 | 0.693147 | -0.064284 | [-0.097015, -0.033125] | yes |
| gc | 503 | 0.624781 | 0.693147 | -0.068366 | [-0.107265, -0.030088] | yes |
| offseason | 88 | 0.676672 | 0.693147 | -0.016476 | [-0.076716, 0.035489] | no |
| international=1 | 192 | 0.676881 | 0.693147 | -0.016266 | [-0.048851, 0.015536] | no |
| international=0 | 1471 | 0.647387 | 0.693147 | -0.045760 | [-0.063422, -0.028261] | yes |

| Model | Section | Rows | Log loss | Brier | Accuracy | ECE |
|---|---|---:|---:|---:|---:|---:|
| player_round_glicko_rookie_tier_revert+none | all | 1663 | 0.650324 | 0.230253 | 0.594408 | 0.037163 |
| player_round_glicko_rookie_tier_revert+none | vct | 768 | 0.673665 | 0.240183 | 0.563802 | 0.049037 |
| player_round_glicko_rookie_tier_revert+none | vcl | 304 | 0.627411 | 0.219529 | 0.639803 | 0.076997 |
| player_round_glicko_rookie_tier_revert+none | gc | 503 | 0.624335 | 0.219552 | 0.622266 | 0.039874 |
| player_round_glicko_rookie_tier_revert+none | t3 | 0 | — | — | — | — |
| player_round_glicko_rookie_tier_revert+none | collegiate | 0 | — | — | — | — |
| player_round_glicko_rookie_tier_revert+none | offseason | 88 | 0.674320 | 0.241805 | 0.545455 | 0.059252 |
| player_round_glicko_rookie_tier_revert+none | unknown | 0 | — | — | — | — |
| player_round_glicko_rookie_tier_revert+none | international=1 | 192 | 0.670585 | 0.239469 | 0.510417 | 0.101056 |
| player_round_glicko_rookie_tier_revert+none | international=0 | 1471 | 0.647679 | 0.229050 | 0.605370 | 0.034004 |

player_round_glicko_rookie_tier_revert+none − coin (paired log loss):

| Section | Rows | player_round_glicko_rookie_tier_revert+none log loss | coin log loss | Difference | 95% interval | Significant |
|---|---:|---:|---:|---:|---|---|
| all | 1663 | 0.650324 | 0.693147 | -0.042824 | [-0.058412, -0.027504] | yes |
| vct | 768 | 0.673665 | 0.693147 | -0.019483 | [-0.039074, -0.000243] | yes |
| vcl | 304 | 0.627411 | 0.693147 | -0.065736 | [-0.096978, -0.036063] | yes |
| gc | 503 | 0.624335 | 0.693147 | -0.068812 | [-0.105428, -0.033303] | yes |
| offseason | 88 | 0.674320 | 0.693147 | -0.018827 | [-0.074716, 0.028555] | no |
| international=1 | 192 | 0.670585 | 0.693147 | -0.022562 | [-0.052061, 0.007195] | no |
| international=0 | 1471 | 0.647679 | 0.693147 | -0.045468 | [-0.062615, -0.029149] | yes |

player_round_glicko_rookie − team_elo (paired log loss):

| Section | Rows | player_round_glicko_rookie log loss | team_elo log loss | Difference | 95% interval | Significant |
|---|---:|---:|---:|---:|---|---|
| all | 1663 | 0.650792 | 0.669703 | -0.018911 | [-0.031210, -0.006413] | yes |

player_round_glicko_rookie_tier_revert − team_elo (paired log loss):

| Section | Rows | player_round_glicko_rookie_tier_revert log loss | team_elo log loss | Difference | 95% interval | Significant |
|---|---:|---:|---:|---:|---|---|
| all | 1663 | 0.650324 | 0.669703 | -0.019380 | [-0.031141, -0.007998] | yes |

team_elo+none − team_elo (paired log loss):

| Section | Rows | team_elo+none log loss | team_elo log loss | Difference | 95% interval | Significant |
|---|---:|---:|---:|---:|---|---|
| all | 1663 | 0.669703 | 0.669703 | 0.000000 | [0.000000, 0.000000] | no |

player_round_glicko_rookie+none − team_elo (paired log loss):

| Section | Rows | player_round_glicko_rookie+none log loss | team_elo log loss | Difference | 95% interval | Significant |
|---|---:|---:|---:|---:|---|---|
| all | 1663 | 0.650792 | 0.669703 | -0.018911 | [-0.031210, -0.006413] | yes |

player_round_glicko_rookie_tier_revert+none − team_elo (paired log loss):

| Section | Rows | player_round_glicko_rookie_tier_revert+none log loss | team_elo log loss | Difference | 95% interval | Significant |
|---|---:|---:|---:|---:|---|---|
| all | 1663 | 0.650324 | 0.669703 | -0.019380 | [-0.031141, -0.007998] | yes |

### Series

| Model | Section | Rows | Log loss | Brier | Accuracy | ECE |
|---|---|---:|---:|---:|---:|---:|
| coin | all | 653 | 0.693147 | 0.250000 | 0.500000 | 0.029862 |
| coin | vct | 308 | 0.693147 | 0.250000 | 0.500000 | 0.006494 |
| coin | vcl | 117 | 0.693147 | 0.250000 | 0.500000 | 0.038462 |
| coin | gc | 196 | 0.693147 | 0.250000 | 0.500000 | 0.071429 |
| coin | t3 | 0 | — | — | — | — |
| coin | collegiate | 0 | — | — | — | — |
| coin | offseason | 32 | 0.693147 | 0.250000 | 0.500000 | 0.093750 |
| coin | unknown | 0 | — | — | — | — |
| coin | international=1 | 76 | 0.693147 | 0.250000 | 0.500000 | 0.065789 |
| coin | international=0 | 577 | 0.693147 | 0.250000 | 0.500000 | 0.025130 |

| Model | Section | Rows | Log loss | Brier | Accuracy | ECE |
|---|---|---:|---:|---:|---:|---:|
| team_elo | all | 653 | 0.652743 | 0.229997 | 0.607963 | 0.040609 |
| team_elo | vct | 308 | 0.682950 | 0.243187 | 0.564935 | 0.088936 |
| team_elo | vcl | 117 | 0.607922 | 0.209456 | 0.649573 | 0.111697 |
| team_elo | gc | 196 | 0.634995 | 0.223076 | 0.642857 | 0.085057 |
| team_elo | t3 | 0 | — | — | — | — |
| team_elo | collegiate | 0 | — | — | — | — |
| team_elo | offseason | 32 | 0.634577 | 0.220544 | 0.656250 | 0.148049 |
| team_elo | unknown | 0 | — | — | — | — |
| team_elo | international=1 | 76 | 0.637878 | 0.224644 | 0.605263 | 0.091923 |
| team_elo | international=0 | 577 | 0.654701 | 0.230702 | 0.608319 | 0.042215 |

team_elo − coin (paired log loss):

| Section | Rows | team_elo log loss | coin log loss | Difference | 95% interval | Significant |
|---|---:|---:|---:|---:|---|---|
| all | 653 | 0.652743 | 0.693147 | -0.040405 | [-0.067099, -0.013720] | yes |
| vct | 308 | 0.682950 | 0.693147 | -0.010197 | [-0.053419, 0.033878] | no |
| vcl | 117 | 0.607922 | 0.693147 | -0.085225 | [-0.137266, -0.028191] | yes |
| gc | 196 | 0.634995 | 0.693147 | -0.058152 | [-0.104963, -0.009438] | yes |
| offseason | 32 | 0.634577 | 0.693147 | -0.058570 | [-0.151684, 0.048589] | no |
| international=1 | 76 | 0.637878 | 0.693147 | -0.055269 | [-0.113852, 0.006434] | no |
| international=0 | 577 | 0.654701 | 0.693147 | -0.038447 | [-0.067869, -0.008735] | yes |

| Model | Section | Rows | Log loss | Brier | Accuracy | ECE |
|---|---|---:|---:|---:|---:|---:|
| player_round_glicko_rookie | all | 653 | 0.625738 | 0.219640 | 0.623277 | 0.047237 |
| player_round_glicko_rookie | vct | 308 | 0.640060 | 0.226089 | 0.594156 | 0.061893 |
| player_round_glicko_rookie | vcl | 117 | 0.588819 | 0.201796 | 0.683761 | 0.118895 |
| player_round_glicko_rookie | gc | 196 | 0.616109 | 0.216134 | 0.647959 | 0.061677 |
| player_round_glicko_rookie | t3 | 0 | — | — | — | — |
| player_round_glicko_rookie | collegiate | 0 | — | — | — | — |
| player_round_glicko_rookie | offseason | 32 | 0.681846 | 0.244283 | 0.531250 | 0.127385 |
| player_round_glicko_rookie | unknown | 0 | — | — | — | — |
| player_round_glicko_rookie | international=1 | 76 | 0.671268 | 0.239996 | 0.500000 | 0.148501 |
| player_round_glicko_rookie | international=0 | 577 | 0.619741 | 0.216959 | 0.639515 | 0.043474 |

player_round_glicko_rookie − coin (paired log loss):

| Section | Rows | player_round_glicko_rookie log loss | coin log loss | Difference | 95% interval | Significant |
|---|---:|---:|---:|---:|---|---|
| all | 653 | 0.625738 | 0.693147 | -0.067409 | [-0.095314, -0.037279] | yes |
| vct | 308 | 0.640060 | 0.693147 | -0.053087 | [-0.088689, -0.013747] | yes |
| vcl | 117 | 0.588819 | 0.693147 | -0.104328 | [-0.162537, -0.047494] | yes |
| gc | 196 | 0.616109 | 0.693147 | -0.077038 | [-0.138960, -0.007917] | yes |
| offseason | 32 | 0.681846 | 0.693147 | -0.011301 | [-0.118333, 0.103886] | no |
| international=1 | 76 | 0.671268 | 0.693147 | -0.021879 | [-0.083213, 0.043158] | no |
| international=0 | 577 | 0.619741 | 0.693147 | -0.073406 | [-0.104074, -0.042523] | yes |

| Model | Section | Rows | Log loss | Brier | Accuracy | ECE |
|---|---|---:|---:|---:|---:|---:|
| player_round_glicko_rookie_tier_revert | all | 653 | 0.626858 | 0.220125 | 0.617917 | 0.055762 |
| player_round_glicko_rookie_tier_revert | vct | 308 | 0.646001 | 0.228506 | 0.584416 | 0.071973 |
| player_round_glicko_rookie_tier_revert | vcl | 117 | 0.580031 | 0.199030 | 0.679487 | 0.089798 |
| player_round_glicko_rookie_tier_revert | gc | 196 | 0.616285 | 0.215886 | 0.632653 | 0.088554 |
| player_round_glicko_rookie_tier_revert | t3 | 0 | — | — | — | — |
| player_round_glicko_rookie_tier_revert | collegiate | 0 | — | — | — | — |
| player_round_glicko_rookie_tier_revert | offseason | 32 | 0.678579 | 0.242543 | 0.625000 | 0.130914 |
| player_round_glicko_rookie_tier_revert | unknown | 0 | — | — | — | — |
| player_round_glicko_rookie_tier_revert | international=1 | 76 | 0.662910 | 0.236612 | 0.552632 | 0.109635 |
| player_round_glicko_rookie_tier_revert | international=0 | 577 | 0.622109 | 0.217953 | 0.626516 | 0.053641 |

player_round_glicko_rookie_tier_revert − coin (paired log loss):

| Section | Rows | player_round_glicko_rookie_tier_revert log loss | coin log loss | Difference | 95% interval | Significant |
|---|---:|---:|---:|---:|---|---|
| all | 653 | 0.626858 | 0.693147 | -0.066289 | [-0.094746, -0.036566] | yes |
| vct | 308 | 0.646001 | 0.693147 | -0.047146 | [-0.085265, -0.007573] | yes |
| vcl | 117 | 0.580031 | 0.693147 | -0.113116 | [-0.169801, -0.056705] | yes |
| gc | 196 | 0.616285 | 0.693147 | -0.076863 | [-0.139398, -0.006887] | yes |
| offseason | 32 | 0.678579 | 0.693147 | -0.014568 | [-0.116381, 0.097345] | no |
| international=1 | 76 | 0.662910 | 0.693147 | -0.030237 | [-0.090233, 0.034089] | no |
| international=0 | 577 | 0.622109 | 0.693147 | -0.071038 | [-0.102784, -0.038184] | yes |

| Model | Section | Rows | Log loss | Brier | Accuracy | ECE |
|---|---|---:|---:|---:|---:|---:|
| team_elo+none | all | 653 | 0.652743 | 0.229997 | 0.607963 | 0.040609 |
| team_elo+none | vct | 308 | 0.682950 | 0.243187 | 0.564935 | 0.088936 |
| team_elo+none | vcl | 117 | 0.607922 | 0.209456 | 0.649573 | 0.111697 |
| team_elo+none | gc | 196 | 0.634995 | 0.223076 | 0.642857 | 0.085057 |
| team_elo+none | t3 | 0 | — | — | — | — |
| team_elo+none | collegiate | 0 | — | — | — | — |
| team_elo+none | offseason | 32 | 0.634577 | 0.220544 | 0.656250 | 0.148049 |
| team_elo+none | unknown | 0 | — | — | — | — |
| team_elo+none | international=1 | 76 | 0.637878 | 0.224644 | 0.605263 | 0.091923 |
| team_elo+none | international=0 | 577 | 0.654701 | 0.230702 | 0.608319 | 0.042215 |

team_elo+none − coin (paired log loss):

| Section | Rows | team_elo+none log loss | coin log loss | Difference | 95% interval | Significant |
|---|---:|---:|---:|---:|---|---|
| all | 653 | 0.652743 | 0.693147 | -0.040405 | [-0.067099, -0.013720] | yes |
| vct | 308 | 0.682950 | 0.693147 | -0.010197 | [-0.053419, 0.033878] | no |
| vcl | 117 | 0.607922 | 0.693147 | -0.085225 | [-0.137266, -0.028191] | yes |
| gc | 196 | 0.634995 | 0.693147 | -0.058152 | [-0.104963, -0.009438] | yes |
| offseason | 32 | 0.634577 | 0.693147 | -0.058570 | [-0.151684, 0.048589] | no |
| international=1 | 76 | 0.637878 | 0.693147 | -0.055269 | [-0.113852, 0.006434] | no |
| international=0 | 577 | 0.654701 | 0.693147 | -0.038447 | [-0.067869, -0.008735] | yes |

| Model | Section | Rows | Log loss | Brier | Accuracy | ECE |
|---|---|---:|---:|---:|---:|---:|
| player_round_glicko_rookie+none | all | 653 | 0.625738 | 0.219640 | 0.623277 | 0.047237 |
| player_round_glicko_rookie+none | vct | 308 | 0.640060 | 0.226089 | 0.594156 | 0.061893 |
| player_round_glicko_rookie+none | vcl | 117 | 0.588819 | 0.201796 | 0.683761 | 0.118895 |
| player_round_glicko_rookie+none | gc | 196 | 0.616109 | 0.216134 | 0.647959 | 0.061677 |
| player_round_glicko_rookie+none | t3 | 0 | — | — | — | — |
| player_round_glicko_rookie+none | collegiate | 0 | — | — | — | — |
| player_round_glicko_rookie+none | offseason | 32 | 0.681846 | 0.244283 | 0.531250 | 0.127385 |
| player_round_glicko_rookie+none | unknown | 0 | — | — | — | — |
| player_round_glicko_rookie+none | international=1 | 76 | 0.671268 | 0.239996 | 0.500000 | 0.148501 |
| player_round_glicko_rookie+none | international=0 | 577 | 0.619741 | 0.216959 | 0.639515 | 0.043474 |

player_round_glicko_rookie+none − coin (paired log loss):

| Section | Rows | player_round_glicko_rookie+none log loss | coin log loss | Difference | 95% interval | Significant |
|---|---:|---:|---:|---:|---|---|
| all | 653 | 0.625738 | 0.693147 | -0.067409 | [-0.095314, -0.037279] | yes |
| vct | 308 | 0.640060 | 0.693147 | -0.053087 | [-0.088689, -0.013747] | yes |
| vcl | 117 | 0.588819 | 0.693147 | -0.104328 | [-0.162537, -0.047494] | yes |
| gc | 196 | 0.616109 | 0.693147 | -0.077038 | [-0.138960, -0.007917] | yes |
| offseason | 32 | 0.681846 | 0.693147 | -0.011301 | [-0.118333, 0.103886] | no |
| international=1 | 76 | 0.671268 | 0.693147 | -0.021879 | [-0.083213, 0.043158] | no |
| international=0 | 577 | 0.619741 | 0.693147 | -0.073406 | [-0.104074, -0.042523] | yes |

| Model | Section | Rows | Log loss | Brier | Accuracy | ECE |
|---|---|---:|---:|---:|---:|---:|
| player_round_glicko_rookie_tier_revert+none | all | 653 | 0.626858 | 0.220125 | 0.617917 | 0.055762 |
| player_round_glicko_rookie_tier_revert+none | vct | 308 | 0.646001 | 0.228506 | 0.584416 | 0.071973 |
| player_round_glicko_rookie_tier_revert+none | vcl | 117 | 0.580031 | 0.199030 | 0.679487 | 0.089798 |
| player_round_glicko_rookie_tier_revert+none | gc | 196 | 0.616285 | 0.215886 | 0.632653 | 0.088554 |
| player_round_glicko_rookie_tier_revert+none | t3 | 0 | — | — | — | — |
| player_round_glicko_rookie_tier_revert+none | collegiate | 0 | — | — | — | — |
| player_round_glicko_rookie_tier_revert+none | offseason | 32 | 0.678579 | 0.242543 | 0.625000 | 0.130914 |
| player_round_glicko_rookie_tier_revert+none | unknown | 0 | — | — | — | — |
| player_round_glicko_rookie_tier_revert+none | international=1 | 76 | 0.662910 | 0.236612 | 0.552632 | 0.109635 |
| player_round_glicko_rookie_tier_revert+none | international=0 | 577 | 0.622109 | 0.217953 | 0.626516 | 0.053641 |

player_round_glicko_rookie_tier_revert+none − coin (paired log loss):

| Section | Rows | player_round_glicko_rookie_tier_revert+none log loss | coin log loss | Difference | 95% interval | Significant |
|---|---:|---:|---:|---:|---|---|
| all | 653 | 0.626858 | 0.693147 | -0.066289 | [-0.094746, -0.036566] | yes |
| vct | 308 | 0.646001 | 0.693147 | -0.047146 | [-0.085265, -0.007573] | yes |
| vcl | 117 | 0.580031 | 0.693147 | -0.113116 | [-0.169801, -0.056705] | yes |
| gc | 196 | 0.616285 | 0.693147 | -0.076863 | [-0.139398, -0.006887] | yes |
| offseason | 32 | 0.678579 | 0.693147 | -0.014568 | [-0.116381, 0.097345] | no |
| international=1 | 76 | 0.662910 | 0.693147 | -0.030237 | [-0.090233, 0.034089] | no |
| international=0 | 577 | 0.622109 | 0.693147 | -0.071038 | [-0.102784, -0.038184] | yes |

player_round_glicko_rookie − team_elo (paired log loss):

| Section | Rows | player_round_glicko_rookie log loss | team_elo log loss | Difference | 95% interval | Significant |
|---|---:|---:|---:|---:|---|---|
| all | 653 | 0.625738 | 0.652743 | -0.027005 | [-0.049995, -0.002860] | yes |

player_round_glicko_rookie_tier_revert − team_elo (paired log loss):

| Section | Rows | player_round_glicko_rookie_tier_revert log loss | team_elo log loss | Difference | 95% interval | Significant |
|---|---:|---:|---:|---:|---|---|
| all | 653 | 0.626858 | 0.652743 | -0.025885 | [-0.048771, -0.002878] | yes |

team_elo+none − team_elo (paired log loss):

| Section | Rows | team_elo+none log loss | team_elo log loss | Difference | 95% interval | Significant |
|---|---:|---:|---:|---:|---|---|
| all | 653 | 0.652743 | 0.652743 | 0.000000 | [0.000000, 0.000000] | no |

player_round_glicko_rookie+none − team_elo (paired log loss):

| Section | Rows | player_round_glicko_rookie+none log loss | team_elo log loss | Difference | 95% interval | Significant |
|---|---:|---:|---:|---:|---|---|
| all | 653 | 0.625738 | 0.652743 | -0.027005 | [-0.049995, -0.002860] | yes |

player_round_glicko_rookie_tier_revert+none − team_elo (paired log loss):

| Section | Rows | player_round_glicko_rookie_tier_revert+none log loss | team_elo log loss | Difference | 95% interval | Significant |
|---|---:|---:|---:|---:|---|---|
| all | 653 | 0.626858 | 0.652743 | -0.025885 | [-0.048771, -0.002878] | yes |

## Holdout vs Kalshi

### team_elo: Kalshi comparison and returns



#### Log loss vs Kalshi

| Kind | Slice | Rows | Model log loss | Kalshi log loss | Difference [95% interval] | Significant |
|---|---|---:|---:|---:|---|---|
| series | all | 586 | 0.654951 | 0.627894 | 0.027057 [0.005745, 0.050260] | yes |
| series | vct | 306 | 0.674893 | 0.648387 | 0.026506 [-0.002664, 0.056761] | no |
| series | vcl | 96 | 0.607534 | 0.616703 | -0.009169 [-0.050140, 0.030573] | no |
| series | gc | 151 | 0.649853 | 0.586384 | 0.063469 [0.014400, 0.118587] | yes |
| series | t3 | 0 | — | — | — | — |
| series | collegiate | 0 | — | — | — | — |
| series | offseason | 33 | 0.631306 | 0.660365 | -0.029059 [-0.092768, 0.030661] | no |
| series | international=1 | 77 | 0.636434 | 0.603125 | 0.033309 [-0.015653, 0.082010] | no |
| series | international=0 | 509 | 0.657753 | 0.631641 | 0.026112 [0.002613, 0.050552] | yes |
| map | all | 991 | 0.676730 | 0.651191 | 0.025539 [0.011510, 0.039860] | yes |
| map | vct | 598 | 0.700498 | 0.670975 | 0.029523 [0.009417, 0.049391] | yes |
| map | vcl | 144 | 0.625081 | 0.628359 | -0.003277 [-0.028757, 0.020597] | no |
| map | gc | 193 | 0.640775 | 0.600063 | 0.040711 [0.007520, 0.077974] | yes |
| map | t3 | 0 | — | — | — | — |
| map | collegiate | 0 | — | — | — | — |
| map | offseason | 56 | 0.679656 | 0.674841 | 0.004815 [-0.013551, 0.024200] | no |
| map | international=1 | 128 | 0.650049 | 0.650599 | -0.000550 [-0.023246, 0.025750] | no |
| map | international=0 | 863 | 0.680687 | 0.651279 | 0.029409 [0.013069, 0.046689] | yes |

#### Full-Kelly returns

| Kind | Slice | Bets | Matches | Mean edge | Flat ROI [95% interval] | Kelly, LoL caps ($50 start) | Multiple | Max drawdown | Largest stake | Bets filled | Flat ROI depth-capped [95% interval] | Kelly depth-capped final |
|---|---|---:|---:|---:|---|---:|---:|---:|---:|---:|---|---:|
| series | all | 403 | 403 | 0.0853 | -9.03% [-20.58%, 2.62%] | $1.24 | 0.025× | 99.40% | $15.72 | 215 (188 unfilled) | -2.99% [-19.10%, 13.33%] | $20.46 |
| series | vct | 196 | 196 | 0.0792 | -10.12% [-26.26%, 6.58%] | $7.08 | 0.142× | 88.95% | $5.70 | 103 (93 unfilled) | -2.10% [-24.80%, 23.13%] | $25.96 |
| series | vcl | 65 | 65 | 0.0616 | 0.51% [-31.99%, 37.14%] | $75.11 | 1.502× | 57.99% | $12.99 | 38 (27 unfilled) | -13.34% [-43.02%, 18.88%] | $41.21 |
| series | gc | 120 | 120 | 0.1142 | -13.87% [-34.98%, 8.16%] | $7.60 | 0.152× | 88.43% | $4.59 | 58 (62 unfilled) | -2.40% [-35.97%, 33.40%] | $47.32 |
| series | t3 | 0 | 0 | — | — | $50.00 | 1.000× | 0.00% | $0.00 | 0 (0 unfilled) | — | $50.00 |
| series | collegiate | 0 | 0 | — | — | $50.00 | 1.000× | 0.00% | $0.00 | 0 (0 unfilled) | — | $50.00 |
| series | offseason | 22 | 22 | 0.0521 | -1.07% [-41.77%, 40.25%] | $62.28 | 1.246× | 15.94% | $5.69 | 16 (6 unfilled) | 13.64% [-36.66%, 63.55%] | $56.03 |
| series | international=1 | 52 | 52 | 0.0733 | -14.24% [-41.29%, 11.53%] | $25.48 | 0.510× | 65.50% | $5.69 | 39 (13 unfilled) | -1.25% [-31.68%, 29.59%] | $37.13 |
| series | international=0 | 351 | 351 | 0.0871 | -8.25% [-21.12%, 5.12%] | $3.41 | 0.068× | 98.06% | $13.78 | 176 (175 unfilled) | -3.38% [-21.27%, 15.73%] | $27.08 |
| map | all | 610 | 305 | 0.0710 | -10.10% [-17.73%, -2.68%] | $1.19 | 0.024× | 98.07% | $5.42 | 70 (540 unfilled) | -8.05% [-30.41%, 15.68%] | $38.74 |
| map | vct | 403 | 201 | 0.0712 | -9.80% [-18.74%, -0.46%] | $5.60 | 0.112× | 89.05% | $2.92 | 33 (370 unfilled) | -17.71% [-49.79%, 13.70%] | $36.22 |
| map | vcl | 64 | 32 | 0.0538 | -3.38% [-21.54%, 12.87%] | $38.01 | 0.760× | 39.59% | $5.28 | 13 (51 unfilled) | -40.08% [-87.77%, -1.47%] | $36.53 |
| map | gc | 119 | 60 | 0.0853 | -14.18% [-34.74%, 6.58%] | $25.97 | 0.519× | 68.23% | $4.77 | 24 (95 unfilled) | 22.48% [-22.64%, 67.27%] | $74.42 |
| map | t3 | 0 | 0 | — | — | $50.00 | 1.000× | 0.00% | $0.00 | 0 (0 unfilled) | — | $50.00 |
| map | collegiate | 0 | 0 | — | — | $50.00 | 1.000× | 0.00% | $0.00 | 0 (0 unfilled) | — | $50.00 |
| map | offseason | 24 | 12 | 0.0434 | -12.78% [-32.98%, 4.96%] | $43.49 | 0.870× | 17.50% | $2.84 | 0 (24 unfilled) | — | $50.00 |
| map | international=1 | 64 | 32 | 0.0541 | -3.55% [-19.58%, 12.39%] | $47.99 | 0.960× | 27.59% | $4.55 | 9 (55 unfilled) | -19.16% [-72.93%, 33.99%] | $42.15 |
| map | international=0 | 546 | 273 | 0.0730 | -10.87% [-18.67%, -3.02%] | $1.58 | 0.032× | 97.49% | $5.28 | 61 (485 unfilled) | -6.41% [-31.84%, 19.11%] | $46.78 |
| series+map | all | 1013 | 469 | 0.0767 | -9.67% [-17.54%, -2.04%] | $0.94 | 0.019× | 99.42% | $12.52 | 285 (728 unfilled) | -4.23% [-18.58%, 11.21%] | $20.32 |

#### Monthly market blend fits

UTC monthly fits use earlier rows of the same kind from 2025-09-01, excluding holdout; minimum 100 rows. logit(p_blend) = a·logit(mid) + b·(logit(p_model) − logit(mid)); inputs clipped to [0.01, 0.99], no intercept, ridge 1e-6. Unfitted rows use mid unchanged; excluded from blended tables: 0 rows. Rating parameters remain selected on the tuning window.

| Month | Kind | n | a | b | Status |
|---|---|---:|---:|---:|---|
| 2026-07 | series | 677 | 0.930056 | 0.134077 | fitted |
| 2026-07 | map | 1049 | 0.888658 | 0.392963 | fitted |
| 2026-08 | series | 677 | 0.930056 | 0.134077 | fitted |
| 2026-08 | map | 1049 | 0.888658 | 0.392963 | fitted |
| 2026-09 | series | 677 | 0.930056 | 0.134077 | fitted |
| 2026-09 | map | 1049 | 0.888658 | 0.392963 | fitted |
| 2026-10 | series | 677 | 0.930056 | 0.134077 | fitted |
| 2026-10 | map | 1049 | 0.888658 | 0.392963 | fitted |

#### Log loss vs Kalshi (blended)

| Kind | Slice | Rows | Model log loss | Kalshi log loss | Difference [95% interval] | Significant |
|---|---|---:|---:|---:|---|---|
| series | all | 586 | 0.627864 | 0.627894 | -0.000030 [-0.004125, 0.003826] | no |
| series | vct | 306 | 0.647785 | 0.648387 | -0.000602 [-0.005622, 0.004493] | no |
| series | vcl | 96 | 0.614306 | 0.616703 | -0.002397 [-0.012206, 0.006797] | no |
| series | gc | 151 | 0.590378 | 0.586384 | 0.003994 [-0.003960, 0.012393] | no |
| series | t3 | 0 | — | — | — | — |
| series | collegiate | 0 | — | — | — | — |
| series | offseason | 33 | 0.654109 | 0.660365 | -0.006256 [-0.019636, 0.005895] | no |
| series | international=1 | 77 | 0.607367 | 0.603125 | 0.004242 [-0.004203, 0.012054] | no |
| series | international=0 | 509 | 0.630965 | 0.631641 | -0.000676 [-0.005032, 0.003583] | no |
| map | all | 991 | 0.656282 | 0.651191 | 0.005091 [-0.000412, 0.010272] | no |
| map | vct | 598 | 0.675090 | 0.670975 | 0.004114 [-0.003805, 0.011513] | no |
| map | vcl | 144 | 0.627852 | 0.628359 | -0.000507 [-0.011199, 0.009142] | no |
| map | gc | 193 | 0.613771 | 0.600063 | 0.013707 [0.000185, 0.027252] | yes |
| map | t3 | 0 | — | — | — | — |
| map | collegiate | 0 | — | — | — | — |
| map | offseason | 56 | 0.675068 | 0.674841 | 0.000227 [-0.006161, 0.006999] | no |
| map | international=1 | 128 | 0.649283 | 0.650599 | -0.001316 [-0.009718, 0.008288] | no |
| map | international=0 | 863 | 0.657320 | 0.651279 | 0.006042 [0.000133, 0.012474] | yes |

#### Full-Kelly returns (blended)

| Kind | Slice | Bets | Matches | Mean edge | Flat ROI [95% interval] | Kelly, LoL caps ($50 start) | Multiple | Max drawdown | Largest stake | Bets filled | Flat ROI depth-capped [95% interval] | Kelly depth-capped final |
|---|---|---:|---:|---:|---|---:|---:|---:|---:|---:|---|---:|
| series | all | 72 | 72 | 0.0141 | 7.93% [-32.36%, 52.50%] | $43.07 | 0.861× | 41.63% | $4.37 | 36 (36 unfilled) | 15.46% [-41.62%, 79.54%] | $61.08 |
| series | vct | 30 | 30 | 0.0155 | 20.42% [-40.75%, 87.58%] | $50.77 | 1.015× | 29.74% | $4.35 | 14 (16 unfilled) | 68.42% [-42.26%, 198.93%] | $61.21 |
| series | vcl | 9 | 9 | 0.0055 | 104.08% [-57.58%, 301.92%] | $51.21 | 1.024× | 3.81% | $1.02 | 4 (5 unfilled) | -100.00% [-100.00%, -100.00%] | $48.16 |
| series | gc | 31 | 31 | 0.0156 | -32.83% [-79.62%, 20.61%] | $40.12 | 0.802× | 33.29% | $3.83 | 16 (15 unfilled) | -2.89% [-80.86%, 90.67%] | $50.98 |
| series | t3 | 0 | 0 | — | — | $50.00 | 1.000× | 0.00% | $0.00 | 0 (0 unfilled) | — | $50.00 |
| series | collegiate | 0 | 0 | — | — | $50.00 | 1.000× | 0.00% | $0.00 | 0 (0 unfilled) | — | $50.00 |
| series | offseason | 2 | 2 | 0.0084 | 21.52% [-100.00%, 144.20%] | $50.70 | 1.014× | 0.95% | $0.78 | 2 (0 unfilled) | 21.52% [-100.00%, 144.20%] | $50.70 |
| series | international=1 | 8 | 8 | 0.0152 | -59.24% [-100.00%, 22.71%] | $44.10 | 0.882× | 14.32% | $2.17 | 3 (5 unfilled) | 9.12% [-100.00%, 228.41%] | $50.31 |
| series | international=0 | 64 | 64 | 0.0139 | 16.35% [-27.20%, 69.18%] | $48.76 | 0.975× | 36.34% | $4.41 | 33 (31 unfilled) | 16.04% [-46.68%, 86.46%] | $60.70 |
| map | all | 258 | 138 | 0.0354 | -6.41% [-19.86%, 6.62%] | $19.94 | 0.399× | 69.35% | $3.99 | 37 (221 unfilled) | -3.24% [-40.27%, 34.63%] | $44.54 |
| map | vct | 156 | 82 | 0.0357 | -5.55% [-21.84%, 10.30%] | $34.32 | 0.686× | 41.58% | $3.19 | 14 (142 unfilled) | -19.46% [-79.47%, 41.75%] | $44.86 |
| map | vcl | 18 | 10 | 0.0292 | -13.40% [-63.94%, 29.14%] | $47.97 | 0.959× | 14.13% | $2.92 | 4 (14 unfilled) | -100.00% [-100.00%, -100.00%] | $42.88 |
| map | gc | 78 | 43 | 0.0377 | -7.01% [-33.56%, 22.36%] | $30.92 | 0.618× | 50.81% | $3.48 | 19 (59 unfilled) | 29.17% [-21.26%, 83.39%] | $57.95 |
| map | t3 | 0 | 0 | — | — | $50.00 | 1.000× | 0.00% | $0.00 | 0 (0 unfilled) | — | $50.00 |
| map | collegiate | 0 | 0 | — | — | $50.00 | 1.000× | 0.00% | $0.00 | 0 (0 unfilled) | — | $50.00 |
| map | offseason | 6 | 3 | 0.0154 | 0.19% [-1.88%, 2.29%] | $49.58 | 0.992× | 0.84% | $2.65 | 0 (6 unfilled) | — | $50.00 |
| map | international=1 | 18 | 10 | 0.0265 | 0.15% [-32.73%, 29.43%] | $47.71 | 0.954× | 12.89% | $3.15 | 4 (14 unfilled) | -100.00% [-100.00%, -100.00%] | $42.35 |
| map | international=0 | 240 | 128 | 0.0361 | -6.90% [-20.91%, 7.74%] | $21.07 | 0.421× | 67.88% | $4.02 | 33 (207 unfilled) | 8.56% [-30.73%, 48.71%] | $52.96 |
| series+map | all | 330 | 174 | 0.0308 | -3.25% [-18.47%, 13.17%] | $22.42 | 0.448× | 72.40% | $3.99 | 73 (257 unfilled) | 6.03% [-27.27%, 45.83%] | $57.95 |

#### Monthly breakdown

All metrics use identical linked rows within each kind/month. Unfitted blend months show —; counts include all rows.

| Kind | Month | Rows | Model log loss | Blended log loss | Kalshi log loss | Raw flat ROI (bets), unlimited Kelly final | Blended flat ROI (bets), unlimited Kelly final | Raw bets filled | Raw Flat ROI depth-capped [95% interval] | Raw Kelly depth-capped final | Blended bets filled | Blended Flat ROI depth-capped [95% interval] | Blended Kelly depth-capped final |
|---|---|---:|---:|---:|---:|---|---|---:|---|---:|---:|---|---:|
| map | 2026-07 | 425 | 0.658811 | 0.649652 | 0.647415 | -12.83% (242), $10.00 | -3.01% (73), $56.87 | 18 (224 unfilled) | 2.70% [-36.25%, 33.29%] | $52.09 | 9 (64 unfilled) | 18.30% [-34.68%, 57.08%] | $56.22 |
| map | 2026-08 | 394 | 0.690101 | 0.667763 | 0.664665 | -4.70% (265), $19.62 | -4.70% (138), $28.73 | 24 (241 unfilled) | 0.91% [-41.71%, 44.57%] | $47.31 | 13 (125 unfilled) | -3.86% [-68.55%, 71.11%] | $45.24 |
| map | 2026-09 | 111 | 0.694030 | 0.643824 | 0.627230 | -10.85% (73), $43.03 | -4.45% (38), $40.89 | 17 (56 unfilled) | 18.80% [-28.23%, 70.12%] | $69.74 | 8 (30 unfilled) | 58.82% [-21.36%, 134.15%] | $61.10 |
| map | 2026-10 | 61 | 0.683736 | 0.650992 | 0.634070 | -34.06% (30), $28.98 | -68.11% (9), $37.41 | 11 (19 unfilled) | -85.79% [-100.00%, -47.83%] | $28.17 | 7 (2 unfilled) | -100.00% [-100.00%, -100.00%] | $35.74 |
| series | 2026-07 | 237 | 0.634382 | 0.631278 | 0.632384 | -8.97% (144), $48.17 | 111.29% (11), $51.33 | 81 (63 unfilled) | -19.36% [-38.23%, 1.00%] | $20.20 | 5 (6 unfilled) | -100.00% [-100.00%, -100.00%] | $47.03 |
| series | 2026-08 | 193 | 0.672524 | 0.647335 | 0.649323 | -9.79% (138), $12.24 | 6.73% (24), $58.72 | 56 (82 unfilled) | 9.56% [-23.64%, 46.01%] | $71.52 | 11 (13 unfilled) | 63.87% [-53.39%, 211.54%] | $58.21 |
| series | 2026-09 | 88 | 0.667508 | 0.609886 | 0.609346 | 4.19% (69), $37.85 | -22.60% (19), $39.11 | 45 (24 unfilled) | 16.65% [-21.48%, 59.30%] | $60.50 | 10 (9 unfilled) | 22.44% [-100.00%, 145.35%] | $49.69 |
| series | 2026-10 | 68 | 0.660519 | 0.583968 | 0.575429 | -24.72% (52), $8.10 | -21.41% (18), $45.75 | 33 (19 unfilled) | -11.10% [-54.20%, 34.20%] | $28.26 | 10 (8 unfilled) | 13.07% [-100.00%, 126.35%] | $55.86 |

### player_round_glicko_rookie: Kalshi comparison and returns



#### Log loss vs Kalshi

| Kind | Slice | Rows | Model log loss | Kalshi log loss | Difference [95% interval] | Significant |
|---|---|---:|---:|---:|---|---|
| series | all | 586 | 0.634448 | 0.627894 | 0.006554 [-0.016401, 0.030330] | no |
| series | vct | 306 | 0.641432 | 0.648387 | -0.006955 [-0.035429, 0.019891] | no |
| series | vcl | 96 | 0.583192 | 0.616703 | -0.033511 [-0.079331, 0.011913] | no |
| series | gc | 151 | 0.642242 | 0.586384 | 0.055858 [-0.000525, 0.119067] | no |
| series | t3 | 0 | — | — | — | — |
| series | collegiate | 0 | — | — | — | — |
| series | offseason | 33 | 0.683129 | 0.660365 | 0.022763 [-0.040513, 0.087699] | no |
| series | international=1 | 77 | 0.671955 | 0.603125 | 0.068830 [0.014333, 0.125943] | yes |
| series | international=0 | 509 | 0.628774 | 0.631641 | -0.002867 [-0.027424, 0.022116] | no |
| map | all | 991 | 0.651453 | 0.651191 | 0.000262 [-0.012252, 0.012630] | no |
| map | vct | 598 | 0.677646 | 0.670975 | 0.006671 [-0.009520, 0.022284] | no |
| map | vcl | 144 | 0.604240 | 0.628359 | -0.024118 [-0.044918, -0.003792] | yes |
| map | gc | 193 | 0.594886 | 0.600063 | -0.005177 [-0.038501, 0.027829] | no |
| map | t3 | 0 | — | — | — | — |
| map | collegiate | 0 | — | — | — | — |
| map | offseason | 56 | 0.688114 | 0.674841 | 0.013274 [-0.019562, 0.046330] | no |
| map | international=1 | 128 | 0.660837 | 0.650599 | 0.010238 [-0.012596, 0.039916] | no |
| map | international=0 | 863 | 0.650061 | 0.651279 | -0.001217 [-0.015186, 0.013189] | no |

#### Full-Kelly returns

| Kind | Slice | Bets | Matches | Mean edge | Flat ROI [95% interval] | Kelly, LoL caps ($50 start) | Multiple | Max drawdown | Largest stake | Bets filled | Flat ROI depth-capped [95% interval] | Kelly depth-capped final |
|---|---|---:|---:|---:|---|---:|---:|---:|---:|---:|---|---:|
| series | all | 425 | 424 | 0.0879 | 3.76% [-7.73%, 15.64%] | $50.99 | 1.020× | 87.84% | $26.39 | 238 (187 unfilled) | 8.95% [-6.56%, 24.56%] | $100.98 |
| series | vct | 222 | 222 | 0.0760 | 4.33% [-12.25%, 20.95%] | $41.84 | 0.837× | 75.18% | $7.94 | 127 (95 unfilled) | 13.98% [-8.81%, 36.47%] | $124.13 |
| series | vcl | 60 | 60 | 0.0800 | 31.36% [-1.98%, 68.04%] | $179.53 | 3.591× | 32.42% | $21.12 | 34 (26 unfilled) | 2.97% [-31.65%, 36.75%] | $42.08 |
| series | gc | 119 | 119 | 0.1188 | -8.86% [-28.18%, 13.02%] | $21.18 | 0.424× | 66.13% | $5.28 | 60 (59 unfilled) | 8.25% [-22.83%, 41.12%] | $72.64 |
| series | t3 | 0 | 0 | — | — | $50.00 | 1.000× | 0.00% | $0.00 | 0 (0 unfilled) | — | $50.00 |
| series | collegiate | 0 | 0 | — | — | $50.00 | 1.000× | 0.00% | $0.00 | 0 (0 unfilled) | — | $50.00 |
| series | offseason | 24 | 23 | 0.0654 | -8.02% [-45.18%, 33.29%] | $38.15 | 0.763× | 40.76% | $5.16 | 17 (7 unfilled) | -14.11% [-58.63%, 33.07%] | $37.36 |
| series | international=1 | 54 | 53 | 0.0890 | -22.24% [-48.05%, 5.24%] | $14.23 | 0.285× | 76.57% | $5.16 | 41 (13 unfilled) | -18.56% [-47.90%, 12.60%] | $25.97 |
| series | international=0 | 371 | 371 | 0.0878 | 7.55% [-4.68%, 21.19%] | $158.95 | 3.179× | 80.96% | $28.65 | 197 (174 unfilled) | 14.67% [-3.65%, 32.74%] | $182.80 |
| map | all | 627 | 312 | 0.0632 | 2.43% [-5.78%, 10.87%] | $63.09 | 1.262× | 64.24% | $6.89 | 67 (560 unfilled) | -1.03% [-24.68%, 23.05%] | $46.01 |
| map | vct | 379 | 191 | 0.0603 | -0.03% [-11.29%, 10.86%] | $23.00 | 0.460× | 78.54% | $3.12 | 27 (352 unfilled) | -25.47% [-61.04%, 14.28%] | $32.14 |
| map | vcl | 77 | 36 | 0.0549 | 12.00% [-6.01%, 28.13%] | $73.17 | 1.463× | 10.00% | $4.06 | 11 (66 unfilled) | -21.47% [-79.38%, 17.37%] | $43.60 |
| map | gc | 130 | 65 | 0.0857 | 8.52% [-9.60%, 27.24%] | $100.60 | 2.012× | 22.99% | $8.77 | 26 (104 unfilled) | 18.98% [-18.97%, 57.17%] | $71.35 |
| map | t3 | 0 | 0 | — | — | $50.00 | 1.000× | 0.00% | $0.00 | 0 (0 unfilled) | — | $50.00 |
| map | collegiate | 0 | 0 | — | — | $50.00 | 1.000× | 0.00% | $0.00 | 0 (0 unfilled) | — | $50.00 |
| map | offseason | 41 | 20 | 0.0343 | -12.11% [-36.96%, 13.47%] | $41.29 | 0.826× | 30.28% | $2.53 | 3 (38 unfilled) | 119.37% [88.54%, 164.55%] | $56.36 |
| map | international=1 | 76 | 39 | 0.0370 | -6.41% [-23.85%, 12.15%] | $39.74 | 0.795× | 30.28% | $2.97 | 10 (66 unfilled) | 7.31% [-51.72%, 80.26%] | $45.98 |
| map | international=0 | 551 | 273 | 0.0668 | 3.65% [-5.03%, 13.11%] | $77.97 | 1.559× | 64.08% | $7.66 | 57 (494 unfilled) | -2.49% [-28.51%, 23.64%] | $49.93 |
| series+map | all | 1052 | 453 | 0.0732 | 2.97% [-5.40%, 11.50%] | $68.52 | 1.370× | 80.59% | $15.70 | 305 (747 unfilled) | 6.76% [-6.44%, 20.39%] | $42.04 |

#### Monthly market blend fits

UTC monthly fits use earlier rows of the same kind from 2025-09-01, excluding holdout; minimum 100 rows. logit(p_blend) = a·logit(mid) + b·(logit(p_model) − logit(mid)); inputs clipped to [0.01, 0.99], no intercept, ridge 1e-6. Unfitted rows use mid unchanged; excluded from blended tables: 0 rows. Rating parameters remain selected on the tuning window.

| Month | Kind | n | a | b | Status |
|---|---|---:|---:|---:|---|
| 2026-07 | series | 677 | 1.091498 | 0.672544 | fitted |
| 2026-07 | map | 1049 | 0.997951 | 0.671517 | fitted |
| 2026-08 | series | 677 | 1.091498 | 0.672544 | fitted |
| 2026-08 | map | 1049 | 0.997951 | 0.671517 | fitted |
| 2026-09 | series | 677 | 1.091498 | 0.672544 | fitted |
| 2026-09 | map | 1049 | 0.997951 | 0.671517 | fitted |
| 2026-10 | series | 677 | 1.091498 | 0.672544 | fitted |
| 2026-10 | map | 1049 | 0.997951 | 0.671517 | fitted |

#### Log loss vs Kalshi (blended)

| Kind | Slice | Rows | Model log loss | Kalshi log loss | Difference [95% interval] | Significant |
|---|---|---:|---:|---:|---|---|
| series | all | 586 | 0.622318 | 0.627894 | -0.005576 [-0.020191, 0.009213] | no |
| series | vct | 306 | 0.637466 | 0.648387 | -0.010920 [-0.029520, 0.006394] | no |
| series | vcl | 96 | 0.586430 | 0.616703 | -0.030273 [-0.058148, -0.001910] | yes |
| series | gc | 151 | 0.603958 | 0.586384 | 0.017574 [-0.017058, 0.054837] | no |
| series | t3 | 0 | — | — | — | — |
| series | collegiate | 0 | — | — | — | — |
| series | offseason | 33 | 0.670262 | 0.660365 | 0.009897 [-0.031902, 0.051352] | no |
| series | international=1 | 77 | 0.633384 | 0.603125 | 0.030260 [-0.000585, 0.061721] | no |
| series | international=0 | 509 | 0.620644 | 0.631641 | -0.010997 [-0.026497, 0.004648] | no |
| map | all | 991 | 0.646950 | 0.651191 | -0.004241 [-0.012604, 0.004072] | no |
| map | vct | 598 | 0.671406 | 0.670975 | 0.000431 [-0.010553, 0.010841] | no |
| map | vcl | 144 | 0.609016 | 0.628359 | -0.019342 [-0.034299, -0.004988] | yes |
| map | gc | 193 | 0.589455 | 0.600063 | -0.010608 [-0.032255, 0.010382] | no |
| map | t3 | 0 | — | — | — | — |
| map | collegiate | 0 | — | — | — | — |
| map | offseason | 56 | 0.681491 | 0.674841 | 0.006650 [-0.015486, 0.028369] | no |
| map | international=1 | 128 | 0.655142 | 0.650599 | 0.004543 [-0.010494, 0.022922] | no |
| map | international=0 | 863 | 0.645735 | 0.651279 | -0.005543 [-0.014876, 0.003918] | no |

#### Full-Kelly returns (blended)

| Kind | Slice | Bets | Matches | Mean edge | Flat ROI [95% interval] | Kelly, LoL caps ($50 start) | Multiple | Max drawdown | Largest stake | Bets filled | Flat ROI depth-capped [95% interval] | Kelly depth-capped final |
|---|---|---:|---:|---:|---|---:|---:|---:|---:|---:|---|---:|
| series | all | 348 | 347 | 0.0565 | 3.55% [-8.76%, 17.05%] | $112.83 | 2.257× | 69.99% | $27.56 | 192 (156 unfilled) | 9.29% [-7.15%, 26.02%] | $105.45 |
| series | vct | 178 | 178 | 0.0482 | -0.14% [-17.04%, 18.55%] | $125.92 | 2.518× | 44.93% | $13.62 | 98 (80 unfilled) | 11.99% [-11.00%, 38.11%] | $143.88 |
| series | vcl | 50 | 50 | 0.0467 | 37.23% [0.13%, 81.85%] | $145.39 | 2.908× | 17.21% | $15.29 | 28 (22 unfilled) | 11.34% [-25.02%, 48.45%] | $55.37 |
| series | gc | 101 | 101 | 0.0790 | -2.79% [-24.81%, 21.69%] | $21.61 | 0.432× | 66.37% | $5.33 | 52 (49 unfilled) | 12.75% [-20.55%, 49.11%] | $55.37 |
| series | t3 | 0 | 0 | — | — | $50.00 | 1.000× | 0.00% | $0.00 | 0 (0 unfilled) | — | $50.00 |
| series | collegiate | 0 | 0 | — | — | $50.00 | 1.000× | 0.00% | $0.00 | 0 (0 unfilled) | — | $50.00 |
| series | offseason | 19 | 18 | 0.0398 | -17.00% [-57.49%, 24.96%] | $34.65 | 0.693× | 36.91% | $4.99 | 14 (5 unfilled) | -26.56% [-71.94%, 22.45%] | $37.16 |
| series | international=1 | 43 | 42 | 0.0528 | -24.12% [-51.86%, 5.67%] | $18.01 | 0.360× | 70.27% | $4.99 | 34 (9 unfilled) | -10.64% [-43.05%, 22.90%] | $34.27 |
| series | international=0 | 305 | 305 | 0.0570 | 7.45% [-6.08%, 22.84%] | $306.34 | 6.127× | 58.62% | $36.80 | 158 (147 unfilled) | 13.57% [-4.98%, 33.11%] | $163.91 |
| map | all | 477 | 246 | 0.0430 | 2.77% [-7.02%, 12.32%] | $49.45 | 0.989× | 49.95% | $4.44 | 54 (423 unfilled) | -6.23% [-33.45%, 22.00%] | $48.30 |
| map | vct | 285 | 150 | 0.0408 | -2.60% [-15.28%, 10.56%] | $24.48 | 0.490× | 62.73% | $2.83 | 19 (266 unfilled) | -46.29% [-79.82%, -0.40%] | $36.34 |
| map | vcl | 59 | 28 | 0.0343 | 19.85% [0.34%, 36.91%] | $64.36 | 1.287× | 7.32% | $3.22 | 10 (49 unfilled) | -13.56% [-76.35%, 25.84%] | $48.83 |
| map | gc | 109 | 55 | 0.0583 | 12.01% [-7.68%, 33.31%] | $78.44 | 1.569× | 24.90% | $7.17 | 23 (86 unfilled) | 17.68% [-24.58%, 62.07%] | $66.33 |
| map | t3 | 0 | 0 | — | — | $50.00 | 1.000× | 0.00% | $0.00 | 0 (0 unfilled) | — | $50.00 |
| map | collegiate | 0 | 0 | — | — | $50.00 | 1.000× | 0.00% | $0.00 | 0 (0 unfilled) | — | $50.00 |
| map | offseason | 24 | 13 | 0.0208 | -17.49% [-54.97%, 29.10%] | $47.18 | 0.944× | 13.19% | $2.70 | 2 (22 unfilled) | 134.71% [104.58%, 164.55%] | $51.51 |
| map | international=1 | 40 | 23 | 0.0278 | -14.13% [-42.27%, 17.31%] | $45.11 | 0.902× | 15.19% | $2.70 | 7 (33 unfilled) | -14.89% [-84.30%, 78.31%] | $45.51 |
| map | international=0 | 437 | 223 | 0.0444 | 4.31% [-6.10%, 14.66%] | $54.35 | 1.087× | 50.36% | $4.67 | 47 (390 unfilled) | -4.94% [-32.41%, 23.69%] | $53.10 |
| series+map | all | 825 | 369 | 0.0487 | 3.10% [-6.14%, 12.86%] | $67.56 | 1.351× | 65.11% | $13.97 | 246 (579 unfilled) | 5.87% [-9.26%, 20.88%] | $52.09 |

#### Monthly breakdown

All metrics use identical linked rows within each kind/month. Unfitted blend months show —; counts include all rows.

| Kind | Month | Rows | Model log loss | Blended log loss | Kalshi log loss | Raw flat ROI (bets), unlimited Kelly final | Blended flat ROI (bets), unlimited Kelly final | Raw bets filled | Raw Flat ROI depth-capped [95% interval] | Raw Kelly depth-capped final | Blended bets filled | Blended Flat ROI depth-capped [95% interval] | Blended Kelly depth-capped final |
|---|---|---:|---:|---:|---:|---|---|---:|---|---:|---:|---|---:|
| map | 2026-07 | 425 | 0.651149 | 0.646502 | 0.647415 | -3.82% (251), $29.33 | -2.41% (190), $28.59 | 20 (231 unfilled) | 18.42% [-19.72%, 51.45%] | $58.29 | 16 (174 unfilled) | 19.00% [-27.23%, 60.54%] | $57.30 |
| map | 2026-08 | 394 | 0.659584 | 0.656599 | 0.664665 | 4.42% (259), $67.83 | 5.25% (199), $70.57 | 20 (239 unfilled) | -7.25% [-49.72%, 37.03%] | $43.78 | 17 (182 unfilled) | -16.38% [-58.66%, 28.24%] | $44.92 |
| map | 2026-09 | 111 | 0.628418 | 0.620009 | 0.627230 | 15.95% (87), $89.55 | 12.39% (74), $65.24 | 15 (72 unfilled) | 4.27% [-47.35%, 79.46%] | $56.43 | 12 (62 unfilled) | 11.16% [-49.43%, 91.57%] | $56.17 |
| map | 2026-10 | 61 | 0.642975 | 0.636780 | 0.634070 | -1.60% (30), $45.28 | -13.15% (14), $47.68 | 12 (18 unfilled) | -29.48% [-81.85%, 22.06%] | $39.92 | 9 (5 unfilled) | -54.56% [-100.00%, 2.71%] | $41.92 |
| series | 2026-07 | 237 | 0.632933 | 0.624852 | 0.632384 | 7.96% (162), $103.93 | 6.70% (131), $79.70 | 94 (68 unfilled) | -0.69% [-22.90%, 20.97%] | $38.81 | 75 (56 unfilled) | -0.75% [-23.90%, 24.01%] | $42.67 |
| series | 2026-08 | 193 | 0.646108 | 0.641039 | 0.649323 | 0.65% (147), $35.55 | 1.08% (119), $109.77 | 70 (77 unfilled) | 21.96% [-5.50%, 52.88%] | $135.22 | 55 (64 unfilled) | 18.26% [-13.89%, 55.04%] | $138.26 |
| series | 2026-09 | 88 | 0.619694 | 0.602216 | 0.609346 | 7.62% (65), $59.47 | 5.94% (57), $53.17 | 41 (24 unfilled) | 22.96% [-14.99%, 65.12%] | $94.93 | 36 (21 unfilled) | 22.60% [-16.04%, 66.61%] | $72.45 |
| series | 2026-10 | 68 | 0.625727 | 0.586365 | 0.575429 | -5.48% (51), $28.59 | -2.66% (41), $30.04 | 33 (18 unfilled) | -8.52% [-48.35%, 38.42%] | $31.10 | 26 (15 unfilled) | 0.90% [-48.09%, 54.06%] | $35.42 |

### player_round_glicko_rookie_tier_revert: Kalshi comparison and returns



#### Log loss vs Kalshi

| Kind | Slice | Rows | Model log loss | Kalshi log loss | Difference [95% interval] | Significant |
|---|---|---:|---:|---:|---|---|
| series | all | 586 | 0.636720 | 0.627894 | 0.008826 [-0.014982, 0.033541] | no |
| series | vct | 306 | 0.647848 | 0.648387 | -0.000539 [-0.030823, 0.028161] | no |
| series | vcl | 96 | 0.578044 | 0.616703 | -0.038659 [-0.084654, 0.006892] | no |
| series | gc | 151 | 0.641802 | 0.586384 | 0.055419 [-0.001577, 0.120122] | no |
| series | t3 | 0 | — | — | — | — |
| series | collegiate | 0 | — | — | — | — |
| series | offseason | 33 | 0.680970 | 0.660365 | 0.020605 [-0.042233, 0.084869] | no |
| series | international=1 | 77 | 0.664138 | 0.603125 | 0.061014 [0.011042, 0.114989] | yes |
| series | international=0 | 509 | 0.632572 | 0.631641 | 0.000931 [-0.025337, 0.027684] | no |
| map | all | 991 | 0.651675 | 0.651191 | 0.000484 [-0.011628, 0.012532] | no |
| map | vct | 598 | 0.676169 | 0.670975 | 0.005194 [-0.011823, 0.020945] | no |
| map | vcl | 144 | 0.605885 | 0.628359 | -0.022474 [-0.042731, -0.003064] | yes |
| map | gc | 193 | 0.600631 | 0.600063 | 0.000568 [-0.032547, 0.032837] | no |
| map | t3 | 0 | — | — | — | — |
| map | collegiate | 0 | — | — | — | — |
| map | offseason | 56 | 0.683779 | 0.674841 | 0.008938 [-0.021742, 0.041724] | no |
| map | international=1 | 128 | 0.656590 | 0.650599 | 0.005991 [-0.015403, 0.033852] | no |
| map | international=0 | 863 | 0.650946 | 0.651279 | -0.000332 [-0.013570, 0.013571] | no |

#### Full-Kelly returns

| Kind | Slice | Bets | Matches | Mean edge | Flat ROI [95% interval] | Kelly, LoL caps ($50 start) | Multiple | Max drawdown | Largest stake | Bets filled | Flat ROI depth-capped [95% interval] | Kelly depth-capped final |
|---|---|---:|---:|---:|---|---:|---:|---:|---:|---:|---|---:|
| series | all | 428 | 427 | 0.0910 | 5.38% [-5.93%, 17.12%] | $148.09 | 2.962× | 71.79% | $32.57 | 237 (191 unfilled) | 12.01% [-2.85%, 27.12%] | $199.18 |
| series | vct | 220 | 220 | 0.0829 | 8.21% [-8.39%, 25.40%] | $91.04 | 1.821× | 64.50% | $12.68 | 121 (99 unfilled) | 17.79% [-4.51%, 40.89%] | $183.88 |
| series | vcl | 65 | 65 | 0.0757 | 31.44% [0.79%, 66.36%] | $252.24 | 5.045× | 18.14% | $22.87 | 41 (24 unfilled) | 11.31% [-16.77%, 39.08%] | $59.66 |
| series | gc | 122 | 122 | 0.1169 | -10.52% [-30.28%, 11.55%] | $18.53 | 0.371× | 68.91% | $4.94 | 61 (61 unfilled) | 8.84% [-19.14%, 40.28%] | $88.22 |
| series | t3 | 0 | 0 | — | — | $50.00 | 1.000× | 0.00% | $0.00 | 0 (0 unfilled) | — | $50.00 |
| series | collegiate | 0 | 0 | — | — | $50.00 | 1.000× | 0.00% | $0.00 | 0 (0 unfilled) | — | $50.00 |
| series | offseason | 21 | 20 | 0.0726 | -12.46% [-54.53%, 31.60%] | $39.32 | 0.786× | 27.97% | $4.86 | 14 (7 unfilled) | -22.06% [-67.89%, 32.43%] | $39.28 |
| series | international=1 | 51 | 50 | 0.0876 | -27.15% [-51.73%, 1.51%] | $17.56 | 0.351× | 70.56% | $4.86 | 39 (12 unfilled) | -21.78% [-51.43%, 10.11%] | $33.82 |
| series | international=0 | 377 | 377 | 0.0914 | 9.79% [-2.88%, 22.69%] | $369.90 | 7.398× | 66.60% | $37.52 | 198 (179 unfilled) | 18.66% [1.74%, 36.61%] | $275.46 |
| map | all | 603 | 305 | 0.0634 | 3.83% [-4.87%, 12.27%] | $147.62 | 2.952× | 48.58% | $11.51 | 65 (538 unfilled) | -3.59% [-28.67%, 23.52%] | $56.90 |
| map | vct | 363 | 186 | 0.0628 | 2.57% [-8.56%, 14.84%] | $59.41 | 1.188× | 60.70% | $4.13 | 22 (341 unfilled) | -25.57% [-65.49%, 22.90%] | $38.36 |
| map | vcl | 71 | 34 | 0.0552 | 15.80% [-1.63%, 32.81%] | $64.21 | 1.284× | 11.77% | $3.13 | 11 (60 unfilled) | -2.84% [-62.89%, 33.28%] | $47.12 |
| map | gc | 137 | 69 | 0.0770 | 3.67% [-14.50%, 22.61%] | $75.13 | 1.503× | 30.02% | $6.81 | 30 (107 unfilled) | 2.94% [-34.80%, 39.09%] | $65.02 |
| map | t3 | 0 | 0 | — | — | $50.00 | 1.000× | 0.00% | $0.00 | 0 (0 unfilled) | — | $50.00 |
| map | collegiate | 0 | 0 | — | — | $50.00 | 1.000× | 0.00% | $0.00 | 0 (0 unfilled) | — | $50.00 |
| map | offseason | 32 | 16 | 0.0301 | -7.72% [-34.96%, 20.67%] | $58.55 | 1.171× | 7.67% | $4.04 | 2 (30 unfilled) | 134.71% [104.58%, 164.55%] | $59.18 |
| map | international=1 | 63 | 33 | 0.0367 | -0.88% [-23.75%, 21.51%] | $62.10 | 1.242× | 13.57% | $4.04 | 7 (56 unfilled) | 9.11% [-63.61%, 102.75%] | $51.81 |
| map | international=0 | 540 | 272 | 0.0665 | 4.38% [-4.50%, 13.84%] | $116.20 | 2.324× | 48.62% | $9.64 | 58 (482 unfilled) | -5.13% [-32.32%, 22.92%] | $54.13 |
| series+map | all | 1031 | 448 | 0.0748 | 4.47% [-4.01%, 13.16%] | $289.08 | 5.782× | 57.77% | $41.94 | 302 (729 unfilled) | 8.64% [-5.31%, 22.77%] | $113.47 |

#### Monthly market blend fits

UTC monthly fits use earlier rows of the same kind from 2025-09-01, excluding holdout; minimum 100 rows. logit(p_blend) = a·logit(mid) + b·(logit(p_model) − logit(mid)); inputs clipped to [0.01, 0.99], no intercept, ridge 1e-6. Unfitted rows use mid unchanged; excluded from blended tables: 0 rows. Rating parameters remain selected on the tuning window.

| Month | Kind | n | a | b | Status |
|---|---|---:|---:|---:|---|
| 2026-07 | series | 677 | 1.087605 | 0.659058 | fitted |
| 2026-07 | map | 1049 | 1.070712 | 0.743860 | fitted |
| 2026-08 | series | 677 | 1.087605 | 0.659058 | fitted |
| 2026-08 | map | 1049 | 1.070712 | 0.743860 | fitted |
| 2026-09 | series | 677 | 1.087605 | 0.659058 | fitted |
| 2026-09 | map | 1049 | 1.070712 | 0.743860 | fitted |
| 2026-10 | series | 677 | 1.087605 | 0.659058 | fitted |
| 2026-10 | map | 1049 | 1.070712 | 0.743860 | fitted |

#### Log loss vs Kalshi (blended)

| Kind | Slice | Rows | Model log loss | Kalshi log loss | Difference [95% interval] | Significant |
|---|---|---:|---:|---:|---|---|
| series | all | 586 | 0.623173 | 0.627894 | -0.004721 [-0.019561, 0.010691] | no |
| series | vct | 306 | 0.640631 | 0.648387 | -0.007756 [-0.027681, 0.010607] | no |
| series | vcl | 96 | 0.583598 | 0.616703 | -0.033105 [-0.060385, -0.004408] | yes |
| series | gc | 151 | 0.603043 | 0.586384 | 0.016659 [-0.017994, 0.054947] | no |
| series | t3 | 0 | — | — | — | — |
| series | collegiate | 0 | — | — | — | — |
| series | offseason | 33 | 0.668529 | 0.660365 | 0.008163 [-0.033022, 0.048558] | no |
| series | international=1 | 77 | 0.628794 | 0.603125 | 0.025670 [-0.003459, 0.055564] | no |
| series | international=0 | 509 | 0.622322 | 0.631641 | -0.009318 [-0.026084, 0.006899] | no |
| map | all | 991 | 0.647051 | 0.651191 | -0.004140 [-0.012836, 0.004586] | no |
| map | vct | 598 | 0.671534 | 0.670975 | 0.000559 [-0.011262, 0.011839] | no |
| map | vcl | 144 | 0.606814 | 0.628359 | -0.021544 [-0.037418, -0.007048] | yes |
| map | gc | 193 | 0.591802 | 0.600063 | -0.008262 [-0.030898, 0.014216] | no |
| map | t3 | 0 | — | — | — | — |
| map | collegiate | 0 | — | — | — | — |
| map | offseason | 56 | 0.679490 | 0.674841 | 0.004649 [-0.017580, 0.027368] | no |
| map | international=1 | 128 | 0.651736 | 0.650599 | 0.001137 [-0.014260, 0.019587] | no |
| map | international=0 | 863 | 0.646356 | 0.651279 | -0.004922 [-0.014211, 0.005185] | no |

#### Full-Kelly returns (blended)

| Kind | Slice | Bets | Matches | Mean edge | Flat ROI [95% interval] | Kelly, LoL caps ($50 start) | Multiple | Max drawdown | Largest stake | Bets filled | Flat ROI depth-capped [95% interval] | Kelly depth-capped final |
|---|---|---:|---:|---:|---|---:|---:|---:|---:|---:|---|---:|
| series | all | 350 | 349 | 0.0582 | 7.48% [-4.63%, 20.91%] | $97.39 | 1.948× | 67.16% | $17.37 | 195 (155 unfilled) | 17.01% [0.99%, 33.70%] | $126.88 |
| series | vct | 173 | 173 | 0.0545 | 6.34% [-10.33%, 25.20%] | $63.79 | 1.276× | 59.18% | $8.59 | 97 (76 unfilled) | 18.59% [-5.43%, 43.82%] | $108.18 |
| series | vcl | 55 | 55 | 0.0436 | 39.00% [4.20%, 78.14%] | $156.58 | 3.132× | 6.04% | $14.67 | 33 (22 unfilled) | 22.33% [-8.88%, 54.01%] | $59.44 |
| series | gc | 104 | 104 | 0.0755 | -4.45% [-24.65%, 17.94%] | $29.93 | 0.599× | 61.34% | $6.06 | 52 (52 unfilled) | 18.96% [-13.26%, 53.21%] | $69.16 |
| series | t3 | 0 | 0 | — | — | $50.00 | 1.000× | 0.00% | $0.00 | 0 (0 unfilled) | — | $50.00 |
| series | collegiate | 0 | 0 | — | — | $50.00 | 1.000× | 0.00% | $0.00 | 0 (0 unfilled) | — | $50.00 |
| series | offseason | 18 | 17 | 0.0386 | -8.91% [-52.61%, 40.38%] | $41.42 | 0.828× | 22.62% | $4.86 | 13 (5 unfilled) | -16.08% [-64.42%, 38.77%] | $40.18 |
| series | international=1 | 38 | 37 | 0.0533 | -21.96% [-52.50%, 9.47%] | $25.97 | 0.519× | 58.10% | $4.86 | 29 (9 unfilled) | -5.52% [-39.82%, 32.61%] | $42.42 |
| series | international=0 | 312 | 312 | 0.0588 | 11.08% [-2.49%, 25.38%] | $189.61 | 3.792× | 67.11% | $21.33 | 166 (146 unfilled) | 20.95% [2.54%, 40.28%] | $160.52 |
| map | all | 474 | 242 | 0.0478 | 4.29% [-4.52%, 13.71%] | $43.97 | 0.879× | 62.98% | $5.98 | 54 (420 unfilled) | -3.34% [-30.01%, 24.86%] | $44.82 |
| map | vct | 292 | 150 | 0.0459 | 1.62% [-10.63%, 14.65%] | $27.14 | 0.543× | 66.30% | $3.43 | 18 (274 unfilled) | -43.24% [-79.82%, 3.17%] | $35.89 |
| map | vcl | 55 | 26 | 0.0414 | 11.61% [-8.59%, 28.04%] | $62.24 | 1.245× | 5.38% | $3.05 | 9 (46 unfilled) | -3.67% [-72.19%, 32.68%] | $48.11 |
| map | gc | 107 | 56 | 0.0613 | 9.21% [-10.07%, 30.38%] | $60.05 | 1.201× | 24.76% | $5.81 | 25 (82 unfilled) | 14.32% [-23.28%, 52.26%] | $61.25 |
| map | t3 | 0 | 0 | — | — | $50.00 | 1.000× | 0.00% | $0.00 | 0 (0 unfilled) | — | $50.00 |
| map | collegiate | 0 | 0 | — | — | $50.00 | 1.000× | 0.00% | $0.00 | 0 (0 unfilled) | — | $50.00 |
| map | offseason | 20 | 10 | 0.0208 | -3.16% [-43.91%, 45.71%] | $52.06 | 1.041× | 7.17% | $2.52 | 2 (18 unfilled) | 134.71% [104.58%, 164.55%] | $52.71 |
| map | international=1 | 38 | 21 | 0.0301 | -0.11% [-31.49%, 31.84%] | $56.50 | 1.130× | 10.90% | $3.02 | 6 (32 unfilled) | -0.78% [-82.07%, 113.97%] | $47.67 |
| map | international=0 | 436 | 221 | 0.0493 | 4.68% [-5.33%, 14.54%] | $38.50 | 0.770× | 63.13% | $5.73 | 48 (388 unfilled) | -3.66% [-31.84%, 25.59%] | $46.91 |
| series+map | all | 824 | 373 | 0.0522 | 5.65% [-3.14%, 15.33%] | $85.62 | 1.712× | 71.92% | $13.28 | 249 (575 unfilled) | 12.59% [-2.52%, 27.75%] | $65.60 |

#### Monthly breakdown

All metrics use identical linked rows within each kind/month. Unfitted blend months show —; counts include all rows.

| Kind | Month | Rows | Model log loss | Blended log loss | Kalshi log loss | Raw flat ROI (bets), unlimited Kelly final | Blended flat ROI (bets), unlimited Kelly final | Raw bets filled | Raw Flat ROI depth-capped [95% interval] | Raw Kelly depth-capped final | Blended bets filled | Blended Flat ROI depth-capped [95% interval] | Blended Kelly depth-capped final |
|---|---|---:|---:|---:|---:|---|---|---:|---|---:|---:|---|---:|
| map | 2026-07 | 425 | 0.647531 | 0.643697 | 0.647415 | -0.91% (237), $62.51 | 2.11% (185), $43.91 | 18 (219 unfilled) | 5.64% [-42.50%, 51.31%] | $63.41 | 15 (170 unfilled) | 27.04% [-15.24%, 66.45%] | $58.49 |
| map | 2026-08 | 394 | 0.662793 | 0.658986 | 0.664665 | 6.26% (261), $79.62 | 5.68% (207), $43.73 | 21 (240 unfilled) | -3.40% [-49.69%, 42.27%] | $48.24 | 18 (189 unfilled) | -13.81% [-54.11%, 29.92%] | $44.77 |
| map | 2026-09 | 111 | 0.634649 | 0.624780 | 0.627230 | 10.02% (79), $75.14 | 8.23% (69), $60.92 | 15 (64 unfilled) | 3.94% [-49.95%, 71.78%] | $54.79 | 13 (56 unfilled) | 4.34% [-52.88%, 84.17%] | $50.82 |
| map | 2026-10 | 61 | 0.639720 | 0.633860 | 0.634070 | 3.66% (26), $48.88 | -7.74% (13), $47.26 | 11 (15 unfilled) | -29.11% [-80.88%, 32.24%] | $41.94 | 8 (5 unfilled) | -48.77% [-100.00%, 14.23%] | $42.02 |
| series | 2026-07 | 237 | 0.630929 | 0.623362 | 0.632384 | 12.09% (160), $156.83 | 10.29% (137), $86.61 | 87 (73 unfilled) | 6.17% [-16.94%, 29.69%] | $51.62 | 77 (60 unfilled) | 3.44% [-17.94%, 27.45%] | $34.05 |
| series | 2026-08 | 193 | 0.655696 | 0.645107 | 0.649323 | 1.54% (147), $53.96 | 6.73% (114), $55.13 | 69 (78 unfilled) | 19.07% [-9.68%, 51.52%] | $171.42 | 55 (59 unfilled) | 28.95% [-4.65%, 64.25%] | $138.43 |
| series | 2026-09 | 88 | 0.622652 | 0.604020 | 0.609346 | 3.29% (69), $55.48 | 3.70% (58), $71.27 | 46 (23 unfilled) | 21.33% [-12.63%, 56.84%] | $109.54 | 37 (21 unfilled) | 29.77% [-8.93%, 74.12%] | $88.78 |
| series | 2026-10 | 68 | 0.621248 | 0.585048 | 0.575429 | -1.60% (52), $38.70 | 5.54% (41), $35.59 | 35 (17 unfilled) | 0.34% [-38.65%, 46.47%] | $43.48 | 26 (15 unfilled) | 13.85% [-34.57%, 65.77%] | $39.95 |

### team_elo+none: Kalshi comparison and returns

none

#### Log loss vs Kalshi

| Kind | Slice | Rows | Model log loss | Kalshi log loss | Difference [95% interval] | Significant |
|---|---|---:|---:|---:|---|---|
| series | all | 586 | 0.654951 | 0.627894 | 0.027057 [0.005745, 0.050260] | yes |
| series | vct | 306 | 0.674893 | 0.648387 | 0.026506 [-0.002664, 0.056761] | no |
| series | vcl | 96 | 0.607534 | 0.616703 | -0.009169 [-0.050140, 0.030573] | no |
| series | gc | 151 | 0.649853 | 0.586384 | 0.063469 [0.014400, 0.118587] | yes |
| series | t3 | 0 | — | — | — | — |
| series | collegiate | 0 | — | — | — | — |
| series | offseason | 33 | 0.631306 | 0.660365 | -0.029059 [-0.092768, 0.030661] | no |
| series | international=1 | 77 | 0.636434 | 0.603125 | 0.033309 [-0.015653, 0.082010] | no |
| series | international=0 | 509 | 0.657753 | 0.631641 | 0.026112 [0.002613, 0.050552] | yes |
| map | all | 991 | 0.676730 | 0.651191 | 0.025539 [0.011510, 0.039860] | yes |
| map | vct | 598 | 0.700498 | 0.670975 | 0.029523 [0.009417, 0.049391] | yes |
| map | vcl | 144 | 0.625081 | 0.628359 | -0.003277 [-0.028757, 0.020597] | no |
| map | gc | 193 | 0.640775 | 0.600063 | 0.040711 [0.007520, 0.077974] | yes |
| map | t3 | 0 | — | — | — | — |
| map | collegiate | 0 | — | — | — | — |
| map | offseason | 56 | 0.679656 | 0.674841 | 0.004815 [-0.013551, 0.024200] | no |
| map | international=1 | 128 | 0.650049 | 0.650599 | -0.000550 [-0.023246, 0.025750] | no |
| map | international=0 | 863 | 0.680687 | 0.651279 | 0.029409 [0.013069, 0.046689] | yes |

#### Full-Kelly returns

| Kind | Slice | Bets | Matches | Mean edge | Flat ROI [95% interval] | Kelly, LoL caps ($50 start) | Multiple | Max drawdown | Largest stake | Bets filled | Flat ROI depth-capped [95% interval] | Kelly depth-capped final |
|---|---|---:|---:|---:|---|---:|---:|---:|---:|---:|---|---:|
| series | all | 403 | 403 | 0.0853 | -9.03% [-20.58%, 2.62%] | $1.24 | 0.025× | 99.40% | $15.72 | 215 (188 unfilled) | -2.99% [-19.10%, 13.33%] | $20.46 |
| series | vct | 196 | 196 | 0.0792 | -10.12% [-26.26%, 6.58%] | $7.08 | 0.142× | 88.95% | $5.70 | 103 (93 unfilled) | -2.10% [-24.80%, 23.13%] | $25.96 |
| series | vcl | 65 | 65 | 0.0616 | 0.51% [-31.99%, 37.14%] | $75.11 | 1.502× | 57.99% | $12.99 | 38 (27 unfilled) | -13.34% [-43.02%, 18.88%] | $41.21 |
| series | gc | 120 | 120 | 0.1142 | -13.87% [-34.98%, 8.16%] | $7.60 | 0.152× | 88.43% | $4.59 | 58 (62 unfilled) | -2.40% [-35.97%, 33.40%] | $47.32 |
| series | t3 | 0 | 0 | — | — | $50.00 | 1.000× | 0.00% | $0.00 | 0 (0 unfilled) | — | $50.00 |
| series | collegiate | 0 | 0 | — | — | $50.00 | 1.000× | 0.00% | $0.00 | 0 (0 unfilled) | — | $50.00 |
| series | offseason | 22 | 22 | 0.0521 | -1.07% [-41.77%, 40.25%] | $62.28 | 1.246× | 15.94% | $5.69 | 16 (6 unfilled) | 13.64% [-36.66%, 63.55%] | $56.03 |
| series | international=1 | 52 | 52 | 0.0733 | -14.24% [-41.29%, 11.53%] | $25.48 | 0.510× | 65.50% | $5.69 | 39 (13 unfilled) | -1.25% [-31.68%, 29.59%] | $37.13 |
| series | international=0 | 351 | 351 | 0.0871 | -8.25% [-21.12%, 5.12%] | $3.41 | 0.068× | 98.06% | $13.78 | 176 (175 unfilled) | -3.38% [-21.27%, 15.73%] | $27.08 |
| map | all | 610 | 305 | 0.0710 | -10.10% [-17.73%, -2.68%] | $1.19 | 0.024× | 98.07% | $5.42 | 70 (540 unfilled) | -8.05% [-30.41%, 15.68%] | $38.74 |
| map | vct | 403 | 201 | 0.0712 | -9.80% [-18.74%, -0.46%] | $5.60 | 0.112× | 89.05% | $2.92 | 33 (370 unfilled) | -17.71% [-49.79%, 13.70%] | $36.22 |
| map | vcl | 64 | 32 | 0.0538 | -3.38% [-21.54%, 12.87%] | $38.01 | 0.760× | 39.59% | $5.28 | 13 (51 unfilled) | -40.08% [-87.77%, -1.47%] | $36.53 |
| map | gc | 119 | 60 | 0.0853 | -14.18% [-34.74%, 6.58%] | $25.97 | 0.519× | 68.23% | $4.77 | 24 (95 unfilled) | 22.48% [-22.64%, 67.27%] | $74.42 |
| map | t3 | 0 | 0 | — | — | $50.00 | 1.000× | 0.00% | $0.00 | 0 (0 unfilled) | — | $50.00 |
| map | collegiate | 0 | 0 | — | — | $50.00 | 1.000× | 0.00% | $0.00 | 0 (0 unfilled) | — | $50.00 |
| map | offseason | 24 | 12 | 0.0434 | -12.78% [-32.98%, 4.96%] | $43.49 | 0.870× | 17.50% | $2.84 | 0 (24 unfilled) | — | $50.00 |
| map | international=1 | 64 | 32 | 0.0541 | -3.55% [-19.58%, 12.39%] | $47.99 | 0.960× | 27.59% | $4.55 | 9 (55 unfilled) | -19.16% [-72.93%, 33.99%] | $42.15 |
| map | international=0 | 546 | 273 | 0.0730 | -10.87% [-18.67%, -3.02%] | $1.58 | 0.032× | 97.49% | $5.28 | 61 (485 unfilled) | -6.41% [-31.84%, 19.11%] | $46.78 |
| series+map | all | 1013 | 469 | 0.0767 | -9.67% [-17.54%, -2.04%] | $0.94 | 0.019× | 99.42% | $12.52 | 285 (728 unfilled) | -4.23% [-18.58%, 11.21%] | $20.32 |

#### Monthly market blend fits

UTC monthly fits use earlier rows of the same kind from 2025-09-01, excluding holdout; minimum 100 rows. logit(p_blend) = a·logit(mid) + b·(logit(p_model) − logit(mid)); inputs clipped to [0.01, 0.99], no intercept, ridge 1e-6. Unfitted rows use mid unchanged; excluded from blended tables: 0 rows. Rating parameters remain selected on the tuning window.

| Month | Kind | n | a | b | Status |
|---|---|---:|---:|---:|---|
| 2026-07 | series | 677 | 0.930056 | 0.134077 | fitted |
| 2026-07 | map | 1049 | 0.888658 | 0.392963 | fitted |
| 2026-08 | series | 677 | 0.930056 | 0.134077 | fitted |
| 2026-08 | map | 1049 | 0.888658 | 0.392963 | fitted |
| 2026-09 | series | 677 | 0.930056 | 0.134077 | fitted |
| 2026-09 | map | 1049 | 0.888658 | 0.392963 | fitted |
| 2026-10 | series | 677 | 0.930056 | 0.134077 | fitted |
| 2026-10 | map | 1049 | 0.888658 | 0.392963 | fitted |

#### Log loss vs Kalshi (blended)

| Kind | Slice | Rows | Model log loss | Kalshi log loss | Difference [95% interval] | Significant |
|---|---|---:|---:|---:|---|---|
| series | all | 586 | 0.627864 | 0.627894 | -0.000030 [-0.004125, 0.003826] | no |
| series | vct | 306 | 0.647785 | 0.648387 | -0.000602 [-0.005622, 0.004493] | no |
| series | vcl | 96 | 0.614306 | 0.616703 | -0.002397 [-0.012206, 0.006797] | no |
| series | gc | 151 | 0.590378 | 0.586384 | 0.003994 [-0.003960, 0.012393] | no |
| series | t3 | 0 | — | — | — | — |
| series | collegiate | 0 | — | — | — | — |
| series | offseason | 33 | 0.654109 | 0.660365 | -0.006256 [-0.019636, 0.005895] | no |
| series | international=1 | 77 | 0.607367 | 0.603125 | 0.004242 [-0.004203, 0.012054] | no |
| series | international=0 | 509 | 0.630965 | 0.631641 | -0.000676 [-0.005032, 0.003583] | no |
| map | all | 991 | 0.656282 | 0.651191 | 0.005091 [-0.000412, 0.010272] | no |
| map | vct | 598 | 0.675090 | 0.670975 | 0.004114 [-0.003805, 0.011513] | no |
| map | vcl | 144 | 0.627852 | 0.628359 | -0.000507 [-0.011199, 0.009142] | no |
| map | gc | 193 | 0.613771 | 0.600063 | 0.013707 [0.000185, 0.027252] | yes |
| map | t3 | 0 | — | — | — | — |
| map | collegiate | 0 | — | — | — | — |
| map | offseason | 56 | 0.675068 | 0.674841 | 0.000227 [-0.006161, 0.006999] | no |
| map | international=1 | 128 | 0.649283 | 0.650599 | -0.001316 [-0.009718, 0.008288] | no |
| map | international=0 | 863 | 0.657320 | 0.651279 | 0.006042 [0.000133, 0.012474] | yes |

#### Full-Kelly returns (blended)

| Kind | Slice | Bets | Matches | Mean edge | Flat ROI [95% interval] | Kelly, LoL caps ($50 start) | Multiple | Max drawdown | Largest stake | Bets filled | Flat ROI depth-capped [95% interval] | Kelly depth-capped final |
|---|---|---:|---:|---:|---|---:|---:|---:|---:|---:|---|---:|
| series | all | 72 | 72 | 0.0141 | 7.93% [-32.36%, 52.50%] | $43.07 | 0.861× | 41.63% | $4.37 | 36 (36 unfilled) | 15.46% [-41.62%, 79.54%] | $61.08 |
| series | vct | 30 | 30 | 0.0155 | 20.42% [-40.75%, 87.58%] | $50.77 | 1.015× | 29.74% | $4.35 | 14 (16 unfilled) | 68.42% [-42.26%, 198.93%] | $61.21 |
| series | vcl | 9 | 9 | 0.0055 | 104.08% [-57.58%, 301.92%] | $51.21 | 1.024× | 3.81% | $1.02 | 4 (5 unfilled) | -100.00% [-100.00%, -100.00%] | $48.16 |
| series | gc | 31 | 31 | 0.0156 | -32.83% [-79.62%, 20.61%] | $40.12 | 0.802× | 33.29% | $3.83 | 16 (15 unfilled) | -2.89% [-80.86%, 90.67%] | $50.98 |
| series | t3 | 0 | 0 | — | — | $50.00 | 1.000× | 0.00% | $0.00 | 0 (0 unfilled) | — | $50.00 |
| series | collegiate | 0 | 0 | — | — | $50.00 | 1.000× | 0.00% | $0.00 | 0 (0 unfilled) | — | $50.00 |
| series | offseason | 2 | 2 | 0.0084 | 21.52% [-100.00%, 144.20%] | $50.70 | 1.014× | 0.95% | $0.78 | 2 (0 unfilled) | 21.52% [-100.00%, 144.20%] | $50.70 |
| series | international=1 | 8 | 8 | 0.0152 | -59.24% [-100.00%, 22.71%] | $44.10 | 0.882× | 14.32% | $2.17 | 3 (5 unfilled) | 9.12% [-100.00%, 228.41%] | $50.31 |
| series | international=0 | 64 | 64 | 0.0139 | 16.35% [-27.20%, 69.18%] | $48.76 | 0.975× | 36.34% | $4.41 | 33 (31 unfilled) | 16.04% [-46.68%, 86.46%] | $60.70 |
| map | all | 258 | 138 | 0.0354 | -6.41% [-19.86%, 6.62%] | $19.94 | 0.399× | 69.35% | $3.99 | 37 (221 unfilled) | -3.24% [-40.27%, 34.63%] | $44.54 |
| map | vct | 156 | 82 | 0.0357 | -5.55% [-21.84%, 10.30%] | $34.32 | 0.686× | 41.58% | $3.19 | 14 (142 unfilled) | -19.46% [-79.47%, 41.75%] | $44.86 |
| map | vcl | 18 | 10 | 0.0292 | -13.40% [-63.94%, 29.14%] | $47.97 | 0.959× | 14.13% | $2.92 | 4 (14 unfilled) | -100.00% [-100.00%, -100.00%] | $42.88 |
| map | gc | 78 | 43 | 0.0377 | -7.01% [-33.56%, 22.36%] | $30.92 | 0.618× | 50.81% | $3.48 | 19 (59 unfilled) | 29.17% [-21.26%, 83.39%] | $57.95 |
| map | t3 | 0 | 0 | — | — | $50.00 | 1.000× | 0.00% | $0.00 | 0 (0 unfilled) | — | $50.00 |
| map | collegiate | 0 | 0 | — | — | $50.00 | 1.000× | 0.00% | $0.00 | 0 (0 unfilled) | — | $50.00 |
| map | offseason | 6 | 3 | 0.0154 | 0.19% [-1.88%, 2.29%] | $49.58 | 0.992× | 0.84% | $2.65 | 0 (6 unfilled) | — | $50.00 |
| map | international=1 | 18 | 10 | 0.0265 | 0.15% [-32.73%, 29.43%] | $47.71 | 0.954× | 12.89% | $3.15 | 4 (14 unfilled) | -100.00% [-100.00%, -100.00%] | $42.35 |
| map | international=0 | 240 | 128 | 0.0361 | -6.90% [-20.91%, 7.74%] | $21.07 | 0.421× | 67.88% | $4.02 | 33 (207 unfilled) | 8.56% [-30.73%, 48.71%] | $52.96 |
| series+map | all | 330 | 174 | 0.0308 | -3.25% [-18.47%, 13.17%] | $22.42 | 0.448× | 72.40% | $3.99 | 73 (257 unfilled) | 6.03% [-27.27%, 45.83%] | $57.95 |

#### Monthly breakdown

All metrics use identical linked rows within each kind/month. Unfitted blend months show —; counts include all rows.

| Kind | Month | Rows | Model log loss | Blended log loss | Kalshi log loss | Raw flat ROI (bets), unlimited Kelly final | Blended flat ROI (bets), unlimited Kelly final | Raw bets filled | Raw Flat ROI depth-capped [95% interval] | Raw Kelly depth-capped final | Blended bets filled | Blended Flat ROI depth-capped [95% interval] | Blended Kelly depth-capped final |
|---|---|---:|---:|---:|---:|---|---|---:|---|---:|---:|---|---:|
| map | 2026-07 | 425 | 0.658811 | 0.649652 | 0.647415 | -12.83% (242), $10.00 | -3.01% (73), $56.87 | 18 (224 unfilled) | 2.70% [-36.25%, 33.29%] | $52.09 | 9 (64 unfilled) | 18.30% [-34.68%, 57.08%] | $56.22 |
| map | 2026-08 | 394 | 0.690101 | 0.667763 | 0.664665 | -4.70% (265), $19.62 | -4.70% (138), $28.73 | 24 (241 unfilled) | 0.91% [-41.71%, 44.57%] | $47.31 | 13 (125 unfilled) | -3.86% [-68.55%, 71.11%] | $45.24 |
| map | 2026-09 | 111 | 0.694030 | 0.643824 | 0.627230 | -10.85% (73), $43.03 | -4.45% (38), $40.89 | 17 (56 unfilled) | 18.80% [-28.23%, 70.12%] | $69.74 | 8 (30 unfilled) | 58.82% [-21.36%, 134.15%] | $61.10 |
| map | 2026-10 | 61 | 0.683736 | 0.650992 | 0.634070 | -34.06% (30), $28.98 | -68.11% (9), $37.41 | 11 (19 unfilled) | -85.79% [-100.00%, -47.83%] | $28.17 | 7 (2 unfilled) | -100.00% [-100.00%, -100.00%] | $35.74 |
| series | 2026-07 | 237 | 0.634382 | 0.631278 | 0.632384 | -8.97% (144), $48.17 | 111.29% (11), $51.33 | 81 (63 unfilled) | -19.36% [-38.23%, 1.00%] | $20.20 | 5 (6 unfilled) | -100.00% [-100.00%, -100.00%] | $47.03 |
| series | 2026-08 | 193 | 0.672524 | 0.647335 | 0.649323 | -9.79% (138), $12.24 | 6.73% (24), $58.72 | 56 (82 unfilled) | 9.56% [-23.64%, 46.01%] | $71.52 | 11 (13 unfilled) | 63.87% [-53.39%, 211.54%] | $58.21 |
| series | 2026-09 | 88 | 0.667508 | 0.609886 | 0.609346 | 4.19% (69), $37.85 | -22.60% (19), $39.11 | 45 (24 unfilled) | 16.65% [-21.48%, 59.30%] | $60.50 | 10 (9 unfilled) | 22.44% [-100.00%, 145.35%] | $49.69 |
| series | 2026-10 | 68 | 0.660519 | 0.583968 | 0.575429 | -24.72% (52), $8.10 | -21.41% (18), $45.75 | 33 (19 unfilled) | -11.10% [-54.20%, 34.20%] | $28.26 | 10 (8 unfilled) | 13.07% [-100.00%, 126.35%] | $55.86 |

### player_round_glicko_rookie+none: Kalshi comparison and returns

none

#### Log loss vs Kalshi

| Kind | Slice | Rows | Model log loss | Kalshi log loss | Difference [95% interval] | Significant |
|---|---|---:|---:|---:|---|---|
| series | all | 586 | 0.634448 | 0.627894 | 0.006554 [-0.016401, 0.030330] | no |
| series | vct | 306 | 0.641432 | 0.648387 | -0.006955 [-0.035429, 0.019891] | no |
| series | vcl | 96 | 0.583192 | 0.616703 | -0.033511 [-0.079331, 0.011913] | no |
| series | gc | 151 | 0.642242 | 0.586384 | 0.055858 [-0.000525, 0.119067] | no |
| series | t3 | 0 | — | — | — | — |
| series | collegiate | 0 | — | — | — | — |
| series | offseason | 33 | 0.683129 | 0.660365 | 0.022763 [-0.040513, 0.087699] | no |
| series | international=1 | 77 | 0.671955 | 0.603125 | 0.068830 [0.014333, 0.125943] | yes |
| series | international=0 | 509 | 0.628774 | 0.631641 | -0.002867 [-0.027424, 0.022116] | no |
| map | all | 991 | 0.651453 | 0.651191 | 0.000262 [-0.012252, 0.012630] | no |
| map | vct | 598 | 0.677646 | 0.670975 | 0.006671 [-0.009520, 0.022284] | no |
| map | vcl | 144 | 0.604240 | 0.628359 | -0.024118 [-0.044918, -0.003792] | yes |
| map | gc | 193 | 0.594886 | 0.600063 | -0.005177 [-0.038501, 0.027829] | no |
| map | t3 | 0 | — | — | — | — |
| map | collegiate | 0 | — | — | — | — |
| map | offseason | 56 | 0.688114 | 0.674841 | 0.013274 [-0.019562, 0.046330] | no |
| map | international=1 | 128 | 0.660837 | 0.650599 | 0.010238 [-0.012596, 0.039916] | no |
| map | international=0 | 863 | 0.650061 | 0.651279 | -0.001217 [-0.015186, 0.013189] | no |

#### Full-Kelly returns

| Kind | Slice | Bets | Matches | Mean edge | Flat ROI [95% interval] | Kelly, LoL caps ($50 start) | Multiple | Max drawdown | Largest stake | Bets filled | Flat ROI depth-capped [95% interval] | Kelly depth-capped final |
|---|---|---:|---:|---:|---|---:|---:|---:|---:|---:|---|---:|
| series | all | 425 | 424 | 0.0879 | 3.76% [-7.73%, 15.64%] | $50.99 | 1.020× | 87.84% | $26.39 | 238 (187 unfilled) | 8.95% [-6.56%, 24.56%] | $100.98 |
| series | vct | 222 | 222 | 0.0760 | 4.33% [-12.25%, 20.95%] | $41.84 | 0.837× | 75.18% | $7.94 | 127 (95 unfilled) | 13.98% [-8.81%, 36.47%] | $124.13 |
| series | vcl | 60 | 60 | 0.0800 | 31.36% [-1.98%, 68.04%] | $179.53 | 3.591× | 32.42% | $21.12 | 34 (26 unfilled) | 2.97% [-31.65%, 36.75%] | $42.08 |
| series | gc | 119 | 119 | 0.1188 | -8.86% [-28.18%, 13.02%] | $21.18 | 0.424× | 66.13% | $5.28 | 60 (59 unfilled) | 8.25% [-22.83%, 41.12%] | $72.64 |
| series | t3 | 0 | 0 | — | — | $50.00 | 1.000× | 0.00% | $0.00 | 0 (0 unfilled) | — | $50.00 |
| series | collegiate | 0 | 0 | — | — | $50.00 | 1.000× | 0.00% | $0.00 | 0 (0 unfilled) | — | $50.00 |
| series | offseason | 24 | 23 | 0.0654 | -8.02% [-45.18%, 33.29%] | $38.15 | 0.763× | 40.76% | $5.16 | 17 (7 unfilled) | -14.11% [-58.63%, 33.07%] | $37.36 |
| series | international=1 | 54 | 53 | 0.0890 | -22.24% [-48.05%, 5.24%] | $14.23 | 0.285× | 76.57% | $5.16 | 41 (13 unfilled) | -18.56% [-47.90%, 12.60%] | $25.97 |
| series | international=0 | 371 | 371 | 0.0878 | 7.55% [-4.68%, 21.19%] | $158.95 | 3.179× | 80.96% | $28.65 | 197 (174 unfilled) | 14.67% [-3.65%, 32.74%] | $182.80 |
| map | all | 627 | 312 | 0.0632 | 2.43% [-5.78%, 10.87%] | $63.09 | 1.262× | 64.24% | $6.89 | 67 (560 unfilled) | -1.03% [-24.68%, 23.05%] | $46.01 |
| map | vct | 379 | 191 | 0.0603 | -0.03% [-11.29%, 10.86%] | $23.00 | 0.460× | 78.54% | $3.12 | 27 (352 unfilled) | -25.47% [-61.04%, 14.28%] | $32.14 |
| map | vcl | 77 | 36 | 0.0549 | 12.00% [-6.01%, 28.13%] | $73.17 | 1.463× | 10.00% | $4.06 | 11 (66 unfilled) | -21.47% [-79.38%, 17.37%] | $43.60 |
| map | gc | 130 | 65 | 0.0857 | 8.52% [-9.60%, 27.24%] | $100.60 | 2.012× | 22.99% | $8.77 | 26 (104 unfilled) | 18.98% [-18.97%, 57.17%] | $71.35 |
| map | t3 | 0 | 0 | — | — | $50.00 | 1.000× | 0.00% | $0.00 | 0 (0 unfilled) | — | $50.00 |
| map | collegiate | 0 | 0 | — | — | $50.00 | 1.000× | 0.00% | $0.00 | 0 (0 unfilled) | — | $50.00 |
| map | offseason | 41 | 20 | 0.0343 | -12.11% [-36.96%, 13.47%] | $41.29 | 0.826× | 30.28% | $2.53 | 3 (38 unfilled) | 119.37% [88.54%, 164.55%] | $56.36 |
| map | international=1 | 76 | 39 | 0.0370 | -6.41% [-23.85%, 12.15%] | $39.74 | 0.795× | 30.28% | $2.97 | 10 (66 unfilled) | 7.31% [-51.72%, 80.26%] | $45.98 |
| map | international=0 | 551 | 273 | 0.0668 | 3.65% [-5.03%, 13.11%] | $77.97 | 1.559× | 64.08% | $7.66 | 57 (494 unfilled) | -2.49% [-28.51%, 23.64%] | $49.93 |
| series+map | all | 1052 | 453 | 0.0732 | 2.97% [-5.40%, 11.50%] | $68.52 | 1.370× | 80.59% | $15.70 | 305 (747 unfilled) | 6.76% [-6.44%, 20.39%] | $42.04 |

#### Monthly market blend fits

UTC monthly fits use earlier rows of the same kind from 2025-09-01, excluding holdout; minimum 100 rows. logit(p_blend) = a·logit(mid) + b·(logit(p_model) − logit(mid)); inputs clipped to [0.01, 0.99], no intercept, ridge 1e-6. Unfitted rows use mid unchanged; excluded from blended tables: 0 rows. Rating parameters remain selected on the tuning window.

| Month | Kind | n | a | b | Status |
|---|---|---:|---:|---:|---|
| 2026-07 | series | 677 | 1.091498 | 0.672544 | fitted |
| 2026-07 | map | 1049 | 0.997951 | 0.671517 | fitted |
| 2026-08 | series | 677 | 1.091498 | 0.672544 | fitted |
| 2026-08 | map | 1049 | 0.997951 | 0.671517 | fitted |
| 2026-09 | series | 677 | 1.091498 | 0.672544 | fitted |
| 2026-09 | map | 1049 | 0.997951 | 0.671517 | fitted |
| 2026-10 | series | 677 | 1.091498 | 0.672544 | fitted |
| 2026-10 | map | 1049 | 0.997951 | 0.671517 | fitted |

#### Log loss vs Kalshi (blended)

| Kind | Slice | Rows | Model log loss | Kalshi log loss | Difference [95% interval] | Significant |
|---|---|---:|---:|---:|---|---|
| series | all | 586 | 0.622318 | 0.627894 | -0.005576 [-0.020191, 0.009213] | no |
| series | vct | 306 | 0.637466 | 0.648387 | -0.010920 [-0.029520, 0.006394] | no |
| series | vcl | 96 | 0.586430 | 0.616703 | -0.030273 [-0.058148, -0.001910] | yes |
| series | gc | 151 | 0.603958 | 0.586384 | 0.017574 [-0.017058, 0.054837] | no |
| series | t3 | 0 | — | — | — | — |
| series | collegiate | 0 | — | — | — | — |
| series | offseason | 33 | 0.670262 | 0.660365 | 0.009897 [-0.031902, 0.051352] | no |
| series | international=1 | 77 | 0.633384 | 0.603125 | 0.030260 [-0.000585, 0.061721] | no |
| series | international=0 | 509 | 0.620644 | 0.631641 | -0.010997 [-0.026497, 0.004648] | no |
| map | all | 991 | 0.646950 | 0.651191 | -0.004241 [-0.012604, 0.004072] | no |
| map | vct | 598 | 0.671406 | 0.670975 | 0.000431 [-0.010553, 0.010841] | no |
| map | vcl | 144 | 0.609016 | 0.628359 | -0.019342 [-0.034299, -0.004988] | yes |
| map | gc | 193 | 0.589455 | 0.600063 | -0.010608 [-0.032255, 0.010382] | no |
| map | t3 | 0 | — | — | — | — |
| map | collegiate | 0 | — | — | — | — |
| map | offseason | 56 | 0.681491 | 0.674841 | 0.006650 [-0.015486, 0.028369] | no |
| map | international=1 | 128 | 0.655142 | 0.650599 | 0.004543 [-0.010494, 0.022922] | no |
| map | international=0 | 863 | 0.645735 | 0.651279 | -0.005543 [-0.014876, 0.003918] | no |

#### Full-Kelly returns (blended)

| Kind | Slice | Bets | Matches | Mean edge | Flat ROI [95% interval] | Kelly, LoL caps ($50 start) | Multiple | Max drawdown | Largest stake | Bets filled | Flat ROI depth-capped [95% interval] | Kelly depth-capped final |
|---|---|---:|---:|---:|---|---:|---:|---:|---:|---:|---|---:|
| series | all | 348 | 347 | 0.0565 | 3.55% [-8.76%, 17.05%] | $112.83 | 2.257× | 69.99% | $27.56 | 192 (156 unfilled) | 9.29% [-7.15%, 26.02%] | $105.45 |
| series | vct | 178 | 178 | 0.0482 | -0.14% [-17.04%, 18.55%] | $125.92 | 2.518× | 44.93% | $13.62 | 98 (80 unfilled) | 11.99% [-11.00%, 38.11%] | $143.88 |
| series | vcl | 50 | 50 | 0.0467 | 37.23% [0.13%, 81.85%] | $145.39 | 2.908× | 17.21% | $15.29 | 28 (22 unfilled) | 11.34% [-25.02%, 48.45%] | $55.37 |
| series | gc | 101 | 101 | 0.0790 | -2.79% [-24.81%, 21.69%] | $21.61 | 0.432× | 66.37% | $5.33 | 52 (49 unfilled) | 12.75% [-20.55%, 49.11%] | $55.37 |
| series | t3 | 0 | 0 | — | — | $50.00 | 1.000× | 0.00% | $0.00 | 0 (0 unfilled) | — | $50.00 |
| series | collegiate | 0 | 0 | — | — | $50.00 | 1.000× | 0.00% | $0.00 | 0 (0 unfilled) | — | $50.00 |
| series | offseason | 19 | 18 | 0.0398 | -17.00% [-57.49%, 24.96%] | $34.65 | 0.693× | 36.91% | $4.99 | 14 (5 unfilled) | -26.56% [-71.94%, 22.45%] | $37.16 |
| series | international=1 | 43 | 42 | 0.0528 | -24.12% [-51.86%, 5.67%] | $18.01 | 0.360× | 70.27% | $4.99 | 34 (9 unfilled) | -10.64% [-43.05%, 22.90%] | $34.27 |
| series | international=0 | 305 | 305 | 0.0570 | 7.45% [-6.08%, 22.84%] | $306.34 | 6.127× | 58.62% | $36.80 | 158 (147 unfilled) | 13.57% [-4.98%, 33.11%] | $163.91 |
| map | all | 477 | 246 | 0.0430 | 2.77% [-7.02%, 12.32%] | $49.45 | 0.989× | 49.95% | $4.44 | 54 (423 unfilled) | -6.23% [-33.45%, 22.00%] | $48.30 |
| map | vct | 285 | 150 | 0.0408 | -2.60% [-15.28%, 10.56%] | $24.48 | 0.490× | 62.73% | $2.83 | 19 (266 unfilled) | -46.29% [-79.82%, -0.40%] | $36.34 |
| map | vcl | 59 | 28 | 0.0343 | 19.85% [0.34%, 36.91%] | $64.36 | 1.287× | 7.32% | $3.22 | 10 (49 unfilled) | -13.56% [-76.35%, 25.84%] | $48.83 |
| map | gc | 109 | 55 | 0.0583 | 12.01% [-7.68%, 33.31%] | $78.44 | 1.569× | 24.90% | $7.17 | 23 (86 unfilled) | 17.68% [-24.58%, 62.07%] | $66.33 |
| map | t3 | 0 | 0 | — | — | $50.00 | 1.000× | 0.00% | $0.00 | 0 (0 unfilled) | — | $50.00 |
| map | collegiate | 0 | 0 | — | — | $50.00 | 1.000× | 0.00% | $0.00 | 0 (0 unfilled) | — | $50.00 |
| map | offseason | 24 | 13 | 0.0208 | -17.49% [-54.97%, 29.10%] | $47.18 | 0.944× | 13.19% | $2.70 | 2 (22 unfilled) | 134.71% [104.58%, 164.55%] | $51.51 |
| map | international=1 | 40 | 23 | 0.0278 | -14.13% [-42.27%, 17.31%] | $45.11 | 0.902× | 15.19% | $2.70 | 7 (33 unfilled) | -14.89% [-84.30%, 78.31%] | $45.51 |
| map | international=0 | 437 | 223 | 0.0444 | 4.31% [-6.10%, 14.66%] | $54.35 | 1.087× | 50.36% | $4.67 | 47 (390 unfilled) | -4.94% [-32.41%, 23.69%] | $53.10 |
| series+map | all | 825 | 369 | 0.0487 | 3.10% [-6.14%, 12.86%] | $67.56 | 1.351× | 65.11% | $13.97 | 246 (579 unfilled) | 5.87% [-9.26%, 20.88%] | $52.09 |

#### Monthly breakdown

All metrics use identical linked rows within each kind/month. Unfitted blend months show —; counts include all rows.

| Kind | Month | Rows | Model log loss | Blended log loss | Kalshi log loss | Raw flat ROI (bets), unlimited Kelly final | Blended flat ROI (bets), unlimited Kelly final | Raw bets filled | Raw Flat ROI depth-capped [95% interval] | Raw Kelly depth-capped final | Blended bets filled | Blended Flat ROI depth-capped [95% interval] | Blended Kelly depth-capped final |
|---|---|---:|---:|---:|---:|---|---|---:|---|---:|---:|---|---:|
| map | 2026-07 | 425 | 0.651149 | 0.646502 | 0.647415 | -3.82% (251), $29.33 | -2.41% (190), $28.59 | 20 (231 unfilled) | 18.42% [-19.72%, 51.45%] | $58.29 | 16 (174 unfilled) | 19.00% [-27.23%, 60.54%] | $57.30 |
| map | 2026-08 | 394 | 0.659584 | 0.656599 | 0.664665 | 4.42% (259), $67.83 | 5.25% (199), $70.57 | 20 (239 unfilled) | -7.25% [-49.72%, 37.03%] | $43.78 | 17 (182 unfilled) | -16.38% [-58.66%, 28.24%] | $44.92 |
| map | 2026-09 | 111 | 0.628418 | 0.620009 | 0.627230 | 15.95% (87), $89.55 | 12.39% (74), $65.24 | 15 (72 unfilled) | 4.27% [-47.35%, 79.46%] | $56.43 | 12 (62 unfilled) | 11.16% [-49.43%, 91.57%] | $56.17 |
| map | 2026-10 | 61 | 0.642975 | 0.636780 | 0.634070 | -1.60% (30), $45.28 | -13.15% (14), $47.68 | 12 (18 unfilled) | -29.48% [-81.85%, 22.06%] | $39.92 | 9 (5 unfilled) | -54.56% [-100.00%, 2.71%] | $41.92 |
| series | 2026-07 | 237 | 0.632933 | 0.624852 | 0.632384 | 7.96% (162), $103.93 | 6.70% (131), $79.70 | 94 (68 unfilled) | -0.69% [-22.90%, 20.97%] | $38.81 | 75 (56 unfilled) | -0.75% [-23.90%, 24.01%] | $42.67 |
| series | 2026-08 | 193 | 0.646108 | 0.641039 | 0.649323 | 0.65% (147), $35.55 | 1.08% (119), $109.77 | 70 (77 unfilled) | 21.96% [-5.50%, 52.88%] | $135.22 | 55 (64 unfilled) | 18.26% [-13.89%, 55.04%] | $138.26 |
| series | 2026-09 | 88 | 0.619694 | 0.602216 | 0.609346 | 7.62% (65), $59.47 | 5.94% (57), $53.17 | 41 (24 unfilled) | 22.96% [-14.99%, 65.12%] | $94.93 | 36 (21 unfilled) | 22.60% [-16.04%, 66.61%] | $72.45 |
| series | 2026-10 | 68 | 0.625727 | 0.586365 | 0.575429 | -5.48% (51), $28.59 | -2.66% (41), $30.04 | 33 (18 unfilled) | -8.52% [-48.35%, 38.42%] | $31.10 | 26 (15 unfilled) | 0.90% [-48.09%, 54.06%] | $35.42 |

### player_round_glicko_rookie_tier_revert+none: Kalshi comparison and returns

none

#### Log loss vs Kalshi

| Kind | Slice | Rows | Model log loss | Kalshi log loss | Difference [95% interval] | Significant |
|---|---|---:|---:|---:|---|---|
| series | all | 586 | 0.636720 | 0.627894 | 0.008826 [-0.014982, 0.033541] | no |
| series | vct | 306 | 0.647848 | 0.648387 | -0.000539 [-0.030823, 0.028161] | no |
| series | vcl | 96 | 0.578044 | 0.616703 | -0.038659 [-0.084654, 0.006892] | no |
| series | gc | 151 | 0.641802 | 0.586384 | 0.055419 [-0.001577, 0.120122] | no |
| series | t3 | 0 | — | — | — | — |
| series | collegiate | 0 | — | — | — | — |
| series | offseason | 33 | 0.680970 | 0.660365 | 0.020605 [-0.042233, 0.084869] | no |
| series | international=1 | 77 | 0.664138 | 0.603125 | 0.061014 [0.011042, 0.114989] | yes |
| series | international=0 | 509 | 0.632572 | 0.631641 | 0.000931 [-0.025337, 0.027684] | no |
| map | all | 991 | 0.651675 | 0.651191 | 0.000484 [-0.011628, 0.012532] | no |
| map | vct | 598 | 0.676169 | 0.670975 | 0.005194 [-0.011823, 0.020945] | no |
| map | vcl | 144 | 0.605885 | 0.628359 | -0.022474 [-0.042731, -0.003064] | yes |
| map | gc | 193 | 0.600631 | 0.600063 | 0.000568 [-0.032547, 0.032837] | no |
| map | t3 | 0 | — | — | — | — |
| map | collegiate | 0 | — | — | — | — |
| map | offseason | 56 | 0.683779 | 0.674841 | 0.008938 [-0.021742, 0.041724] | no |
| map | international=1 | 128 | 0.656590 | 0.650599 | 0.005991 [-0.015403, 0.033852] | no |
| map | international=0 | 863 | 0.650946 | 0.651279 | -0.000332 [-0.013570, 0.013571] | no |

#### Full-Kelly returns

| Kind | Slice | Bets | Matches | Mean edge | Flat ROI [95% interval] | Kelly, LoL caps ($50 start) | Multiple | Max drawdown | Largest stake | Bets filled | Flat ROI depth-capped [95% interval] | Kelly depth-capped final |
|---|---|---:|---:|---:|---|---:|---:|---:|---:|---:|---|---:|
| series | all | 428 | 427 | 0.0910 | 5.38% [-5.93%, 17.12%] | $148.09 | 2.962× | 71.79% | $32.57 | 237 (191 unfilled) | 12.01% [-2.85%, 27.12%] | $199.18 |
| series | vct | 220 | 220 | 0.0829 | 8.21% [-8.39%, 25.40%] | $91.04 | 1.821× | 64.50% | $12.68 | 121 (99 unfilled) | 17.79% [-4.51%, 40.89%] | $183.88 |
| series | vcl | 65 | 65 | 0.0757 | 31.44% [0.79%, 66.36%] | $252.24 | 5.045× | 18.14% | $22.87 | 41 (24 unfilled) | 11.31% [-16.77%, 39.08%] | $59.66 |
| series | gc | 122 | 122 | 0.1169 | -10.52% [-30.28%, 11.55%] | $18.53 | 0.371× | 68.91% | $4.94 | 61 (61 unfilled) | 8.84% [-19.14%, 40.28%] | $88.22 |
| series | t3 | 0 | 0 | — | — | $50.00 | 1.000× | 0.00% | $0.00 | 0 (0 unfilled) | — | $50.00 |
| series | collegiate | 0 | 0 | — | — | $50.00 | 1.000× | 0.00% | $0.00 | 0 (0 unfilled) | — | $50.00 |
| series | offseason | 21 | 20 | 0.0726 | -12.46% [-54.53%, 31.60%] | $39.32 | 0.786× | 27.97% | $4.86 | 14 (7 unfilled) | -22.06% [-67.89%, 32.43%] | $39.28 |
| series | international=1 | 51 | 50 | 0.0876 | -27.15% [-51.73%, 1.51%] | $17.56 | 0.351× | 70.56% | $4.86 | 39 (12 unfilled) | -21.78% [-51.43%, 10.11%] | $33.82 |
| series | international=0 | 377 | 377 | 0.0914 | 9.79% [-2.88%, 22.69%] | $369.90 | 7.398× | 66.60% | $37.52 | 198 (179 unfilled) | 18.66% [1.74%, 36.61%] | $275.46 |
| map | all | 603 | 305 | 0.0634 | 3.83% [-4.87%, 12.27%] | $147.62 | 2.952× | 48.58% | $11.51 | 65 (538 unfilled) | -3.59% [-28.67%, 23.52%] | $56.90 |
| map | vct | 363 | 186 | 0.0628 | 2.57% [-8.56%, 14.84%] | $59.41 | 1.188× | 60.70% | $4.13 | 22 (341 unfilled) | -25.57% [-65.49%, 22.90%] | $38.36 |
| map | vcl | 71 | 34 | 0.0552 | 15.80% [-1.63%, 32.81%] | $64.21 | 1.284× | 11.77% | $3.13 | 11 (60 unfilled) | -2.84% [-62.89%, 33.28%] | $47.12 |
| map | gc | 137 | 69 | 0.0770 | 3.67% [-14.50%, 22.61%] | $75.13 | 1.503× | 30.02% | $6.81 | 30 (107 unfilled) | 2.94% [-34.80%, 39.09%] | $65.02 |
| map | t3 | 0 | 0 | — | — | $50.00 | 1.000× | 0.00% | $0.00 | 0 (0 unfilled) | — | $50.00 |
| map | collegiate | 0 | 0 | — | — | $50.00 | 1.000× | 0.00% | $0.00 | 0 (0 unfilled) | — | $50.00 |
| map | offseason | 32 | 16 | 0.0301 | -7.72% [-34.96%, 20.67%] | $58.55 | 1.171× | 7.67% | $4.04 | 2 (30 unfilled) | 134.71% [104.58%, 164.55%] | $59.18 |
| map | international=1 | 63 | 33 | 0.0367 | -0.88% [-23.75%, 21.51%] | $62.10 | 1.242× | 13.57% | $4.04 | 7 (56 unfilled) | 9.11% [-63.61%, 102.75%] | $51.81 |
| map | international=0 | 540 | 272 | 0.0665 | 4.38% [-4.50%, 13.84%] | $116.20 | 2.324× | 48.62% | $9.64 | 58 (482 unfilled) | -5.13% [-32.32%, 22.92%] | $54.13 |
| series+map | all | 1031 | 448 | 0.0748 | 4.47% [-4.01%, 13.16%] | $289.08 | 5.782× | 57.77% | $41.94 | 302 (729 unfilled) | 8.64% [-5.31%, 22.77%] | $113.47 |

#### Monthly market blend fits

UTC monthly fits use earlier rows of the same kind from 2025-09-01, excluding holdout; minimum 100 rows. logit(p_blend) = a·logit(mid) + b·(logit(p_model) − logit(mid)); inputs clipped to [0.01, 0.99], no intercept, ridge 1e-6. Unfitted rows use mid unchanged; excluded from blended tables: 0 rows. Rating parameters remain selected on the tuning window.

| Month | Kind | n | a | b | Status |
|---|---|---:|---:|---:|---|
| 2026-07 | series | 677 | 1.087605 | 0.659058 | fitted |
| 2026-07 | map | 1049 | 1.070712 | 0.743860 | fitted |
| 2026-08 | series | 677 | 1.087605 | 0.659058 | fitted |
| 2026-08 | map | 1049 | 1.070712 | 0.743860 | fitted |
| 2026-09 | series | 677 | 1.087605 | 0.659058 | fitted |
| 2026-09 | map | 1049 | 1.070712 | 0.743860 | fitted |
| 2026-10 | series | 677 | 1.087605 | 0.659058 | fitted |
| 2026-10 | map | 1049 | 1.070712 | 0.743860 | fitted |

#### Log loss vs Kalshi (blended)

| Kind | Slice | Rows | Model log loss | Kalshi log loss | Difference [95% interval] | Significant |
|---|---|---:|---:|---:|---|---|
| series | all | 586 | 0.623173 | 0.627894 | -0.004721 [-0.019561, 0.010691] | no |
| series | vct | 306 | 0.640631 | 0.648387 | -0.007756 [-0.027681, 0.010607] | no |
| series | vcl | 96 | 0.583598 | 0.616703 | -0.033105 [-0.060385, -0.004408] | yes |
| series | gc | 151 | 0.603043 | 0.586384 | 0.016659 [-0.017994, 0.054947] | no |
| series | t3 | 0 | — | — | — | — |
| series | collegiate | 0 | — | — | — | — |
| series | offseason | 33 | 0.668529 | 0.660365 | 0.008163 [-0.033022, 0.048558] | no |
| series | international=1 | 77 | 0.628794 | 0.603125 | 0.025670 [-0.003459, 0.055564] | no |
| series | international=0 | 509 | 0.622322 | 0.631641 | -0.009318 [-0.026084, 0.006899] | no |
| map | all | 991 | 0.647051 | 0.651191 | -0.004140 [-0.012836, 0.004586] | no |
| map | vct | 598 | 0.671534 | 0.670975 | 0.000559 [-0.011262, 0.011839] | no |
| map | vcl | 144 | 0.606814 | 0.628359 | -0.021544 [-0.037418, -0.007048] | yes |
| map | gc | 193 | 0.591802 | 0.600063 | -0.008262 [-0.030898, 0.014216] | no |
| map | t3 | 0 | — | — | — | — |
| map | collegiate | 0 | — | — | — | — |
| map | offseason | 56 | 0.679490 | 0.674841 | 0.004649 [-0.017580, 0.027368] | no |
| map | international=1 | 128 | 0.651736 | 0.650599 | 0.001137 [-0.014260, 0.019587] | no |
| map | international=0 | 863 | 0.646356 | 0.651279 | -0.004922 [-0.014211, 0.005185] | no |

#### Full-Kelly returns (blended)

| Kind | Slice | Bets | Matches | Mean edge | Flat ROI [95% interval] | Kelly, LoL caps ($50 start) | Multiple | Max drawdown | Largest stake | Bets filled | Flat ROI depth-capped [95% interval] | Kelly depth-capped final |
|---|---|---:|---:|---:|---|---:|---:|---:|---:|---:|---|---:|
| series | all | 350 | 349 | 0.0582 | 7.48% [-4.63%, 20.91%] | $97.39 | 1.948× | 67.16% | $17.37 | 195 (155 unfilled) | 17.01% [0.99%, 33.70%] | $126.88 |
| series | vct | 173 | 173 | 0.0545 | 6.34% [-10.33%, 25.20%] | $63.79 | 1.276× | 59.18% | $8.59 | 97 (76 unfilled) | 18.59% [-5.43%, 43.82%] | $108.18 |
| series | vcl | 55 | 55 | 0.0436 | 39.00% [4.20%, 78.14%] | $156.58 | 3.132× | 6.04% | $14.67 | 33 (22 unfilled) | 22.33% [-8.88%, 54.01%] | $59.44 |
| series | gc | 104 | 104 | 0.0755 | -4.45% [-24.65%, 17.94%] | $29.93 | 0.599× | 61.34% | $6.06 | 52 (52 unfilled) | 18.96% [-13.26%, 53.21%] | $69.16 |
| series | t3 | 0 | 0 | — | — | $50.00 | 1.000× | 0.00% | $0.00 | 0 (0 unfilled) | — | $50.00 |
| series | collegiate | 0 | 0 | — | — | $50.00 | 1.000× | 0.00% | $0.00 | 0 (0 unfilled) | — | $50.00 |
| series | offseason | 18 | 17 | 0.0386 | -8.91% [-52.61%, 40.38%] | $41.42 | 0.828× | 22.62% | $4.86 | 13 (5 unfilled) | -16.08% [-64.42%, 38.77%] | $40.18 |
| series | international=1 | 38 | 37 | 0.0533 | -21.96% [-52.50%, 9.47%] | $25.97 | 0.519× | 58.10% | $4.86 | 29 (9 unfilled) | -5.52% [-39.82%, 32.61%] | $42.42 |
| series | international=0 | 312 | 312 | 0.0588 | 11.08% [-2.49%, 25.38%] | $189.61 | 3.792× | 67.11% | $21.33 | 166 (146 unfilled) | 20.95% [2.54%, 40.28%] | $160.52 |
| map | all | 474 | 242 | 0.0478 | 4.29% [-4.52%, 13.71%] | $43.97 | 0.879× | 62.98% | $5.98 | 54 (420 unfilled) | -3.34% [-30.01%, 24.86%] | $44.82 |
| map | vct | 292 | 150 | 0.0459 | 1.62% [-10.63%, 14.65%] | $27.14 | 0.543× | 66.30% | $3.43 | 18 (274 unfilled) | -43.24% [-79.82%, 3.17%] | $35.89 |
| map | vcl | 55 | 26 | 0.0414 | 11.61% [-8.59%, 28.04%] | $62.24 | 1.245× | 5.38% | $3.05 | 9 (46 unfilled) | -3.67% [-72.19%, 32.68%] | $48.11 |
| map | gc | 107 | 56 | 0.0613 | 9.21% [-10.07%, 30.38%] | $60.05 | 1.201× | 24.76% | $5.81 | 25 (82 unfilled) | 14.32% [-23.28%, 52.26%] | $61.25 |
| map | t3 | 0 | 0 | — | — | $50.00 | 1.000× | 0.00% | $0.00 | 0 (0 unfilled) | — | $50.00 |
| map | collegiate | 0 | 0 | — | — | $50.00 | 1.000× | 0.00% | $0.00 | 0 (0 unfilled) | — | $50.00 |
| map | offseason | 20 | 10 | 0.0208 | -3.16% [-43.91%, 45.71%] | $52.06 | 1.041× | 7.17% | $2.52 | 2 (18 unfilled) | 134.71% [104.58%, 164.55%] | $52.71 |
| map | international=1 | 38 | 21 | 0.0301 | -0.11% [-31.49%, 31.84%] | $56.50 | 1.130× | 10.90% | $3.02 | 6 (32 unfilled) | -0.78% [-82.07%, 113.97%] | $47.67 |
| map | international=0 | 436 | 221 | 0.0493 | 4.68% [-5.33%, 14.54%] | $38.50 | 0.770× | 63.13% | $5.73 | 48 (388 unfilled) | -3.66% [-31.84%, 25.59%] | $46.91 |
| series+map | all | 824 | 373 | 0.0522 | 5.65% [-3.14%, 15.33%] | $85.62 | 1.712× | 71.92% | $13.28 | 249 (575 unfilled) | 12.59% [-2.52%, 27.75%] | $65.60 |

#### Monthly breakdown

All metrics use identical linked rows within each kind/month. Unfitted blend months show —; counts include all rows.

| Kind | Month | Rows | Model log loss | Blended log loss | Kalshi log loss | Raw flat ROI (bets), unlimited Kelly final | Blended flat ROI (bets), unlimited Kelly final | Raw bets filled | Raw Flat ROI depth-capped [95% interval] | Raw Kelly depth-capped final | Blended bets filled | Blended Flat ROI depth-capped [95% interval] | Blended Kelly depth-capped final |
|---|---|---:|---:|---:|---:|---|---|---:|---|---:|---:|---|---:|
| map | 2026-07 | 425 | 0.647531 | 0.643697 | 0.647415 | -0.91% (237), $62.51 | 2.11% (185), $43.91 | 18 (219 unfilled) | 5.64% [-42.50%, 51.31%] | $63.41 | 15 (170 unfilled) | 27.04% [-15.24%, 66.45%] | $58.49 |
| map | 2026-08 | 394 | 0.662793 | 0.658986 | 0.664665 | 6.26% (261), $79.62 | 5.68% (207), $43.73 | 21 (240 unfilled) | -3.40% [-49.69%, 42.27%] | $48.24 | 18 (189 unfilled) | -13.81% [-54.11%, 29.92%] | $44.77 |
| map | 2026-09 | 111 | 0.634649 | 0.624780 | 0.627230 | 10.02% (79), $75.14 | 8.23% (69), $60.92 | 15 (64 unfilled) | 3.94% [-49.95%, 71.78%] | $54.79 | 13 (56 unfilled) | 4.34% [-52.88%, 84.17%] | $50.82 |
| map | 2026-10 | 61 | 0.639720 | 0.633860 | 0.634070 | 3.66% (26), $48.88 | -7.74% (13), $47.26 | 11 (15 unfilled) | -29.11% [-80.88%, 32.24%] | $41.94 | 8 (5 unfilled) | -48.77% [-100.00%, 14.23%] | $42.02 |
| series | 2026-07 | 237 | 0.630929 | 0.623362 | 0.632384 | 12.09% (160), $156.83 | 10.29% (137), $86.61 | 87 (73 unfilled) | 6.17% [-16.94%, 29.69%] | $51.62 | 77 (60 unfilled) | 3.44% [-17.94%, 27.45%] | $34.05 |
| series | 2026-08 | 193 | 0.655696 | 0.645107 | 0.649323 | 1.54% (147), $53.96 | 6.73% (114), $55.13 | 69 (78 unfilled) | 19.07% [-9.68%, 51.52%] | $171.42 | 55 (59 unfilled) | 28.95% [-4.65%, 64.25%] | $138.43 |
| series | 2026-09 | 88 | 0.622652 | 0.604020 | 0.609346 | 3.29% (69), $55.48 | 3.70% (58), $71.27 | 46 (23 unfilled) | 21.33% [-12.63%, 56.84%] | $109.54 | 37 (21 unfilled) | 29.77% [-8.93%, 74.12%] | $88.78 |
| series | 2026-10 | 68 | 0.621248 | 0.585048 | 0.575429 | -1.60% (52), $38.70 | 5.54% (41), $35.59 | 35 (17 unfilled) | 0.34% [-38.65%, 46.47%] | $43.48 | 26 (15 unfilled) | 13.85% [-34.57%, 65.77%] | $39.95 |
