# Current state

## Status

2026-10-29: VLR backfill complete (2021 on, 28,770 matches). Model: `player_round_glicko_rookie` (player Glicko-style RD, round credit, rookie discount 200/400 maps) with a stage-1 series temperature; parameters in `promval/ratings/elo_weights.json`. Two-stage benchmark run on the full crawl ([report](../elo_backtest.md), [ledger](../research/README.md)); holdout (July 2026 on) unopened.

- Kalshi: catalogs, final trade tapes, hourly candles and open-book snapshots save to `data/kalshi/` (scheduled every 6 h once secrets/variable are set and S3 is seeded). The first full backfill was started 2026-10-28.
- Linking: catalog loader, team matching, learned aliases, map links and settlement cross-checks.
- VLR: raw cache, parsers and `scripts/setup_db.sh`; full backfill parsed with 407 page errors (1.4%, mostly old pages with broken scores).
- Events: tier lists and overrides build `events`; seven-map vetoes build pool periods and map active spans offline via `setup_db.sh`.

## Known limits

- VLR's VCT tier includes some tier-2 events; sections are coarse, refine via overrides. Pool history reflects observed vetoes, not exact patch boundaries.
- Order-book history exists only from when snapshots run.
- VLR's economy tab has eco/half/full buy categories (no separate semi-eco/semi-buy) and omits overtime rounds.
- Some player rows have no rating (70 of 560 in the sample).

## Future work

- Model increments: map strength → veto model; map-2 momentum (+3 points after a map-1 win) in series odds.
- Store the series temperature with the weights for live use.
- Open the July 2026+ holdout once, after the model is frozen (ask the user first).
- Review unlinked Kalshi events; two matches (8 markets) settle differently on Kalshi and VLR.
- bo3.gg is not used: its robots.txt disallows `/api/`; Kalshi's own settled results cross-check VLR instead.
