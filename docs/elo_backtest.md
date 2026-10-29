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

Fit through 2025-08-31. Unknown host-region map rows: 7142 (including missing/un).

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
