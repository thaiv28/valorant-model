# Current state

## Status

2026-10-28: Kalshi collector and VLR crawler, parsers and DB build are in place. No model yet.

- Kalshi: catalogs, final trade tapes, hourly candles and open-book snapshots save to `data/kalshi/` (run manually; not scheduled). The first full backfill was started 2026-10-28.
- VLR: raw cache, parsers and `scripts/setup_db.sh`; a live sample of 27 matches (2021–2026) parsed with no errors. The full backfill has not run.

## Known limits

- Order-book history exists only from when snapshots run.
- VLR's economy tab has eco/half/full buy categories (no separate semi-eco/semi-buy) and omits overtime rounds.
- Some player rows have no rating (70 of 560 in the sample).

## Future work

- Schedule the Kalshi collector (storage needs a decision: S3 via the infrastructure repo, or local).
- Run `promval kalshi books --every 30` around match starts to time the veto window.
- Run the VLR backfill (`promval vlr crawl --since 2021-01-01 --full`); add event tiers and team aliases.
- bo3.gg cross-check; Liquipedia rosters and map pool.
- Elo v1 and the benchmark harness (design plan Phase 2).
