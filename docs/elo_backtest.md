# Elo variants benchmark

## Combined summary (validation, all sections)

| Model | Series Δ log loss | Series flat ROI | Series Kelly (LoL caps) $ | Series flat ROI depth-capped | Series Kelly depth-capped $ | Map Δ log loss | Map flat ROI | Map Kelly (LoL caps) $ | Map flat ROI depth-capped | Map Kelly depth-capped $ | Series blended Δ log loss | Series blended flat ROI | Series blended Kelly (LoL caps) $ | Series blended flat ROI depth-capped | Series blended Kelly depth-capped $ | Map blended Δ log loss | Map blended flat ROI | Map blended Kelly (LoL caps) $ | Map blended flat ROI depth-capped | Map blended Kelly depth-capped $ |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| player_round_glicko_rookie | -0.004416 | 11.72% | $675.70 | 17.56% | $680.10 | -0.011038 | 19.06% | $5289.17 | 52.44% | $227.94 | -0.012846 | 15.80% | $489.40 | 16.18% | $221.77 | 0.003543 | 0.87% | $15.37 | 0.83% | $44.69 |
| player_round_glicko_rookie+form | -0.005159 | 11.46% | $1150.86 | 17.43% | $367.67 | -0.012138 | 20.90% | $5938.13 | 56.01% | $247.69 | -0.014489 | 16.96% | $443.35 | 17.83% | $180.87 | 0.001234 | 2.53% | $23.29 | 8.66% | $62.15 |

Parameters minimize tuning map log loss across all sections. Replay predicts before update; Replay starts at the first map. Tuning: [2024-03-01, 2025-09-01); validation: [2025-09-01, 2026-07-01). Holdout is scored only with --holdout and never selects parameters. Series use the first map prediction and independent maps in an odd best-of; missing/even best-of or unknown results are skipped. Accuracy gives 0.5 predictions half credit; ECE uses 10 equal-width bins. Log loss clips probabilities at 1e-6. Paired bootstrap uses 2,000 resamples, seed 0, clustered by match_id. Differences are the named model minus its comparator; negative favors the model. Significance requires a 95% percentile interval excluding zero. Tuning scores are selection diagnostics, not independent evidence of improvement.

Fit through 2025-08-31. Unknown host-region map rows: 3185 (including missing/un).

## Stage 1 — tuning (outcomes)

### Leaderboard

| Model | Best params | Map log loss | Series log loss | Rows |
|---|---|---:|---:|---:|
| player_round_glicko_rookie | {"k": 32, "new_player": "teammates", "rd_info": 0.25, "rd_new": 280, "rookie_maps": 200, "rookie_penalty": 150, "tau": 0.5} | 0.639796 | 0.610267 | 13802 |
| team_elo | {"k": 32} | 0.662507 | 0.646705 | 13802 |

Kalshi uses the first hourly bid/ask (midpoint for log loss, ask/bid for bets) ending ≥30 min after the market opened and ≥2 h before the scheduled start, with a spread ≤ 0.06: a price a bot could trade before any veto. Markets without such a quote are skipped. oriented to team1 using aliases. One contract per event, preferring team1. Compare identical rows; map predictions use the first map's pre-match chance. Missing links, aliases or candles are skipped; unplayed maps are not in the rows. Returns use frozen stage-1 parameters. Each bet buys $1 of contracts, fees extra; order fees ceil to a cent (0.07 × contracts × price × (1−price)). Edge selection uses unrounded per-contract fees. ROI divides profit by stake plus fees; intervals resample matches 2,000 times. Unlimited depth and depth-capped returns are shown together. Depth uses 0.5 of acceptable-price tape volume in the 6 hours after the quote, missing tapes give zero fills. Partial Kelly fills are allowed; flat bets require the full $1 stake. Kelly uses LoL caps and rounded-fee affordability, from a $50 seed. Each slice runs independently. Tape volume is a fill proxy; no slippage is modeled.

## Quote-time robustness

| Quote rule | Model | Kind | Rows | Raw Δ log loss | Blended Δ log loss | Raw flat ROI depth-capped | Blended flat ROI depth-capped |
|---|---|---|---:|---:|---:|---:|---:|
| tradeable | player_round_glicko_rookie | series | 677 | -0.004416 | -0.012846 | 17.56% | 16.18% |
| tradeable | player_round_glicko_rookie | map | 1049 | -0.011038 | 0.003543 | 52.44% | 0.83% |
| tradeable | player_round_glicko_rookie+form | series | 677 | -0.005159 | -0.014489 | 17.43% | 17.83% |
| tradeable | player_round_glicko_rookie+form | map | 1049 | -0.012138 | 0.001234 | 56.01% | 8.66% |
| hours24 | player_round_glicko_rookie | series | 375 | 0.007392 | 0.003216 | 9.40% | 11.96% |
| hours24 | player_round_glicko_rookie | map | 608 | -0.022161 | -0.000782 | 168.15% | 21.52% |
| hours24 | player_round_glicko_rookie+form | series | 375 | 0.007590 | 0.000382 | 8.83% | 5.67% |
| hours24 | player_round_glicko_rookie+form | map | 608 | -0.021754 | -0.003487 | 168.15% | 21.52% |
| hours6 | player_round_glicko_rookie | series | 644 | 0.005494 | -0.002819 | 4.26% | -1.15% |
| hours6 | player_round_glicko_rookie | map | 983 | -0.007439 | 0.009693 | 18.30% | 3.21% |
| hours6 | player_round_glicko_rookie+form | series | 644 | 0.005020 | -0.004080 | 6.46% | -0.17% |
| hours6 | player_round_glicko_rookie+form | map | 983 | -0.008380 | 0.006826 | 21.24% | 5.81% |

## Series independence: player_round_glicko_rookie

Series independence [2025-09-01, 2026-07-01): 2421 matches.

Bo3: 2218 series, log loss 0.608080.

Bo5: 203 series, log loss 0.605573.

Map 2 after map-1 win: win rate 0.6469, model 0.6086, residual 0.0383 [0.0121, 0.0650], n=1317.

Map 2 after map-1 loss: win rate 0.4303, model 0.4419, residual -0.0116 [-0.0398, 0.0165], n=1104.

Map-2 residual contrast (win minus loss): 95% [0.0122, 0.0855].

Bo3 1–1 decider: residual 0.0144 [-0.0191, 0.0488], n=852.

Intervals resample whole matches; residual = won − model pre-map chance.

| Best of | Probability bin | Rows | Predicted | Actual |
|---:|---|---:|---:|---:|
| 3 | 0.0–0.1 | 55 | 0.0514 | 0.0909 |
| 3 | 0.1–0.2 | 109 | 0.1558 | 0.2018 |
| 3 | 0.2–0.3 | 174 | 0.2561 | 0.3448 |
| 3 | 0.3–0.4 | 262 | 0.3530 | 0.3893 |
| 3 | 0.4–0.5 | 309 | 0.4495 | 0.4725 |
| 3 | 0.5–0.6 | 356 | 0.5496 | 0.5815 |
| 3 | 0.6–0.7 | 367 | 0.6492 | 0.6540 |
| 3 | 0.7–0.8 | 283 | 0.7457 | 0.7032 |
| 3 | 0.8–0.9 | 168 | 0.8466 | 0.8036 |
| 3 | 0.9–1.0 | 135 | 0.9557 | 0.9259 |
| 5 | 0.0–0.1 | 4 | 0.0289 | 0.2500 |
| 5 | 0.1–0.2 | 10 | 0.1589 | 0.1000 |
| 5 | 0.2–0.3 | 15 | 0.2588 | 0.2000 |
| 5 | 0.3–0.4 | 21 | 0.3603 | 0.3333 |
| 5 | 0.4–0.5 | 33 | 0.4503 | 0.6061 |
| 5 | 0.5–0.6 | 47 | 0.5463 | 0.5532 |
| 5 | 0.6–0.7 | 33 | 0.6524 | 0.6364 |
| 5 | 0.7–0.8 | 18 | 0.7449 | 0.8889 |
| 5 | 0.8–0.9 | 17 | 0.8557 | 0.8235 |
| 5 | 0.9–1.0 | 5 | 0.9474 | 1.0000 |

## Series independence: player_round_glicko_rookie+form

Series independence [2025-09-01, 2026-07-01): 2421 matches.

Bo3: 2218 series, log loss 0.608897.

Bo5: 203 series, log loss 0.605961.

Map 2 after map-1 win: win rate 0.6469, model 0.6256, residual 0.0214 [-0.0046, 0.0479], n=1317.

Map 2 after map-1 loss: win rate 0.4303, model 0.4240, residual 0.0063 [-0.0221, 0.0344], n=1104.

Map-2 residual contrast (win minus loss): 95% [-0.0220, 0.0506].

Bo3 1–1 decider: residual 0.0140 [-0.0198, 0.0488], n=852.

Intervals resample whole matches; residual = won − model pre-map chance.

| Best of | Probability bin | Rows | Predicted | Actual |
|---:|---|---:|---:|---:|
| 3 | 0.0–0.1 | 70 | 0.0522 | 0.1000 |
| 3 | 0.1–0.2 | 120 | 0.1556 | 0.2333 |
| 3 | 0.2–0.3 | 195 | 0.2553 | 0.3538 |
| 3 | 0.3–0.4 | 255 | 0.3534 | 0.4000 |
| 3 | 0.4–0.5 | 296 | 0.4521 | 0.4932 |
| 3 | 0.5–0.6 | 321 | 0.5530 | 0.5857 |
| 3 | 0.6–0.7 | 326 | 0.6505 | 0.6350 |
| 3 | 0.7–0.8 | 291 | 0.7454 | 0.6942 |
| 3 | 0.8–0.9 | 190 | 0.8459 | 0.8053 |
| 3 | 0.9–1.0 | 154 | 0.9556 | 0.9026 |
| 5 | 0.0–0.1 | 4 | 0.0257 | 0.2500 |
| 5 | 0.1–0.2 | 13 | 0.1416 | 0.0769 |
| 5 | 0.2–0.3 | 17 | 0.2551 | 0.2353 |
| 5 | 0.3–0.4 | 19 | 0.3446 | 0.4737 |
| 5 | 0.4–0.5 | 34 | 0.4476 | 0.6176 |
| 5 | 0.5–0.6 | 38 | 0.5371 | 0.5000 |
| 5 | 0.6–0.7 | 33 | 0.6414 | 0.6061 |
| 5 | 0.7–0.8 | 21 | 0.7491 | 0.8571 |
| 5 | 0.8–0.9 | 17 | 0.8550 | 0.8824 |
| 5 | 0.9–1.0 | 7 | 0.9361 | 0.8571 |

### Maps

| Model | Section | Rows | Log loss | Brier | Accuracy | ECE |
|---|---|---:|---:|---:|---:|---:|
| coin | all | 13802 | 0.693147 | 0.250000 | 0.500000 | 0.036806 |
| coin | vct | 2200 | 0.693147 | 0.250000 | 0.500000 | 0.016364 |
| coin | vcl | 8173 | 0.693147 | 0.250000 | 0.500000 | 0.026245 |
| coin | gc | 2036 | 0.693147 | 0.250000 | 0.500000 | 0.083988 |
| coin | t3 | 312 | 0.693147 | 0.250000 | 0.500000 | 0.012821 |
| coin | collegiate | 0 | — | — | — | — |
| coin | offseason | 1081 | 0.693147 | 0.250000 | 0.500000 | 0.076318 |
| coin | unknown | 0 | — | — | — | — |
| coin | international=1 | 497 | 0.693147 | 0.250000 | 0.500000 | 0.017103 |
| coin | international=0 | 13305 | 0.693147 | 0.250000 | 0.500000 | 0.037542 |

| Model | Section | Rows | Log loss | Brier | Accuracy | ECE |
|---|---|---:|---:|---:|---:|---:|
| player_round_glicko_rookie | all | 13802 | 0.639796 | 0.224703 | 0.629872 | 0.009367 |
| player_round_glicko_rookie | vct | 2200 | 0.677567 | 0.241734 | 0.586591 | 0.020223 |
| player_round_glicko_rookie | vcl | 8173 | 0.639439 | 0.224425 | 0.630858 | 0.010200 |
| player_round_glicko_rookie | gc | 2036 | 0.588906 | 0.202418 | 0.690815 | 0.037554 |
| player_round_glicko_rookie | t3 | 312 | 0.671268 | 0.239344 | 0.570513 | 0.052422 |
| player_round_glicko_rookie | collegiate | 0 | — | — | — | — |
| player_round_glicko_rookie | offseason | 1081 | 0.652381 | 0.229894 | 0.612858 | 0.033023 |
| player_round_glicko_rookie | unknown | 0 | — | — | — | — |
| player_round_glicko_rookie | international=1 | 497 | 0.675261 | 0.240768 | 0.582495 | 0.046284 |
| player_round_glicko_rookie | international=0 | 13305 | 0.638471 | 0.224103 | 0.631642 | 0.009526 |

player_round_glicko_rookie − coin (paired log loss):

| Section | Rows | player_round_glicko_rookie log loss | coin log loss | Difference | 95% interval | Significant |
|---|---:|---:|---:|---:|---|---|
| all | 13802 | 0.639796 | 0.693147 | -0.053352 | [-0.058928, -0.047430] | yes |

player_round_glicko_rookie − team_elo (paired log loss):

| Section | Rows | player_round_glicko_rookie log loss | team_elo log loss | Difference | 95% interval | Significant |
|---|---:|---:|---:|---:|---|---|
| all | 13802 | 0.639796 | 0.662507 | -0.022712 | [-0.026419, -0.018806] | yes |

### Series

| Model | Section | Rows | Log loss | Brier | Accuracy | ECE |
|---|---|---:|---:|---:|---:|---:|
| coin | all | 5781 | 0.693147 | 0.250000 | 0.500000 | 0.050251 |
| coin | vct | 864 | 0.693147 | 0.250000 | 0.500000 | 0.037037 |
| coin | vcl | 3452 | 0.693147 | 0.250000 | 0.500000 | 0.034183 |
| coin | gc | 827 | 0.693147 | 0.250000 | 0.500000 | 0.113059 |
| coin | t3 | 143 | 0.693147 | 0.250000 | 0.500000 | 0.003497 |
| coin | collegiate | 0 | — | — | — | — |
| coin | offseason | 495 | 0.693147 | 0.250000 | 0.500000 | 0.095960 |
| coin | unknown | 0 | — | — | — | — |
| coin | international=1 | 209 | 0.693147 | 0.250000 | 0.500000 | 0.031100 |
| coin | international=0 | 5572 | 0.693147 | 0.250000 | 0.500000 | 0.050969 |

| Model | Section | Rows | Log loss | Brier | Accuracy | ECE |
|---|---|---:|---:|---:|---:|---:|
| player_round_glicko_rookie | all | 5781 | 0.610267 | 0.210359 | 0.664158 | 0.024003 |
| player_round_glicko_rookie | vct | 864 | 0.657479 | 0.231399 | 0.616898 | 0.042576 |
| player_round_glicko_rookie | vcl | 3452 | 0.611367 | 0.210183 | 0.664108 | 0.020939 |
| player_round_glicko_rookie | gc | 827 | 0.526634 | 0.175374 | 0.741233 | 0.050192 |
| player_round_glicko_rookie | t3 | 143 | 0.690951 | 0.246536 | 0.587413 | 0.096641 |
| player_round_glicko_rookie | collegiate | 0 | — | — | — | — |
| player_round_glicko_rookie | offseason | 495 | 0.636603 | 0.222855 | 0.640404 | 0.052052 |
| player_round_glicko_rookie | unknown | 0 | — | — | — | — |
| player_round_glicko_rookie | international=1 | 209 | 0.673014 | 0.238954 | 0.578947 | 0.069261 |
| player_round_glicko_rookie | international=0 | 5572 | 0.607913 | 0.209286 | 0.667355 | 0.024064 |

player_round_glicko_rookie − coin (paired log loss):

| Section | Rows | player_round_glicko_rookie log loss | coin log loss | Difference | 95% interval | Significant |
|---|---:|---:|---:|---:|---|---|
| all | 5781 | 0.610267 | 0.693147 | -0.082880 | [-0.094375, -0.070887] | yes |

player_round_glicko_rookie − team_elo (paired log loss):

| Section | Rows | player_round_glicko_rookie log loss | team_elo log loss | Difference | 95% interval | Significant |
|---|---:|---:|---:|---:|---|---|
| all | 5781 | 0.610267 | 0.646705 | -0.036438 | [-0.045296, -0.027497] | yes |

## Stage 2 — validation (outcomes)

### Leaderboard (frozen stage-1 parameters)

| Model | Best params | Map log loss | Series log loss | Rows |
|---|---|---:|---:|---:|
| player_round_glicko_rookie+form | {"k": 32, "new_player": "teammates", "rd_info": 0.25, "rd_new": 280, "rookie_maps": 200, "rookie_penalty": 150, "tau": 0.5} | 0.639350 | 0.611754 | 6337 |
| player_round_glicko_rookie | {"k": 32, "new_player": "teammates", "rd_info": 0.25, "rd_new": 280, "rookie_maps": 200, "rookie_penalty": 150, "tau": 0.5} | 0.640026 | 0.610985 | 6337 |

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
| player_round_glicko_rookie | all | 6337 | 0.640026 | 0.224796 | 0.624822 | 0.020069 |
| player_round_glicko_rookie | vct | 1080 | 0.667268 | 0.237649 | 0.577315 | 0.031157 |
| player_round_glicko_rookie | vcl | 3374 | 0.644309 | 0.226475 | 0.625667 | 0.032135 |
| player_round_glicko_rookie | gc | 1005 | 0.601314 | 0.207939 | 0.666667 | 0.041223 |
| player_round_glicko_rookie | t3 | 16 | 0.514968 | 0.173389 | 0.750000 | 0.127648 |
| player_round_glicko_rookie | collegiate | 7 | 0.751519 | 0.278881 | 0.357143 | 0.274478 |
| player_round_glicko_rookie | offseason | 855 | 0.635641 | 0.222267 | 0.632164 | 0.018575 |
| player_round_glicko_rookie | unknown | 0 | — | — | — | — |
| player_round_glicko_rookie | international=1 | 268 | 0.665812 | 0.236795 | 0.597015 | 0.033468 |
| player_round_glicko_rookie | international=0 | 6069 | 0.638887 | 0.224266 | 0.626050 | 0.020961 |

player_round_glicko_rookie − coin (paired log loss):

| Section | Rows | player_round_glicko_rookie log loss | coin log loss | Difference | 95% interval | Significant |
|---|---:|---:|---:|---:|---|---|
| all | 6337 | 0.640026 | 0.693147 | -0.053122 | [-0.061292, -0.045096] | yes |
| vct | 1080 | 0.667268 | 0.693147 | -0.025879 | [-0.040581, -0.012165] | yes |
| vcl | 3374 | 0.644309 | 0.693147 | -0.048838 | [-0.060169, -0.037036] | yes |
| gc | 1005 | 0.601314 | 0.693147 | -0.091833 | [-0.116730, -0.068455] | yes |
| t3 | 16 | 0.514968 | 0.693147 | -0.178179 | [-0.426326, -0.034865] | yes |
| collegiate | 7 | 0.751519 | 0.693147 | 0.058372 | [0.055210, 0.062588] | yes |
| offseason | 855 | 0.635641 | 0.693147 | -0.057506 | [-0.082205, -0.032753] | yes |
| international=1 | 268 | 0.665812 | 0.693147 | -0.027335 | [-0.055413, -0.001955] | yes |
| international=0 | 6069 | 0.638887 | 0.693147 | -0.054260 | [-0.063003, -0.046007] | yes |

| Model | Section | Rows | Log loss | Brier | Accuracy | ECE |
|---|---|---:|---:|---:|---:|---:|
| player_round_glicko_rookie+form | all | 6337 | 0.639350 | 0.224471 | 0.627268 | 0.021887 |
| player_round_glicko_rookie+form | vct | 1080 | 0.667874 | 0.238070 | 0.584259 | 0.026646 |
| player_round_glicko_rookie+form | vcl | 3374 | 0.643313 | 0.225854 | 0.628631 | 0.032671 |
| player_round_glicko_rookie+form | gc | 1005 | 0.601660 | 0.208234 | 0.663682 | 0.043018 |
| player_round_glicko_rookie+form | t3 | 16 | 0.493042 | 0.163906 | 0.812500 | 0.164797 |
| player_round_glicko_rookie+form | collegiate | 7 | 0.775225 | 0.289901 | 0.357143 | 0.293434 |
| player_round_glicko_rookie+form | offseason | 855 | 0.633605 | 0.221516 | 0.632164 | 0.013809 |
| player_round_glicko_rookie+form | unknown | 0 | — | — | — | — |
| player_round_glicko_rookie+form | international=1 | 268 | 0.667381 | 0.237576 | 0.589552 | 0.042888 |
| player_round_glicko_rookie+form | international=0 | 6069 | 0.638112 | 0.223892 | 0.628934 | 0.022226 |

player_round_glicko_rookie+form − coin (paired log loss):

| Section | Rows | player_round_glicko_rookie+form log loss | coin log loss | Difference | 95% interval | Significant |
|---|---:|---:|---:|---:|---|---|
| all | 6337 | 0.639350 | 0.693147 | -0.053798 | [-0.062761, -0.045165] | yes |
| vct | 1080 | 0.667874 | 0.693147 | -0.025273 | [-0.041295, -0.009956] | yes |
| vcl | 3374 | 0.643313 | 0.693147 | -0.049834 | [-0.062403, -0.037028] | yes |
| gc | 1005 | 0.601660 | 0.693147 | -0.091487 | [-0.118378, -0.066464] | yes |
| t3 | 16 | 0.493042 | 0.693147 | -0.200105 | [-0.461121, -0.049649] | yes |
| collegiate | 7 | 0.775225 | 0.693147 | 0.082078 | [0.075283, 0.091138] | yes |
| offseason | 855 | 0.633605 | 0.693147 | -0.059542 | [-0.085934, -0.032892] | yes |
| international=1 | 268 | 0.667381 | 0.693147 | -0.025766 | [-0.056129, 0.002912] | no |
| international=0 | 6069 | 0.638112 | 0.693147 | -0.055035 | [-0.064447, -0.046086] | yes |

player_round_glicko_rookie − team_elo (paired log loss):

| Section | Rows | player_round_glicko_rookie log loss | team_elo log loss | Difference | 95% interval | Significant |
|---|---:|---:|---:|---:|---|---|
| all | 6337 | 0.640026 | 0.668065 | -0.028040 | [-0.034345, -0.021721] | yes |

player_round_glicko_rookie+form − team_elo (paired log loss):

| Section | Rows | player_round_glicko_rookie+form log loss | team_elo log loss | Difference | 95% interval | Significant |
|---|---:|---:|---:|---:|---|---|
| all | 6337 | 0.639350 | 0.668065 | -0.028716 | [-0.035334, -0.022256] | yes |

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
| player_round_glicko_rookie | all | 2618 | 0.610985 | 0.211846 | 0.661383 | 0.033243 |
| player_round_glicko_rookie | vct | 415 | 0.642619 | 0.226978 | 0.618072 | 0.055562 |
| player_round_glicko_rookie | vcl | 1351 | 0.620240 | 0.214624 | 0.661732 | 0.049952 |
| player_round_glicko_rookie | gc | 409 | 0.539456 | 0.184385 | 0.721271 | 0.052328 |
| player_round_glicko_rookie | t3 | 6 | 0.396459 | 0.127908 | 0.833333 | 0.150481 |
| player_round_glicko_rookie | collegiate | 2 | 0.592606 | 0.200519 | 0.750000 | 0.444318 |
| player_round_glicko_rookie | offseason | 435 | 0.622357 | 0.215815 | 0.642529 | 0.035480 |
| player_round_glicko_rookie | unknown | 0 | — | — | — | — |
| player_round_glicko_rookie | international=1 | 103 | 0.634562 | 0.221871 | 0.640777 | 0.094659 |
| player_round_glicko_rookie | international=0 | 2515 | 0.610019 | 0.211436 | 0.662227 | 0.033475 |

player_round_glicko_rookie − coin (paired log loss):

| Section | Rows | player_round_glicko_rookie log loss | coin log loss | Difference | 95% interval | Significant |
|---|---:|---:|---:|---:|---|---|
| all | 2618 | 0.610985 | 0.693147 | -0.082163 | [-0.099454, -0.064304] | yes |
| vct | 415 | 0.642619 | 0.693147 | -0.050528 | [-0.082039, -0.017136] | yes |
| vcl | 1351 | 0.620240 | 0.693147 | -0.072907 | [-0.098255, -0.046751] | yes |
| gc | 409 | 0.539456 | 0.693147 | -0.153691 | [-0.196532, -0.109751] | yes |
| t3 | 6 | 0.396459 | 0.693147 | -0.296688 | [-0.527465, -0.084629] | yes |
| collegiate | 2 | 0.592606 | 0.693147 | -0.100542 | [-0.201083, 0.000000] | no |
| offseason | 435 | 0.622357 | 0.693147 | -0.070790 | [-0.110186, -0.028986] | yes |
| international=1 | 103 | 0.634562 | 0.693147 | -0.058585 | [-0.124315, 0.004527] | no |
| international=0 | 2515 | 0.610019 | 0.693147 | -0.083128 | [-0.100133, -0.065142] | yes |

| Model | Section | Rows | Log loss | Brier | Accuracy | ECE |
|---|---|---:|---:|---:|---:|---:|
| player_round_glicko_rookie+form | all | 2618 | 0.611754 | 0.212125 | 0.658136 | 0.045976 |
| player_round_glicko_rookie+form | vct | 415 | 0.642169 | 0.226839 | 0.616867 | 0.061777 |
| player_round_glicko_rookie+form | vcl | 1351 | 0.620232 | 0.214495 | 0.661732 | 0.058815 |
| player_round_glicko_rookie+form | gc | 409 | 0.547761 | 0.187904 | 0.709046 | 0.066622 |
| player_round_glicko_rookie+form | t3 | 6 | 0.353053 | 0.109224 | 0.833333 | 0.136429 |
| player_round_glicko_rookie+form | collegiate | 2 | 0.592606 | 0.200519 | 0.750000 | 0.444318 |
| player_round_glicko_rookie+form | offseason | 435 | 0.620229 | 0.214972 | 0.635632 | 0.052242 |
| player_round_glicko_rookie+form | unknown | 0 | — | — | — | — |
| player_round_glicko_rookie+form | international=1 | 103 | 0.636929 | 0.222755 | 0.611650 | 0.103141 |
| player_round_glicko_rookie+form | international=0 | 2515 | 0.610723 | 0.211690 | 0.660040 | 0.045620 |

player_round_glicko_rookie+form − coin (paired log loss):

| Section | Rows | player_round_glicko_rookie+form log loss | coin log loss | Difference | 95% interval | Significant |
|---|---:|---:|---:|---:|---|---|
| all | 2618 | 0.611754 | 0.693147 | -0.081394 | [-0.099547, -0.062885] | yes |
| vct | 415 | 0.642169 | 0.693147 | -0.050978 | [-0.085167, -0.015255] | yes |
| vcl | 1351 | 0.620232 | 0.693147 | -0.072915 | [-0.100183, -0.044744] | yes |
| gc | 409 | 0.547761 | 0.693147 | -0.145386 | [-0.190854, -0.098101] | yes |
| t3 | 6 | 0.353053 | 0.693147 | -0.340094 | [-0.550125, -0.133666] | yes |
| collegiate | 2 | 0.592606 | 0.693147 | -0.100542 | [-0.201083, 0.000000] | no |
| offseason | 435 | 0.620229 | 0.693147 | -0.072918 | [-0.113691, -0.029225] | yes |
| international=1 | 103 | 0.636929 | 0.693147 | -0.056218 | [-0.128268, 0.012008] | no |
| international=0 | 2515 | 0.610723 | 0.693147 | -0.082425 | [-0.100527, -0.063457] | yes |

player_round_glicko_rookie − team_elo (paired log loss):

| Section | Rows | player_round_glicko_rookie log loss | team_elo log loss | Difference | 95% interval | Significant |
|---|---:|---:|---:|---:|---|---|
| all | 2618 | 0.610985 | 0.666264 | -0.055280 | [-0.070926, -0.039926] | yes |

player_round_glicko_rookie+form − team_elo (paired log loss):

| Section | Rows | player_round_glicko_rookie+form log loss | team_elo log loss | Difference | 95% interval | Significant |
|---|---:|---:|---:|---:|---|---|
| all | 2618 | 0.611754 | 0.666264 | -0.054511 | [-0.070239, -0.038484] | yes |

## Stage 2 — validation vs Kalshi

### player_round_glicko_rookie: Kalshi comparison and returns



#### Log loss vs Kalshi

| Kind | Slice | Rows | Model log loss | Kalshi log loss | Difference [95% interval] | Significant |
|---|---|---:|---:|---:|---|---|
| series | all | 677 | 0.628825 | 0.633240 | -0.004416 [-0.028425, 0.021291] | no |
| series | vct | 278 | 0.626733 | 0.634755 | -0.008022 [-0.039451, 0.022501] | no |
| series | vcl | 340 | 0.621172 | 0.619968 | 0.001204 [-0.040983, 0.043454] | no |
| series | gc | 0 | — | — | — | — |
| series | t3 | 0 | — | — | — | — |
| series | collegiate | 0 | — | — | — | — |
| series | offseason | 59 | 0.682780 | 0.702587 | -0.019807 [-0.079815, 0.039800] | no |
| series | international=1 | 41 | 0.603923 | 0.653397 | -0.049473 [-0.094209, -0.002226] | yes |
| series | international=0 | 636 | 0.630430 | 0.631941 | -0.001511 [-0.028562, 0.025595] | no |
| map | all | 1049 | 0.657187 | 0.668225 | -0.011038 [-0.032469, 0.007123] | no |
| map | vct | 461 | 0.659168 | 0.665762 | -0.006594 [-0.026226, 0.010777] | no |
| map | vcl | 490 | 0.650436 | 0.668365 | -0.017929 [-0.059772, 0.017852] | no |
| map | gc | 0 | — | — | — | — |
| map | t3 | 0 | — | — | — | — |
| map | collegiate | 0 | — | — | — | — |
| map | offseason | 98 | 0.681624 | 0.679111 | 0.002514 [-0.026714, 0.031644] | no |
| map | international=1 | 59 | 0.657367 | 0.649653 | 0.007714 [-0.015892, 0.032448] | no |
| map | international=0 | 990 | 0.657176 | 0.669332 | -0.012155 [-0.033914, 0.007725] | no |

#### Full-Kelly returns

| Kind | Slice | Bets | Matches | Mean edge | Flat ROI [95% interval] | Kelly, LoL caps ($50 start) | Multiple | Max drawdown | Largest stake | Bets filled | Flat ROI depth-capped [95% interval] | Kelly depth-capped final |
|---|---|---:|---:|---:|---|---:|---:|---:|---:|---:|---|---:|
| series | all | 510 | 510 | 0.0969 | 11.72% [0.33%, 23.72%] | $675.70 | 13.514× | 69.72% | $137.77 | 297 (213 unfilled) | 17.56% [2.43%, 33.67%] | $680.10 |
| series | vct | 210 | 210 | 0.0797 | 12.13% [-5.88%, 30.95%] | $122.09 | 2.442× | 68.44% | $11.11 | 131 (79 unfilled) | 23.10% [-0.86%, 48.44%] | $277.84 |
| series | vcl | 262 | 262 | 0.1132 | 11.97% [-3.94%, 29.80%] | $165.31 | 3.306× | 66.98% | $29.15 | 136 (126 unfilled) | 15.58% [-8.03%, 40.85%] | $85.80 |
| series | gc | 0 | 0 | — | — | $50.00 | 1.000× | 0.00% | $0.00 | 0 (0 unfilled) | — | $50.00 |
| series | t3 | 0 | 0 | — | — | $50.00 | 1.000× | 0.00% | $0.00 | 0 (0 unfilled) | — | $50.00 |
| series | collegiate | 0 | 0 | — | — | $50.00 | 1.000× | 0.00% | $0.00 | 0 (0 unfilled) | — | $50.00 |
| series | offseason | 38 | 38 | 0.0791 | 7.71% [-31.74%, 48.71%] | $73.78 | 1.476× | 36.33% | $9.14 | 30 (8 unfilled) | 2.36% [-39.13%, 46.27%] | $58.07 |
| series | international=1 | 28 | 28 | 0.0518 | 34.71% [-5.94%, 78.73%] | $110.93 | 2.219× | 19.12% | $8.83 | 27 (1 unfilled) | 34.09% [-10.08%, 79.16%] | $106.37 |
| series | international=0 | 482 | 482 | 0.0995 | 10.38% [-1.36%, 23.43%] | $322.01 | 6.440× | 69.83% | $85.62 | 270 (212 unfilled) | 15.91% [-1.36%, 32.71%] | $256.80 |
| map | all | 658 | 351 | 0.0669 | 19.06% [2.00%, 39.90%] | $5289.17 | 105.783× | 42.36% | $245.53 | 95 (563 unfilled) | 52.44% [-6.05%, 130.70%] | $227.94 |
| map | vct | 272 | 140 | 0.0510 | 11.25% [-6.77%, 36.63%] | $151.49 | 3.030× | 35.07% | $10.89 | 51 (221 unfilled) | 52.69% [-14.17%, 159.17%] | $109.10 |
| map | vcl | 337 | 186 | 0.0837 | 28.53% [-0.74%, 65.75%] | $2485.15 | 49.703× | 38.38% | $245.53 | 39 (298 unfilled) | 51.54% [-37.19%, 179.94%] | $110.35 |
| map | gc | 0 | 0 | — | — | $50.00 | 1.000× | 0.00% | $0.00 | 0 (0 unfilled) | — | $50.00 |
| map | t3 | 0 | 0 | — | — | $50.00 | 1.000× | 0.00% | $0.00 | 0 (0 unfilled) | — | $50.00 |
| map | collegiate | 0 | 0 | — | — | $50.00 | 1.000× | 0.00% | $0.00 | 0 (0 unfilled) | — | $50.00 |
| map | offseason | 49 | 25 | 0.0401 | -2.93% [-30.04%, 26.29%] | $60.59 | 1.212× | 13.74% | $4.18 | 5 (44 unfilled) | 57.01% [-51.92%, 178.39%] | $57.88 |
| map | international=1 | 28 | 15 | 0.0428 | -4.77% [-32.45%, 22.45%] | $43.60 | 0.872× | 17.16% | $4.86 | 12 (16 unfilled) | 14.47% [-21.82%, 54.81%] | $52.20 |
| map | international=0 | 630 | 336 | 0.0680 | 20.11% [1.72%, 42.54%] | $5334.34 | 106.687× | 38.58% | $245.53 | 83 (547 unfilled) | 57.88% [-7.77%, 143.23%] | $220.05 |
| series+map | all | 1168 | 530 | 0.0800 | 15.85% [3.69%, 28.73%] | $5302.51 | 106.050× | 55.89% | $248.08 | 392 (776 unfilled) | 26.04% [7.02%, 47.30%] | $372.04 |

#### Monthly market blend fits

UTC monthly fits use earlier rows of the same kind from 2025-09-01, excluding holdout; minimum 100 rows. logit(p_blend) = a·logit(mid) + b·(logit(p_model) − logit(mid)); inputs clipped to [0.01, 0.99], no intercept, ridge 1e-6. Unfitted rows use mid unchanged; excluded from blended tables: 240 rows. Rating parameters remain selected on the tuning window.

| Month | Kind | n | a | b | Status |
|---|---|---:|---:|---:|---|
| 2026-01 | series | 0 | 1.000000 | 0.000000 | unfitted |
| 2026-02 | series | 21 | 1.000000 | 0.000000 | unfitted |
| 2026-02 | map | 0 | 1.000000 | 0.000000 | unfitted |
| 2026-03 | series | 72 | 1.000000 | 0.000000 | unfitted |
| 2026-03 | map | 48 | 1.000000 | 0.000000 | unfitted |
| 2026-04 | series | 136 | 1.191825 | 0.528581 | fitted |
| 2026-04 | map | 104 | 1.606087 | 0.521611 | fitted |
| 2026-05 | series | 357 | 1.012523 | 0.537930 | fitted |
| 2026-05 | map | 456 | 1.194298 | 1.001550 | fitted |
| 2026-06 | series | 556 | 0.961421 | 0.546688 | fitted |
| 2026-06 | map | 833 | 1.021403 | 0.841878 | fitted |

#### Log loss vs Kalshi (blended)

| Kind | Slice | Rows | Model log loss | Kalshi log loss | Difference [95% interval] | Significant |
|---|---|---:|---:|---:|---|---|
| series | all | 541 | 0.621501 | 0.634347 | -0.012846 [-0.026646, 0.001643] | no |
| series | vct | 201 | 0.633653 | 0.644147 | -0.010494 [-0.028219, 0.008123] | no |
| series | vcl | 291 | 0.604100 | 0.621829 | -0.017729 [-0.038577, 0.006164] | no |
| series | gc | 0 | — | — | — | — |
| series | t3 | 0 | — | — | — | — |
| series | collegiate | 0 | — | — | — | — |
| series | offseason | 49 | 0.674997 | 0.668490 | 0.006507 [-0.025894, 0.036456] | no |
| series | international=1 | 24 | 0.654574 | 0.682705 | -0.028132 [-0.066383, 0.009006] | no |
| series | international=0 | 517 | 0.619966 | 0.632102 | -0.012136 [-0.025963, 0.002835] | no |
| map | all | 945 | 0.676735 | 0.673192 | 0.003543 [-0.006954, 0.014745] | no |
| map | vct | 392 | 0.667434 | 0.667249 | 0.000185 [-0.014591, 0.014308] | no |
| map | vcl | 456 | 0.682593 | 0.676303 | 0.006290 [-0.010379, 0.023578] | no |
| map | gc | 0 | — | — | — | — |
| map | t3 | 0 | — | — | — | — |
| map | collegiate | 0 | — | — | — | — |
| map | offseason | 97 | 0.686784 | 0.682581 | 0.004203 [-0.025449, 0.034726] | no |
| map | international=1 | 50 | 0.657225 | 0.651359 | 0.005867 [-0.015256, 0.025787] | no |
| map | international=0 | 895 | 0.677825 | 0.674412 | 0.003414 [-0.008071, 0.014396] | no |

#### Full-Kelly returns (blended)

| Kind | Slice | Bets | Matches | Mean edge | Flat ROI [95% interval] | Kelly, LoL caps ($50 start) | Multiple | Max drawdown | Largest stake | Bets filled | Flat ROI depth-capped [95% interval] | Kelly depth-capped final |
|---|---|---:|---:|---:|---|---:|---:|---:|---:|---:|---|---:|
| series | all | 289 | 289 | 0.0457 | 15.80% [0.24%, 32.19%] | $489.40 | 9.788× | 41.96% | $53.87 | 158 (131 unfilled) | 16.18% [-4.40%, 37.47%] | $221.77 |
| series | vct | 101 | 101 | 0.0372 | 10.22% [-15.62%, 38.75%] | $55.28 | 1.106× | 41.34% | $5.40 | 60 (41 unfilled) | 18.56% [-12.13%, 52.29%] | $94.92 |
| series | vcl | 167 | 167 | 0.0525 | 21.36% [1.19%, 43.33%] | $419.96 | 8.399× | 32.34% | $46.23 | 82 (85 unfilled) | 21.82% [-5.35%, 52.11%] | $114.49 |
| series | gc | 0 | 0 | — | — | $50.00 | 1.000× | 0.00% | $0.00 | 0 (0 unfilled) | — | $50.00 |
| series | t3 | 0 | 0 | — | — | $50.00 | 1.000× | 0.00% | $0.00 | 0 (0 unfilled) | — | $50.00 |
| series | collegiate | 0 | 0 | — | — | $50.00 | 1.000× | 0.00% | $0.00 | 0 (0 unfilled) | — | $50.00 |
| series | offseason | 21 | 21 | 0.0325 | -1.46% [-50.73%, 53.86%] | $51.89 | 1.038× | 10.08% | $4.83 | 16 (5 unfilled) | -21.53% [-70.80%, 31.27%] | $45.17 |
| series | international=1 | 10 | 10 | 0.0338 | 66.05% [-19.68%, 162.22%] | $73.38 | 1.468× | 4.78% | $6.08 | 10 (0 unfilled) | 66.05% [-19.68%, 162.22%] | $73.38 |
| series | international=0 | 279 | 279 | 0.0461 | 14.00% [-1.50%, 30.74%] | $333.94 | 6.679× | 41.96% | $36.76 | 148 (131 unfilled) | 12.81% [-6.96%, 34.14%] | $141.11 |
| map | all | 574 | 306 | 0.0431 | 0.87% [-9.35%, 12.81%] | $15.37 | 0.307× | 80.67% | $7.15 | 77 (497 unfilled) | 0.83% [-18.99%, 21.55%] | $44.69 |
| map | vct | 230 | 120 | 0.0409 | -1.09% [-12.90%, 11.00%] | $33.05 | 0.661× | 43.80% | $5.74 | 34 (196 unfilled) | 23.59% [-7.11%, 57.51%] | $62.55 |
| map | vcl | 293 | 160 | 0.0463 | 1.76% [-15.05%, 22.71%] | $20.88 | 0.418× | 73.94% | $7.29 | 38 (255 unfilled) | -21.00% [-46.58%, 4.21%] | $34.81 |
| map | gc | 0 | 0 | — | — | $50.00 | 1.000× | 0.00% | $0.00 | 0 (0 unfilled) | — | $50.00 |
| map | t3 | 0 | 0 | — | — | $50.00 | 1.000× | 0.00% | $0.00 | 0 (0 unfilled) | — | $50.00 |
| map | collegiate | 0 | 0 | — | — | $50.00 | 1.000× | 0.00% | $0.00 | 0 (0 unfilled) | — | $50.00 |
| map | offseason | 51 | 26 | 0.0341 | 4.61% [-22.44%, 31.28%] | $49.12 | 0.982× | 13.72% | $3.77 | 5 (46 unfilled) | 12.31% [-54.39%, 67.66%] | $51.21 |
| map | international=1 | 23 | 11 | 0.0342 | 0.73% [-29.38%, 29.69%] | $45.94 | 0.919× | 9.55% | $2.69 | 9 (14 unfilled) | 13.86% [-17.62%, 63.48%] | $49.65 |
| map | international=0 | 551 | 295 | 0.0434 | 0.88% [-9.31%, 14.30%] | $16.83 | 0.337× | 78.82% | $7.15 | 68 (483 unfilled) | -0.89% [-23.43%, 23.03%] | $45.13 |
| series+map | all | 863 | 378 | 0.0439 | 5.88% [-4.17%, 16.74%] | $86.60 | 1.732× | 61.19% | $13.14 | 235 (628 unfilled) | 11.17% [-4.17%, 26.60%] | $93.33 |

#### Monthly breakdown

All metrics use identical linked rows within each kind/month. Unfitted blend months show —; counts include all rows.

| Kind | Month | Rows | Model log loss | Blended log loss | Kalshi log loss | Raw flat ROI (bets), unlimited Kelly final | Blended flat ROI (bets), unlimited Kelly final | Raw bets filled | Raw Flat ROI depth-capped [95% interval] | Raw Kelly depth-capped final | Blended bets filled | Blended Flat ROI depth-capped [95% interval] | Blended Kelly depth-capped final |
|---|---|---:|---:|---:|---:|---|---|---:|---|---:|---:|---|---:|
| map | 2026-02 | 48 | 0.705248 | — | 0.690786 | 1.68% (39), $46.31 | — | 11 (28 unfilled) | 0.62% [-72.68%, 56.89%] | $50.05 | — | — | — |
| map | 2026-03 | 56 | 0.604159 | — | 0.565065 | -11.42% (43), $33.27 | — | 12 (31 unfilled) | -39.10% [-86.87%, 16.47%] | $42.07 | — | — | — |
| map | 2026-04 | 352 | 0.635726 | 0.688899 | 0.690793 | 59.45% (236), $5852.95 | 5.69% (239), $42.77 | 27 (209 unfilled) | 187.37% [0.07%, 441.42%] | $238.41 | 30 (209 unfilled) | -5.94% [-26.00%, 14.17%] | $52.68 |
| map | 2026-05 | 377 | 0.682931 | 0.685489 | 0.687018 | 3.49% (210), $83.82 | 4.93% (212), $42.71 | 26 (184 unfilled) | 23.23% [-28.65%, 75.14%] | $63.54 | 28 (184 unfilled) | 17.51% [-24.91%, 60.78%] | $56.24 |
| map | 2026-06 | 216 | 0.650295 | 0.641634 | 0.620377 | -13.83% (130), $20.03 | -15.36% (123), $21.34 | 19 (111 unfilled) | -13.18% [-48.56%, 27.29%] | $38.26 | 19 (104 unfilled) | -13.18% [-48.56%, 27.29%] | $37.88 |
| series | 2026-01 | 21 | 0.606062 | — | 0.661069 | 9.93% (19), $74.48 | — | 11 (8 unfilled) | -20.76% [-80.73%, 43.15%] | $50.39 | — | — | — |
| series | 2026-02 | 51 | 0.692180 | — | 0.694525 | 4.86% (40), $52.92 | — | 28 (12 unfilled) | 25.54% [-28.30%, 97.45%] | $74.39 | — | — | — |
| series | 2026-03 | 64 | 0.604680 | — | 0.565917 | -5.08% (58), $31.63 | — | 43 (15 unfilled) | 8.97% [-21.14%, 35.88%] | $57.73 | — | — | — |
| series | 2026-04 | 221 | 0.616885 | 0.612442 | 0.627690 | 21.40% (163), $310.56 | 18.56% (120), $151.80 | 75 (88 unfilled) | 44.78% [6.66%, 88.68%] | $232.22 | 55 (65 unfilled) | 31.25% [-4.35%, 72.62%] | $97.80 |
| series | 2026-05 | 199 | 0.651730 | 0.649360 | 0.663719 | 13.64% (148), $139.90 | 19.04% (106), $96.77 | 97 (51 unfilled) | 5.42% [-16.77%, 30.18%] | $54.41 | 68 (38 unfilled) | 4.57% [-22.81%, 35.26%] | $63.61 |
| series | 2026-06 | 121 | 0.602978 | 0.592231 | 0.598199 | 4.61% (82), $40.54 | 5.16% (63), $82.49 | 43 (39 unfilled) | 10.55% [-23.54%, 48.25%] | $57.73 | 35 (28 unfilled) | 15.16% [-25.87%, 57.64%] | $76.14 |

### player_round_glicko_rookie+form: Kalshi comparison and returns

form: rows=13161, H=2, w=0.76446

#### Log loss vs Kalshi

| Kind | Slice | Rows | Model log loss | Kalshi log loss | Difference [95% interval] | Significant |
|---|---|---:|---:|---:|---|---|
| series | all | 677 | 0.628081 | 0.633240 | -0.005159 [-0.030978, 0.021621] | no |
| series | vct | 278 | 0.625705 | 0.634755 | -0.009050 [-0.042393, 0.023049] | no |
| series | vcl | 340 | 0.621792 | 0.619968 | 0.001824 [-0.042597, 0.046900] | no |
| series | gc | 0 | — | — | — | — |
| series | t3 | 0 | — | — | — | — |
| series | collegiate | 0 | — | — | — | — |
| series | offseason | 59 | 0.675519 | 0.702587 | -0.027068 [-0.093508, 0.042035] | no |
| series | international=1 | 41 | 0.594298 | 0.653397 | -0.059099 [-0.107442, -0.007625] | yes |
| series | international=0 | 636 | 0.630259 | 0.631941 | -0.001682 [-0.030507, 0.026600] | no |
| map | all | 1049 | 0.656087 | 0.668225 | -0.012138 [-0.034068, 0.006165] | no |
| map | vct | 461 | 0.657721 | 0.665762 | -0.008040 [-0.027756, 0.009574] | no |
| map | vcl | 490 | 0.649324 | 0.668365 | -0.019041 [-0.060413, 0.016932] | no |
| map | gc | 0 | — | — | — | — |
| map | t3 | 0 | — | — | — | — |
| map | collegiate | 0 | — | — | — | — |
| map | offseason | 98 | 0.682215 | 0.679111 | 0.003104 [-0.030388, 0.037065] | no |
| map | international=1 | 59 | 0.650351 | 0.649653 | 0.000698 [-0.028442, 0.028792] | no |
| map | international=0 | 990 | 0.656429 | 0.669332 | -0.012903 [-0.034961, 0.007454] | no |

#### Full-Kelly returns

| Kind | Slice | Bets | Matches | Mean edge | Flat ROI [95% interval] | Kelly, LoL caps ($50 start) | Multiple | Max drawdown | Largest stake | Bets filled | Flat ROI depth-capped [95% interval] | Kelly depth-capped final |
|---|---|---:|---:|---:|---|---:|---:|---:|---:|---:|---|---:|
| series | all | 534 | 534 | 0.1002 | 11.46% [0.67%, 22.94%] | $1150.86 | 23.017× | 65.49% | $219.60 | 307 (227 unfilled) | 17.43% [3.30%, 32.43%] | $367.67 |
| series | vct | 224 | 224 | 0.0822 | 11.89% [-4.41%, 29.26%] | $113.03 | 2.261× | 68.13% | $10.79 | 135 (89 unfilled) | 22.12% [1.22%, 45.31%] | $238.27 |
| series | vcl | 273 | 273 | 0.1158 | 11.00% [-4.13%, 28.31%] | $271.69 | 5.434× | 68.17% | $47.89 | 142 (131 unfilled) | 15.72% [-6.44%, 39.12%] | $104.68 |
| series | gc | 0 | 0 | — | — | $50.00 | 1.000× | 0.00% | $0.00 | 0 (0 unfilled) | — | $50.00 |
| series | t3 | 0 | 0 | — | — | $50.00 | 1.000× | 0.00% | $0.00 | 0 (0 unfilled) | — | $50.00 |
| series | collegiate | 0 | 0 | — | — | $50.00 | 1.000× | 0.00% | $0.00 | 0 (0 unfilled) | — | $50.00 |
| series | offseason | 37 | 37 | 0.0941 | 12.34% [-23.97%, 52.51%] | $72.80 | 1.456× | 39.55% | $9.52 | 30 (7 unfilled) | 4.48% [-33.52%, 47.39%] | $46.73 |
| series | international=1 | 33 | 33 | 0.0491 | 31.06% [-2.79%, 68.51%] | $125.95 | 2.519× | 18.36% | $10.03 | 32 (1 unfilled) | 30.42% [-4.78%, 70.90%] | $122.15 |
| series | international=0 | 501 | 501 | 0.1036 | 10.18% [-1.13%, 22.26%] | $479.30 | 9.586× | 66.51% | $119.06 | 275 (226 unfilled) | 15.92% [0.13%, 30.73%] | $120.11 |
| map | all | 675 | 362 | 0.0720 | 20.90% [4.16%, 41.26%] | $5938.13 | 118.763× | 45.67% | $245.53 | 99 (576 unfilled) | 56.01% [1.03%, 131.75%] | $247.69 |
| map | vct | 280 | 146 | 0.0569 | 12.15% [-6.05%, 34.88%] | $131.40 | 2.628× | 31.51% | $10.50 | 52 (228 unfilled) | 58.41% [-6.60%, 159.89%] | $107.35 |
| map | vcl | 341 | 189 | 0.0883 | 31.62% [3.57%, 66.29%] | $2469.82 | 49.396× | 38.07% | $245.53 | 42 (299 unfilled) | 52.93% [-31.79%, 164.98%] | $124.73 |
| map | gc | 0 | 0 | — | — | $50.00 | 1.000× | 0.00% | $0.00 | 0 (0 unfilled) | — | $50.00 |
| map | t3 | 0 | 0 | — | — | $50.00 | 1.000× | 0.00% | $0.00 | 0 (0 unfilled) | — | $50.00 |
| map | collegiate | 0 | 0 | — | — | $50.00 | 1.000× | 0.00% | $0.00 | 0 (0 unfilled) | — | $50.00 |
| map | offseason | 54 | 27 | 0.0468 | -1.61% [-30.29%, 29.69%] | $53.32 | 1.066× | 20.03% | $4.14 | 5 (49 unfilled) | 57.01% [-51.92%, 178.39%] | $58.96 |
| map | international=1 | 30 | 17 | 0.0499 | 4.29% [-24.09%, 30.48%] | $40.54 | 0.811× | 25.77% | $4.92 | 15 (15 unfilled) | 22.50% [-9.92%, 55.40%] | $48.45 |
| map | international=0 | 645 | 345 | 0.0730 | 21.67% [3.95%, 44.02%] | $6077.02 | 121.540× | 38.58% | $245.53 | 84 (561 unfilled) | 61.92% [-6.67%, 142.58%] | $245.81 |
| series+map | all | 1209 | 558 | 0.0844 | 16.73% [4.64%, 29.74%] | $4637.07 | 92.741× | 57.89% | $248.60 | 406 (803 unfilled) | 26.87% [7.88%, 47.77%] | $298.03 |

#### Monthly market blend fits

UTC monthly fits use earlier rows of the same kind from 2025-09-01, excluding holdout; minimum 100 rows. logit(p_blend) = a·logit(mid) + b·(logit(p_model) − logit(mid)); inputs clipped to [0.01, 0.99], no intercept, ridge 1e-6. Unfitted rows use mid unchanged; excluded from blended tables: 240 rows. Rating parameters remain selected on the tuning window.

| Month | Kind | n | a | b | Status |
|---|---|---:|---:|---:|---|
| 2026-01 | series | 0 | 1.000000 | 0.000000 | unfitted |
| 2026-02 | series | 21 | 1.000000 | 0.000000 | unfitted |
| 2026-02 | map | 0 | 1.000000 | 0.000000 | unfitted |
| 2026-03 | series | 72 | 1.000000 | 0.000000 | unfitted |
| 2026-03 | map | 48 | 1.000000 | 0.000000 | unfitted |
| 2026-04 | series | 136 | 1.190517 | 0.543978 | fitted |
| 2026-04 | map | 104 | 1.590482 | 0.527286 | fitted |
| 2026-05 | series | 357 | 0.994100 | 0.521099 | fitted |
| 2026-05 | map | 456 | 1.116457 | 0.912690 | fitted |
| 2026-06 | series | 556 | 0.938586 | 0.532333 | fitted |
| 2026-06 | map | 833 | 0.966804 | 0.785852 | fitted |

#### Log loss vs Kalshi (blended)

| Kind | Slice | Rows | Model log loss | Kalshi log loss | Difference [95% interval] | Significant |
|---|---|---:|---:|---:|---|---|
| series | all | 541 | 0.619858 | 0.634347 | -0.014489 [-0.029442, 0.000739] | no |
| series | vct | 201 | 0.632868 | 0.644147 | -0.011279 [-0.030710, 0.008617] | no |
| series | vcl | 291 | 0.601876 | 0.621829 | -0.019952 [-0.042906, 0.005091] | no |
| series | gc | 0 | — | — | — | — |
| series | t3 | 0 | — | — | — | — |
| series | collegiate | 0 | — | — | — | — |
| series | offseason | 49 | 0.673284 | 0.668490 | 0.004794 [-0.030425, 0.038120] | no |
| series | international=1 | 24 | 0.641893 | 0.682705 | -0.040812 [-0.083101, 0.000304] | no |
| series | international=0 | 517 | 0.618835 | 0.632102 | -0.013267 [-0.028359, 0.002277] | no |
| map | all | 945 | 0.674426 | 0.673192 | 0.001234 [-0.009370, 0.012733] | no |
| map | vct | 392 | 0.665532 | 0.667249 | -0.001718 [-0.016971, 0.012487] | no |
| map | vcl | 456 | 0.679564 | 0.676303 | 0.003261 [-0.013470, 0.020471] | no |
| map | gc | 0 | — | — | — | — |
| map | t3 | 0 | — | — | — | — |
| map | collegiate | 0 | — | — | — | — |
| map | offseason | 97 | 0.686216 | 0.682581 | 0.003635 [-0.027984, 0.036440] | no |
| map | international=1 | 50 | 0.649076 | 0.651359 | -0.002283 [-0.026841, 0.020265] | no |
| map | international=0 | 895 | 0.675842 | 0.674412 | 0.001431 [-0.010233, 0.012146] | no |

#### Full-Kelly returns (blended)

| Kind | Slice | Bets | Matches | Mean edge | Flat ROI [95% interval] | Kelly, LoL caps ($50 start) | Multiple | Max drawdown | Largest stake | Bets filled | Flat ROI depth-capped [95% interval] | Kelly depth-capped final |
|---|---|---:|---:|---:|---|---:|---:|---:|---:|---:|---|---:|
| series | all | 302 | 302 | 0.0506 | 16.96% [1.84%, 31.69%] | $443.35 | 8.867× | 56.72% | $53.80 | 158 (144 unfilled) | 17.83% [-1.08%, 38.43%] | $180.87 |
| series | vct | 109 | 109 | 0.0412 | 10.82% [-11.94%, 35.19%] | $48.74 | 0.975× | 62.23% | $5.47 | 63 (46 unfilled) | 19.03% [-8.50%, 47.44%] | $92.11 |
| series | vcl | 172 | 172 | 0.0578 | 22.62% [3.00%, 42.19%] | $458.82 | 9.176× | 34.10% | $55.68 | 79 (93 unfilled) | 26.46% [-1.25%, 57.52%] | $107.62 |
| series | gc | 0 | 0 | — | — | $50.00 | 1.000× | 0.00% | $0.00 | 0 (0 unfilled) | — | $50.00 |
| series | t3 | 0 | 0 | — | — | $50.00 | 1.000× | 0.00% | $0.00 | 0 (0 unfilled) | — | $50.00 |
| series | collegiate | 0 | 0 | — | — | $50.00 | 1.000× | 0.00% | $0.00 | 0 (0 unfilled) | — | $50.00 |
| series | offseason | 21 | 21 | 0.0416 | 2.48% [-48.71%, 55.09%] | $48.51 | 0.970× | 14.60% | $4.42 | 16 (5 unfilled) | -29.41% [-73.60%, 20.01%] | $39.94 |
| series | international=1 | 10 | 10 | 0.0427 | 63.06% [-18.12%, 162.35%] | $77.71 | 1.554× | 7.89% | $6.28 | 10 (0 unfilled) | 63.06% [-18.12%, 162.35%] | $77.71 |
| series | international=0 | 292 | 292 | 0.0509 | 15.38% [1.12%, 30.40%] | $285.82 | 5.716× | 56.72% | $34.69 | 148 (144 unfilled) | 14.78% [-4.05%, 34.09%] | $107.27 |
| map | all | 566 | 307 | 0.0463 | 2.53% [-7.55%, 14.92%] | $23.29 | 0.466× | 72.02% | $7.03 | 74 (492 unfilled) | 8.66% [-12.27%, 33.05%] | $62.15 |
| map | vct | 225 | 118 | 0.0442 | -3.04% [-13.33%, 7.90%] | $36.81 | 0.736× | 49.86% | $5.53 | 32 (193 unfilled) | 25.70% [-6.42%, 62.87%] | $73.17 |
| map | vcl | 294 | 164 | 0.0486 | 7.22% [-9.40%, 28.98%] | $28.40 | 0.568× | 71.90% | $9.12 | 38 (256 unfilled) | -14.95% [-41.63%, 12.64%] | $39.49 |
| map | gc | 0 | 0 | — | — | $50.00 | 1.000× | 0.00% | $0.00 | 0 (0 unfilled) | — | $50.00 |
| map | t3 | 0 | 0 | — | — | $50.00 | 1.000× | 0.00% | $0.00 | 0 (0 unfilled) | — | $50.00 |
| map | collegiate | 0 | 0 | — | — | $50.00 | 1.000× | 0.00% | $0.00 | 0 (0 unfilled) | — | $50.00 |
| map | offseason | 47 | 25 | 0.0420 | -0.15% [-32.16%, 33.46%] | $49.56 | 0.991× | 15.90% | $4.39 | 4 (43 unfilled) | 95.88% [13.38%, 262.84%] | $53.66 |
| map | international=1 | 21 | 10 | 0.0443 | -7.03% [-41.78%, 27.30%] | $48.61 | 0.972× | 8.05% | $2.58 | 8 (13 unfilled) | 7.57% [-25.23%, 62.76%] | $50.39 |
| map | international=0 | 545 | 297 | 0.0464 | 2.90% [-7.56%, 15.37%] | $24.02 | 0.480× | 71.15% | $7.03 | 66 (479 unfilled) | 8.80% [-15.10%, 34.15%] | $61.70 |
| series+map | all | 868 | 385 | 0.0478 | 7.56% [-1.64%, 17.92%] | $77.70 | 1.554× | 64.95% | $12.46 | 232 (636 unfilled) | 14.92% [0.08%, 30.13%] | $106.24 |

#### Monthly breakdown

All metrics use identical linked rows within each kind/month. Unfitted blend months show —; counts include all rows.

| Kind | Month | Rows | Model log loss | Blended log loss | Kalshi log loss | Raw flat ROI (bets), unlimited Kelly final | Blended flat ROI (bets), unlimited Kelly final | Raw bets filled | Raw Flat ROI depth-capped [95% interval] | Raw Kelly depth-capped final | Blended bets filled | Blended Flat ROI depth-capped [95% interval] | Blended Kelly depth-capped final |
|---|---|---:|---:|---:|---:|---|---|---:|---|---:|---:|---|---:|
| map | 2026-02 | 48 | 0.704133 | — | 0.690786 | 0.72% (33), $42.57 | — | 10 (23 unfilled) | -11.20% [-100.00%, 51.16%] | $46.09 | — | — | — |
| map | 2026-03 | 56 | 0.599537 | — | 0.565065 | -7.59% (43), $33.89 | — | 12 (31 unfilled) | -25.42% [-75.34%, 36.09%] | $40.51 | — | — | — |
| map | 2026-04 | 352 | 0.637262 | 0.687736 | 0.690793 | 57.66% (237), $6433.88 | 9.55% (240), $46.20 | 28 (209 unfilled) | 184.01% [6.10%, 416.01%] | $235.69 | 30 (210 unfilled) | -5.94% [-26.00%, 14.17%] | $52.82 |
| map | 2026-05 | 377 | 0.681796 | 0.682833 | 0.687018 | 6.87% (231), $84.17 | 2.26% (213), $63.07 | 28 (203 unfilled) | 33.07% [-12.63%, 80.42%] | $75.97 | 26 (187 unfilled) | 43.34% [-6.62%, 93.84%] | $76.17 |
| map | 2026-06 | 216 | 0.645877 | 0.638063 | 0.620377 | -6.45% (131), $22.62 | -11.69% (113), $20.03 | 21 (110 unfilled) | -7.28% [-43.28%, 29.70%] | $38.08 | 18 (95 unfilled) | -17.44% [-56.26%, 23.04%] | $38.79 |
| series | 2026-01 | 21 | 0.588066 | — | 0.661069 | 22.85% (17), $72.66 | — | 10 (7 unfilled) | -12.88% [-78.84%, 59.15%] | $47.23 | — | — | — |
| series | 2026-02 | 51 | 0.688613 | — | 0.694525 | 5.12% (43), $60.04 | — | 30 (13 unfilled) | 28.04% [-26.26%, 91.69%] | $82.49 | — | — | — |
| series | 2026-03 | 64 | 0.606299 | — | 0.565917 | -3.22% (57), $33.68 | — | 44 (13 unfilled) | 6.68% [-22.09%, 34.87%] | $57.02 | — | — | — |
| series | 2026-04 | 221 | 0.620375 | 0.612101 | 0.627690 | 17.72% (176), $364.83 | 21.02% (132), $146.08 | 72 (104 unfilled) | 44.25% [8.81%, 87.33%] | $175.61 | 58 (74 unfilled) | 37.35% [3.38%, 75.39%] | $88.41 |
| series | 2026-05 | 199 | 0.650987 | 0.647486 | 0.663719 | 17.53% (152), $137.98 | 19.44% (107), $97.02 | 101 (51 unfilled) | 8.06% [-14.47%, 32.05%] | $38.53 | 67 (40 unfilled) | 1.72% [-21.26%, 24.82%] | $56.22 |
| series | 2026-06 | 121 | 0.597437 | 0.588590 | 0.598199 | -0.99% (89), $50.11 | 4.31% (63), $77.38 | 50 (39 unfilled) | 6.80% [-22.04%, 39.13%] | $76.58 | 33 (30 unfilled) | 16.31% [-27.22%, 58.97%] | $77.54 |
