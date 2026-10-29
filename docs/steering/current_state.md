# Current state

## Status

2026-10-28: Kalshi collector (scheduled) and VLR crawler, parsers, events and DB build are in place. No model yet.

- Kalshi: catalogs, final trade tapes, hourly candles and open-book snapshots save to `data/kalshi/` (scheduled every 6 h once secrets/variable are set and S3 is seeded). The first full backfill was started 2026-10-28.
- VLR: raw cache, parsers and `scripts/setup_db.sh`; a live sample of 27 matches (2021–2026) parsed with no errors. The full backfill has not run.
- Events: tier lists and overrides build `events`; seven-map vetoes build pool periods and map active spans offline via `setup_db.sh`.

## Known limits

- VLR's VCT tier includes some tier-2 events; sections are coarse, refine via overrides. Pool history reflects observed vetoes, not exact patch boundaries.
- Order-book history exists only from when snapshots run.
- VLR's economy tab has eco/half/full buy categories (no separate semi-eco/semi-buy) and omits overtime rounds.
- Some player rows have no rating (70 of 560 in the sample).

## Future work

- The VLR backfill is running (`promval vlr crawl --since 2021-01-01 --full`, started 2026-10-28).
- Team aliases and Kalshi–VLR links.
- bo3.gg is not used: its robots.txt disallows `/api/`; Kalshi's own settled results cross-check VLR instead.
- Elo v1 and the benchmark harness (design plan Phase 2).
