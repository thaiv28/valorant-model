# Elo variants benchmark

## Combined summary (validation, all sections)

| Model | Series Δ log loss | Series flat ROI | Series Kelly (LoL caps) $ | Map Δ log loss | Map flat ROI | Map Kelly (LoL caps) $ | Series blended Δ log loss | Series blended flat ROI | Series blended Kelly (LoL caps) $ | Map blended Δ log loss | Map blended flat ROI | Map blended Kelly (LoL caps) $ |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| team_elo | 0.047450 | 2.54% | $0.35 | 0.005735 | 13.04% | $596.77 | 0.001219 | -2.16% | $27.44 | 0.012801 | -6.71% | $8.52 |
| player_round_glicko | 0.000805 | 8.81% | $145.02 | -0.004729 | 15.63% | $3517.67 | -0.006022 | 10.99% | $128.12 | 0.008849 | -3.64% | $10.93 |
| player_round_glicko_rookie | -0.008487 | 12.48% | $1039.73 | -0.008821 | 15.54% | $3658.56 | -0.016021 | 17.02% | $787.94 | 0.005885 | -3.03% | $21.98 |
| team_elo+form | 0.048199 | 3.08% | $3.34 | 0.004183 | 14.04% | $1425.04 | 0.001559 | 6.27% | $24.91 | 0.009745 | -4.34% | $7.41 |
| team_elo+regional_form | 0.047003 | 3.46% | $3.80 | 0.002892 | 14.04% | $2358.82 | 0.001260 | 8.39% | $24.95 | 0.009067 | 0.79% | $7.84 |
| player_round_glicko+form | 0.001046 | 10.20% | $329.18 | -0.005317 | 18.38% | $3608.51 | -0.007046 | 10.05% | $102.97 | 0.006945 | -5.19% | $8.82 |
| player_round_glicko+regional_form | 0.001322 | 9.20% | $257.01 | -0.006039 | 18.45% | $4572.62 | -0.007436 | 8.07% | $101.27 | 0.005920 | -0.23% | $8.72 |
| player_round_glicko_rookie+form | -0.010793 | 16.71% | $1207.87 | -0.010728 | 19.01% | $4158.03 | -0.017310 | 17.39% | $552.51 | 0.003187 | 1.08% | $24.77 |
| player_round_glicko_rookie+regional_form | -0.010497 | 15.02% | $967.92 | -0.011536 | 19.15% | $5056.26 | -0.017304 | 18.07% | $507.70 | 0.001927 | 0.97% | $30.00 |

Parameters minimize tuning map log loss across all sections. Replay predicts before update; Replay starts at the first map. Tuning: [2024-10-01, 2025-09-01); validation: [2025-09-01, 2026-07-01). Holdout is scored only with --holdout and never selects parameters. Series use the first map prediction and independent maps in an odd best-of; missing/even best-of or unknown results are skipped. Accuracy gives 0.5 predictions half credit; ECE uses 10 equal-width bins. Log loss clips probabilities at 1e-6. Paired bootstrap uses 2,000 resamples, seed 0, clustered by match_id. Differences are the named model minus its comparator; negative favors the model. Significance requires a 95% percentile interval excluding zero. Tuning scores are selection diagnostics, not independent evidence of improvement.

Fit through 2025-08-31. Unknown host-region map rows: 2668 (including missing/un).

## Stage 1 — tuning (outcomes)

### Leaderboard

| Model | Best params | Map log loss | Series log loss | Rows |
|---|---|---:|---:|---:|
| player_round_glicko_rookie | {"k": 32, "new_player": "teammates", "rd_info": 0.25, "rd_new": 280, "rookie_maps": 100, "rookie_penalty": 200, "tau": 0.4} | 0.646962 | 0.617002 | 8241 |
| player_round_glicko | {"k": 32, "new_player": "teammates", "rd_info": 0.25, "rd_new": 280, "tau": 0.5} | 0.651611 | 0.630314 | 8241 |
| team_elo | {"k": 32} | 0.667801 | 0.656035 | 8241 |

Kalshi uses the first hourly bid/ask (midpoint for log loss, ask/bid for bets) ending ≥30 min after the market opened and ≥2 h before the scheduled start, with a spread ≤ 0.06: a price a bot could trade before any veto. Markets without such a quote are skipped. oriented to team1 using aliases. One contract per event, preferring team1. Compare identical rows; map predictions use the first map's pre-match chance. Missing links, aliases or candles are skipped. Backtests use frozen stage-1 parameters on validation rows. Layers fit only tuning rows. Fills are assumed at the hourly candle’s ask/bid with no depth limit or slippage; unplayed maps are not in the rows. Kalshi taker fees use unrounded f(c)=0.07×c×(1−c) per contract. Buy the larger positive after-fee edge, otherwise skip; require a two-sided quote with both buy costs in (0,1). Full Kelly uses fraction (q−c′)/(1−c′), c′=c+f(c). All bets in a match use its starting bankroll, scaling fractions to sum to at most one, then settle together. Each kind/slice runs its own $50 path. Drawdown uses settled match balances. Flat stakes are $1 all-in per bet; ROI intervals resample whole matches 2,000 times, seed 0.

### Maps

| Model | Section | Rows | Log loss | Brier | Accuracy | ECE |
|---|---|---:|---:|---:|---:|---:|
| coin | all | 8241 | 0.693147 | 0.250000 | 0.500000 | 0.046050 |
| coin | vct | 1260 | 0.693147 | 0.250000 | 0.500000 | 0.015079 |
| coin | vcl | 4384 | 0.693147 | 0.250000 | 0.500000 | 0.036268 |
| coin | gc | 1258 | 0.693147 | 0.250000 | 0.500000 | 0.093005 |
| coin | t3 | 283 | 0.693147 | 0.250000 | 0.500000 | 0.012367 |
| coin | collegiate | 0 | — | — | — | — |
| coin | offseason | 1056 | 0.693147 | 0.250000 | 0.500000 | 0.076705 |
| coin | unknown | 0 | — | — | — | — |
| coin | international=1 | 300 | 0.693147 | 0.250000 | 0.500000 | 0.006667 |
| coin | international=0 | 7941 | 0.693147 | 0.250000 | 0.500000 | 0.047538 |

| Model | Section | Rows | Log loss | Brier | Accuracy | ECE |
|---|---|---:|---:|---:|---:|---:|
| team_elo | all | 8241 | 0.667801 | 0.237452 | 0.595134 | 0.033857 |
| team_elo | vct | 1260 | 0.688933 | 0.247071 | 0.565476 | 0.049623 |
| team_elo | vcl | 4384 | 0.663260 | 0.235323 | 0.606182 | 0.028636 |
| team_elo | gc | 1258 | 0.646857 | 0.227715 | 0.615660 | 0.069239 |
| team_elo | t3 | 283 | 0.705413 | 0.254981 | 0.521201 | 0.039764 |
| team_elo | collegiate | 0 | — | — | — | — |
| team_elo | offseason | 1056 | 0.676308 | 0.241715 | 0.580019 | 0.051697 |
| team_elo | unknown | 0 | — | — | — | — |
| team_elo | international=1 | 300 | 0.672784 | 0.240041 | 0.583333 | 0.041017 |
| team_elo | international=0 | 7941 | 0.667612 | 0.237354 | 0.595580 | 0.036153 |

team_elo − coin (paired log loss):

| Section | Rows | team_elo log loss | coin log loss | Difference | 95% interval | Significant |
|---|---:|---:|---:|---:|---|---|
| all | 8241 | 0.667801 | 0.693147 | -0.025347 | [-0.030821, -0.019779] | yes |

| Model | Section | Rows | Log loss | Brier | Accuracy | ECE |
|---|---|---:|---:|---:|---:|---:|
| player_round_glicko | all | 8241 | 0.651611 | 0.230070 | 0.611334 | 0.023576 |
| player_round_glicko | vct | 1260 | 0.672588 | 0.239659 | 0.598413 | 0.033823 |
| player_round_glicko | vcl | 4384 | 0.651845 | 0.230209 | 0.604015 | 0.020460 |
| player_round_glicko | gc | 1258 | 0.611047 | 0.211533 | 0.667329 | 0.056566 |
| player_round_glicko | t3 | 283 | 0.687307 | 0.246439 | 0.575972 | 0.044942 |
| player_round_glicko | collegiate | 0 | — | — | — | — |
| player_round_glicko | offseason | 1056 | 0.664365 | 0.235746 | 0.599905 | 0.048567 |
| player_round_glicko | unknown | 0 | — | — | — | — |
| player_round_glicko | international=1 | 300 | 0.667913 | 0.236817 | 0.600000 | 0.050255 |
| player_round_glicko | international=0 | 7941 | 0.650995 | 0.229815 | 0.611762 | 0.024581 |

player_round_glicko − coin (paired log loss):

| Section | Rows | player_round_glicko log loss | coin log loss | Difference | 95% interval | Significant |
|---|---:|---:|---:|---:|---|---|
| all | 8241 | 0.651611 | 0.693147 | -0.041536 | [-0.047915, -0.035320] | yes |

| Model | Section | Rows | Log loss | Brier | Accuracy | ECE |
|---|---|---:|---:|---:|---:|---:|
| player_round_glicko_rookie | all | 8241 | 0.646962 | 0.227802 | 0.621648 | 0.021829 |
| player_round_glicko_rookie | vct | 1260 | 0.670641 | 0.238758 | 0.597222 | 0.027789 |
| player_round_glicko_rookie | vcl | 4384 | 0.648724 | 0.228363 | 0.620096 | 0.022148 |
| player_round_glicko_rookie | gc | 1258 | 0.601372 | 0.207535 | 0.678458 | 0.051282 |
| player_round_glicko_rookie | t3 | 283 | 0.681851 | 0.244050 | 0.572438 | 0.033997 |
| player_round_glicko_rookie | collegiate | 0 | — | — | — | — |
| player_round_glicko_rookie | offseason | 1056 | 0.656356 | 0.232190 | 0.602746 | 0.042236 |
| player_round_glicko_rookie | unknown | 0 | — | — | — | — |
| player_round_glicko_rookie | international=1 | 300 | 0.669569 | 0.238137 | 0.600000 | 0.054317 |
| player_round_glicko_rookie | international=0 | 7941 | 0.646108 | 0.227412 | 0.622466 | 0.022967 |

player_round_glicko_rookie − coin (paired log loss):

| Section | Rows | player_round_glicko_rookie log loss | coin log loss | Difference | 95% interval | Significant |
|---|---:|---:|---:|---:|---|---|
| all | 8241 | 0.646962 | 0.693147 | -0.046185 | [-0.052319, -0.039805] | yes |

player_round_glicko − team_elo (paired log loss):

| Section | Rows | player_round_glicko log loss | team_elo log loss | Difference | 95% interval | Significant |
|---|---:|---:|---:|---:|---|---|
| all | 8241 | 0.651611 | 0.667801 | -0.016190 | [-0.020229, -0.012196] | yes |

player_round_glicko_rookie − team_elo (paired log loss):

| Section | Rows | player_round_glicko_rookie log loss | team_elo log loss | Difference | 95% interval | Significant |
|---|---:|---:|---:|---:|---|---|
| all | 8241 | 0.646962 | 0.667801 | -0.020838 | [-0.025324, -0.016160] | yes |

### Series

| Model | Section | Rows | Log loss | Brier | Accuracy | ECE |
|---|---|---:|---:|---:|---:|---:|
| coin | all | 3428 | 0.693147 | 0.250000 | 0.500000 | 0.060968 |
| coin | vct | 497 | 0.693147 | 0.250000 | 0.500000 | 0.035211 |
| coin | vcl | 1807 | 0.693147 | 0.250000 | 0.500000 | 0.043996 |
| coin | gc | 510 | 0.693147 | 0.250000 | 0.500000 | 0.127451 |
| coin | t3 | 129 | 0.693147 | 0.250000 | 0.500000 | 0.003876 |
| coin | collegiate | 0 | — | — | — | — |
| coin | offseason | 485 | 0.693147 | 0.250000 | 0.500000 | 0.095876 |
| coin | unknown | 0 | — | — | — | — |
| coin | international=1 | 133 | 0.693147 | 0.250000 | 0.500000 | 0.011278 |
| coin | international=0 | 3295 | 0.693147 | 0.250000 | 0.500000 | 0.062974 |

| Model | Section | Rows | Log loss | Brier | Accuracy | ECE |
|---|---|---:|---:|---:|---:|---:|
| team_elo | all | 3428 | 0.656035 | 0.231376 | 0.608956 | 0.043105 |
| team_elo | vct | 497 | 0.679024 | 0.240809 | 0.594567 | 0.079538 |
| team_elo | vcl | 1807 | 0.649828 | 0.228050 | 0.623132 | 0.031316 |
| team_elo | gc | 510 | 0.620093 | 0.217060 | 0.622549 | 0.093946 |
| team_elo | t3 | 129 | 0.733630 | 0.264995 | 0.507752 | 0.118048 |
| team_elo | collegiate | 0 | — | — | — | — |
| team_elo | offseason | 485 | 0.672756 | 0.240210 | 0.583505 | 0.074152 |
| team_elo | unknown | 0 | — | — | — | — |
| team_elo | international=1 | 133 | 0.679771 | 0.243043 | 0.578947 | 0.056760 |
| team_elo | international=0 | 3295 | 0.655077 | 0.230905 | 0.610167 | 0.045355 |

team_elo − coin (paired log loss):

| Section | Rows | team_elo log loss | coin log loss | Difference | 95% interval | Significant |
|---|---:|---:|---:|---:|---|---|
| all | 3428 | 0.656035 | 0.693147 | -0.037112 | [-0.048983, -0.025264] | yes |

| Model | Section | Rows | Log loss | Brier | Accuracy | ECE |
|---|---|---:|---:|---:|---:|---:|
| player_round_glicko | all | 3428 | 0.630314 | 0.219809 | 0.638419 | 0.034814 |
| player_round_glicko | vct | 497 | 0.647487 | 0.227207 | 0.646881 | 0.036063 |
| player_round_glicko | vcl | 1807 | 0.634072 | 0.220865 | 0.628666 | 0.028529 |
| player_round_glicko | gc | 510 | 0.565680 | 0.192425 | 0.708824 | 0.073749 |
| player_round_glicko | t3 | 129 | 0.701384 | 0.251812 | 0.596899 | 0.061002 |
| player_round_glicko | collegiate | 0 | — | — | — | — |
| player_round_glicko | offseason | 485 | 0.647778 | 0.228575 | 0.603093 | 0.064053 |
| player_round_glicko | unknown | 0 | — | — | — | — |
| player_round_glicko | international=1 | 133 | 0.658133 | 0.230087 | 0.616541 | 0.088431 |
| player_round_glicko | international=0 | 3295 | 0.629191 | 0.219394 | 0.639302 | 0.036334 |

player_round_glicko − coin (paired log loss):

| Section | Rows | player_round_glicko log loss | coin log loss | Difference | 95% interval | Significant |
|---|---:|---:|---:|---:|---|---|
| all | 3428 | 0.630314 | 0.693147 | -0.062833 | [-0.076007, -0.049824] | yes |

| Model | Section | Rows | Log loss | Brier | Accuracy | ECE |
|---|---|---:|---:|---:|---:|---:|
| player_round_glicko_rookie | all | 3428 | 0.617002 | 0.213067 | 0.658985 | 0.034252 |
| player_round_glicko_rookie | vct | 497 | 0.631868 | 0.221780 | 0.641851 | 0.026513 |
| player_round_glicko_rookie | vcl | 1807 | 0.627072 | 0.215189 | 0.658273 | 0.032148 |
| player_round_glicko_rookie | gc | 510 | 0.524210 | 0.175724 | 0.744118 | 0.056215 |
| player_round_glicko_rookie | t3 | 129 | 0.702531 | 0.253128 | 0.565891 | 0.121274 |
| player_round_glicko_rookie | collegiate | 0 | — | — | — | — |
| player_round_glicko_rookie | offseason | 485 | 0.639075 | 0.224846 | 0.614433 | 0.055932 |
| player_round_glicko_rookie | unknown | 0 | — | — | — | — |
| player_round_glicko_rookie | international=1 | 133 | 0.652113 | 0.229504 | 0.616541 | 0.087934 |
| player_round_glicko_rookie | international=0 | 3295 | 0.615584 | 0.212404 | 0.660698 | 0.035841 |

player_round_glicko_rookie − coin (paired log loss):

| Section | Rows | player_round_glicko_rookie log loss | coin log loss | Difference | 95% interval | Significant |
|---|---:|---:|---:|---:|---|---|
| all | 3428 | 0.617002 | 0.693147 | -0.076145 | [-0.089364, -0.062491] | yes |

player_round_glicko − team_elo (paired log loss):

| Section | Rows | player_round_glicko log loss | team_elo log loss | Difference | 95% interval | Significant |
|---|---:|---:|---:|---:|---|---|
| all | 3428 | 0.630314 | 0.656035 | -0.025721 | [-0.034890, -0.016915] | yes |

player_round_glicko_rookie − team_elo (paired log loss):

| Section | Rows | player_round_glicko_rookie log loss | team_elo log loss | Difference | 95% interval | Significant |
|---|---:|---:|---:|---:|---|---|
| all | 3428 | 0.617002 | 0.656035 | -0.039033 | [-0.050517, -0.028511] | yes |

## Stage 2 — validation (outcomes)

### Leaderboard (frozen stage-1 parameters)

| Model | Best params | Map log loss | Series log loss | Rows |
|---|---|---:|---:|---:|
| player_round_glicko_rookie+regional_form | {"k": 32, "new_player": "teammates", "rd_info": 0.25, "rd_new": 280, "rookie_maps": 100, "rookie_penalty": 200, "tau": 0.4} | 0.637703 | 0.606851 | 6337 |
| player_round_glicko_rookie+form | {"k": 32, "new_player": "teammates", "rd_info": 0.25, "rd_new": 280, "rookie_maps": 100, "rookie_penalty": 200, "tau": 0.4} | 0.638116 | 0.607206 | 6337 |
| player_round_glicko_rookie | {"k": 32, "new_player": "teammates", "rd_info": 0.25, "rd_new": 280, "rookie_maps": 100, "rookie_penalty": 200, "tau": 0.4} | 0.640819 | 0.608464 | 6337 |
| player_round_glicko+regional_form | {"k": 32, "new_player": "teammates", "rd_info": 0.25, "rd_new": 280, "tau": 0.5} | 0.645776 | 0.622635 | 6337 |
| player_round_glicko+form | {"k": 32, "new_player": "teammates", "rd_info": 0.25, "rd_new": 280, "tau": 0.5} | 0.646270 | 0.623306 | 6337 |
| player_round_glicko | {"k": 32, "new_player": "teammates", "rd_info": 0.25, "rd_new": 280, "tau": 0.5} | 0.647771 | 0.623010 | 6337 |
| team_elo+regional_form | {"k": 32} | 0.660780 | 0.657452 | 6337 |
| team_elo+form | {"k": 32} | 0.661713 | 0.659479 | 6337 |
| team_elo | {"k": 32} | 0.668366 | 0.666164 | 6337 |

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
| team_elo | all | 6337 | 0.668366 | 0.237638 | 0.589001 | 0.034220 |
| team_elo | vct | 1080 | 0.691248 | 0.248424 | 0.555556 | 0.070894 |
| team_elo | vcl | 3374 | 0.669567 | 0.237986 | 0.590990 | 0.047046 |
| team_elo | gc | 1005 | 0.632889 | 0.221802 | 0.627363 | 0.044144 |
| team_elo | t3 | 16 | 0.583849 | 0.196579 | 0.812500 | 0.213420 |
| team_elo | collegiate | 7 | 0.713539 | 0.260056 | 0.428571 | 0.102402 |
| team_elo | offseason | 855 | 0.677632 | 0.241838 | 0.575439 | 0.038368 |
| team_elo | unknown | 0 | — | — | — | — |
| team_elo | international=1 | 268 | 0.676901 | 0.242326 | 0.570896 | 0.072341 |
| team_elo | international=0 | 6069 | 0.667989 | 0.237431 | 0.589801 | 0.035654 |

team_elo − coin (paired log loss):

| Section | Rows | team_elo log loss | coin log loss | Difference | 95% interval | Significant |
|---|---:|---:|---:|---:|---|---|
| all | 6337 | 0.668366 | 0.693147 | -0.024781 | [-0.032534, -0.017191] | yes |
| vct | 1080 | 0.691248 | 0.693147 | -0.001899 | [-0.020887, 0.015950] | no |
| vcl | 3374 | 0.669567 | 0.693147 | -0.023580 | [-0.033430, -0.013138] | yes |
| gc | 1005 | 0.632889 | 0.693147 | -0.060258 | [-0.081480, -0.040049] | yes |
| t3 | 16 | 0.583849 | 0.693147 | -0.109298 | [-0.241112, -0.021134] | yes |
| collegiate | 7 | 0.713539 | 0.693147 | 0.020392 | [0.009477, 0.034945] | yes |
| offseason | 855 | 0.677632 | 0.693147 | -0.015515 | [-0.036098, 0.004643] | no |
| international=1 | 268 | 0.676901 | 0.693147 | -0.016246 | [-0.051004, 0.015072] | no |
| international=0 | 6069 | 0.667989 | 0.693147 | -0.025158 | [-0.033285, -0.017278] | yes |

| Model | Section | Rows | Log loss | Brier | Accuracy | ECE |
|---|---|---:|---:|---:|---:|---:|
| player_round_glicko | all | 6337 | 0.647771 | 0.228267 | 0.618668 | 0.019369 |
| player_round_glicko | vct | 1080 | 0.668668 | 0.238173 | 0.583796 | 0.031991 |
| player_round_glicko | vcl | 3374 | 0.652672 | 0.230294 | 0.615886 | 0.031964 |
| player_round_glicko | gc | 1005 | 0.609051 | 0.211074 | 0.655224 | 0.045470 |
| player_round_glicko | t3 | 16 | 0.531588 | 0.174385 | 0.750000 | 0.136964 |
| player_round_glicko | collegiate | 7 | 0.803592 | 0.303773 | 0.357143 | 0.386113 |
| player_round_glicko | offseason | 855 | 0.648443 | 0.228354 | 0.630409 | 0.038892 |
| player_round_glicko | unknown | 0 | — | — | — | — |
| player_round_glicko | international=1 | 268 | 0.676037 | 0.241339 | 0.580224 | 0.044006 |
| player_round_glicko | international=0 | 6069 | 0.646522 | 0.227690 | 0.620366 | 0.020480 |

player_round_glicko − coin (paired log loss):

| Section | Rows | player_round_glicko log loss | coin log loss | Difference | 95% interval | Significant |
|---|---:|---:|---:|---:|---|---|
| all | 6337 | 0.647771 | 0.693147 | -0.045377 | [-0.052645, -0.038305] | yes |
| vct | 1080 | 0.668668 | 0.693147 | -0.024479 | [-0.037826, -0.012125] | yes |
| vcl | 3374 | 0.652672 | 0.693147 | -0.040475 | [-0.050814, -0.030166] | yes |
| gc | 1005 | 0.609051 | 0.693147 | -0.084096 | [-0.106296, -0.063352] | yes |
| t3 | 16 | 0.531588 | 0.693147 | -0.161559 | [-0.352220, -0.045425] | yes |
| collegiate | 7 | 0.803592 | 0.693147 | 0.110445 | [0.055210, 0.184092] | yes |
| offseason | 855 | 0.648443 | 0.693147 | -0.044704 | [-0.063033, -0.027168] | yes |
| international=1 | 268 | 0.676037 | 0.693147 | -0.017111 | [-0.043470, 0.009765] | no |
| international=0 | 6069 | 0.646522 | 0.693147 | -0.046625 | [-0.054195, -0.039421] | yes |

| Model | Section | Rows | Log loss | Brier | Accuracy | ECE |
|---|---|---:|---:|---:|---:|---:|
| player_round_glicko_rookie | all | 6337 | 0.640819 | 0.225242 | 0.623244 | 0.024438 |
| player_round_glicko_rookie | vct | 1080 | 0.667804 | 0.237733 | 0.594444 | 0.035139 |
| player_round_glicko_rookie | vcl | 3374 | 0.645067 | 0.227040 | 0.617813 | 0.034664 |
| player_round_glicko_rookie | gc | 1005 | 0.604314 | 0.209001 | 0.666667 | 0.053355 |
| player_round_glicko_rookie | t3 | 16 | 0.511441 | 0.172309 | 0.687500 | 0.116276 |
| player_round_glicko_rookie | collegiate | 7 | 0.754356 | 0.280289 | 0.214286 | 0.396213 |
| player_round_glicko_rookie | offseason | 855 | 0.634370 | 0.222002 | 0.632164 | 0.033877 |
| player_round_glicko_rookie | unknown | 0 | — | — | — | — |
| player_round_glicko_rookie | international=1 | 268 | 0.670637 | 0.239008 | 0.574627 | 0.031341 |
| player_round_glicko_rookie | international=0 | 6069 | 0.639502 | 0.224634 | 0.625391 | 0.025245 |

player_round_glicko_rookie − coin (paired log loss):

| Section | Rows | player_round_glicko_rookie log loss | coin log loss | Difference | 95% interval | Significant |
|---|---:|---:|---:|---:|---|---|
| all | 6337 | 0.640819 | 0.693147 | -0.052328 | [-0.059618, -0.045501] | yes |
| vct | 1080 | 0.667804 | 0.693147 | -0.025343 | [-0.037317, -0.014398] | yes |
| vcl | 3374 | 0.645067 | 0.693147 | -0.048080 | [-0.057805, -0.038168] | yes |
| gc | 1005 | 0.604314 | 0.693147 | -0.088834 | [-0.110852, -0.068074] | yes |
| t3 | 16 | 0.511441 | 0.693147 | -0.181706 | [-0.444335, -0.028480] | yes |
| collegiate | 7 | 0.754356 | 0.693147 | 0.061209 | [0.043079, 0.085382] | yes |
| offseason | 855 | 0.634370 | 0.693147 | -0.058777 | [-0.079673, -0.037760] | yes |
| international=1 | 268 | 0.670637 | 0.693147 | -0.022510 | [-0.044575, -0.002391] | yes |
| international=0 | 6069 | 0.639502 | 0.693147 | -0.053645 | [-0.061138, -0.046571] | yes |

| Model | Section | Rows | Log loss | Brier | Accuracy | ECE |
|---|---|---:|---:|---:|---:|---:|
| team_elo+form | all | 6337 | 0.661713 | 0.234164 | 0.609594 | 0.034448 |
| team_elo+form | vct | 1080 | 0.690839 | 0.247933 | 0.565741 | 0.068383 |
| team_elo+form | vcl | 3374 | 0.664066 | 0.234691 | 0.614404 | 0.045200 |
| team_elo+form | gc | 1005 | 0.618793 | 0.215694 | 0.657214 | 0.041795 |
| team_elo+form | t3 | 16 | 0.541553 | 0.177680 | 0.812500 | 0.165688 |
| team_elo+form | collegiate | 7 | 0.772148 | 0.288936 | 0.285714 | 0.293919 |
| team_elo+form | offseason | 855 | 0.667434 | 0.237010 | 0.588889 | 0.042729 |
| team_elo+form | unknown | 0 | — | — | — | — |
| team_elo+form | international=1 | 268 | 0.678834 | 0.242875 | 0.589552 | 0.051487 |
| team_elo+form | international=0 | 6069 | 0.660957 | 0.233779 | 0.610479 | 0.035348 |

team_elo+form − coin (paired log loss):

| Section | Rows | team_elo+form log loss | coin log loss | Difference | 95% interval | Significant |
|---|---:|---:|---:|---:|---|---|
| all | 6337 | 0.661713 | 0.693147 | -0.031434 | [-0.040775, -0.022450] | yes |
| vct | 1080 | 0.690839 | 0.693147 | -0.002309 | [-0.022762, 0.016925] | no |
| vcl | 3374 | 0.664066 | 0.693147 | -0.029081 | [-0.042315, -0.015864] | yes |
| gc | 1005 | 0.618793 | 0.693147 | -0.074355 | [-0.101026, -0.049814] | yes |
| t3 | 16 | 0.541553 | 0.693147 | -0.151594 | [-0.337538, -0.031084] | yes |
| collegiate | 7 | 0.772148 | 0.693147 | 0.079001 | [0.047637, 0.120820] | yes |
| offseason | 855 | 0.667434 | 0.693147 | -0.025713 | [-0.049050, -0.002797] | yes |
| international=1 | 268 | 0.678834 | 0.693147 | -0.014313 | [-0.053931, 0.021626] | no |
| international=0 | 6069 | 0.660957 | 0.693147 | -0.032190 | [-0.042069, -0.022884] | yes |

| Model | Section | Rows | Log loss | Brier | Accuracy | ECE |
|---|---|---:|---:|---:|---:|---:|
| team_elo+regional_form | all | 6337 | 0.660780 | 0.233751 | 0.609437 | 0.033761 |
| team_elo+regional_form | vct | 1080 | 0.687718 | 0.246471 | 0.564815 | 0.063370 |
| team_elo+regional_form | vcl | 3374 | 0.664063 | 0.234694 | 0.614701 | 0.045151 |
| team_elo+regional_form | gc | 1005 | 0.618407 | 0.215544 | 0.654229 | 0.040160 |
| team_elo+regional_form | t3 | 16 | 0.541683 | 0.177735 | 0.812500 | 0.165855 |
| team_elo+regional_form | collegiate | 7 | 0.771873 | 0.288804 | 0.285714 | 0.293716 |
| team_elo+regional_form | offseason | 855 | 0.664923 | 0.235964 | 0.591228 | 0.036188 |
| team_elo+regional_form | unknown | 0 | — | — | — | — |
| team_elo+regional_form | international=1 | 268 | 0.664387 | 0.236382 | 0.582090 | 0.058932 |
| team_elo+regional_form | international=0 | 6069 | 0.660621 | 0.233635 | 0.610644 | 0.034503 |

team_elo+regional_form − coin (paired log loss):

| Section | Rows | team_elo+regional_form log loss | coin log loss | Difference | 95% interval | Significant |
|---|---:|---:|---:|---:|---|---|
| all | 6337 | 0.660780 | 0.693147 | -0.032367 | [-0.041645, -0.023502] | yes |
| vct | 1080 | 0.687718 | 0.693147 | -0.005429 | [-0.025924, 0.014109] | no |
| vcl | 3374 | 0.664063 | 0.693147 | -0.029084 | [-0.042300, -0.015870] | yes |
| gc | 1005 | 0.618407 | 0.693147 | -0.074740 | [-0.101307, -0.050274] | yes |
| t3 | 16 | 0.541683 | 0.693147 | -0.151465 | [-0.337221, -0.031053] | yes |
| collegiate | 7 | 0.771873 | 0.693147 | 0.078725 | [0.047431, 0.120452] | yes |
| offseason | 855 | 0.664923 | 0.693147 | -0.028225 | [-0.050425, -0.006044] | yes |
| international=1 | 268 | 0.664387 | 0.693147 | -0.028760 | [-0.065683, 0.005337] | no |
| international=0 | 6069 | 0.660621 | 0.693147 | -0.032527 | [-0.042406, -0.023244] | yes |

| Model | Section | Rows | Log loss | Brier | Accuracy | ECE |
|---|---|---:|---:|---:|---:|---:|
| player_round_glicko+form | all | 6337 | 0.646270 | 0.227557 | 0.620798 | 0.019789 |
| player_round_glicko+form | vct | 1080 | 0.669205 | 0.238514 | 0.595370 | 0.038806 |
| player_round_glicko+form | vcl | 3374 | 0.651056 | 0.229385 | 0.614701 | 0.033077 |
| player_round_glicko+form | gc | 1005 | 0.606852 | 0.210283 | 0.664677 | 0.045359 |
| player_round_glicko+form | t3 | 16 | 0.508952 | 0.164537 | 0.750000 | 0.156025 |
| player_round_glicko+form | collegiate | 7 | 0.835562 | 0.317853 | 0.357143 | 0.315953 |
| player_round_glicko+form | offseason | 855 | 0.645769 | 0.227244 | 0.625146 | 0.032814 |
| player_round_glicko+form | unknown | 0 | — | — | — | — |
| player_round_glicko+form | international=1 | 268 | 0.676325 | 0.241389 | 0.593284 | 0.058349 |
| player_round_glicko+form | international=0 | 6069 | 0.644943 | 0.226946 | 0.622014 | 0.019396 |

player_round_glicko+form − coin (paired log loss):

| Section | Rows | player_round_glicko+form log loss | coin log loss | Difference | 95% interval | Significant |
|---|---:|---:|---:|---:|---|---|
| all | 6337 | 0.646270 | 0.693147 | -0.046877 | [-0.055081, -0.039016] | yes |
| vct | 1080 | 0.669205 | 0.693147 | -0.023942 | [-0.038741, -0.009940] | yes |
| vcl | 3374 | 0.651056 | 0.693147 | -0.042092 | [-0.053563, -0.030420] | yes |
| gc | 1005 | 0.606852 | 0.693147 | -0.086295 | [-0.110886, -0.063703] | yes |
| t3 | 16 | 0.508952 | 0.693147 | -0.184195 | [-0.389345, -0.059719] | yes |
| collegiate | 7 | 0.835562 | 0.693147 | 0.142415 | [0.075766, 0.231281] | yes |
| offseason | 855 | 0.645769 | 0.693147 | -0.047379 | [-0.068122, -0.027852] | yes |
| international=1 | 268 | 0.676325 | 0.693147 | -0.016822 | [-0.046124, 0.012005] | no |
| international=0 | 6069 | 0.644943 | 0.693147 | -0.048204 | [-0.056721, -0.040086] | yes |

| Model | Section | Rows | Log loss | Brier | Accuracy | ECE |
|---|---|---:|---:|---:|---:|---:|
| player_round_glicko+regional_form | all | 6337 | 0.645776 | 0.227333 | 0.621588 | 0.018877 |
| player_round_glicko+regional_form | vct | 1080 | 0.667508 | 0.237757 | 0.597222 | 0.042020 |
| player_round_glicko+regional_form | vcl | 3374 | 0.651058 | 0.229390 | 0.615293 | 0.032592 |
| player_round_glicko+regional_form | gc | 1005 | 0.605927 | 0.209846 | 0.664677 | 0.045702 |
| player_round_glicko+regional_form | t3 | 16 | 0.509300 | 0.164684 | 0.750000 | 0.156166 |
| player_round_glicko+regional_form | collegiate | 7 | 0.834985 | 0.317607 | 0.357143 | 0.315503 |
| player_round_glicko+regional_form | offseason | 855 | 0.645326 | 0.227035 | 0.626316 | 0.033199 |
| player_round_glicko+regional_form | unknown | 0 | — | — | — | — |
| player_round_glicko+regional_form | international=1 | 268 | 0.665594 | 0.236619 | 0.604478 | 0.045429 |
| player_round_glicko+regional_form | international=0 | 6069 | 0.644901 | 0.226923 | 0.622343 | 0.019166 |

player_round_glicko+regional_form − coin (paired log loss):

| Section | Rows | player_round_glicko+regional_form log loss | coin log loss | Difference | 95% interval | Significant |
|---|---:|---:|---:|---:|---|---|
| all | 6337 | 0.645776 | 0.693147 | -0.047371 | [-0.055644, -0.039358] | yes |
| vct | 1080 | 0.667508 | 0.693147 | -0.025639 | [-0.041139, -0.011031] | yes |
| vcl | 3374 | 0.651058 | 0.693147 | -0.042089 | [-0.053543, -0.030436] | yes |
| gc | 1005 | 0.605927 | 0.693147 | -0.087221 | [-0.111849, -0.064666] | yes |
| t3 | 16 | 0.509300 | 0.693147 | -0.183847 | [-0.388803, -0.059529] | yes |
| collegiate | 7 | 0.834985 | 0.693147 | 0.141838 | [0.075370, 0.230462] | yes |
| offseason | 855 | 0.645326 | 0.693147 | -0.047821 | [-0.068708, -0.028694] | yes |
| international=1 | 268 | 0.665594 | 0.693147 | -0.027553 | [-0.061219, 0.003932] | no |
| international=0 | 6069 | 0.644901 | 0.693147 | -0.048246 | [-0.056717, -0.040028] | yes |

| Model | Section | Rows | Log loss | Brier | Accuracy | ECE |
|---|---|---:|---:|---:|---:|---:|
| player_round_glicko_rookie+form | all | 6337 | 0.638116 | 0.224051 | 0.624428 | 0.020173 |
| player_round_glicko_rookie+form | vct | 1080 | 0.667845 | 0.237906 | 0.587963 | 0.037291 |
| player_round_glicko_rookie+form | vcl | 3374 | 0.642074 | 0.225532 | 0.620628 | 0.030755 |
| player_round_glicko_rookie+form | gc | 1005 | 0.600394 | 0.207573 | 0.667662 | 0.041720 |
| player_round_glicko_rookie+form | t3 | 16 | 0.482892 | 0.160108 | 0.625000 | 0.258482 |
| player_round_glicko_rookie+form | collegiate | 7 | 0.794048 | 0.298558 | 0.357143 | 0.289563 |
| player_round_glicko_rookie+form | offseason | 855 | 0.630911 | 0.220661 | 0.636842 | 0.025009 |
| player_round_glicko_rookie+form | unknown | 0 | — | — | — | — |
| player_round_glicko_rookie+form | international=1 | 268 | 0.670125 | 0.238780 | 0.589552 | 0.030697 |
| player_round_glicko_rookie+form | international=0 | 6069 | 0.636702 | 0.223400 | 0.625968 | 0.020770 |

player_round_glicko_rookie+form − coin (paired log loss):

| Section | Rows | player_round_glicko_rookie+form log loss | coin log loss | Difference | 95% interval | Significant |
|---|---:|---:|---:|---:|---|---|
| all | 6337 | 0.638116 | 0.693147 | -0.055031 | [-0.063397, -0.047334] | yes |
| vct | 1080 | 0.667845 | 0.693147 | -0.025302 | [-0.038949, -0.012264] | yes |
| vcl | 3374 | 0.642074 | 0.693147 | -0.051073 | [-0.062930, -0.039420] | yes |
| gc | 1005 | 0.600394 | 0.693147 | -0.092753 | [-0.117110, -0.069040] | yes |
| t3 | 16 | 0.482892 | 0.693147 | -0.210255 | [-0.485736, -0.044967] | yes |
| collegiate | 7 | 0.794048 | 0.693147 | 0.100901 | [0.069593, 0.142645] | yes |
| offseason | 855 | 0.630911 | 0.693147 | -0.062236 | [-0.085422, -0.038811] | yes |
| international=1 | 268 | 0.670125 | 0.693147 | -0.023022 | [-0.048173, 0.001119] | no |
| international=0 | 6069 | 0.636702 | 0.693147 | -0.056445 | [-0.065067, -0.048129] | yes |

| Model | Section | Rows | Log loss | Brier | Accuracy | ECE |
|---|---|---:|---:|---:|---:|---:|
| player_round_glicko_rookie+regional_form | all | 6337 | 0.637703 | 0.223864 | 0.625533 | 0.020134 |
| player_round_glicko_rookie+regional_form | vct | 1080 | 0.666151 | 0.237187 | 0.591667 | 0.035340 |
| player_round_glicko_rookie+regional_form | vcl | 3374 | 0.642084 | 0.225542 | 0.620332 | 0.029769 |
| player_round_glicko_rookie+regional_form | gc | 1005 | 0.599793 | 0.207260 | 0.669652 | 0.037722 |
| player_round_glicko_rookie+regional_form | t3 | 16 | 0.483441 | 0.160334 | 0.625000 | 0.258791 |
| player_round_glicko_rookie+regional_form | collegiate | 7 | 0.793097 | 0.298137 | 0.357143 | 0.288786 |
| player_round_glicko_rookie+regional_form | offseason | 855 | 0.630657 | 0.220513 | 0.639181 | 0.027625 |
| player_round_glicko_rookie+regional_form | unknown | 0 | — | — | — | — |
| player_round_glicko_rookie+regional_form | international=1 | 268 | 0.660979 | 0.234749 | 0.615672 | 0.061806 |
| player_round_glicko_rookie+regional_form | international=0 | 6069 | 0.636675 | 0.223383 | 0.625968 | 0.020687 |

player_round_glicko_rookie+regional_form − coin (paired log loss):

| Section | Rows | player_round_glicko_rookie+regional_form log loss | coin log loss | Difference | 95% interval | Significant |
|---|---:|---:|---:|---:|---|---|
| all | 6337 | 0.637703 | 0.693147 | -0.055444 | [-0.063864, -0.047595] | yes |
| vct | 1080 | 0.666151 | 0.693147 | -0.026997 | [-0.041277, -0.012928] | yes |
| vcl | 3374 | 0.642084 | 0.693147 | -0.051064 | [-0.062895, -0.039448] | yes |
| gc | 1005 | 0.599793 | 0.693147 | -0.093355 | [-0.117917, -0.070271] | yes |
| t3 | 16 | 0.483441 | 0.693147 | -0.209706 | [-0.484927, -0.044573] | yes |
| collegiate | 7 | 0.793097 | 0.693147 | 0.099950 | [0.068907, 0.141342] | yes |
| offseason | 855 | 0.630657 | 0.693147 | -0.062490 | [-0.085976, -0.039243] | yes |
| international=1 | 268 | 0.660979 | 0.693147 | -0.032168 | [-0.065112, -0.000679] | yes |
| international=0 | 6069 | 0.636675 | 0.693147 | -0.056472 | [-0.065114, -0.048140] | yes |

player_round_glicko − team_elo (paired log loss):

| Section | Rows | player_round_glicko log loss | team_elo log loss | Difference | 95% interval | Significant |
|---|---:|---:|---:|---:|---|---|
| all | 6337 | 0.647771 | 0.668366 | -0.020595 | [-0.026053, -0.015300] | yes |

player_round_glicko_rookie − team_elo (paired log loss):

| Section | Rows | player_round_glicko_rookie log loss | team_elo log loss | Difference | 95% interval | Significant |
|---|---:|---:|---:|---:|---|---|
| all | 6337 | 0.640819 | 0.668366 | -0.027547 | [-0.033793, -0.021393] | yes |

team_elo+form − team_elo (paired log loss):

| Section | Rows | team_elo+form log loss | team_elo log loss | Difference | 95% interval | Significant |
|---|---:|---:|---:|---:|---|---|
| all | 6337 | 0.661713 | 0.668366 | -0.006652 | [-0.009502, -0.003935] | yes |

team_elo+regional_form − team_elo (paired log loss):

| Section | Rows | team_elo+regional_form log loss | team_elo log loss | Difference | 95% interval | Significant |
|---|---:|---:|---:|---:|---|---|
| all | 6337 | 0.660780 | 0.668366 | -0.007586 | [-0.010469, -0.004745] | yes |

player_round_glicko+form − team_elo (paired log loss):

| Section | Rows | player_round_glicko+form log loss | team_elo log loss | Difference | 95% interval | Significant |
|---|---:|---:|---:|---:|---|---|
| all | 6337 | 0.646270 | 0.668366 | -0.022096 | [-0.027814, -0.016376] | yes |

player_round_glicko+regional_form − team_elo (paired log loss):

| Section | Rows | player_round_glicko+regional_form log loss | team_elo log loss | Difference | 95% interval | Significant |
|---|---:|---:|---:|---:|---|---|
| all | 6337 | 0.645776 | 0.668366 | -0.022590 | [-0.028330, -0.016943] | yes |

player_round_glicko_rookie+form − team_elo (paired log loss):

| Section | Rows | player_round_glicko_rookie+form log loss | team_elo log loss | Difference | 95% interval | Significant |
|---|---:|---:|---:|---:|---|---|
| all | 6337 | 0.638116 | 0.668366 | -0.030250 | [-0.036812, -0.023820] | yes |

player_round_glicko_rookie+regional_form − team_elo (paired log loss):

| Section | Rows | player_round_glicko_rookie+regional_form log loss | team_elo log loss | Difference | 95% interval | Significant |
|---|---:|---:|---:|---:|---|---|
| all | 6337 | 0.637703 | 0.668366 | -0.030663 | [-0.037268, -0.024204] | yes |

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
| team_elo | all | 2618 | 0.666164 | 0.234683 | 0.611727 | 0.057361 |
| team_elo | vct | 415 | 0.699584 | 0.248839 | 0.590361 | 0.101804 |
| team_elo | vcl | 1351 | 0.669003 | 0.234788 | 0.615840 | 0.064632 |
| team_elo | gc | 409 | 0.599422 | 0.208332 | 0.646699 | 0.065741 |
| team_elo | t3 | 6 | 0.449197 | 0.133117 | 0.833333 | 0.356771 |
| team_elo | collegiate | 2 | 0.693147 | 0.250000 | 0.500000 | 0.000000 |
| team_elo | offseason | 435 | 0.691086 | 0.246957 | 0.583908 | 0.085380 |
| team_elo | unknown | 0 | — | — | — | — |
| team_elo | international=1 | 103 | 0.659398 | 0.235327 | 0.621359 | 0.130369 |
| team_elo | international=0 | 2515 | 0.666441 | 0.234656 | 0.611332 | 0.056664 |

team_elo − coin (paired log loss):

| Section | Rows | team_elo log loss | coin log loss | Difference | 95% interval | Significant |
|---|---:|---:|---:|---:|---|---|
| all | 2618 | 0.666164 | 0.693147 | -0.026983 | [-0.043473, -0.010418] | yes |
| vct | 415 | 0.699584 | 0.693147 | 0.006437 | [-0.037685, 0.054874] | no |
| vcl | 1351 | 0.669003 | 0.693147 | -0.024144 | [-0.046643, -0.000572] | yes |
| gc | 409 | 0.599422 | 0.693147 | -0.093725 | [-0.133983, -0.051067] | yes |
| t3 | 6 | 0.449197 | 0.693147 | -0.243950 | [-0.325332, -0.129109] | yes |
| collegiate | 2 | 0.693147 | 0.693147 | 0.000000 | [0.000000, 0.000000] | no |
| offseason | 435 | 0.691086 | 0.693147 | -0.002061 | [-0.037334, 0.034672] | no |
| international=1 | 103 | 0.659398 | 0.693147 | -0.033750 | [-0.111737, 0.043813] | no |
| international=0 | 2515 | 0.666441 | 0.693147 | -0.026706 | [-0.043828, -0.009069] | yes |

| Model | Section | Rows | Log loss | Brier | Accuracy | ECE |
|---|---|---:|---:|---:|---:|---:|
| player_round_glicko | all | 2618 | 0.623010 | 0.217188 | 0.652024 | 0.025251 |
| player_round_glicko | vct | 415 | 0.643485 | 0.226319 | 0.631325 | 0.032744 |
| player_round_glicko | vcl | 1351 | 0.633597 | 0.220768 | 0.643967 | 0.038099 |
| player_round_glicko | gc | 409 | 0.551942 | 0.189479 | 0.701711 | 0.048949 |
| player_round_glicko | t3 | 6 | 0.404423 | 0.123543 | 0.833333 | 0.164917 |
| player_round_glicko | collegiate | 2 | 0.911858 | 0.354266 | 0.250000 | 0.588575 |
| player_round_glicko | offseason | 435 | 0.639106 | 0.224069 | 0.649425 | 0.046020 |
| player_round_glicko | unknown | 0 | — | — | — | — |
| player_round_glicko | international=1 | 103 | 0.649386 | 0.227639 | 0.601942 | 0.068846 |
| player_round_glicko | international=0 | 2515 | 0.621930 | 0.216759 | 0.654076 | 0.024511 |

player_round_glicko − coin (paired log loss):

| Section | Rows | player_round_glicko log loss | coin log loss | Difference | 95% interval | Significant |
|---|---:|---:|---:|---:|---|---|
| all | 2618 | 0.623010 | 0.693147 | -0.070137 | [-0.084476, -0.054813] | yes |
| vct | 415 | 0.643485 | 0.693147 | -0.049662 | [-0.080254, -0.019281] | yes |
| vcl | 1351 | 0.633597 | 0.693147 | -0.059551 | [-0.081779, -0.037344] | yes |
| gc | 409 | 0.551942 | 0.693147 | -0.141206 | [-0.179622, -0.102334] | yes |
| t3 | 6 | 0.404423 | 0.693147 | -0.288725 | [-0.477590, -0.081425] | yes |
| collegiate | 2 | 0.911858 | 0.693147 | 0.218711 | [0.000000, 0.437422] | no |
| offseason | 435 | 0.639106 | 0.693147 | -0.054042 | [-0.081529, -0.026369] | yes |
| international=1 | 103 | 0.649386 | 0.693147 | -0.043761 | [-0.110824, 0.023153] | no |
| international=0 | 2515 | 0.621930 | 0.693147 | -0.071217 | [-0.086193, -0.055280] | yes |

| Model | Section | Rows | Log loss | Brier | Accuracy | ECE |
|---|---|---:|---:|---:|---:|---:|
| player_round_glicko_rookie | all | 2618 | 0.608464 | 0.210788 | 0.662529 | 0.023747 |
| player_round_glicko_rookie | vct | 415 | 0.638850 | 0.225112 | 0.631325 | 0.040706 |
| player_round_glicko_rookie | vcl | 1351 | 0.617282 | 0.213526 | 0.658401 | 0.038892 |
| player_round_glicko_rookie | gc | 409 | 0.541807 | 0.184652 | 0.721271 | 0.054365 |
| player_round_glicko_rookie | t3 | 6 | 0.447995 | 0.155276 | 0.666667 | 0.193666 |
| player_round_glicko_rookie | collegiate | 2 | 0.707688 | 0.257268 | 0.250000 | 0.507166 |
| player_round_glicko_rookie | offseason | 435 | 0.616518 | 0.213744 | 0.651724 | 0.035925 |
| player_round_glicko_rookie | unknown | 0 | — | — | — | — |
| player_round_glicko_rookie | international=1 | 103 | 0.639958 | 0.224484 | 0.611650 | 0.112032 |
| player_round_glicko_rookie | international=0 | 2515 | 0.607174 | 0.210227 | 0.664612 | 0.023671 |

player_round_glicko_rookie − coin (paired log loss):

| Section | Rows | player_round_glicko_rookie log loss | coin log loss | Difference | 95% interval | Significant |
|---|---:|---:|---:|---:|---|---|
| all | 2618 | 0.608464 | 0.693147 | -0.084683 | [-0.099889, -0.068865] | yes |
| vct | 415 | 0.638850 | 0.693147 | -0.054297 | [-0.079783, -0.028927] | yes |
| vcl | 1351 | 0.617282 | 0.693147 | -0.075865 | [-0.099033, -0.051483] | yes |
| gc | 409 | 0.541807 | 0.693147 | -0.151340 | [-0.189643, -0.112405] | yes |
| t3 | 6 | 0.447995 | 0.693147 | -0.245152 | [-0.536322, 0.046017] | no |
| collegiate | 2 | 0.707688 | 0.693147 | 0.014541 | [0.000000, 0.029082] | no |
| offseason | 435 | 0.616518 | 0.693147 | -0.076629 | [-0.110203, -0.040780] | yes |
| international=1 | 103 | 0.639958 | 0.693147 | -0.053189 | [-0.104565, -0.005452] | yes |
| international=0 | 2515 | 0.607174 | 0.693147 | -0.085973 | [-0.101220, -0.070178] | yes |

| Model | Section | Rows | Log loss | Brier | Accuracy | ECE |
|---|---|---:|---:|---:|---:|---:|
| team_elo+form | all | 2618 | 0.659479 | 0.229764 | 0.636746 | 0.059451 |
| team_elo+form | vct | 415 | 0.699161 | 0.246839 | 0.612048 | 0.111060 |
| team_elo+form | vcl | 1351 | 0.663669 | 0.229631 | 0.643967 | 0.066794 |
| team_elo+form | gc | 409 | 0.584626 | 0.200542 | 0.698044 | 0.067301 |
| team_elo+form | t3 | 6 | 0.374748 | 0.105632 | 0.833333 | 0.298996 |
| team_elo+form | collegiate | 2 | 0.693147 | 0.250000 | 0.500000 | 0.000000 |
| team_elo+form | offseason | 435 | 0.682760 | 0.242981 | 0.578161 | 0.096874 |
| team_elo+form | unknown | 0 | — | — | — | — |
| team_elo+form | international=1 | 103 | 0.660187 | 0.234606 | 0.650485 | 0.144899 |
| team_elo+form | international=0 | 2515 | 0.659450 | 0.229566 | 0.636183 | 0.057224 |

team_elo+form − coin (paired log loss):

| Section | Rows | team_elo+form log loss | coin log loss | Difference | 95% interval | Significant |
|---|---:|---:|---:|---:|---|---|
| all | 2618 | 0.659479 | 0.693147 | -0.033668 | [-0.053765, -0.014330] | yes |
| vct | 415 | 0.699161 | 0.693147 | 0.006014 | [-0.043755, 0.057404] | no |
| vcl | 1351 | 0.663669 | 0.693147 | -0.029478 | [-0.056914, -0.000760] | yes |
| gc | 409 | 0.584626 | 0.693147 | -0.108522 | [-0.158989, -0.057915] | yes |
| t3 | 6 | 0.374748 | 0.693147 | -0.318399 | [-0.457976, -0.135579] | yes |
| collegiate | 2 | 0.693147 | 0.693147 | 0.000000 | [0.000000, 0.000000] | no |
| offseason | 435 | 0.682760 | 0.693147 | -0.010387 | [-0.051006, 0.031086] | no |
| international=1 | 103 | 0.660187 | 0.693147 | -0.032960 | [-0.124782, 0.055631] | no |
| international=0 | 2515 | 0.659450 | 0.693147 | -0.033697 | [-0.053744, -0.013402] | yes |

| Model | Section | Rows | Log loss | Brier | Accuracy | ECE |
|---|---|---:|---:|---:|---:|---:|
| team_elo+regional_form | all | 2618 | 0.657452 | 0.228922 | 0.635982 | 0.055579 |
| team_elo+regional_form | vct | 415 | 0.693709 | 0.244272 | 0.607229 | 0.103005 |
| team_elo+regional_form | vcl | 1351 | 0.663644 | 0.229635 | 0.644708 | 0.066715 |
| team_elo+regional_form | gc | 409 | 0.583562 | 0.200211 | 0.693154 | 0.066739 |
| team_elo+regional_form | t3 | 6 | 0.374969 | 0.105700 | 0.833333 | 0.299183 |
| team_elo+regional_form | collegiate | 2 | 0.693147 | 0.250000 | 0.500000 | 0.000000 |
| team_elo+regional_form | offseason | 435 | 0.676839 | 0.240663 | 0.580460 | 0.080553 |
| team_elo+regional_form | unknown | 0 | — | — | — | — |
| team_elo+regional_form | international=1 | 103 | 0.636912 | 0.223897 | 0.621359 | 0.105765 |
| team_elo+regional_form | international=0 | 2515 | 0.658293 | 0.229128 | 0.636581 | 0.055476 |

team_elo+regional_form − coin (paired log loss):

| Section | Rows | team_elo+regional_form log loss | coin log loss | Difference | 95% interval | Significant |
|---|---:|---:|---:|---:|---|---|
| all | 2618 | 0.657452 | 0.693147 | -0.035695 | [-0.055457, -0.016409] | yes |
| vct | 415 | 0.693709 | 0.693147 | 0.000562 | [-0.048470, 0.051190] | no |
| vcl | 1351 | 0.663644 | 0.693147 | -0.029503 | [-0.056901, -0.000824] | yes |
| gc | 409 | 0.583562 | 0.693147 | -0.109586 | [-0.159313, -0.059432] | yes |
| t3 | 6 | 0.374969 | 0.693147 | -0.318178 | [-0.457566, -0.135583] | yes |
| collegiate | 2 | 0.693147 | 0.693147 | 0.000000 | [0.000000, 0.000000] | no |
| offseason | 435 | 0.676839 | 0.693147 | -0.016308 | [-0.055508, 0.024435] | no |
| international=1 | 103 | 0.636912 | 0.693147 | -0.056236 | [-0.139766, 0.024428] | no |
| international=0 | 2515 | 0.658293 | 0.693147 | -0.034854 | [-0.054955, -0.014761] | yes |

| Model | Section | Rows | Log loss | Brier | Accuracy | ECE |
|---|---|---:|---:|---:|---:|---:|
| player_round_glicko+form | all | 2618 | 0.623306 | 0.216999 | 0.652406 | 0.034925 |
| player_round_glicko+form | vct | 415 | 0.644425 | 0.226766 | 0.631325 | 0.046807 |
| player_round_glicko+form | vcl | 1351 | 0.633889 | 0.220182 | 0.646188 | 0.049583 |
| player_round_glicko+form | gc | 409 | 0.554034 | 0.190560 | 0.711491 | 0.059727 |
| player_round_glicko+form | t3 | 6 | 0.365270 | 0.107678 | 0.833333 | 0.282406 |
| player_round_glicko+form | collegiate | 2 | 0.911858 | 0.354266 | 0.250000 | 0.588575 |
| player_round_glicko+form | offseason | 435 | 0.637651 | 0.223529 | 0.635632 | 0.033945 |
| player_round_glicko+form | unknown | 0 | — | — | — | — |
| player_round_glicko+form | international=1 | 103 | 0.649548 | 0.227332 | 0.631068 | 0.088551 |
| player_round_glicko+form | international=0 | 2515 | 0.622231 | 0.216575 | 0.653280 | 0.033626 |

player_round_glicko+form − coin (paired log loss):

| Section | Rows | player_round_glicko+form log loss | coin log loss | Difference | 95% interval | Significant |
|---|---:|---:|---:|---:|---|---|
| all | 2618 | 0.623306 | 0.693147 | -0.069841 | [-0.086059, -0.053069] | yes |
| vct | 415 | 0.644425 | 0.693147 | -0.048722 | [-0.081222, -0.015741] | yes |
| vcl | 1351 | 0.633889 | 0.693147 | -0.059258 | [-0.084169, -0.034045] | yes |
| gc | 409 | 0.554034 | 0.693147 | -0.139113 | [-0.183064, -0.095259] | yes |
| t3 | 6 | 0.365270 | 0.693147 | -0.327877 | [-0.507853, -0.100212] | yes |
| collegiate | 2 | 0.911858 | 0.693147 | 0.218711 | [0.000000, 0.437422] | no |
| offseason | 435 | 0.637651 | 0.693147 | -0.055496 | [-0.087198, -0.024438] | yes |
| international=1 | 103 | 0.649548 | 0.693147 | -0.043599 | [-0.116048, 0.027713] | no |
| international=0 | 2515 | 0.622231 | 0.693147 | -0.070916 | [-0.087194, -0.053639] | yes |

| Model | Section | Rows | Log loss | Brier | Accuracy | ECE |
|---|---|---:|---:|---:|---:|---:|
| player_round_glicko+regional_form | all | 2618 | 0.622635 | 0.216724 | 0.652788 | 0.034580 |
| player_round_glicko+regional_form | vct | 415 | 0.643155 | 0.226141 | 0.631325 | 0.044875 |
| player_round_glicko+regional_form | vcl | 1351 | 0.633842 | 0.220177 | 0.647668 | 0.050966 |
| player_round_glicko+regional_form | gc | 409 | 0.551735 | 0.189704 | 0.709046 | 0.063688 |
| player_round_glicko+regional_form | t3 | 6 | 0.365850 | 0.107899 | 0.833333 | 0.282856 |
| player_round_glicko+regional_form | collegiate | 2 | 0.911858 | 0.354266 | 0.250000 | 0.588575 |
| player_round_glicko+regional_form | offseason | 435 | 0.637126 | 0.223292 | 0.635632 | 0.032633 |
| player_round_glicko+regional_form | unknown | 0 | — | — | — | — |
| player_round_glicko+regional_form | international=1 | 103 | 0.635556 | 0.221592 | 0.621359 | 0.118983 |
| player_round_glicko+regional_form | international=0 | 2515 | 0.622106 | 0.216525 | 0.654076 | 0.033858 |

player_round_glicko+regional_form − coin (paired log loss):

| Section | Rows | player_round_glicko+regional_form log loss | coin log loss | Difference | 95% interval | Significant |
|---|---:|---:|---:|---:|---|---|
| all | 2618 | 0.622635 | 0.693147 | -0.070512 | [-0.086706, -0.053615] | yes |
| vct | 415 | 0.643155 | 0.693147 | -0.049992 | [-0.083462, -0.015053] | yes |
| vcl | 1351 | 0.633842 | 0.693147 | -0.059305 | [-0.084190, -0.034160] | yes |
| gc | 409 | 0.551735 | 0.693147 | -0.141413 | [-0.184536, -0.097965] | yes |
| t3 | 6 | 0.365850 | 0.693147 | -0.327297 | [-0.507254, -0.099981] | yes |
| collegiate | 2 | 0.911858 | 0.693147 | 0.218711 | [0.000000, 0.437422] | no |
| offseason | 435 | 0.637126 | 0.693147 | -0.056021 | [-0.087808, -0.024279] | yes |
| international=1 | 103 | 0.635556 | 0.693147 | -0.057591 | [-0.136499, 0.018616] | no |
| international=0 | 2515 | 0.622106 | 0.693147 | -0.071041 | [-0.087474, -0.053869] | yes |

| Model | Section | Rows | Log loss | Brier | Accuracy | ECE |
|---|---|---:|---:|---:|---:|---:|
| player_round_glicko_rookie+form | all | 2618 | 0.607206 | 0.210182 | 0.662720 | 0.025158 |
| player_round_glicko_rookie+form | vct | 415 | 0.638710 | 0.225236 | 0.626506 | 0.034533 |
| player_round_glicko_rookie+form | vcl | 1351 | 0.615523 | 0.212328 | 0.658771 | 0.041819 |
| player_round_glicko_rookie+form | gc | 409 | 0.542950 | 0.185785 | 0.723716 | 0.047780 |
| player_round_glicko_rookie+form | t3 | 6 | 0.394735 | 0.132260 | 0.833333 | 0.282771 |
| player_round_glicko_rookie+form | collegiate | 2 | 0.707688 | 0.257268 | 0.250000 | 0.507166 |
| player_round_glicko_rookie+form | offseason | 435 | 0.614201 | 0.212952 | 0.651724 | 0.051147 |
| player_round_glicko_rookie+form | unknown | 0 | — | — | — | — |
| player_round_glicko_rookie+form | international=1 | 103 | 0.638528 | 0.223720 | 0.611650 | 0.108959 |
| player_round_glicko_rookie+form | international=0 | 2515 | 0.605923 | 0.209627 | 0.664811 | 0.026419 |

player_round_glicko_rookie+form − coin (paired log loss):

| Section | Rows | player_round_glicko_rookie+form log loss | coin log loss | Difference | 95% interval | Significant |
|---|---:|---:|---:|---:|---|---|
| all | 2618 | 0.607206 | 0.693147 | -0.085942 | [-0.103305, -0.068273] | yes |
| vct | 415 | 0.638710 | 0.693147 | -0.054437 | [-0.083812, -0.024313] | yes |
| vcl | 1351 | 0.615523 | 0.693147 | -0.077624 | [-0.103909, -0.050056] | yes |
| gc | 409 | 0.542950 | 0.693147 | -0.150197 | [-0.192894, -0.106089] | yes |
| t3 | 6 | 0.394735 | 0.693147 | -0.298412 | [-0.576299, 0.012427] | no |
| collegiate | 2 | 0.707688 | 0.693147 | 0.014541 | [0.000000, 0.029082] | no |
| offseason | 435 | 0.614201 | 0.693147 | -0.078947 | [-0.114689, -0.039924] | yes |
| international=1 | 103 | 0.638528 | 0.693147 | -0.054619 | [-0.114871, 0.000261] | no |
| international=0 | 2515 | 0.605923 | 0.693147 | -0.087224 | [-0.104182, -0.069501] | yes |

| Model | Section | Rows | Log loss | Brier | Accuracy | ECE |
|---|---|---:|---:|---:|---:|---:|
| player_round_glicko_rookie+regional_form | all | 2618 | 0.606851 | 0.210024 | 0.664629 | 0.027520 |
| player_round_glicko_rookie+regional_form | vct | 415 | 0.638153 | 0.224984 | 0.631325 | 0.036989 |
| player_round_glicko_rookie+regional_form | vcl | 1351 | 0.615468 | 0.212321 | 0.660252 | 0.043465 |
| player_round_glicko_rookie+regional_form | gc | 409 | 0.541132 | 0.184958 | 0.728606 | 0.045950 |
| player_round_glicko_rookie+regional_form | t3 | 6 | 0.395721 | 0.132668 | 0.833333 | 0.283488 |
| player_round_glicko_rookie+regional_form | collegiate | 2 | 0.707688 | 0.257268 | 0.250000 | 0.507166 |
| player_round_glicko_rookie+regional_form | offseason | 435 | 0.614468 | 0.213035 | 0.649425 | 0.042239 |
| player_round_glicko_rookie+regional_form | unknown | 0 | — | — | — | — |
| player_round_glicko_rookie+regional_form | international=1 | 103 | 0.629866 | 0.219825 | 0.660194 | 0.112397 |
| player_round_glicko_rookie+regional_form | international=0 | 2515 | 0.605909 | 0.209622 | 0.664811 | 0.027931 |

player_round_glicko_rookie+regional_form − coin (paired log loss):

| Section | Rows | player_round_glicko_rookie+regional_form log loss | coin log loss | Difference | 95% interval | Significant |
|---|---:|---:|---:|---:|---|---|
| all | 2618 | 0.606851 | 0.693147 | -0.086296 | [-0.103656, -0.068475] | yes |
| vct | 415 | 0.638153 | 0.693147 | -0.054994 | [-0.086306, -0.023100] | yes |
| vcl | 1351 | 0.615468 | 0.693147 | -0.077679 | [-0.103900, -0.050175] | yes |
| gc | 409 | 0.541132 | 0.693147 | -0.152015 | [-0.194517, -0.108168] | yes |
| t3 | 6 | 0.395721 | 0.693147 | -0.297427 | [-0.575560, 0.012745] | no |
| collegiate | 2 | 0.707688 | 0.693147 | 0.014541 | [0.000000, 0.029082] | no |
| offseason | 435 | 0.614468 | 0.693147 | -0.078679 | [-0.115400, -0.037462] | yes |
| international=1 | 103 | 0.629866 | 0.693147 | -0.063281 | [-0.139141, 0.008210] | no |
| international=0 | 2515 | 0.605909 | 0.693147 | -0.087238 | [-0.104455, -0.069542] | yes |

player_round_glicko − team_elo (paired log loss):

| Section | Rows | player_round_glicko log loss | team_elo log loss | Difference | 95% interval | Significant |
|---|---:|---:|---:|---:|---|---|
| all | 2618 | 0.623010 | 0.666164 | -0.043154 | [-0.055287, -0.031006] | yes |

player_round_glicko_rookie − team_elo (paired log loss):

| Section | Rows | player_round_glicko_rookie log loss | team_elo log loss | Difference | 95% interval | Significant |
|---|---:|---:|---:|---:|---|---|
| all | 2618 | 0.608464 | 0.666164 | -0.057700 | [-0.073133, -0.042144] | yes |

team_elo+form − team_elo (paired log loss):

| Section | Rows | team_elo+form log loss | team_elo log loss | Difference | 95% interval | Significant |
|---|---:|---:|---:|---:|---|---|
| all | 2618 | 0.659479 | 0.666164 | -0.006685 | [-0.012835, -0.000576] | yes |

team_elo+regional_form − team_elo (paired log loss):

| Section | Rows | team_elo+regional_form log loss | team_elo log loss | Difference | 95% interval | Significant |
|---|---:|---:|---:|---:|---|---|
| all | 2618 | 0.657452 | 0.666164 | -0.008712 | [-0.015165, -0.002675] | yes |

player_round_glicko+form − team_elo (paired log loss):

| Section | Rows | player_round_glicko+form log loss | team_elo log loss | Difference | 95% interval | Significant |
|---|---:|---:|---:|---:|---|---|
| all | 2618 | 0.623306 | 0.666164 | -0.042859 | [-0.055471, -0.029543] | yes |

player_round_glicko+regional_form − team_elo (paired log loss):

| Section | Rows | player_round_glicko+regional_form log loss | team_elo log loss | Difference | 95% interval | Significant |
|---|---:|---:|---:|---:|---|---|
| all | 2618 | 0.622635 | 0.666164 | -0.043529 | [-0.056207, -0.030314] | yes |

player_round_glicko_rookie+form − team_elo (paired log loss):

| Section | Rows | player_round_glicko_rookie+form log loss | team_elo log loss | Difference | 95% interval | Significant |
|---|---:|---:|---:|---:|---|---|
| all | 2618 | 0.607206 | 0.666164 | -0.058959 | [-0.075335, -0.042577] | yes |

player_round_glicko_rookie+regional_form − team_elo (paired log loss):

| Section | Rows | player_round_glicko_rookie+regional_form log loss | team_elo log loss | Difference | 95% interval | Significant |
|---|---:|---:|---:|---:|---|---|
| all | 2618 | 0.606851 | 0.666164 | -0.059313 | [-0.075799, -0.042842] | yes |

## Stage 2 — validation vs Kalshi

### team_elo: Kalshi comparison and returns



#### Log loss vs Kalshi

| Kind | Slice | Rows | Model log loss | Kalshi log loss | Difference [95% interval] | Significant |
|---|---|---:|---:|---:|---|---|
| series | all | 677 | 0.680690 | 0.633240 | 0.047450 [0.020396, 0.075926] | yes |
| series | vct | 278 | 0.684476 | 0.634755 | 0.049721 [0.008838, 0.093876] | yes |
| series | vcl | 340 | 0.667581 | 0.619968 | 0.047613 [0.007487, 0.090130] | yes |
| series | gc | 0 | — | — | — | — |
| series | t3 | 0 | — | — | — | — |
| series | collegiate | 0 | — | — | — | — |
| series | offseason | 59 | 0.738397 | 0.702587 | 0.035810 [-0.054746, 0.131057] | no |
| series | international=1 | 41 | 0.662467 | 0.653397 | 0.009070 [-0.060093, 0.081445] | no |
| series | international=0 | 636 | 0.681865 | 0.631941 | 0.049924 [0.020253, 0.081424] | yes |
| map | all | 1049 | 0.673960 | 0.668225 | 0.005735 [-0.015609, 0.025041] | no |
| map | vct | 461 | 0.676454 | 0.665762 | 0.010693 [-0.013375, 0.034200] | no |
| map | vcl | 490 | 0.669736 | 0.668365 | 0.001371 [-0.038275, 0.035482] | no |
| map | gc | 0 | — | — | — | — |
| map | t3 | 0 | — | — | — | — |
| map | collegiate | 0 | — | — | — | — |
| map | offseason | 98 | 0.683345 | 0.679111 | 0.004235 [-0.028780, 0.040252] | no |
| map | international=1 | 59 | 0.673767 | 0.649653 | 0.024115 [-0.012163, 0.060480] | no |
| map | international=0 | 990 | 0.673971 | 0.669332 | 0.004640 [-0.018040, 0.025305] | no |

#### Full-Kelly returns

| Kind | Slice | Bets | Matches | Mean edge | Flat ROI [95% interval] | Kelly, LoL caps ($50 start) | Multiple | Max drawdown | Largest stake |
|---|---|---:|---:|---:|---|---:|---:|---:|---:|
| series | all | 521 | 521 | 0.1095 | 2.54% [-8.74%, 14.54%] | $0.35 | 0.007× | 99.64% | $7.89 |
| series | vct | 213 | 213 | 0.1065 | 3.46% [-12.12%, 20.30%] | $11.73 | 0.235× | 81.11% | $6.21 |
| series | vcl | 261 | 261 | 0.1124 | 2.75% [-14.50%, 20.42%] | $2.33 | 0.047× | 96.42% | $5.14 |
| series | gc | 0 | 0 | — | — | $50.00 | 1.000× | 0.00% | $0.00 |
| series | t3 | 0 | 0 | — | — | $50.00 | 1.000× | 0.00% | $0.00 |
| series | collegiate | 0 | 0 | — | — | $50.00 | 1.000× | 0.00% | $0.00 |
| series | offseason | 47 | 47 | 0.1073 | -2.77% [-29.82%, 25.82%] | $34.98 | 0.700× | 62.18% | $7.58 |
| series | international=1 | 37 | 37 | 0.0736 | 5.39% [-28.74%, 40.23%] | $40.83 | 0.817× | 36.65% | $6.44 |
| series | international=0 | 484 | 484 | 0.1123 | 2.33% [-9.02%, 14.91%] | $0.44 | 0.009× | 99.50% | $6.89 |
| map | all | 695 | 370 | 0.0766 | 13.04% [-2.45%, 32.95%] | $596.77 | 11.935× | 81.72% | $200.49 |
| map | vct | 282 | 148 | 0.0746 | 6.74% [-9.45%, 29.27%] | $105.83 | 2.117× | 44.34% | $12.40 |
| map | vcl | 341 | 186 | 0.0851 | 21.49% [-6.69%, 55.85%] | $325.68 | 6.514× | 72.71% | $78.79 |
| map | gc | 0 | 0 | — | — | $50.00 | 1.000× | 0.00% | $0.00 |
| map | t3 | 0 | 0 | — | — | $50.00 | 1.000× | 0.00% | $0.00 |
| map | collegiate | 0 | 0 | — | — | $50.00 | 1.000× | 0.00% | $0.00 |
| map | offseason | 72 | 36 | 0.0441 | -2.35% [-23.92%, 17.92%] | $43.20 | 0.864× | 27.63% | $5.00 |
| map | international=1 | 38 | 21 | 0.0515 | -17.25% [-43.53%, 8.51%] | $34.23 | 0.685× | 31.55% | $4.82 |
| map | international=0 | 657 | 349 | 0.0780 | 14.79% [-1.62%, 35.01%] | $733.81 | 14.676× | 77.90% | $205.67 |
| series+map | all | 1216 | 538 | 0.0907 | 8.54% [-2.86%, 21.03%] | $87.80 | 1.756× | 95.47% | $153.34 |

#### Monthly market blend fits

UTC monthly fits use earlier rows of the same kind from 2025-09-01, excluding holdout; minimum 100 rows. logit(p_blend) = a·logit(mid) + b·(logit(p_model) − logit(mid)); inputs clipped to [0.01, 0.99], no intercept, ridge 1e-6. Unfitted rows use mid unchanged; excluded from blended tables: 240 rows. Rating parameters remain selected on the tuning window.

| Month | Kind | n | a | b | Status |
|---|---|---:|---:|---:|---|
| 2026-01 | series | 0 | 1.000000 | 0.000000 | unfitted |
| 2026-02 | series | 21 | 1.000000 | 0.000000 | unfitted |
| 2026-02 | map | 0 | 1.000000 | 0.000000 | unfitted |
| 2026-03 | series | 72 | 1.000000 | 0.000000 | unfitted |
| 2026-03 | map | 48 | 1.000000 | 0.000000 | unfitted |
| 2026-04 | series | 136 | 1.039597 | 0.202241 | fitted |
| 2026-04 | map | 104 | 1.337322 | 0.016754 | fitted |
| 2026-05 | series | 357 | 0.899603 | 0.180030 | fitted |
| 2026-05 | map | 456 | 0.904798 | 0.569288 | fitted |
| 2026-06 | series | 556 | 0.831284 | 0.075311 | fitted |
| 2026-06 | map | 833 | 0.786307 | 0.417440 | fitted |

#### Log loss vs Kalshi (blended)

| Kind | Slice | Rows | Model log loss | Kalshi log loss | Difference [95% interval] | Significant |
|---|---|---:|---:|---:|---|---|
| series | all | 541 | 0.635566 | 0.634347 | 0.001219 [-0.004444, 0.006863] | no |
| series | vct | 201 | 0.643472 | 0.644147 | -0.000675 [-0.010271, 0.009359] | no |
| series | vcl | 291 | 0.623026 | 0.621829 | 0.001197 [-0.006314, 0.008707] | no |
| series | gc | 0 | — | — | — | — |
| series | t3 | 0 | — | — | — | — |
| series | collegiate | 0 | — | — | — | — |
| series | offseason | 49 | 0.677612 | 0.668490 | 0.009122 [-0.004669, 0.023042] | no |
| series | international=1 | 24 | 0.679288 | 0.682705 | -0.003417 [-0.031730, 0.019595] | no |
| series | international=0 | 517 | 0.633537 | 0.632102 | 0.001435 [-0.004540, 0.007525] | no |
| map | all | 945 | 0.685993 | 0.673192 | 0.012801 [0.003636, 0.021909] | yes |
| map | vct | 392 | 0.673356 | 0.667249 | 0.006106 [-0.006097, 0.018894] | no |
| map | vcl | 456 | 0.697999 | 0.676303 | 0.021696 [0.006945, 0.036859] | yes |
| map | gc | 0 | — | — | — | — |
| map | t3 | 0 | — | — | — | — |
| map | collegiate | 0 | — | — | — | — |
| map | offseason | 97 | 0.680620 | 0.682581 | -0.001961 [-0.017444, 0.014282] | no |
| map | international=1 | 50 | 0.661425 | 0.651359 | 0.010067 [-0.007505, 0.027543] | no |
| map | international=0 | 895 | 0.687365 | 0.674412 | 0.012954 [0.003342, 0.022490] | yes |

#### Full-Kelly returns (blended)

| Kind | Slice | Bets | Matches | Mean edge | Flat ROI [95% interval] | Kelly, LoL caps ($50 start) | Multiple | Max drawdown | Largest stake |
|---|---|---:|---:|---:|---|---:|---:|---:|---:|
| series | all | 104 | 104 | 0.0161 | -2.16% [-28.31%, 26.25%] | $27.44 | 0.549× | 53.52% | $5.00 |
| series | vct | 51 | 51 | 0.0181 | 5.87% [-28.99%, 48.26%] | $32.27 | 0.645× | 50.07% | $5.00 |
| series | vcl | 49 | 49 | 0.0141 | -6.63% [-43.58%, 34.99%] | $46.01 | 0.920× | 13.87% | $5.04 |
| series | gc | 0 | 0 | — | — | $50.00 | 1.000× | 0.00% | $0.00 |
| series | t3 | 0 | 0 | — | — | $50.00 | 1.000× | 0.00% | $0.00 |
| series | collegiate | 0 | 0 | — | — | $50.00 | 1.000× | 0.00% | $0.00 |
| series | offseason | 4 | 4 | 0.0138 | -49.75% [-100.00%, 50.76%] | $46.20 | 0.924× | 9.11% | $2.10 |
| series | international=1 | 7 | 7 | 0.0080 | 64.11% [-57.39%, 227.23%] | $56.65 | 1.133× | 2.28% | $1.19 |
| series | international=0 | 97 | 97 | 0.0167 | -6.94% [-31.82%, 19.41%] | $24.22 | 0.484× | 54.31% | $5.00 |
| map | all | 354 | 203 | 0.0289 | -6.71% [-16.98%, 3.63%] | $8.52 | 0.170× | 85.18% | $5.30 |
| map | vct | 138 | 74 | 0.0306 | -1.57% [-17.72%, 16.40%] | $35.04 | 0.701× | 40.97% | $4.89 |
| map | vcl | 187 | 113 | 0.0286 | -11.37% [-26.29%, 3.40%] | $13.15 | 0.263× | 75.92% | $5.03 |
| map | gc | 0 | 0 | — | — | $50.00 | 1.000× | 0.00% | $0.00 |
| map | t3 | 0 | 0 | — | — | $50.00 | 1.000× | 0.00% | $0.00 |
| map | collegiate | 0 | 0 | — | — | $50.00 | 1.000× | 0.00% | $0.00 |
| map | offseason | 29 | 16 | 0.0229 | -1.07% [-32.34%, 32.04%] | $45.74 | 0.915× | 12.17% | $2.72 |
| map | international=1 | 18 | 9 | 0.0251 | -28.99% [-71.06%, 16.58%] | $45.18 | 0.904× | 14.91% | $2.75 |
| map | international=0 | 336 | 194 | 0.0291 | -5.51% [-16.26%, 5.42%] | $9.42 | 0.188× | 83.60% | $5.30 |
| series+map | all | 458 | 243 | 0.0260 | -5.67% [-17.90%, 7.25%] | $5.55 | 0.111× | 90.50% | $5.21 |

#### Monthly breakdown

All metrics use identical linked rows within each kind/month. Unfitted blend months show —; counts include all rows.

| Kind | Month | Rows | Model log loss | Blended log loss | Kalshi log loss | Raw flat ROI (bets) | Blended flat ROI (bets) |
|---|---|---:|---:|---:|---:|---|---|
| map | 2026-02 | 48 | 0.713944 | — | 0.690786 | 0.87% (27) | — |
| map | 2026-03 | 56 | 0.656362 | — | 0.565065 | -37.75% (46) | — |
| map | 2026-04 | 352 | 0.658022 | 0.713240 | 0.690793 | 50.32% (232) | -8.07% (108) |
| map | 2026-05 | 377 | 0.700355 | 0.688357 | 0.687018 | 3.62% (250) | 3.57% (156) |
| map | 2026-06 | 216 | 0.649542 | 0.637464 | 0.620377 | -12.90% (140) | -22.87% (90) |
| series | 2026-01 | 21 | 0.714136 | — | 0.661069 | 7.61% (18) | — |
| series | 2026-02 | 51 | 0.688956 | — | 0.694525 | 36.06% (39) | — |
| series | 2026-03 | 64 | 0.681114 | — | 0.565917 | -25.91% (56) | — |
| series | 2026-04 | 221 | 0.660684 | 0.625579 | 0.627690 | 10.90% (163) | 0.81% (43) |
| series | 2026-05 | 199 | 0.726930 | 0.665638 | 0.663719 | -2.09% (152) | -22.53% (37) |
| series | 2026-06 | 121 | 0.631671 | 0.604350 | 0.598199 | -2.43% (93) | 23.91% (24) |

### player_round_glicko: Kalshi comparison and returns



#### Log loss vs Kalshi

| Kind | Slice | Rows | Model log loss | Kalshi log loss | Difference [95% interval] | Significant |
|---|---|---:|---:|---:|---|---|
| series | all | 677 | 0.634045 | 0.633240 | 0.000805 [-0.023351, 0.026600] | no |
| series | vct | 278 | 0.629475 | 0.634755 | -0.005280 [-0.037707, 0.026598] | no |
| series | vcl | 340 | 0.629140 | 0.619968 | 0.009172 [-0.031107, 0.052122] | no |
| series | gc | 0 | — | — | — | — |
| series | t3 | 0 | — | — | — | — |
| series | collegiate | 0 | — | — | — | — |
| series | offseason | 59 | 0.683843 | 0.702587 | -0.018744 [-0.081522, 0.042831] | no |
| series | international=1 | 41 | 0.604847 | 0.653397 | -0.048550 [-0.095300, -0.000770] | yes |
| series | international=0 | 636 | 0.635927 | 0.631941 | 0.003987 [-0.022147, 0.029787] | no |
| map | all | 1049 | 0.663495 | 0.668225 | -0.004729 [-0.026369, 0.013642] | no |
| map | vct | 461 | 0.664887 | 0.665762 | -0.000875 [-0.020108, 0.016697] | no |
| map | vcl | 490 | 0.657613 | 0.668365 | -0.010752 [-0.053012, 0.024245] | no |
| map | gc | 0 | — | — | — | — |
| map | t3 | 0 | — | — | — | — |
| map | collegiate | 0 | — | — | — | — |
| map | offseason | 98 | 0.686363 | 0.679111 | 0.007253 [-0.022155, 0.037270] | no |
| map | international=1 | 59 | 0.661765 | 0.649653 | 0.012112 [-0.009515, 0.034166] | no |
| map | international=0 | 990 | 0.663599 | 0.669332 | -0.005733 [-0.027631, 0.014380] | no |

#### Full-Kelly returns

| Kind | Slice | Bets | Matches | Mean edge | Flat ROI [95% interval] | Kelly, LoL caps ($50 start) | Multiple | Max drawdown | Largest stake |
|---|---|---:|---:|---:|---|---:|---:|---:|---:|
| series | all | 505 | 505 | 0.0957 | 8.81% [-2.77%, 21.23%] | $145.02 | 2.900× | 81.99% | $53.43 |
| series | vct | 201 | 201 | 0.0849 | 13.30% [-5.23%, 33.41%] | $59.80 | 1.196× | 70.28% | $8.64 |
| series | vcl | 263 | 263 | 0.1075 | 6.51% [-10.42%, 23.70%] | $103.03 | 2.061× | 60.97% | $22.61 |
| series | gc | 0 | 0 | — | — | $50.00 | 1.000× | 0.00% | $0.00 |
| series | t3 | 0 | 0 | — | — | $50.00 | 1.000× | 0.00% | $0.00 |
| series | collegiate | 0 | 0 | — | — | $50.00 | 1.000× | 0.00% | $0.00 |
| series | offseason | 41 | 41 | 0.0731 | 1.51% [-34.84%, 41.32%] | $55.12 | 1.102× | 55.42% | $9.05 |
| series | international=1 | 28 | 28 | 0.0541 | 37.82% [-7.08%, 86.22%] | $100.50 | 2.010× | 22.30% | $8.39 |
| series | international=0 | 477 | 477 | 0.0982 | 7.11% [-5.41%, 20.41%] | $72.34 | 1.447× | 84.74% | $40.61 |
| map | all | 648 | 346 | 0.0664 | 15.63% [-2.02%, 36.72%] | $3517.67 | 70.353× | 55.00% | $250.00 |
| map | vct | 275 | 141 | 0.0506 | 7.73% [-11.18%, 30.45%] | $97.29 | 1.946× | 43.34% | $8.34 |
| map | vcl | 325 | 179 | 0.0850 | 25.67% [-3.02%, 61.19%] | $794.27 | 15.885× | 70.43% | $220.10 |
| map | gc | 0 | 0 | — | — | $50.00 | 1.000× | 0.00% | $0.00 |
| map | t3 | 0 | 0 | — | — | $50.00 | 1.000× | 0.00% | $0.00 |
| map | collegiate | 0 | 0 | — | — | $50.00 | 1.000× | 0.00% | $0.00 |
| map | offseason | 48 | 26 | 0.0310 | -7.16% [-36.14%, 25.94%] | $55.80 | 1.116× | 15.18% | $3.12 |
| map | international=1 | 31 | 16 | 0.0362 | -22.79% [-52.74%, 6.21%] | $36.10 | 0.722× | 28.48% | $5.00 |
| map | international=0 | 617 | 330 | 0.0679 | 17.56% [-1.42%, 39.01%] | $4433.87 | 88.677× | 50.09% | $250.00 |
| series+map | all | 1153 | 532 | 0.0792 | 12.64% [-0.04%, 26.30%] | $2999.99 | 60.000× | 56.51% | $250.00 |

#### Monthly market blend fits

UTC monthly fits use earlier rows of the same kind from 2025-09-01, excluding holdout; minimum 100 rows. logit(p_blend) = a·logit(mid) + b·(logit(p_model) − logit(mid)); inputs clipped to [0.01, 0.99], no intercept, ridge 1e-6. Unfitted rows use mid unchanged; excluded from blended tables: 240 rows. Rating parameters remain selected on the tuning window.

| Month | Kind | n | a | b | Status |
|---|---|---:|---:|---:|---|
| 2026-01 | series | 0 | 1.000000 | 0.000000 | unfitted |
| 2026-02 | series | 21 | 1.000000 | 0.000000 | unfitted |
| 2026-02 | map | 0 | 1.000000 | 0.000000 | unfitted |
| 2026-03 | series | 72 | 1.000000 | 0.000000 | unfitted |
| 2026-03 | map | 48 | 1.000000 | 0.000000 | unfitted |
| 2026-04 | series | 136 | 1.384841 | 0.701267 | fitted |
| 2026-04 | map | 104 | 1.508791 | 0.303578 | fitted |
| 2026-05 | series | 357 | 1.079660 | 0.541880 | fitted |
| 2026-05 | map | 456 | 1.200022 | 0.940096 | fitted |
| 2026-06 | series | 556 | 1.022765 | 0.528480 | fitted |
| 2026-06 | map | 833 | 1.024604 | 0.753237 | fitted |

#### Log loss vs Kalshi (blended)

| Kind | Slice | Rows | Model log loss | Kalshi log loss | Difference [95% interval] | Significant |
|---|---|---:|---:|---:|---|---|
| series | all | 541 | 0.628325 | 0.634347 | -0.006022 [-0.021437, 0.010194] | no |
| series | vct | 201 | 0.640032 | 0.644147 | -0.004115 [-0.024712, 0.017983] | no |
| series | vcl | 291 | 0.611216 | 0.621829 | -0.010613 [-0.033698, 0.016425] | no |
| series | gc | 0 | — | — | — | — |
| series | t3 | 0 | — | — | — | — |
| series | collegiate | 0 | — | — | — | — |
| series | offseason | 49 | 0.681909 | 0.668490 | 0.013419 [-0.014157, 0.040404] | no |
| series | international=1 | 24 | 0.656229 | 0.682705 | -0.026477 [-0.061993, 0.006922] | no |
| series | international=0 | 517 | 0.627030 | 0.632102 | -0.005073 [-0.020318, 0.011988] | no |
| map | all | 945 | 0.682041 | 0.673192 | 0.008849 [0.000096, 0.018209] | yes |
| map | vct | 392 | 0.670106 | 0.667249 | 0.002856 [-0.010047, 0.015453] | no |
| map | vcl | 456 | 0.690572 | 0.676303 | 0.014269 [-0.000086, 0.029356] | no |
| map | gc | 0 | — | — | — | — |
| map | t3 | 0 | — | — | — | — |
| map | collegiate | 0 | — | — | — | — |
| map | offseason | 97 | 0.690168 | 0.682581 | 0.007587 [-0.018518, 0.035664] | no |
| map | international=1 | 50 | 0.657420 | 0.651359 | 0.006061 [-0.010844, 0.023016] | no |
| map | international=0 | 895 | 0.683416 | 0.674412 | 0.009005 [-0.001019, 0.018445] | no |

#### Full-Kelly returns (blended)

| Kind | Slice | Bets | Matches | Mean edge | Flat ROI [95% interval] | Kelly, LoL caps ($50 start) | Multiple | Max drawdown | Largest stake |
|---|---|---:|---:|---:|---|---:|---:|---:|---:|
| series | all | 308 | 308 | 0.0443 | 10.99% [-2.91%, 25.40%] | $128.12 | 2.562× | 53.73% | $13.61 |
| series | vct | 120 | 120 | 0.0413 | 4.84% [-14.12%, 26.15%] | $32.72 | 0.654× | 61.20% | $6.02 |
| series | vcl | 169 | 169 | 0.0484 | 18.01% [-2.30%, 38.27%] | $231.80 | 4.636× | 28.57% | $22.70 |
| series | gc | 0 | 0 | — | — | $50.00 | 1.000× | 0.00% | $0.00 |
| series | t3 | 0 | 0 | — | — | $50.00 | 1.000× | 0.00% | $0.00 |
| series | collegiate | 0 | 0 | — | — | $50.00 | 1.000× | 0.00% | $0.00 |
| series | offseason | 19 | 19 | 0.0265 | -12.66% [-67.24%, 47.38%] | $43.56 | 0.871× | 21.30% | $4.27 |
| series | international=1 | 9 | 9 | 0.0310 | 58.39% [-34.23%, 168.18%] | $67.74 | 1.355× | 3.32% | $5.93 |
| series | international=0 | 299 | 299 | 0.0447 | 9.56% [-4.27%, 24.21%] | $94.57 | 1.891× | 55.58% | $13.61 |
| map | all | 493 | 264 | 0.0349 | -3.64% [-12.24%, 5.15%] | $10.93 | 0.219× | 84.44% | $6.07 |
| map | vct | 203 | 106 | 0.0312 | -0.50% [-13.20%, 14.02%] | $39.18 | 0.784× | 37.46% | $5.71 |
| map | vcl | 253 | 139 | 0.0386 | -6.11% [-18.31%, 6.30%] | $15.55 | 0.311× | 74.44% | $5.26 |
| map | gc | 0 | 0 | — | — | $50.00 | 1.000× | 0.00% | $0.00 |
| map | t3 | 0 | 0 | — | — | $50.00 | 1.000× | 0.00% | $0.00 |
| map | collegiate | 0 | 0 | — | — | $50.00 | 1.000× | 0.00% | $0.00 |
| map | offseason | 37 | 19 | 0.0299 | -4.04% [-37.60%, 27.97%] | $44.74 | 0.895× | 16.14% | $2.75 |
| map | international=1 | 21 | 10 | 0.0259 | -24.65% [-69.66%, 17.96%] | $47.95 | 0.959× | 9.98% | $2.83 |
| map | international=0 | 472 | 254 | 0.0353 | -2.71% [-11.83%, 6.02%] | $11.39 | 0.228× | 83.77% | $6.07 |
| series+map | all | 801 | 363 | 0.0385 | 1.98% [-6.43%, 11.32%] | $19.30 | 0.386× | 83.24% | $7.82 |

#### Monthly breakdown

All metrics use identical linked rows within each kind/month. Unfitted blend months show —; counts include all rows.

| Kind | Month | Rows | Model log loss | Blended log loss | Kalshi log loss | Raw flat ROI (bets) | Blended flat ROI (bets) |
|---|---|---:|---:|---:|---:|---|---|
| map | 2026-02 | 48 | 0.708502 | — | 0.690786 | -0.27% (41) | — |
| map | 2026-03 | 56 | 0.626002 | — | 0.565065 | -19.99% (39) | — |
| map | 2026-04 | 352 | 0.644660 | 0.701761 | 0.690793 | 55.64% (225) | -2.59% (192) |
| map | 2026-05 | 377 | 0.687427 | 0.688399 | 0.687018 | 5.97% (201) | 2.81% (184) |
| map | 2026-06 | 216 | 0.652139 | 0.638808 | 0.620377 | -19.73% (142) | -15.52% (117) |
| series | 2026-01 | 21 | 0.576770 | — | 0.661069 | 26.31% (18) | — |
| series | 2026-02 | 51 | 0.679741 | — | 0.694525 | 17.18% (39) | — |
| series | 2026-03 | 64 | 0.615700 | — | 0.565917 | -5.88% (50) | — |
| series | 2026-04 | 221 | 0.627814 | 0.625234 | 0.627690 | 13.93% (158) | 13.07% (145) |
| series | 2026-05 | 199 | 0.658197 | 0.654601 | 0.663719 | 11.63% (145) | 7.93% (99) |
| series | 2026-06 | 121 | 0.606087 | 0.590755 | 0.598199 | -3.05% (95) | 10.99% (64) |

### player_round_glicko_rookie: Kalshi comparison and returns



#### Log loss vs Kalshi

| Kind | Slice | Rows | Model log loss | Kalshi log loss | Difference [95% interval] | Significant |
|---|---|---:|---:|---:|---|---|
| series | all | 677 | 0.624753 | 0.633240 | -0.008487 [-0.031352, 0.015646] | no |
| series | vct | 278 | 0.624782 | 0.634755 | -0.009973 [-0.041876, 0.019634] | no |
| series | vcl | 340 | 0.614997 | 0.619968 | -0.004970 [-0.042718, 0.032073] | no |
| series | gc | 0 | — | — | — | — |
| series | t3 | 0 | — | — | — | — |
| series | collegiate | 0 | — | — | — | — |
| series | offseason | 59 | 0.680831 | 0.702587 | -0.021756 [-0.076853, 0.032800] | no |
| series | international=1 | 41 | 0.611472 | 0.653397 | -0.041925 [-0.091362, 0.005493] | no |
| series | international=0 | 636 | 0.625609 | 0.631941 | -0.006332 [-0.031154, 0.017622] | no |
| map | all | 1049 | 0.659403 | 0.668225 | -0.008821 [-0.030015, 0.009331] | no |
| map | vct | 461 | 0.661975 | 0.665762 | -0.003787 [-0.023047, 0.012314] | no |
| map | vcl | 490 | 0.651878 | 0.668365 | -0.016487 [-0.057766, 0.017947] | no |
| map | gc | 0 | — | — | — | — |
| map | t3 | 0 | — | — | — | — |
| map | collegiate | 0 | — | — | — | — |
| map | offseason | 98 | 0.684938 | 0.679111 | 0.005827 [-0.024606, 0.033088] | no |
| map | international=1 | 59 | 0.664774 | 0.649653 | 0.015121 [-0.005332, 0.035238] | no |
| map | international=0 | 990 | 0.659083 | 0.669332 | -0.010248 [-0.031448, 0.009133] | no |

#### Full-Kelly returns

| Kind | Slice | Bets | Matches | Mean edge | Flat ROI [95% interval] | Kelly, LoL caps ($50 start) | Multiple | Max drawdown | Largest stake |
|---|---|---:|---:|---:|---|---:|---:|---:|---:|
| series | all | 506 | 506 | 0.0925 | 12.48% [0.01%, 25.23%] | $1039.73 | 20.795× | 70.13% | $250.00 |
| series | vct | 204 | 204 | 0.0758 | 10.57% [-8.31%, 31.42%] | $97.10 | 1.942× | 68.17% | $8.10 |
| series | vcl | 261 | 261 | 0.1095 | 14.66% [-2.45%, 33.22%] | $286.93 | 5.739× | 60.30% | $63.72 |
| series | gc | 0 | 0 | — | — | $50.00 | 1.000× | 0.00% | $0.00 |
| series | t3 | 0 | 0 | — | — | $50.00 | 1.000× | 0.00% | $0.00 |
| series | collegiate | 0 | 0 | — | — | $50.00 | 1.000× | 0.00% | $0.00 |
| series | offseason | 41 | 41 | 0.0676 | 8.16% [-31.46%, 50.95%] | $79.31 | 1.586× | 41.60% | $9.40 |
| series | international=1 | 29 | 29 | 0.0456 | 38.96% [-10.07%, 91.45%] | $101.88 | 2.038× | 28.15% | $8.50 |
| series | international=0 | 477 | 477 | 0.0953 | 10.88% [-1.93%, 24.12%] | $624.08 | 12.482× | 70.13% | $137.27 |
| map | all | 631 | 342 | 0.0649 | 15.54% [-2.70%, 37.15%] | $3658.56 | 73.171× | 54.43% | $250.00 |
| map | vct | 246 | 132 | 0.0490 | 8.44% [-11.07%, 34.86%] | $146.27 | 2.925× | 36.93% | $11.63 |
| map | vcl | 341 | 188 | 0.0798 | 22.73% [-5.36%, 59.43%] | $651.79 | 13.036× | 75.99% | $219.29 |
| map | gc | 0 | 0 | — | — | $50.00 | 1.000× | 0.00% | $0.00 |
| map | t3 | 0 | 0 | — | — | $50.00 | 1.000× | 0.00% | $0.00 |
| map | collegiate | 0 | 0 | — | — | $50.00 | 1.000× | 0.00% | $0.00 |
| map | offseason | 44 | 22 | 0.0385 | -0.51% [-36.99%, 41.38%] | $56.21 | 1.124× | 23.36% | $3.65 |
| map | international=1 | 28 | 15 | 0.0377 | -26.50% [-62.04%, 4.42%] | $33.77 | 0.675× | 33.16% | $4.92 |
| map | international=0 | 603 | 327 | 0.0662 | 17.49% [-0.83%, 39.61%] | $4846.99 | 96.940× | 47.52% | $250.00 |
| series+map | all | 1137 | 526 | 0.0772 | 14.18% [1.90%, 27.55%] | $4168.56 | 83.371× | 68.94% | $250.00 |

#### Monthly market blend fits

UTC monthly fits use earlier rows of the same kind from 2025-09-01, excluding holdout; minimum 100 rows. logit(p_blend) = a·logit(mid) + b·(logit(p_model) − logit(mid)); inputs clipped to [0.01, 0.99], no intercept, ridge 1e-6. Unfitted rows use mid unchanged; excluded from blended tables: 240 rows. Rating parameters remain selected on the tuning window.

| Month | Kind | n | a | b | Status |
|---|---|---:|---:|---:|---|
| 2026-01 | series | 0 | 1.000000 | 0.000000 | unfitted |
| 2026-02 | series | 21 | 1.000000 | 0.000000 | unfitted |
| 2026-02 | map | 0 | 1.000000 | 0.000000 | unfitted |
| 2026-03 | series | 72 | 1.000000 | 0.000000 | unfitted |
| 2026-03 | map | 48 | 1.000000 | 0.000000 | unfitted |
| 2026-04 | series | 136 | 1.343216 | 0.662584 | fitted |
| 2026-04 | map | 104 | 1.663930 | 0.514024 | fitted |
| 2026-05 | series | 357 | 1.175539 | 0.707788 | fitted |
| 2026-05 | map | 456 | 1.414420 | 1.208581 | fitted |
| 2026-06 | series | 556 | 1.130288 | 0.732615 | fitted |
| 2026-06 | map | 833 | 1.203493 | 1.007620 | fitted |

#### Log loss vs Kalshi (blended)

| Kind | Slice | Rows | Model log loss | Kalshi log loss | Difference [95% interval] | Significant |
|---|---|---:|---:|---:|---|---|
| series | all | 541 | 0.618326 | 0.634347 | -0.016021 [-0.030496, -0.001454] | yes |
| series | vct | 201 | 0.630234 | 0.644147 | -0.013912 [-0.031605, 0.004048] | no |
| series | vcl | 291 | 0.600350 | 0.621829 | -0.021478 [-0.043277, 0.002568] | no |
| series | gc | 0 | — | — | — | — |
| series | t3 | 0 | — | — | — | — |
| series | collegiate | 0 | — | — | — | — |
| series | offseason | 49 | 0.676226 | 0.668490 | 0.007736 [-0.023791, 0.038387] | no |
| series | international=1 | 24 | 0.653871 | 0.682705 | -0.028834 [-0.070556, 0.009455] | no |
| series | international=0 | 517 | 0.616676 | 0.632102 | -0.015427 [-0.029827, -0.000247] | yes |
| map | all | 945 | 0.679077 | 0.673192 | 0.005885 [-0.004293, 0.017395] | no |
| map | vct | 392 | 0.668370 | 0.667249 | 0.001121 [-0.012650, 0.014842] | no |
| map | vcl | 456 | 0.685918 | 0.676303 | 0.009614 [-0.008006, 0.026687] | no |
| map | gc | 0 | — | — | — | — |
| map | t3 | 0 | — | — | — | — |
| map | collegiate | 0 | — | — | — | — |
| map | offseason | 97 | 0.690189 | 0.682581 | 0.007608 [-0.020532, 0.038380] | no |
| map | international=1 | 50 | 0.659979 | 0.651359 | 0.008620 [-0.009745, 0.026794] | no |
| map | international=0 | 895 | 0.680144 | 0.674412 | 0.005733 [-0.005652, 0.016407] | no |

#### Full-Kelly returns (blended)

| Kind | Slice | Bets | Matches | Mean edge | Flat ROI [95% interval] | Kelly, LoL caps ($50 start) | Multiple | Max drawdown | Largest stake |
|---|---|---:|---:|---:|---|---:|---:|---:|---:|
| series | all | 304 | 304 | 0.0481 | 17.02% [2.98%, 32.21%] | $787.94 | 15.759× | 35.58% | $92.86 |
| series | vct | 106 | 106 | 0.0354 | 15.39% [-8.81%, 40.79%] | $74.06 | 1.481× | 38.56% | $6.62 |
| series | vcl | 173 | 173 | 0.0589 | 21.72% [3.04%, 41.86%] | $521.16 | 10.423× | 31.29% | $61.42 |
| series | gc | 0 | 0 | — | — | $50.00 | 1.000× | 0.00% | $0.00 |
| series | t3 | 0 | 0 | — | — | $50.00 | 1.000× | 0.00% | $0.00 |
| series | collegiate | 0 | 0 | — | — | $50.00 | 1.000× | 0.00% | $0.00 |
| series | offseason | 25 | 25 | 0.0270 | -8.57% [-52.36%, 42.48%] | $51.55 | 1.031× | 10.11% | $4.99 |
| series | international=1 | 11 | 11 | 0.0334 | 29.59% [-52.23%, 121.14%] | $70.61 | 1.412× | 5.62% | $5.84 |
| series | international=0 | 293 | 293 | 0.0487 | 16.55% [2.05%, 32.77%] | $559.54 | 11.191× | 44.13% | $65.94 |
| map | all | 549 | 293 | 0.0410 | -3.03% [-11.33%, 4.66%] | $21.98 | 0.440× | 70.06% | $6.88 |
| map | vct | 226 | 116 | 0.0352 | -2.36% [-13.96%, 10.30%] | $41.38 | 0.828× | 44.85% | $5.64 |
| map | vcl | 281 | 154 | 0.0465 | -2.80% [-14.12%, 8.28%] | $25.70 | 0.514× | 62.73% | $6.42 |
| map | gc | 0 | 0 | — | — | $50.00 | 1.000× | 0.00% | $0.00 |
| map | t3 | 0 | 0 | — | — | $50.00 | 1.000× | 0.00% | $0.00 |
| map | collegiate | 0 | 0 | — | — | $50.00 | 1.000× | 0.00% | $0.00 |
| map | offseason | 42 | 23 | 0.0347 | -8.12% [-40.72%, 26.22%] | $47.30 | 0.946× | 13.93% | $3.59 |
| map | international=1 | 23 | 12 | 0.0291 | -15.30% [-54.50%, 22.33%] | $46.68 | 0.934× | 10.00% | $2.80 |
| map | international=0 | 526 | 281 | 0.0415 | -2.49% [-11.41%, 5.84%] | $23.55 | 0.471× | 67.93% | $6.88 |
| series+map | all | 853 | 369 | 0.0435 | 4.12% [-4.50%, 12.96%] | $100.10 | 2.002× | 59.23% | $13.10 |

#### Monthly breakdown

All metrics use identical linked rows within each kind/month. Unfitted blend months show —; counts include all rows.

| Kind | Month | Rows | Model log loss | Blended log loss | Kalshi log loss | Raw flat ROI (bets) | Blended flat ROI (bets) |
|---|---|---:|---:|---:|---:|---|---|
| map | 2026-02 | 48 | 0.700971 | — | 0.690786 | 5.18% (36) | — |
| map | 2026-03 | 56 | 0.625062 | — | 0.565065 | -35.79% (36) | — |
| map | 2026-04 | 352 | 0.639265 | 0.694706 | 0.690793 | 61.22% (217) | -4.60% (221) |
| map | 2026-05 | 377 | 0.681003 | 0.685559 | 0.687018 | 7.09% (191) | 5.09% (198) |
| map | 2026-06 | 216 | 0.654189 | 0.642295 | 0.620377 | -24.71% (151) | -12.72% (130) |
| series | 2026-01 | 21 | 0.598069 | — | 0.661069 | 7.55% (18) | — |
| series | 2026-02 | 51 | 0.685124 | — | 0.694525 | 27.72% (43) | — |
| series | 2026-03 | 64 | 0.616452 | — | 0.565917 | -6.09% (50) | — |
| series | 2026-04 | 221 | 0.608834 | 0.609342 | 0.627690 | 23.43% (158) | 19.57% (126) |
| series | 2026-05 | 199 | 0.643934 | 0.646032 | 0.663719 | 13.58% (143) | 21.86% (105) |
| series | 2026-06 | 121 | 0.605857 | 0.589167 | 0.598199 | -3.72% (94) | 5.66% (73) |

### team_elo+form: Kalshi comparison and returns

form: rows=7863, H=20, w=2.61276

#### Log loss vs Kalshi

| Kind | Slice | Rows | Model log loss | Kalshi log loss | Difference [95% interval] | Significant |
|---|---|---:|---:|---:|---|---|
| series | all | 677 | 0.681439 | 0.633240 | 0.048199 [0.017585, 0.080447] | yes |
| series | vct | 278 | 0.683734 | 0.634755 | 0.048979 [0.004852, 0.097867] | yes |
| series | vcl | 340 | 0.670760 | 0.619968 | 0.050792 [0.005024, 0.096885] | yes |
| series | gc | 0 | — | — | — | — |
| series | t3 | 0 | — | — | — | — |
| series | collegiate | 0 | — | — | — | — |
| series | offseason | 59 | 0.732169 | 0.702587 | 0.029583 [-0.066532, 0.128314] | no |
| series | international=1 | 41 | 0.652101 | 0.653397 | -0.001295 [-0.080435, 0.084279] | no |
| series | international=0 | 636 | 0.683331 | 0.631941 | 0.051390 [0.020219, 0.085848] | yes |
| map | all | 1049 | 0.672407 | 0.668225 | 0.004183 [-0.018037, 0.025194] | no |
| map | vct | 461 | 0.676624 | 0.665762 | 0.010863 [-0.014820, 0.036752] | no |
| map | vcl | 490 | 0.665758 | 0.668365 | -0.002606 [-0.041290, 0.033309] | no |
| map | gc | 0 | — | — | — | — |
| map | t3 | 0 | — | — | — | — |
| map | collegiate | 0 | — | — | — | — |
| map | offseason | 98 | 0.685814 | 0.679111 | 0.006703 [-0.032035, 0.047846] | no |
| map | international=1 | 59 | 0.670687 | 0.649653 | 0.021035 [-0.020498, 0.063823] | no |
| map | international=0 | 990 | 0.672510 | 0.669332 | 0.003178 [-0.019765, 0.024721] | no |

#### Full-Kelly returns

| Kind | Slice | Bets | Matches | Mean edge | Flat ROI [95% interval] | Kelly, LoL caps ($50 start) | Multiple | Max drawdown | Largest stake |
|---|---|---:|---:|---:|---|---:|---:|---:|---:|
| series | all | 546 | 546 | 0.1156 | 3.08% [-7.24%, 14.01%] | $3.34 | 0.067× | 97.82% | $12.10 |
| series | vct | 231 | 231 | 0.1098 | 6.56% [-7.78%, 23.35%] | $27.43 | 0.549× | 73.26% | $10.26 |
| series | vcl | 264 | 264 | 0.1222 | 0.20% [-15.43%, 16.55%] | $8.47 | 0.169× | 86.61% | $5.00 |
| series | gc | 0 | 0 | — | — | $50.00 | 1.000× | 0.00% | $0.00 |
| series | t3 | 0 | 0 | — | — | $50.00 | 1.000× | 0.00% | $0.00 |
| series | collegiate | 0 | 0 | — | — | $50.00 | 1.000× | 0.00% | $0.00 |
| series | offseason | 51 | 51 | 0.1077 | 2.18% [-24.27%, 28.56%] | $39.18 | 0.784× | 54.23% | $7.83 |
| series | international=1 | 35 | 35 | 0.0906 | 3.05% [-28.48%, 32.91%] | $52.32 | 1.046× | 27.88% | $7.26 |
| series | international=0 | 511 | 511 | 0.1173 | 3.08% [-7.93%, 14.65%] | $3.21 | 0.064× | 97.05% | $8.59 |
| map | all | 740 | 393 | 0.0805 | 14.04% [-1.29%, 32.87%] | $1425.04 | 28.501× | 62.93% | $250.00 |
| map | vct | 324 | 167 | 0.0754 | 8.33% [-7.19%, 26.87%] | $112.92 | 2.258× | 35.75% | $10.71 |
| map | vcl | 343 | 190 | 0.0914 | 23.59% [-3.27%, 56.63%] | $426.75 | 8.535× | 73.56% | $111.61 |
| map | gc | 0 | 0 | — | — | $50.00 | 1.000× | 0.00% | $0.00 |
| map | t3 | 0 | 0 | — | — | $50.00 | 1.000× | 0.00% | $0.00 |
| map | collegiate | 0 | 0 | — | — | $50.00 | 1.000× | 0.00% | $0.00 |
| map | offseason | 73 | 36 | 0.0517 | -5.51% [-27.10%, 15.45%] | $36.74 | 0.735× | 36.38% | $3.71 |
| map | international=1 | 40 | 22 | 0.0619 | -7.46% [-36.56%, 18.35%] | $41.56 | 0.831× | 22.50% | $4.86 |
| map | international=0 | 700 | 371 | 0.0816 | 15.27% [-0.33%, 35.29%] | $2158.48 | 43.170× | 63.04% | $250.00 |
| series+map | all | 1286 | 572 | 0.0954 | 9.38% [-1.19%, 22.06%] | $1256.49 | 25.130× | 74.73% | $250.00 |

#### Monthly market blend fits

UTC monthly fits use earlier rows of the same kind from 2025-09-01, excluding holdout; minimum 100 rows. logit(p_blend) = a·logit(mid) + b·(logit(p_model) − logit(mid)); inputs clipped to [0.01, 0.99], no intercept, ridge 1e-6. Unfitted rows use mid unchanged; excluded from blended tables: 240 rows. Rating parameters remain selected on the tuning window.

| Month | Kind | n | a | b | Status |
|---|---|---:|---:|---:|---|
| 2026-01 | series | 0 | 1.000000 | 0.000000 | unfitted |
| 2026-02 | series | 21 | 1.000000 | 0.000000 | unfitted |
| 2026-02 | map | 0 | 1.000000 | 0.000000 | unfitted |
| 2026-03 | series | 72 | 1.000000 | 0.000000 | unfitted |
| 2026-03 | map | 48 | 1.000000 | 0.000000 | unfitted |
| 2026-04 | series | 136 | 1.070027 | 0.306567 | fitted |
| 2026-04 | map | 104 | 1.470112 | 0.274971 | fitted |
| 2026-05 | series | 357 | 0.888598 | 0.231205 | fitted |
| 2026-05 | map | 456 | 0.890661 | 0.607109 | fitted |
| 2026-06 | series | 556 | 0.830479 | 0.140748 | fitted |
| 2026-06 | map | 833 | 0.765395 | 0.441872 | fitted |

#### Log loss vs Kalshi (blended)

| Kind | Slice | Rows | Model log loss | Kalshi log loss | Difference [95% interval] | Significant |
|---|---|---:|---:|---:|---|---|
| series | all | 541 | 0.635906 | 0.634347 | 0.001559 [-0.007126, 0.010273] | no |
| series | vct | 201 | 0.645766 | 0.644147 | 0.001619 [-0.012574, 0.016887] | no |
| series | vcl | 291 | 0.621718 | 0.621829 | -0.000110 [-0.011660, 0.012230] | no |
| series | gc | 0 | — | — | — | — |
| series | t3 | 0 | — | — | — | — |
| series | collegiate | 0 | — | — | — | — |
| series | offseason | 49 | 0.679719 | 0.668490 | 0.011229 [-0.007334, 0.029846] | no |
| series | international=1 | 24 | 0.679554 | 0.682705 | -0.003152 [-0.033635, 0.020372] | no |
| series | international=0 | 517 | 0.633880 | 0.632102 | 0.001778 [-0.007333, 0.011172] | no |
| map | all | 945 | 0.682936 | 0.673192 | 0.009745 [0.000401, 0.018869] | yes |
| map | vct | 392 | 0.673397 | 0.667249 | 0.006148 [-0.009041, 0.021063] | no |
| map | vcl | 456 | 0.691378 | 0.676303 | 0.015075 [0.001426, 0.028855] | yes |
| map | gc | 0 | — | — | — | — |
| map | t3 | 0 | — | — | — | — |
| map | collegiate | 0 | — | — | — | — |
| map | offseason | 97 | 0.681803 | 0.682581 | -0.000778 [-0.021994, 0.020549] | no |
| map | international=1 | 50 | 0.659440 | 0.651359 | 0.008082 [-0.011910, 0.027218] | no |
| map | international=0 | 895 | 0.684249 | 0.674412 | 0.009837 [-0.000098, 0.019373] | no |

#### Full-Kelly returns (blended)

| Kind | Slice | Bets | Matches | Mean edge | Flat ROI [95% interval] | Kelly, LoL caps ($50 start) | Multiple | Max drawdown | Largest stake |
|---|---|---:|---:|---:|---|---:|---:|---:|---:|
| series | all | 188 | 188 | 0.0264 | 6.27% [-13.36%, 27.13%] | $24.91 | 0.498× | 67.44% | $6.48 |
| series | vct | 74 | 74 | 0.0330 | 3.06% [-23.06%, 33.70%] | $22.28 | 0.446× | 61.86% | $5.07 |
| series | vcl | 103 | 103 | 0.0227 | 16.17% [-11.58%, 46.50%] | $68.43 | 1.369× | 19.45% | $8.01 |
| series | gc | 0 | 0 | — | — | $50.00 | 1.000× | 0.00% | $0.00 |
| series | t3 | 0 | 0 | — | — | $50.00 | 1.000× | 0.00% | $0.00 |
| series | collegiate | 0 | 0 | — | — | $50.00 | 1.000× | 0.00% | $0.00 |
| series | offseason | 11 | 11 | 0.0157 | -64.81% [-100.00%, -14.03%] | $42.17 | 0.843× | 20.41% | $3.88 |
| series | international=1 | 5 | 5 | 0.0148 | 70.09% [-100.00%, 269.32%] | $55.08 | 1.102× | 4.37% | $1.72 |
| series | international=0 | 183 | 183 | 0.0267 | 4.52% [-14.58%, 24.07%] | $22.62 | 0.452× | 67.08% | $6.48 |
| map | all | 501 | 276 | 0.0360 | -4.34% [-12.61%, 3.88%] | $7.41 | 0.148× | 87.70% | $5.65 |
| map | vct | 224 | 117 | 0.0372 | -3.12% [-15.94%, 8.51%] | $28.68 | 0.574× | 58.03% | $5.13 |
| map | vcl | 239 | 138 | 0.0358 | -5.03% [-16.65%, 6.73%] | $14.00 | 0.280× | 77.81% | $5.92 |
| map | gc | 0 | 0 | — | — | $50.00 | 1.000× | 0.00% | $0.00 |
| map | t3 | 0 | 0 | — | — | $50.00 | 1.000× | 0.00% | $0.00 |
| map | collegiate | 0 | 0 | — | — | $50.00 | 1.000× | 0.00% | $0.00 |
| map | offseason | 38 | 21 | 0.0298 | -7.11% [-35.62%, 21.91%] | $46.07 | 0.921× | 11.76% | $2.69 |
| map | international=1 | 19 | 10 | 0.0261 | -22.56% [-63.70%, 23.81%] | $47.70 | 0.954× | 13.42% | $2.83 |
| map | international=0 | 482 | 266 | 0.0364 | -3.62% [-12.33%, 4.76%] | $7.77 | 0.155× | 87.10% | $5.65 |
| series+map | all | 689 | 322 | 0.0334 | -1.44% [-10.17%, 8.21%] | $7.59 | 0.152× | 86.26% | $5.05 |

#### Monthly breakdown

All metrics use identical linked rows within each kind/month. Unfitted blend months show —; counts include all rows.

| Kind | Month | Rows | Model log loss | Blended log loss | Kalshi log loss | Raw flat ROI (bets) | Blended flat ROI (bets) |
|---|---|---:|---:|---:|---:|---|---|
| map | 2026-02 | 48 | 0.711428 | — | 0.690786 | -1.07% (33) | — |
| map | 2026-03 | 56 | 0.621135 | — | 0.565065 | -17.96% (44) | — |
| map | 2026-04 | 352 | 0.655668 | 0.703755 | 0.690793 | 51.33% (240) | -7.18% (209) |
| map | 2026-05 | 377 | 0.705352 | 0.690499 | 0.687018 | 1.02% (278) | 2.62% (198) |
| map | 2026-06 | 216 | 0.646807 | 0.635811 | 0.620377 | -9.59% (145) | -12.66% (94) |
| series | 2026-01 | 21 | 0.687937 | — | 0.661069 | 12.62% (20) | — |
| series | 2026-02 | 51 | 0.676635 | — | 0.694525 | 17.64% (40) | — |
| series | 2026-03 | 64 | 0.666708 | — | 0.565917 | -10.55% (55) | — |
| series | 2026-04 | 221 | 0.666803 | 0.626961 | 0.627690 | 11.55% (173) | 13.15% (84) |
| series | 2026-05 | 199 | 0.735131 | 0.666466 | 0.663719 | 0.08% (165) | -7.60% (70) |
| series | 2026-06 | 121 | 0.628559 | 0.601985 | 0.598199 | -7.64% (93) | 17.82% (34) |

### team_elo+regional_form: Kalshi comparison and returns

regional_form: regional: rows=327, ridge=4, s=0.581887, effects: Americas=0.186351, EMEA=0.0249164, Pacific=0.103968, China=-0.315235; form: rows=7863, H=20, w=2.60313

#### Log loss vs Kalshi

| Kind | Slice | Rows | Model log loss | Kalshi log loss | Difference [95% interval] | Significant |
|---|---|---:|---:|---:|---|---|
| series | all | 677 | 0.680243 | 0.633240 | 0.047003 [0.016682, 0.079447] | yes |
| series | vct | 278 | 0.680870 | 0.634755 | 0.046115 [0.002589, 0.094665] | yes |
| series | vcl | 340 | 0.670718 | 0.619968 | 0.050750 [0.005010, 0.096855] | yes |
| series | gc | 0 | — | — | — | — |
| series | t3 | 0 | — | — | — | — |
| series | collegiate | 0 | — | — | — | — |
| series | offseason | 59 | 0.732177 | 0.702587 | 0.029590 [-0.066480, 0.128306] | no |
| series | international=1 | 41 | 0.632805 | 0.653397 | -0.020592 [-0.080123, 0.043853] | no |
| series | international=0 | 636 | 0.683301 | 0.631941 | 0.051360 [0.020195, 0.085814] | yes |
| map | all | 1049 | 0.671117 | 0.668225 | 0.002892 [-0.019242, 0.023703] | no |
| map | vct | 461 | 0.673689 | 0.665762 | 0.007927 [-0.017502, 0.033811] | no |
| map | vcl | 490 | 0.665761 | 0.668365 | -0.002604 [-0.041308, 0.033311] | no |
| map | gc | 0 | — | — | — | — |
| map | t3 | 0 | — | — | — | — |
| map | collegiate | 0 | — | — | — | — |
| map | offseason | 98 | 0.685800 | 0.679111 | 0.006689 [-0.032038, 0.047771] | no |
| map | international=1 | 59 | 0.647820 | 0.649653 | -0.001833 [-0.035749, 0.032469] | no |
| map | international=0 | 990 | 0.672505 | 0.669332 | 0.003174 [-0.019759, 0.024713] | no |

#### Full-Kelly returns

| Kind | Slice | Bets | Matches | Mean edge | Flat ROI [95% interval] | Kelly, LoL caps ($50 start) | Multiple | Max drawdown | Largest stake |
|---|---|---:|---:|---:|---|---:|---:|---:|---:|
| series | all | 545 | 545 | 0.1144 | 3.46% [-7.07%, 14.27%] | $3.80 | 0.076× | 97.53% | $12.17 |
| series | vct | 229 | 229 | 0.1076 | 7.22% [-7.23%, 22.77%] | $31.20 | 0.624× | 77.89% | $10.41 |
| series | vcl | 265 | 265 | 0.1216 | 0.45% [-15.39%, 17.92%] | $8.42 | 0.168× | 86.69% | $5.00 |
| series | gc | 0 | 0 | — | — | $50.00 | 1.000× | 0.00% | $0.00 |
| series | t3 | 0 | 0 | — | — | $50.00 | 1.000× | 0.00% | $0.00 |
| series | collegiate | 0 | 0 | — | — | $50.00 | 1.000× | 0.00% | $0.00 |
| series | offseason | 51 | 51 | 0.1076 | 2.18% [-24.27%, 28.56%] | $39.11 | 0.782× | 54.28% | $7.82 |
| series | international=1 | 33 | 33 | 0.0746 | 7.41% [-22.01%, 36.97%] | $59.81 | 1.196× | 39.95% | $7.35 |
| series | international=0 | 512 | 512 | 0.1170 | 3.20% [-7.18%, 14.55%] | $3.17 | 0.063× | 97.07% | $8.54 |
| map | all | 744 | 394 | 0.0792 | 14.04% [-0.89%, 31.93%] | $2358.82 | 47.176× | 61.34% | $250.00 |
| map | vct | 328 | 168 | 0.0726 | 8.39% [-6.18%, 27.57%] | $121.18 | 2.424× | 31.02% | $11.22 |
| map | vcl | 343 | 190 | 0.0914 | 23.59% [-3.27%, 56.63%] | $426.82 | 8.536× | 73.53% | $111.49 |
| map | gc | 0 | 0 | — | — | $50.00 | 1.000× | 0.00% | $0.00 |
| map | t3 | 0 | 0 | — | — | $50.00 | 1.000× | 0.00% | $0.00 |
| map | collegiate | 0 | 0 | — | — | $50.00 | 1.000× | 0.00% | $0.00 |
| map | offseason | 73 | 36 | 0.0516 | -5.51% [-27.10%, 15.45%] | $36.75 | 0.735× | 36.43% | $3.72 |
| map | international=1 | 44 | 23 | 0.0426 | -5.51% [-31.30%, 18.84%] | $44.56 | 0.891× | 18.42% | $3.93 |
| map | international=0 | 700 | 371 | 0.0815 | 15.27% [-0.33%, 35.29%] | $2185.35 | 43.707× | 63.13% | $250.00 |
| series+map | all | 1289 | 570 | 0.0941 | 9.56% [-0.88%, 21.50%] | $984.88 | 19.698× | 75.09% | $250.00 |

#### Monthly market blend fits

UTC monthly fits use earlier rows of the same kind from 2025-09-01, excluding holdout; minimum 100 rows. logit(p_blend) = a·logit(mid) + b·(logit(p_model) − logit(mid)); inputs clipped to [0.01, 0.99], no intercept, ridge 1e-6. Unfitted rows use mid unchanged; excluded from blended tables: 240 rows. Rating parameters remain selected on the tuning window.

| Month | Kind | n | a | b | Status |
|---|---|---:|---:|---:|---|
| 2026-01 | series | 0 | 1.000000 | 0.000000 | unfitted |
| 2026-02 | series | 21 | 1.000000 | 0.000000 | unfitted |
| 2026-02 | map | 0 | 1.000000 | 0.000000 | unfitted |
| 2026-03 | series | 72 | 1.000000 | 0.000000 | unfitted |
| 2026-03 | map | 48 | 1.000000 | 0.000000 | unfitted |
| 2026-04 | series | 136 | 1.068688 | 0.297550 | fitted |
| 2026-04 | map | 104 | 1.535561 | 0.379256 | fitted |
| 2026-05 | series | 357 | 0.888334 | 0.225927 | fitted |
| 2026-05 | map | 456 | 0.899307 | 0.619889 | fitted |
| 2026-06 | series | 556 | 0.830243 | 0.136090 | fitted |
| 2026-06 | map | 833 | 0.769204 | 0.448645 | fitted |

#### Log loss vs Kalshi (blended)

| Kind | Slice | Rows | Model log loss | Kalshi log loss | Difference [95% interval] | Significant |
|---|---|---:|---:|---:|---|---|
| series | all | 541 | 0.635607 | 0.634347 | 0.001260 [-0.007263, 0.009876] | no |
| series | vct | 201 | 0.645044 | 0.644147 | 0.000897 [-0.012871, 0.015670] | no |
| series | vcl | 291 | 0.621717 | 0.621829 | -0.000112 [-0.011355, 0.011835] | no |
| series | gc | 0 | — | — | — | — |
| series | t3 | 0 | — | — | — | — |
| series | collegiate | 0 | — | — | — | — |
| series | offseason | 49 | 0.679392 | 0.668490 | 0.010902 [-0.007279, 0.029004] | no |
| series | international=1 | 24 | 0.675400 | 0.682705 | -0.007305 [-0.033394, 0.013533] | no |
| series | international=0 | 517 | 0.633760 | 0.632102 | 0.001658 [-0.007183, 0.010824] | no |
| map | all | 945 | 0.682259 | 0.673192 | 0.009067 [-0.000854, 0.018854] | no |
| map | vct | 392 | 0.673908 | 0.667249 | 0.006659 [-0.010120, 0.023197] | no |
| map | vcl | 456 | 0.689479 | 0.676303 | 0.013176 [-0.001086, 0.027955] | no |
| map | gc | 0 | — | — | — | — |
| map | t3 | 0 | — | — | — | — |
| map | collegiate | 0 | — | — | — | — |
| map | offseason | 97 | 0.682062 | 0.682581 | -0.000519 [-0.022278, 0.021551] | no |
| map | international=1 | 50 | 0.652685 | 0.651359 | 0.001327 [-0.013379, 0.015606] | no |
| map | international=0 | 895 | 0.683911 | 0.674412 | 0.009499 [-0.001508, 0.019706] | no |

#### Full-Kelly returns (blended)

| Kind | Slice | Bets | Matches | Mean edge | Flat ROI [95% interval] | Kelly, LoL caps ($50 start) | Multiple | Max drawdown | Largest stake |
|---|---|---:|---:|---:|---|---:|---:|---:|---:|
| series | all | 182 | 182 | 0.0256 | 8.39% [-12.06%, 28.96%] | $24.95 | 0.499× | 65.96% | $6.25 |
| series | vct | 72 | 72 | 0.0320 | 8.12% [-20.07%, 39.91%] | $22.60 | 0.452× | 61.43% | $5.09 |
| series | vcl | 100 | 100 | 0.0220 | 15.56% [-10.68%, 44.60%] | $66.33 | 1.327× | 19.35% | $7.79 |
| series | gc | 0 | 0 | — | — | $50.00 | 1.000× | 0.00% | $0.00 |
| series | t3 | 0 | 0 | — | — | $50.00 | 1.000× | 0.00% | $0.00 |
| series | collegiate | 0 | 0 | — | — | $50.00 | 1.000× | 0.00% | $0.00 |
| series | offseason | 10 | 10 | 0.0161 | -61.29% [-100.00%, -3.98%] | $42.84 | 0.857× | 18.97% | $3.76 |
| series | international=1 | 5 | 5 | 0.0113 | 129.75% [-40.34%, 299.84%] | $56.21 | 1.124× | 2.44% | $1.19 |
| series | international=0 | 177 | 177 | 0.0260 | 4.96% [-13.77%, 25.44%] | $22.20 | 0.444× | 66.53% | $6.25 |
| map | all | 520 | 282 | 0.0405 | 0.79% [-9.48%, 14.04%] | $7.84 | 0.157× | 89.06% | $6.73 |
| map | vct | 231 | 120 | 0.0439 | -1.59% [-13.76%, 10.81%] | $24.35 | 0.487× | 63.92% | $5.22 |
| map | vcl | 248 | 140 | 0.0391 | 4.08% [-14.30%, 29.33%] | $17.44 | 0.349× | 76.99% | $7.12 |
| map | gc | 0 | 0 | — | — | $50.00 | 1.000× | 0.00% | $0.00 |
| map | t3 | 0 | 0 | — | — | $50.00 | 1.000× | 0.00% | $0.00 |
| map | collegiate | 0 | 0 | — | — | $50.00 | 1.000× | 0.00% | $0.00 |
| map | offseason | 41 | 22 | 0.0292 | -5.72% [-33.91%, 22.76%] | $45.53 | 0.911× | 12.99% | $2.65 |
| map | international=1 | 14 | 7 | 0.0242 | 3.17% [-55.05%, 53.62%] | $46.39 | 0.928× | 10.00% | $2.68 |
| map | international=0 | 506 | 275 | 0.0409 | 0.72% [-10.26%, 13.80%] | $8.45 | 0.169× | 88.21% | $6.73 |
| series+map | all | 702 | 324 | 0.0366 | 2.76% [-8.12%, 14.75%] | $7.99 | 0.160× | 87.24% | $5.76 |

#### Monthly breakdown

All metrics use identical linked rows within each kind/month. Unfitted blend months show —; counts include all rows.

| Kind | Month | Rows | Model log loss | Blended log loss | Kalshi log loss | Raw flat ROI (bets) | Blended flat ROI (bets) |
|---|---|---:|---:|---:|---:|---|---|
| map | 2026-02 | 48 | 0.711430 | — | 0.690786 | -1.07% (33) | — |
| map | 2026-03 | 56 | 0.612804 | — | 0.565065 | -15.57% (45) | — |
| map | 2026-04 | 352 | 0.655667 | 0.702480 | 0.690793 | 51.33% (240) | 2.93% (227) |
| map | 2026-05 | 377 | 0.705326 | 0.690903 | 0.687018 | 1.02% (278) | 2.76% (203) |
| map | 2026-06 | 216 | 0.642748 | 0.634217 | 0.620377 | -9.62% (148) | -9.08% (90) |
| series | 2026-01 | 21 | 0.688014 | — | 0.661069 | 12.62% (20) | — |
| series | 2026-02 | 51 | 0.675544 | — | 0.694525 | 17.64% (40) | — |
| series | 2026-03 | 64 | 0.669794 | — | 0.565917 | -8.89% (54) | — |
| series | 2026-04 | 221 | 0.666759 | 0.626811 | 0.627690 | 11.55% (173) | 13.67% (81) |
| series | 2026-05 | 199 | 0.735075 | 0.666263 | 0.663719 | 0.08% (165) | -7.23% (67) |
| series | 2026-06 | 121 | 0.620849 | 0.601256 | 0.598199 | -6.50% (93) | 26.59% (34) |

### player_round_glicko+form: Kalshi comparison and returns

form: rows=7863, H=5, w=1.06027

#### Log loss vs Kalshi

| Kind | Slice | Rows | Model log loss | Kalshi log loss | Difference [95% interval] | Significant |
|---|---|---:|---:|---:|---|---|
| series | all | 677 | 0.634286 | 0.633240 | 0.001046 [-0.024850, 0.028285] | no |
| series | vct | 278 | 0.629947 | 0.634755 | -0.004808 [-0.039317, 0.028653] | no |
| series | vcl | 340 | 0.629678 | 0.619968 | 0.009711 [-0.032877, 0.055727] | no |
| series | gc | 0 | — | — | — | — |
| series | t3 | 0 | — | — | — | — |
| series | collegiate | 0 | — | — | — | — |
| series | offseason | 59 | 0.681279 | 0.702587 | -0.021308 [-0.090609, 0.049889] | no |
| series | international=1 | 41 | 0.596809 | 0.653397 | -0.056587 [-0.104754, -0.005588] | yes |
| series | international=0 | 636 | 0.636702 | 0.631941 | 0.004761 [-0.023734, 0.032262] | no |
| map | all | 1049 | 0.662908 | 0.668225 | -0.005317 [-0.027431, 0.013438] | no |
| map | vct | 461 | 0.664412 | 0.665762 | -0.001350 [-0.021259, 0.017124] | no |
| map | vcl | 490 | 0.656431 | 0.668365 | -0.011933 [-0.053764, 0.023866] | no |
| map | gc | 0 | — | — | — | — |
| map | t3 | 0 | — | — | — | — |
| map | collegiate | 0 | — | — | — | — |
| map | offseason | 98 | 0.688216 | 0.679111 | 0.009105 [-0.025649, 0.044032] | no |
| map | international=1 | 59 | 0.657272 | 0.649653 | 0.007619 [-0.017521, 0.032465] | no |
| map | international=0 | 990 | 0.663244 | 0.669332 | -0.006088 [-0.028649, 0.014259] | no |

#### Full-Kelly returns

| Kind | Slice | Bets | Matches | Mean edge | Flat ROI [95% interval] | Kelly, LoL caps ($50 start) | Multiple | Max drawdown | Largest stake |
|---|---|---:|---:|---:|---|---:|---:|---:|---:|
| series | all | 528 | 527 | 0.1011 | 10.20% [-1.26%, 22.19%] | $329.18 | 6.584× | 81.10% | $106.41 |
| series | vct | 214 | 214 | 0.0888 | 12.70% [-3.96%, 31.58%] | $105.32 | 2.106× | 66.16% | $12.01 |
| series | vcl | 280 | 279 | 0.1101 | 9.22% [-7.02%, 25.57%] | $151.03 | 3.021× | 61.68% | $33.83 |
| series | gc | 0 | 0 | — | — | $50.00 | 1.000× | 0.00% | $0.00 |
| series | t3 | 0 | 0 | — | — | $50.00 | 1.000× | 0.00% | $0.00 |
| series | collegiate | 0 | 0 | — | — | $50.00 | 1.000× | 0.00% | $0.00 |
| series | offseason | 34 | 34 | 0.1044 | 2.54% [-37.01%, 45.61%] | $47.60 | 0.952× | 59.26% | $9.55 |
| series | international=1 | 26 | 26 | 0.0631 | 39.48% [-2.57%, 86.73%] | $107.94 | 2.159× | 17.42% | $9.01 |
| series | international=0 | 502 | 501 | 0.1031 | 8.68% [-3.37%, 21.13%] | $152.91 | 3.058× | 83.41% | $79.13 |
| map | all | 668 | 361 | 0.0722 | 18.38% [2.56%, 38.40%] | $3608.51 | 72.170× | 57.19% | $250.00 |
| map | vct | 281 | 147 | 0.0574 | 13.69% [-3.72%, 36.04%] | $138.78 | 2.776× | 47.75% | $10.36 |
| map | vcl | 338 | 188 | 0.0888 | 26.68% [-1.11%, 62.66%] | $833.36 | 16.667× | 71.08% | $234.94 |
| map | gc | 0 | 0 | — | — | $50.00 | 1.000× | 0.00% | $0.00 |
| map | t3 | 0 | 0 | — | — | $50.00 | 1.000× | 0.00% | $0.00 |
| map | collegiate | 0 | 0 | — | — | $50.00 | 1.000× | 0.00% | $0.00 |
| map | offseason | 49 | 26 | 0.0423 | -12.01% [-43.42%, 21.62%] | $42.82 | 0.856× | 30.06% | $3.15 |
| map | international=1 | 30 | 16 | 0.0457 | -10.61% [-44.19%, 19.13%] | $39.89 | 0.798× | 26.17% | $5.00 |
| map | international=0 | 638 | 345 | 0.0734 | 19.74% [2.33%, 40.19%] | $4482.11 | 89.642× | 49.35% | $250.00 |
| series+map | all | 1196 | 550 | 0.0850 | 14.77% [3.33%, 27.14%] | $6372.54 | 127.451× | 50.29% | $250.00 |

#### Monthly market blend fits

UTC monthly fits use earlier rows of the same kind from 2025-09-01, excluding holdout; minimum 100 rows. logit(p_blend) = a·logit(mid) + b·(logit(p_model) − logit(mid)); inputs clipped to [0.01, 0.99], no intercept, ridge 1e-6. Unfitted rows use mid unchanged; excluded from blended tables: 240 rows. Rating parameters remain selected on the tuning window.

| Month | Kind | n | a | b | Status |
|---|---|---:|---:|---:|---|
| 2026-01 | series | 0 | 1.000000 | 0.000000 | unfitted |
| 2026-02 | series | 21 | 1.000000 | 0.000000 | unfitted |
| 2026-02 | map | 0 | 1.000000 | 0.000000 | unfitted |
| 2026-03 | series | 72 | 1.000000 | 0.000000 | unfitted |
| 2026-03 | map | 48 | 1.000000 | 0.000000 | unfitted |
| 2026-04 | series | 136 | 1.343607 | 0.666800 | fitted |
| 2026-04 | map | 104 | 1.524516 | 0.358905 | fitted |
| 2026-05 | series | 357 | 1.046637 | 0.514593 | fitted |
| 2026-05 | map | 456 | 1.120494 | 0.860451 | fitted |
| 2026-06 | series | 556 | 0.983552 | 0.490796 | fitted |
| 2026-06 | map | 833 | 0.958734 | 0.686880 | fitted |

#### Log loss vs Kalshi (blended)

| Kind | Slice | Rows | Model log loss | Kalshi log loss | Difference [95% interval] | Significant |
|---|---|---:|---:|---:|---|---|
| series | all | 541 | 0.627301 | 0.634347 | -0.007046 [-0.023229, 0.009836] | no |
| series | vct | 201 | 0.640688 | 0.644147 | -0.003459 [-0.025501, 0.020327] | no |
| series | vcl | 291 | 0.608838 | 0.621829 | -0.012990 [-0.037002, 0.014287] | no |
| series | gc | 0 | — | — | — | — |
| series | t3 | 0 | — | — | — | — |
| series | collegiate | 0 | — | — | — | — |
| series | offseason | 49 | 0.682029 | 0.668490 | 0.013539 [-0.017140, 0.044637] | no |
| series | international=1 | 24 | 0.648268 | 0.682705 | -0.034438 [-0.072116, 0.001039] | no |
| series | international=0 | 517 | 0.626327 | 0.632102 | -0.005775 [-0.022106, 0.012060] | no |
| map | all | 945 | 0.680137 | 0.673192 | 0.006945 [-0.002050, 0.016469] | no |
| map | vct | 392 | 0.669208 | 0.667249 | 0.001959 [-0.011482, 0.014993] | no |
| map | vcl | 456 | 0.687276 | 0.676303 | 0.010973 [-0.003256, 0.025663] | no |
| map | gc | 0 | — | — | — | — |
| map | t3 | 0 | — | — | — | — |
| map | collegiate | 0 | — | — | — | — |
| map | offseason | 97 | 0.690744 | 0.682581 | 0.008163 [-0.021717, 0.039705] | no |
| map | international=1 | 50 | 0.652912 | 0.651359 | 0.001553 [-0.016716, 0.019308] | no |
| map | international=0 | 895 | 0.681658 | 0.674412 | 0.007246 [-0.003151, 0.016803] | no |

#### Full-Kelly returns (blended)

| Kind | Slice | Bets | Matches | Mean edge | Flat ROI [95% interval] | Kelly, LoL caps ($50 start) | Multiple | Max drawdown | Largest stake |
|---|---|---:|---:|---:|---|---:|---:|---:|---:|
| series | all | 319 | 319 | 0.0486 | 10.05% [-3.76%, 24.81%] | $102.97 | 2.059× | 64.44% | $14.48 |
| series | vct | 121 | 121 | 0.0464 | 6.46% [-11.61%, 26.49%] | $26.02 | 0.520× | 69.75% | $5.72 |
| series | vcl | 174 | 174 | 0.0530 | 17.40% [-2.31%, 37.09%] | $239.41 | 4.788× | 32.55% | $25.83 |
| series | gc | 0 | 0 | — | — | $50.00 | 1.000× | 0.00% | $0.00 |
| series | t3 | 0 | 0 | — | — | $50.00 | 1.000× | 0.00% | $0.00 |
| series | collegiate | 0 | 0 | — | — | $50.00 | 1.000× | 0.00% | $0.00 |
| series | offseason | 24 | 24 | 0.0278 | -25.18% [-68.04%, 27.37%] | $42.83 | 0.857× | 22.30% | $4.20 |
| series | international=1 | 10 | 10 | 0.0353 | 57.79% [-22.30%, 156.55%] | $70.67 | 1.413× | 6.04% | $6.22 |
| series | international=0 | 309 | 309 | 0.0491 | 8.50% [-5.03%, 22.64%] | $72.91 | 1.458× | 64.44% | $14.48 |
| map | all | 532 | 284 | 0.0375 | -5.19% [-13.13%, 2.81%] | $8.82 | 0.176× | 88.35% | $6.50 |
| map | vct | 223 | 115 | 0.0338 | -3.69% [-14.94%, 8.70%] | $34.33 | 0.687× | 46.79% | $5.59 |
| map | vcl | 263 | 146 | 0.0421 | -6.04% [-17.55%, 5.86%] | $15.89 | 0.318× | 78.57% | $6.37 |
| map | gc | 0 | 0 | — | — | $50.00 | 1.000× | 0.00% | $0.00 |
| map | t3 | 0 | 0 | — | — | $50.00 | 1.000× | 0.00% | $0.00 |
| map | collegiate | 0 | 0 | — | — | $50.00 | 1.000× | 0.00% | $0.00 |
| map | offseason | 46 | 23 | 0.0297 | -7.59% [-39.48%, 25.37%] | $39.85 | 0.797× | 28.24% | $2.78 |
| map | international=1 | 21 | 10 | 0.0313 | -24.65% [-69.66%, 17.96%] | $49.84 | 0.997× | 10.00% | $2.91 |
| map | international=0 | 511 | 274 | 0.0378 | -4.39% [-12.54%, 4.20%] | $8.85 | 0.177× | 88.31% | $6.50 |
| series+map | all | 851 | 377 | 0.0417 | 0.52% [-8.10%, 9.24%] | $14.93 | 0.299× | 89.89% | $10.02 |

#### Monthly breakdown

All metrics use identical linked rows within each kind/month. Unfitted blend months show —; counts include all rows.

| Kind | Month | Rows | Model log loss | Blended log loss | Kalshi log loss | Raw flat ROI (bets) | Blended flat ROI (bets) |
|---|---|---:|---:|---:|---:|---|---|
| map | 2026-02 | 48 | 0.710084 | — | 0.690786 | 1.33% (41) | — |
| map | 2026-03 | 56 | 0.616431 | — | 0.565065 | -19.12% (40) | — |
| map | 2026-04 | 352 | 0.644426 | 0.698208 | 0.690793 | 57.93% (234) | -3.98% (224) |
| map | 2026-05 | 377 | 0.688894 | 0.688112 | 0.687018 | 5.52% (204) | 0.17% (194) |
| map | 2026-06 | 216 | 0.649237 | 0.636768 | 0.620377 | -11.37% (149) | -16.68% (114) |
| series | 2026-01 | 21 | 0.564204 | — | 0.661069 | 26.73% (19) | — |
| series | 2026-02 | 51 | 0.677641 | — | 0.694525 | 15.60% (39) | — |
| series | 2026-03 | 64 | 0.613870 | — | 0.565917 | -2.98% (53) | — |
| series | 2026-04 | 221 | 0.630462 | 0.624589 | 0.627690 | 15.72% (172) | 15.39% (148) |
| series | 2026-05 | 199 | 0.661674 | 0.654442 | 0.663719 | 12.33% (150) | 2.88% (103) |
| series | 2026-06 | 121 | 0.600913 | 0.587615 | 0.598199 | -1.31% (95) | 9.27% (68) |

### player_round_glicko+regional_form: Kalshi comparison and returns

regional_form: regional: rows=327, ridge=4, s=0.87556, effects: Americas=0.160568, EMEA=0.0715532, Pacific=0.0495464, China=-0.281668; form: rows=7863, H=5, w=1.04267

#### Log loss vs Kalshi

| Kind | Slice | Rows | Model log loss | Kalshi log loss | Difference [95% interval] | Significant |
|---|---|---:|---:|---:|---|---|
| series | all | 677 | 0.634562 | 0.633240 | 0.001322 [-0.024781, 0.028792] | no |
| series | vct | 278 | 0.630669 | 0.634755 | -0.004086 [-0.039646, 0.030092] | no |
| series | vcl | 340 | 0.629636 | 0.619968 | 0.009668 [-0.032856, 0.055661] | no |
| series | gc | 0 | — | — | — | — |
| series | t3 | 0 | — | — | — | — |
| series | collegiate | 0 | — | — | — | — |
| series | offseason | 59 | 0.681292 | 0.702587 | -0.021295 [-0.090342, 0.049866] | no |
| series | international=1 | 41 | 0.602043 | 0.653397 | -0.051354 [-0.102167, 0.003514] | no |
| series | international=0 | 636 | 0.636658 | 0.631941 | 0.004718 [-0.023797, 0.032163] | no |
| map | all | 1049 | 0.662185 | 0.668225 | -0.006039 [-0.028333, 0.012483] | no |
| map | vct | 461 | 0.662771 | 0.665762 | -0.002990 [-0.023120, 0.015143] | no |
| map | vcl | 490 | 0.656436 | 0.668365 | -0.011929 [-0.053812, 0.023848] | no |
| map | gc | 0 | — | — | — | — |
| map | t3 | 0 | — | — | — | — |
| map | collegiate | 0 | — | — | — | — |
| map | offseason | 98 | 0.688174 | 0.679111 | 0.009063 [-0.025620, 0.043972] | no |
| map | international=1 | 59 | 0.644551 | 0.649653 | -0.005102 [-0.038306, 0.025778] | no |
| map | international=0 | 990 | 0.663236 | 0.669332 | -0.006095 [-0.028626, 0.014264] | no |

#### Full-Kelly returns

| Kind | Slice | Bets | Matches | Mean edge | Flat ROI [95% interval] | Kelly, LoL caps ($50 start) | Multiple | Max drawdown | Largest stake |
|---|---|---:|---:|---:|---|---:|---:|---:|---:|
| series | all | 530 | 529 | 0.1009 | 9.20% [-1.92%, 21.45%] | $257.01 | 5.140× | 83.46% | $126.52 |
| series | vct | 216 | 216 | 0.0886 | 10.23% [-6.40%, 27.84%] | $82.39 | 1.648× | 66.35% | $14.30 |
| series | vcl | 280 | 279 | 0.1099 | 9.22% [-7.02%, 25.57%] | $150.92 | 3.018× | 61.67% | $33.79 |
| series | gc | 0 | 0 | — | — | $50.00 | 1.000× | 0.00% | $0.00 |
| series | t3 | 0 | 0 | — | — | $50.00 | 1.000× | 0.00% | $0.00 |
| series | collegiate | 0 | 0 | — | — | $50.00 | 1.000× | 0.00% | $0.00 |
| series | offseason | 34 | 34 | 0.1041 | 2.54% [-37.01%, 45.61%] | $47.65 | 0.953× | 59.26% | $9.55 |
| series | international=1 | 28 | 28 | 0.0645 | 18.53% [-16.44%, 52.03%] | $85.42 | 1.708× | 25.91% | $8.49 |
| series | international=0 | 502 | 501 | 0.1029 | 8.68% [-3.37%, 21.13%] | $150.86 | 3.017× | 83.47% | $78.31 |
| map | all | 666 | 361 | 0.0728 | 18.45% [1.30%, 38.48%] | $4572.62 | 91.452× | 50.15% | $250.00 |
| map | vct | 282 | 148 | 0.0584 | 13.92% [-3.78%, 36.48%] | $177.54 | 3.551× | 39.00% | $12.03 |
| map | vcl | 335 | 187 | 0.0894 | 26.72% [-1.68%, 62.30%] | $832.90 | 16.658× | 70.99% | $234.25 |
| map | gc | 0 | 0 | — | — | $50.00 | 1.000× | 0.00% | $0.00 |
| map | t3 | 0 | 0 | — | — | $50.00 | 1.000× | 0.00% | $0.00 |
| map | collegiate | 0 | 0 | — | — | $50.00 | 1.000× | 0.00% | $0.00 |
| map | offseason | 49 | 26 | 0.0421 | -12.01% [-43.42%, 21.62%] | $42.91 | 0.858× | 29.94% | $3.15 |
| map | international=1 | 32 | 18 | 0.0540 | -5.08% [-28.21%, 19.96%] | $51.06 | 1.021× | 5.74% | $3.05 |
| map | international=0 | 634 | 343 | 0.0737 | 19.64% [1.47%, 40.79%] | $4485.63 | 89.713× | 49.54% | $250.00 |
| series+map | all | 1196 | 551 | 0.0852 | 14.35% [2.99%, 27.60%] | $7010.15 | 140.203× | 47.89% | $250.00 |

#### Monthly market blend fits

UTC monthly fits use earlier rows of the same kind from 2025-09-01, excluding holdout; minimum 100 rows. logit(p_blend) = a·logit(mid) + b·(logit(p_model) − logit(mid)); inputs clipped to [0.01, 0.99], no intercept, ridge 1e-6. Unfitted rows use mid unchanged; excluded from blended tables: 240 rows. Rating parameters remain selected on the tuning window.

| Month | Kind | n | a | b | Status |
|---|---|---:|---:|---:|---|
| 2026-01 | series | 0 | 1.000000 | 0.000000 | unfitted |
| 2026-02 | series | 21 | 1.000000 | 0.000000 | unfitted |
| 2026-02 | map | 0 | 1.000000 | 0.000000 | unfitted |
| 2026-03 | series | 72 | 1.000000 | 0.000000 | unfitted |
| 2026-03 | map | 48 | 1.000000 | 0.000000 | unfitted |
| 2026-04 | series | 136 | 1.316457 | 0.649676 | fitted |
| 2026-04 | map | 104 | 1.566358 | 0.426027 | fitted |
| 2026-05 | series | 357 | 1.041693 | 0.513270 | fitted |
| 2026-05 | map | 456 | 1.129041 | 0.871873 | fitted |
| 2026-06 | series | 556 | 0.980757 | 0.491060 | fitted |
| 2026-06 | map | 833 | 0.963804 | 0.694499 | fitted |

#### Log loss vs Kalshi (blended)

| Kind | Slice | Rows | Model log loss | Kalshi log loss | Difference [95% interval] | Significant |
|---|---|---:|---:|---:|---|---|
| series | all | 541 | 0.626911 | 0.634347 | -0.007436 [-0.023293, 0.009304] | no |
| series | vct | 201 | 0.640380 | 0.644147 | -0.003767 [-0.025411, 0.019059] | no |
| series | vcl | 291 | 0.608352 | 0.621829 | -0.013476 [-0.036823, 0.013415] | no |
| series | gc | 0 | — | — | — | — |
| series | t3 | 0 | — | — | — | — |
| series | collegiate | 0 | — | — | — | — |
| series | offseason | 49 | 0.681876 | 0.668490 | 0.013386 [-0.017052, 0.044395] | no |
| series | international=1 | 24 | 0.651559 | 0.682705 | -0.031146 [-0.069591, 0.005960] | no |
| series | international=0 | 517 | 0.625767 | 0.632102 | -0.006335 [-0.022183, 0.011145] | no |
| map | all | 945 | 0.679112 | 0.673192 | 0.005920 [-0.003476, 0.016009] | no |
| map | vct | 392 | 0.668578 | 0.667249 | 0.001329 [-0.012975, 0.015202] | no |
| map | vcl | 456 | 0.685648 | 0.676303 | 0.009344 [-0.005169, 0.024352] | no |
| map | gc | 0 | — | — | — | — |
| map | t3 | 0 | — | — | — | — |
| map | collegiate | 0 | — | — | — | — |
| map | offseason | 97 | 0.690954 | 0.682581 | 0.008373 [-0.021705, 0.040146] | no |
| map | international=1 | 50 | 0.644807 | 0.651359 | -0.006551 [-0.032975, 0.015741] | no |
| map | international=0 | 895 | 0.681028 | 0.674412 | 0.006616 [-0.003768, 0.016566] | no |

#### Full-Kelly returns (blended)

| Kind | Slice | Bets | Matches | Mean edge | Flat ROI [95% interval] | Kelly, LoL caps ($50 start) | Multiple | Max drawdown | Largest stake |
|---|---|---:|---:|---:|---|---:|---:|---:|---:|
| series | all | 313 | 313 | 0.0485 | 8.07% [-4.97%, 22.43%] | $101.27 | 2.025× | 65.20% | $13.95 |
| series | vct | 120 | 120 | 0.0456 | 1.98% [-15.90%, 23.84%] | $25.69 | 0.514× | 68.51% | $5.60 |
| series | vcl | 169 | 169 | 0.0535 | 17.11% [-2.07%, 38.59%] | $235.73 | 4.715× | 33.39% | $25.48 |
| series | gc | 0 | 0 | — | — | $50.00 | 1.000× | 0.00% | $0.00 |
| series | t3 | 0 | 0 | — | — | $50.00 | 1.000× | 0.00% | $0.00 |
| series | collegiate | 0 | 0 | — | — | $50.00 | 1.000× | 0.00% | $0.00 |
| series | offseason | 24 | 24 | 0.0276 | -25.18% [-68.04%, 27.37%] | $43.28 | 0.866× | 21.48% | $4.24 |
| series | international=1 | 11 | 11 | 0.0424 | 8.95% [-45.99%, 63.80%] | $71.83 | 1.437× | 4.43% | $5.84 |
| series | international=0 | 302 | 302 | 0.0487 | 8.04% [-6.04%, 22.87%] | $70.55 | 1.411× | 65.20% | $13.95 |
| map | all | 540 | 286 | 0.0403 | -0.23% [-10.22%, 11.91%] | $8.72 | 0.174× | 89.35% | $7.03 |
| map | vct | 223 | 114 | 0.0386 | -2.66% [-13.28%, 8.26%] | $31.13 | 0.623× | 51.79% | $5.60 |
| map | vcl | 271 | 149 | 0.0433 | 3.02% [-14.05%, 26.58%] | $17.33 | 0.347× | 79.18% | $7.14 |
| map | gc | 0 | 0 | — | — | $50.00 | 1.000× | 0.00% | $0.00 |
| map | t3 | 0 | 0 | — | — | $50.00 | 1.000× | 0.00% | $0.00 |
| map | collegiate | 0 | 0 | — | — | $50.00 | 1.000× | 0.00% | $0.00 |
| map | offseason | 46 | 23 | 0.0303 | -7.59% [-39.48%, 25.37%] | $39.63 | 0.793× | 28.79% | $2.74 |
| map | international=1 | 20 | 9 | 0.0452 | 3.62% [-17.54%, 27.11%] | $49.90 | 0.998× | 6.48% | $2.61 |
| map | international=0 | 520 | 277 | 0.0401 | -0.38% [-10.82%, 12.94%] | $8.74 | 0.175× | 89.33% | $7.03 |
| series+map | all | 853 | 374 | 0.0433 | 2.82% [-6.51%, 12.77%] | $14.55 | 0.291× | 90.80% | $10.90 |

#### Monthly breakdown

All metrics use identical linked rows within each kind/month. Unfitted blend months show —; counts include all rows.

| Kind | Month | Rows | Model log loss | Blended log loss | Kalshi log loss | Raw flat ROI (bets) | Blended flat ROI (bets) |
|---|---|---:|---:|---:|---:|---|---|
| map | 2026-02 | 48 | 0.710048 | — | 0.690786 | 1.33% (41) | — |
| map | 2026-03 | 56 | 0.612108 | — | 0.565065 | -17.16% (43) | — |
| map | 2026-04 | 352 | 0.644416 | 0.696342 | 0.690793 | 58.49% (231) | 5.97% (233) |
| map | 2026-05 | 377 | 0.688857 | 0.688320 | 0.687018 | 5.52% (204) | -1.03% (192) |
| map | 2026-06 | 216 | 0.646937 | 0.634960 | 0.620377 | -11.34% (147) | -11.47% (115) |
| series | 2026-01 | 21 | 0.564385 | — | 0.661069 | 26.73% (19) | — |
| series | 2026-02 | 51 | 0.672335 | — | 0.694525 | 16.03% (40) | — |
| series | 2026-03 | 64 | 0.616997 | — | 0.565917 | -2.26% (54) | — |
| series | 2026-04 | 221 | 0.630390 | 0.623272 | 0.627690 | 15.72% (172) | 15.75% (141) |
| series | 2026-05 | 199 | 0.661582 | 0.654333 | 0.663719 | 12.33% (150) | 1.49% (103) |
| series | 2026-06 | 121 | 0.603294 | 0.588459 | 0.598199 | -7.38% (95) | 2.19% (69) |

### player_round_glicko_rookie+form: Kalshi comparison and returns

form: rows=7863, H=5, w=1.41117

#### Log loss vs Kalshi

| Kind | Slice | Rows | Model log loss | Kalshi log loss | Difference [95% interval] | Significant |
|---|---|---:|---:|---:|---|---|
| series | all | 677 | 0.622447 | 0.633240 | -0.010793 [-0.035604, 0.014340] | no |
| series | vct | 278 | 0.623721 | 0.634755 | -0.011034 [-0.045012, 0.021420] | no |
| series | vcl | 340 | 0.612314 | 0.619968 | -0.007654 [-0.048415, 0.033164] | no |
| series | gc | 0 | — | — | — | — |
| series | t3 | 0 | — | — | — | — |
| series | collegiate | 0 | — | — | — | — |
| series | offseason | 59 | 0.674837 | 0.702587 | -0.027750 [-0.093287, 0.037660] | no |
| series | international=1 | 41 | 0.599132 | 0.653397 | -0.054264 [-0.103637, -0.005587] | yes |
| series | international=0 | 636 | 0.623950 | 0.631941 | -0.007991 [-0.035032, 0.018228] | no |
| map | all | 1049 | 0.657497 | 0.668225 | -0.010728 [-0.032512, 0.007605] | no |
| map | vct | 461 | 0.660396 | 0.665762 | -0.005365 [-0.024784, 0.011428] | no |
| map | vcl | 490 | 0.648904 | 0.668365 | -0.019461 [-0.060267, 0.015311] | no |
| map | gc | 0 | — | — | — | — |
| map | t3 | 0 | — | — | — | — |
| map | collegiate | 0 | — | — | — | — |
| map | offseason | 98 | 0.686819 | 0.679111 | 0.007709 [-0.028053, 0.041331] | no |
| map | international=1 | 59 | 0.657934 | 0.649653 | 0.008281 [-0.015834, 0.031845] | no |
| map | international=0 | 990 | 0.657471 | 0.669332 | -0.011861 [-0.034067, 0.007413] | no |

#### Full-Kelly returns

| Kind | Slice | Bets | Matches | Mean edge | Flat ROI [95% interval] | Kelly, LoL caps ($50 start) | Multiple | Max drawdown | Largest stake |
|---|---|---:|---:|---:|---|---:|---:|---:|---:|
| series | all | 502 | 501 | 0.1031 | 16.71% [4.71%, 29.27%] | $1207.87 | 24.157× | 76.95% | $241.39 |
| series | vct | 202 | 202 | 0.0859 | 16.66% [-1.81%, 36.76%] | $137.73 | 2.755× | 66.56% | $11.49 |
| series | vcl | 265 | 264 | 0.1172 | 15.91% [-1.22%, 32.84%] | $251.29 | 5.026× | 66.92% | $43.03 |
| series | gc | 0 | 0 | — | — | $50.00 | 1.000× | 0.00% | $0.00 |
| series | t3 | 0 | 0 | — | — | $50.00 | 1.000× | 0.00% | $0.00 |
| series | collegiate | 0 | 0 | — | — | $50.00 | 1.000× | 0.00% | $0.00 |
| series | offseason | 35 | 35 | 0.0961 | 23.07% [-19.85%, 68.64%] | $70.06 | 1.401× | 36.76% | $9.93 |
| series | international=1 | 30 | 30 | 0.0481 | 38.31% [-2.24%, 84.42%] | $105.21 | 2.104× | 21.90% | $8.78 |
| series | international=0 | 472 | 471 | 0.1066 | 15.34% [2.56%, 28.56%] | $587.56 | 11.751× | 76.95% | $111.10 |
| map | all | 639 | 342 | 0.0717 | 19.01% [1.45%, 40.49%] | $4158.03 | 83.161× | 53.83% | $250.00 |
| map | vct | 253 | 131 | 0.0569 | 12.05% [-6.74%, 37.30%] | $186.67 | 3.733× | 32.58% | $13.65 |
| map | vcl | 336 | 186 | 0.0864 | 29.04% [1.60%, 65.07%] | $1009.65 | 20.193× | 71.52% | $250.00 |
| map | gc | 0 | 0 | — | — | $50.00 | 1.000× | 0.00% | $0.00 |
| map | t3 | 0 | 0 | — | — | $50.00 | 1.000× | 0.00% | $0.00 |
| map | collegiate | 0 | 0 | — | — | $50.00 | 1.000× | 0.00% | $0.00 |
| map | offseason | 50 | 25 | 0.0472 | -13.20% [-45.56%, 22.50%] | $44.28 | 0.886× | 28.56% | $2.85 |
| map | international=1 | 28 | 14 | 0.0468 | -21.56% [-54.66%, 9.29%] | $36.74 | 0.735× | 31.47% | $4.51 |
| map | international=0 | 611 | 328 | 0.0728 | 20.86% [3.01%, 42.19%] | $5293.97 | 105.879× | 44.32% | $250.00 |
| series+map | all | 1141 | 525 | 0.0855 | 18.00% [5.50%, 31.58%] | $5242.95 | 104.859× | 68.31% | $250.00 |

#### Monthly market blend fits

UTC monthly fits use earlier rows of the same kind from 2025-09-01, excluding holdout; minimum 100 rows. logit(p_blend) = a·logit(mid) + b·(logit(p_model) − logit(mid)); inputs clipped to [0.01, 0.99], no intercept, ridge 1e-6. Unfitted rows use mid unchanged; excluded from blended tables: 240 rows. Rating parameters remain selected on the tuning window.

| Month | Kind | n | a | b | Status |
|---|---|---:|---:|---:|---|
| 2026-01 | series | 0 | 1.000000 | 0.000000 | unfitted |
| 2026-02 | series | 21 | 1.000000 | 0.000000 | unfitted |
| 2026-02 | map | 0 | 1.000000 | 0.000000 | unfitted |
| 2026-03 | series | 72 | 1.000000 | 0.000000 | unfitted |
| 2026-03 | map | 48 | 1.000000 | 0.000000 | unfitted |
| 2026-04 | series | 136 | 1.316023 | 0.657388 | fitted |
| 2026-04 | map | 104 | 1.640133 | 0.531617 | fitted |
| 2026-05 | series | 357 | 1.107204 | 0.634176 | fitted |
| 2026-05 | map | 456 | 1.246518 | 1.028414 | fitted |
| 2026-06 | series | 556 | 1.049256 | 0.644216 | fitted |
| 2026-06 | map | 833 | 1.064755 | 0.857683 | fitted |

#### Log loss vs Kalshi (blended)

| Kind | Slice | Rows | Model log loss | Kalshi log loss | Difference [95% interval] | Significant |
|---|---|---:|---:|---:|---|---|
| series | all | 541 | 0.617037 | 0.634347 | -0.017310 [-0.033260, -0.001740] | yes |
| series | vct | 201 | 0.631354 | 0.644147 | -0.012793 [-0.033218, 0.007859] | no |
| series | vcl | 291 | 0.597049 | 0.621829 | -0.024779 [-0.048903, 0.001536] | no |
| series | gc | 0 | — | — | — | — |
| series | t3 | 0 | — | — | — | — |
| series | collegiate | 0 | — | — | — | — |
| series | offseason | 49 | 0.677008 | 0.668490 | 0.008518 [-0.027121, 0.044897] | no |
| series | international=1 | 24 | 0.640573 | 0.682705 | -0.042132 [-0.088383, 0.001095] | no |
| series | international=0 | 517 | 0.615944 | 0.632102 | -0.016158 [-0.032231, 0.000343] | no |
| map | all | 945 | 0.676379 | 0.673192 | 0.003187 [-0.007337, 0.014804] | no |
| map | vct | 392 | 0.666578 | 0.667249 | -0.000672 [-0.014647, 0.013578] | no |
| map | vcl | 456 | 0.681620 | 0.676303 | 0.005317 [-0.011341, 0.021996] | no |
| map | gc | 0 | — | — | — | — |
| map | t3 | 0 | — | — | — | — |
| map | collegiate | 0 | — | — | — | — |
| map | offseason | 97 | 0.691355 | 0.682581 | 0.008774 [-0.025572, 0.044522] | no |
| map | international=1 | 50 | 0.652322 | 0.651359 | 0.000963 [-0.020260, 0.020938] | no |
| map | international=0 | 895 | 0.677723 | 0.674412 | 0.003312 [-0.008074, 0.014148] | no |

#### Full-Kelly returns (blended)

| Kind | Slice | Bets | Matches | Mean edge | Flat ROI [95% interval] | Kelly, LoL caps ($50 start) | Multiple | Max drawdown | Largest stake |
|---|---|---:|---:|---:|---|---:|---:|---:|---:|
| series | all | 323 | 323 | 0.0540 | 17.39% [4.00%, 31.18%] | $552.51 | 11.050× | 61.50% | $67.37 |
| series | vct | 115 | 115 | 0.0427 | 11.55% [-10.04%, 35.70%] | $51.19 | 1.024× | 68.42% | $5.58 |
| series | vcl | 187 | 187 | 0.0619 | 23.30% [4.97%, 43.13%] | $603.28 | 12.066× | 37.17% | $73.56 |
| series | gc | 0 | 0 | — | — | $50.00 | 1.000× | 0.00% | $0.00 |
| series | t3 | 0 | 0 | — | — | $50.00 | 1.000× | 0.00% | $0.00 |
| series | collegiate | 0 | 0 | — | — | $50.00 | 1.000× | 0.00% | $0.00 |
| series | offseason | 21 | 21 | 0.0458 | -3.28% [-52.57%, 48.79%] | $44.59 | 0.892× | 18.41% | $5.27 |
| series | international=1 | 10 | 10 | 0.0470 | 57.79% [-22.30%, 156.55%] | $74.87 | 1.497× | 8.46% | $6.20 |
| series | international=0 | 313 | 313 | 0.0542 | 16.10% [2.68%, 29.87%] | $370.05 | 7.401× | 61.50% | $45.12 |
| map | all | 578 | 307 | 0.0436 | 1.08% [-8.79%, 12.70%] | $24.77 | 0.495× | 68.12% | $7.10 |
| map | vct | 229 | 118 | 0.0396 | -1.04% [-11.54%, 9.36%] | $40.91 | 0.818× | 51.24% | $5.41 |
| map | vcl | 299 | 164 | 0.0471 | 3.51% [-12.17%, 25.07%] | $29.37 | 0.587× | 67.97% | $8.23 |
| map | gc | 0 | 0 | — | — | $50.00 | 1.000× | 0.00% | $0.00 |
| map | t3 | 0 | 0 | — | — | $50.00 | 1.000× | 0.00% | $0.00 |
| map | collegiate | 0 | 0 | — | — | $50.00 | 1.000× | 0.00% | $0.00 |
| map | offseason | 50 | 25 | 0.0406 | -3.72% [-33.92%, 30.69%] | $46.34 | 0.927× | 13.53% | $3.10 |
| map | international=1 | 22 | 10 | 0.0384 | -8.96% [-45.15%, 24.71%] | $49.71 | 0.994× | 8.03% | $2.60 |
| map | international=0 | 556 | 297 | 0.0438 | 1.48% [-8.67%, 14.01%] | $24.91 | 0.498× | 67.94% | $7.10 |
| series+map | all | 901 | 387 | 0.0473 | 6.93% [-2.12%, 17.58%] | $89.16 | 1.783× | 64.45% | $11.67 |

#### Monthly breakdown

All metrics use identical linked rows within each kind/month. Unfitted blend months show —; counts include all rows.

| Kind | Month | Rows | Model log loss | Blended log loss | Kalshi log loss | Raw flat ROI (bets) | Blended flat ROI (bets) |
|---|---|---:|---:|---:|---:|---|---|
| map | 2026-02 | 48 | 0.702999 | — | 0.690786 | 12.30% (37) | — |
| map | 2026-03 | 56 | 0.611610 | — | 0.565065 | -12.68% (40) | — |
| map | 2026-04 | 352 | 0.638544 | 0.691167 | 0.690793 | 63.22% (217) | 7.07% (235) |
| map | 2026-05 | 377 | 0.681816 | 0.684791 | 0.687018 | 4.44% (202) | 4.19% (215) |
| map | 2026-06 | 216 | 0.647721 | 0.637600 | 0.620377 | -16.93% (143) | -15.15% (128) |
| series | 2026-01 | 21 | 0.577267 | — | 0.661069 | 21.00% (16) | — |
| series | 2026-02 | 51 | 0.679620 | — | 0.694525 | 30.74% (40) | — |
| series | 2026-03 | 64 | 0.613019 | — | 0.565917 | -6.70% (55) | — |
| series | 2026-04 | 221 | 0.611483 | 0.609627 | 0.627690 | 26.18% (160) | 17.45% (146) |
| series | 2026-05 | 199 | 0.644846 | 0.645792 | 0.663719 | 18.65% (140) | 24.76% (104) |
| series | 2026-06 | 121 | 0.594363 | 0.583279 | 0.598199 | 4.30% (91) | 6.77% (73) |

### player_round_glicko_rookie+regional_form: Kalshi comparison and returns

regional_form: regional: rows=327, ridge=4, s=0.968512, effects: Americas=0.196328, EMEA=0.0481706, Pacific=0.0534876, China=-0.297986; form: rows=7863, H=5, w=1.38115

#### Log loss vs Kalshi

| Kind | Slice | Rows | Model log loss | Kalshi log loss | Difference [95% interval] | Significant |
|---|---|---:|---:|---:|---|---|
| series | all | 677 | 0.622743 | 0.633240 | -0.010497 [-0.035361, 0.014305] | no |
| series | vct | 278 | 0.624448 | 0.634755 | -0.010307 [-0.044260, 0.023339] | no |
| series | vcl | 340 | 0.612300 | 0.619968 | -0.007668 [-0.048370, 0.033036] | no |
| series | gc | 0 | — | — | — | — |
| series | t3 | 0 | — | — | — | — |
| series | collegiate | 0 | — | — | — | — |
| series | offseason | 59 | 0.674895 | 0.702587 | -0.027692 [-0.092903, 0.037496] | no |
| series | international=1 | 41 | 0.604527 | 0.653397 | -0.048869 [-0.100435, 0.006967] | no |
| series | international=0 | 636 | 0.623918 | 0.631941 | -0.008023 [-0.035010, 0.018188] | no |
| map | all | 1049 | 0.656688 | 0.668225 | -0.011536 [-0.033559, 0.006662] | no |
| map | vct | 461 | 0.658540 | 0.665762 | -0.007222 [-0.026949, 0.009821] | no |
| map | vcl | 490 | 0.648933 | 0.668365 | -0.019431 [-0.060227, 0.015378] | no |
| map | gc | 0 | — | — | — | — |
| map | t3 | 0 | — | — | — | — |
| map | collegiate | 0 | — | — | — | — |
| map | offseason | 98 | 0.686754 | 0.679111 | 0.007643 [-0.028050, 0.041088] | no |
| map | international=1 | 59 | 0.643504 | 0.649653 | -0.006149 [-0.042536, 0.026436] | no |
| map | international=0 | 990 | 0.657474 | 0.669332 | -0.011857 [-0.034059, 0.007417] | no |

#### Full-Kelly returns

| Kind | Slice | Bets | Matches | Mean edge | Flat ROI [95% interval] | Kelly, LoL caps ($50 start) | Multiple | Max drawdown | Largest stake |
|---|---|---:|---:|---:|---|---:|---:|---:|---:|
| series | all | 501 | 500 | 0.1038 | 15.02% [2.96%, 27.63%] | $967.92 | 19.358× | 76.94% | $159.57 |
| series | vct | 200 | 200 | 0.0884 | 12.03% [-4.65%, 31.68%] | $103.26 | 2.065× | 65.18% | $10.45 |
| series | vcl | 266 | 265 | 0.1165 | 16.20% [-0.33%, 35.83%] | $250.97 | 5.019× | 66.87% | $43.07 |
| series | gc | 0 | 0 | — | — | $50.00 | 1.000× | 0.00% | $0.00 |
| series | t3 | 0 | 0 | — | — | $50.00 | 1.000× | 0.00% | $0.00 |
| series | collegiate | 0 | 0 | — | — | $50.00 | 1.000× | 0.00% | $0.00 |
| series | offseason | 35 | 35 | 0.0956 | 23.07% [-19.85%, 68.64%] | $70.00 | 1.400× | 36.97% | $9.93 |
| series | international=1 | 28 | 28 | 0.0648 | 11.92% [-22.35%, 44.76%] | $79.06 | 1.581× | 25.01% | $7.31 |
| series | international=0 | 473 | 472 | 0.1061 | 15.20% [1.33%, 27.45%] | $586.90 | 11.738× | 76.94% | $111.78 |
| map | all | 644 | 347 | 0.0717 | 19.15% [2.42%, 38.91%] | $5056.26 | 101.125× | 43.06% | $250.00 |
| map | vct | 259 | 136 | 0.0573 | 12.70% [-5.86%, 36.94%] | $252.03 | 5.041× | 32.60% | $16.74 |
| map | vcl | 335 | 186 | 0.0865 | 28.96% [0.64%, 64.75%] | $1003.94 | 20.079× | 71.60% | $250.00 |
| map | gc | 0 | 0 | — | — | $50.00 | 1.000× | 0.00% | $0.00 |
| map | t3 | 0 | 0 | — | — | $50.00 | 1.000× | 0.00% | $0.00 |
| map | collegiate | 0 | 0 | — | — | $50.00 | 1.000× | 0.00% | $0.00 |
| map | offseason | 50 | 25 | 0.0468 | -13.20% [-45.56%, 22.50%] | $44.55 | 0.891× | 28.52% | $2.85 |
| map | international=1 | 34 | 19 | 0.0536 | -10.67% [-37.97%, 12.83%] | $50.19 | 1.004× | 9.09% | $3.48 |
| map | international=0 | 610 | 328 | 0.0727 | 20.81% [2.43%, 41.83%] | $5334.47 | 106.689× | 44.47% | $250.00 |
| series+map | all | 1145 | 527 | 0.0857 | 17.34% [5.43%, 31.43%] | $5315.55 | 106.311× | 66.08% | $250.00 |

#### Monthly market blend fits

UTC monthly fits use earlier rows of the same kind from 2025-09-01, excluding holdout; minimum 100 rows. logit(p_blend) = a·logit(mid) + b·(logit(p_model) − logit(mid)); inputs clipped to [0.01, 0.99], no intercept, ridge 1e-6. Unfitted rows use mid unchanged; excluded from blended tables: 240 rows. Rating parameters remain selected on the tuning window.

| Month | Kind | n | a | b | Status |
|---|---|---:|---:|---:|---|
| 2026-01 | series | 0 | 1.000000 | 0.000000 | unfitted |
| 2026-02 | series | 21 | 1.000000 | 0.000000 | unfitted |
| 2026-02 | map | 0 | 1.000000 | 0.000000 | unfitted |
| 2026-03 | series | 72 | 1.000000 | 0.000000 | unfitted |
| 2026-03 | map | 48 | 1.000000 | 0.000000 | unfitted |
| 2026-04 | series | 136 | 1.283249 | 0.639266 | fitted |
| 2026-04 | map | 104 | 1.709101 | 0.637107 | fitted |
| 2026-05 | series | 357 | 1.099852 | 0.633518 | fitted |
| 2026-05 | map | 456 | 1.260882 | 1.047536 | fitted |
| 2026-06 | series | 556 | 1.044943 | 0.645656 | fitted |
| 2026-06 | map | 833 | 1.073747 | 0.870954 | fitted |

#### Log loss vs Kalshi (blended)

| Kind | Slice | Rows | Model log loss | Kalshi log loss | Difference [95% interval] | Significant |
|---|---|---:|---:|---:|---|---|
| series | all | 541 | 0.617043 | 0.634347 | -0.017304 [-0.033042, -0.001905] | yes |
| series | vct | 201 | 0.631943 | 0.644147 | -0.012204 [-0.032833, 0.007550] | no |
| series | vcl | 291 | 0.596683 | 0.621829 | -0.025146 [-0.049030, 0.000917] | no |
| series | gc | 0 | — | — | — | — |
| series | t3 | 0 | — | — | — | — |
| series | collegiate | 0 | — | — | — | — |
| series | offseason | 49 | 0.676835 | 0.668490 | 0.008345 [-0.027547, 0.044422] | no |
| series | international=1 | 24 | 0.650431 | 0.682705 | -0.032274 [-0.082509, 0.018449] | no |
| series | international=0 | 517 | 0.615493 | 0.632102 | -0.016609 [-0.032436, -0.000322] | yes |
| map | all | 945 | 0.675119 | 0.673192 | 0.001927 [-0.009149, 0.014255] | no |
| map | vct | 392 | 0.666062 | 0.667249 | -0.001187 [-0.016673, 0.014405] | no |
| map | vcl | 456 | 0.679391 | 0.676303 | 0.003088 [-0.014674, 0.020925] | no |
| map | gc | 0 | — | — | — | — |
| map | t3 | 0 | — | — | — | — |
| map | collegiate | 0 | — | — | — | — |
| map | offseason | 97 | 0.691631 | 0.682581 | 0.009050 [-0.025746, 0.045226] | no |
| map | international=1 | 50 | 0.644216 | 0.651359 | -0.007143 [-0.044870, 0.025321] | no |
| map | international=0 | 895 | 0.676845 | 0.674412 | 0.002433 [-0.009545, 0.014000] | no |

#### Full-Kelly returns (blended)

| Kind | Slice | Bets | Matches | Mean edge | Flat ROI [95% interval] | Kelly, LoL caps ($50 start) | Multiple | Max drawdown | Largest stake |
|---|---|---:|---:|---:|---|---:|---:|---:|---:|
| series | all | 319 | 319 | 0.0542 | 18.07% [4.59%, 32.94%] | $507.70 | 10.154× | 60.01% | $62.47 |
| series | vct | 116 | 116 | 0.0427 | 13.33% [-8.82%, 36.84%] | $47.06 | 0.941× | 66.40% | $5.46 |
| series | vcl | 182 | 182 | 0.0625 | 23.56% [5.59%, 43.34%] | $605.24 | 12.105× | 36.75% | $74.47 |
| series | gc | 0 | 0 | — | — | $50.00 | 1.000× | 0.00% | $0.00 |
| series | t3 | 0 | 0 | — | — | $50.00 | 1.000× | 0.00% | $0.00 |
| series | collegiate | 0 | 0 | — | — | $50.00 | 1.000× | 0.00% | $0.00 |
| series | offseason | 21 | 21 | 0.0457 | -3.28% [-52.57%, 48.79%] | $44.93 | 0.899× | 17.60% | $5.31 |
| series | international=1 | 13 | 13 | 0.0578 | 7.65% [-42.83%, 58.78%] | $64.56 | 1.291× | 19.31% | $5.77 |
| series | international=0 | 306 | 306 | 0.0541 | 18.52% [4.21%, 33.38%] | $394.91 | 7.898× | 60.01% | $48.59 |
| map | all | 597 | 315 | 0.0472 | 0.97% [-8.52%, 11.99%] | $30.00 | 0.600× | 65.74% | $7.61 |
| map | vct | 237 | 122 | 0.0456 | -1.65% [-11.35%, 8.97%] | $41.38 | 0.828× | 50.13% | $5.36 |
| map | vcl | 309 | 168 | 0.0495 | 4.07% [-11.71%, 24.39%] | $35.02 | 0.700× | 67.90% | $9.87 |
| map | gc | 0 | 0 | — | — | $50.00 | 1.000× | 0.00% | $0.00 |
| map | t3 | 0 | 0 | — | — | $50.00 | 1.000× | 0.00% | $0.00 |
| map | collegiate | 0 | 0 | — | — | $50.00 | 1.000× | 0.00% | $0.00 |
| map | offseason | 51 | 25 | 0.0406 | -5.61% [-35.50%, 29.18%] | $46.07 | 0.921× | 13.39% | $3.10 |
| map | international=1 | 28 | 13 | 0.0521 | -9.97% [-38.06%, 16.33%] | $49.76 | 0.995× | 7.75% | $3.02 |
| map | international=0 | 569 | 302 | 0.0469 | 1.51% [-8.69%, 13.86%] | $30.15 | 0.603× | 65.58% | $7.61 |
| series+map | all | 916 | 392 | 0.0496 | 6.93% [-2.22%, 16.65%] | $81.37 | 1.627× | 67.89% | $12.48 |

#### Monthly breakdown

All metrics use identical linked rows within each kind/month. Unfitted blend months show —; counts include all rows.

| Kind | Month | Rows | Model log loss | Blended log loss | Kalshi log loss | Raw flat ROI (bets) | Blended flat ROI (bets) |
|---|---|---:|---:|---:|---:|---|---|
| map | 2026-02 | 48 | 0.702935 | — | 0.690786 | 12.30% (37) | — |
| map | 2026-03 | 56 | 0.605562 | — | 0.565065 | -12.94% (42) | — |
| map | 2026-04 | 352 | 0.638529 | 0.688549 | 0.690793 | 63.22% (217) | 6.49% (243) |
| map | 2026-05 | 377 | 0.681770 | 0.685065 | 0.687018 | 4.90% (203) | 4.08% (218) |
| map | 2026-06 | 216 | 0.645483 | 0.635872 | 0.620377 | -15.83% (145) | -13.87% (136) |
| series | 2026-01 | 21 | 0.577645 | — | 0.661069 | 21.00% (16) | — |
| series | 2026-02 | 51 | 0.673502 | — | 0.694525 | 35.24% (42) | — |
| series | 2026-03 | 64 | 0.614687 | — | 0.565917 | -9.39% (52) | — |
| series | 2026-04 | 221 | 0.611364 | 0.608544 | 0.627690 | 23.86% (162) | 18.66% (139) |
| series | 2026-05 | 199 | 0.644753 | 0.645604 | 0.663719 | 18.47% (139) | 30.35% (104) |
| series | 2026-06 | 121 | 0.598023 | 0.585593 | 0.598199 | -2.63% (90) | 0.20% (76) |
