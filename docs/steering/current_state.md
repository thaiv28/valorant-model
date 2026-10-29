# Current state

## Status

2026-10-29: VLR backfill complete (2021 on, 28,770 matches). Model: `player_round_glicko_rookie_tier_revert` (player Glicko-style RD, round credit, rookie discount 200/400 maps, 20% pull toward the tier mean each Nov 1) with a stage-1 series temperature; parameters in `promval/ratings/elo_weights.json`. Two-stage benchmark run on the full crawl ([report](../elo_backtest.md), [ledger](../research/README.md)); holdout opened 2026-10-29 ([report](../elo_holdout.md)): raw model ≈ Kalshi; blended domestic series the only positive result.

- Kalshi: catalogs, final trade tapes, hourly candles and open-book snapshots save to `data/kalshi/` (scheduled every 6 h; secrets/variable are set, raw S3 seeding required). The first full backfill was started 2026-10-28.
- Execution inputs: frozen monthly blend artifact; feed job exports private Kalshi-named series candidates; Prometheus handles blending, sizing and orders (domestic only).
- Site feed: hourly `refresh-db.yml` saves ratings to S3; `feed.yml` publishes DB-free snapshots every 10 minutes via cron-job.org dispatch (GitHub schedule backup). `promval feed-state` / `export --state` retain frozen calls and Kalshi prices; `--no-fetch` builds offline. Workflows await GitHub validation; runner times unmeasured; seed raw S3 cache once. Freshness follows the last crawl and DB rebuild; same-day results await ingestion, and TBD teams are omitted.
- Linking: catalog loader, team matching, learned aliases, map links and settlement cross-checks.
- VLR: raw cache, parsers and `scripts/setup_db.sh`; full backfill parsed with 407 page errors (1.4%, mostly old pages with broken scores).
- Events: tier lists and overrides build `events`; seven-map vetoes build pool periods and map active spans offline via `setup_db.sh`.

## Known limits

- VLR's VCT tier includes some tier-2 events; sections are coarse, refine via overrides. Pool history reflects observed vetoes, not exact patch boundaries.
- Order-book history exists only from when snapshots run.
- VLR's economy tab has eco/half/full buy categories (no separate semi-eco/semi-buy) and omits overtime rounds.
- Some player rows have no rating (70 of 560 in the sample).

## Future work

- Map strength, pick bonus and momentum were tested and rejected (ledger); a veto model is not worth building on that evidence.
- New model ideas need a fresh forward window (from 2026-10-29); the July–Oct 2026 holdout is spent.
- Review unlinked Kalshi events; two matches (8 markets) settle differently on Kalshi and VLR.
- bo3.gg is not used: its robots.txt disallows `/api/`; Kalshi's own settled results cross-check VLR instead.
