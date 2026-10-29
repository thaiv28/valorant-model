# Current state

## Status

Kalshi collector built (not scheduled), 2026-10-28. Catalogs, final trade tapes, hourly candles and open-book snapshots save to raw files. Offline-tested only; nothing collected live or modelled yet.

## Known limits

Not run against the live API. Book history starts only when snapshots run.

## Future work

- Schedule the collector (storage needs a decision: S3 via the infrastructure repo, or local).
- Run `promval kalshi books --every 30` around match starts to time the veto window.
- VLR crawler, cache, parsers and DB build; bo3.gg cross-check.
- Elo v1 and the benchmark harness (design plan Phase 2).
