# Current state

## Status

VLR crawler, parsers and DB build (backfill not run), 2026-10-28. No model yet.

## Known limits

Offline validation covers five fixture matches only; live crawling is unverified. Economy has eco/half/full categories, without separate semi-eco/semi-buy.

## Future work

- Kalshi collector, then a schedule for it (storage needs a decision: S3 via the infrastructure repo, or local).
- Run VLR backfill; add event tiers and team aliases.
- bo3.gg cross-check; Liquipedia rosters/map pool.
- Elo v1 and the benchmark harness (design plan Phase 2).
