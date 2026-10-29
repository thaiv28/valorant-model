# Research ledger

Every model idea tested, adopted or not, newest first, with its numbers. Rules: [tech.md, Model change rules](../steering/tech.md). Entries before the two-stage benchmark (2026-10-28) were run on a partial crawl with parameters selected in-sample; they are leads, not verdicts, and are rerun on the full history.

## Two-stage runs

Partial crawl (VLR from 2024-06-26, 7,597 matches): seed Jun–Sep 2024, stage 1 Oct 2024 – Aug 2025 (8,241 maps), stage 2 Sep 2025 – Jun 2026 (6,337 maps; Kalshi had no Valorant markets Oct–Dec 2025, so market rows are Sep 2025 and Jan–Jun 2026). Δ = candidate − base map log loss, paired bootstrap by match. Report: [`docs/elo_backtest.md`](../elo_backtest.md). Rerun on the full crawl.

- **Form layer (2026-10-28): adopted (candidate).** Starters' recent VLR rating, logit p′ = logit p + w·(form₁ − form₂), fitted on stage 1 (H = 5 maps, the grid's smallest; w = 1.41). Over `player_round_glicko_rookie`: stage 1 −0.0030 [−0.0047, −0.0013], stage 2 −0.0027 [−0.0045, −0.0010]; VCL significant on both; no section worse. Next: H < 5.
- **Regional calibration layer (2026-10-28): not adopted (retest on full history).** Ridge-4 region effects and scale on cross-region maps (327 stage-1 rows; China −0.30, Americas +0.20, s = 0.97): stage 1 −0.0004 (not significant, below 0.0005); stage 2 international −0.011 [−0.024, +0.001].
- **Rookie discount (2026-10-28): adopted (candidate).** Prometheus's log1p discount (chose penalty 200, 100 maps, both grid maxima). Over `player_round_glicko`: stage 1 −0.0046 [−0.0072, −0.0020], GC −0.0097 significant; stage 2 −0.0070 [−0.0099, −0.0040], VCL significant; no section worse. Next: larger grid.
- **Tier moves (2026-10-28): rejected.** Move-up penalty / move-down bonus by tier: stage 1 −0.0001, stage 2 +0.0002 (no effect).
- **Combined (`player_round_glicko_rookie+form`), stage 2 vs Kalshi (tradeable quotes, LoL-capped Kelly):** raw series −0.011, maps −0.011 (n.s.; international series −0.054 significant); blended series −0.017 (significant), maps +0.003. Flat ROI raw series+map +18.0% [+5.5, +31.6], $50 → $5,243; blended series +17.4% [+4.0, +31.2], $50 → $553. Map raw ROI concentrated in April 2026 (+63%).

## Partial-crawl leads (in-sample, pre-two-stage)

- **Pick advantage (2026-10-28).** Feb–Jun 2026, 2,409 picked maps: the picking team won 52.5% vs 50.0% predicted by `player_round_glicko` (+2.5 pts, 95% [+0.5, +4.4]); a 0.11-logit picker bonus improves picked-map log loss 0.6457 → 0.6443. Cancels for series; pre-veto the map-1 picker is unknown in Bo3 (VLR team1 picks it 46%) but known in Bo5 (70%). Full map/veto model deferred.
- **Kalshi quote timing (2026-10-28).** The last hourly candle before start can price the veto. 30 min after listing, books are empty (median spread 13¢). Adopted for the benchmark: first quote ≥30 min after listing, ≥2 h before start, spread ≤6¢ (83% of markets, median 40 h before start). Kalshi's early price is much less sharp (series log loss 0.632 vs 0.604 pre-start).
- **Market blend (2026-10-28).** Walk-forward monthly logit blend. Series: stable b ≈ 0.33 (keep a third of the model's disagreement); blended series beat raw every fitted month (Apr–Jun flat ROI +13.1% vs +5.2%). Maps: unstable early fits; the raw map edge (+18% Apr–Jun) is almost all April (+54% on 227 bets, when Kalshi map prices had log loss 0.691); May +2%, June −17.5%.
- **Kelly sizing (2026-10-28).** Uncapped full Kelly on the raw model goes broke even at +15% flat ROI. Prometheus caps (10% and $250 per fixture, $1k exposure, $2k day): raw series+map +13.4% flat [+1.5, +27.0], $50 → $3,622 (max drawdown 66%); blended series +9.6%, $50 → $158.
- **Player RD, Glicko-style (2026-10-28), leading candidate.** Prometheus's rule (new 280–350, floor 140, growth 10/√day, information 0.25). Feb–Jun 2026 (4,237 maps): `player_round_glicko` 0.6502 map log loss vs `player_round` 0.6549 and v1 0.6656; vs v1 −0.015 maps, −0.025 series (significant).
- **Credit, unit and region variants (2026-10-28).** June 2026 (549 maps): round credit (exact first-to-13 DP, τ ≈ 0.5) and margin credit (0.5 + 0.5·tanh(diff/c)) beat binary v1 significantly (−0.010 to −0.013 map log loss); player ≈ team (slightly ahead); region offsets chose the smallest weight every time (no gain; little cross-region data).
- **Elo v1 (2026-10-28), baseline.** Team Elo on map wins, K by grid: June 2026 map log loss 0.664 vs coin 0.693 (significant).
