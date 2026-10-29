# Product

## Goal

Price Valorant matches before each map well enough to beat Kalshi's prices after fees, then trade them. Pages and in-game odds come later. Full design: `docs/design_plan.pdf`.

## Markets

- `KXVALORANTGAME`: series winner. Listed from Sep 2025.
- `KXVALORANTMAP`: map winner by slot ("map 1", "map 2"). Listed from Feb 2026, about two days before the match, so before the veto. Maps 3–4 are rarely listed. An unplayed map settles at the fair market price.
- Tiers traded: tier 1, Challengers/VCL, Ascension, Game Changers and third-party events.

## Where the edge comes from

From a better rating model, as in Prometheus: not from speed. Kalshi's map prices react to the veto immediately, so post-veto latency is not an edge to pursue.

## Model

Built: v1 team Elo on binary map wins, with coin baseline and a match-clustered benchmark against Kalshi pre-match prices. Real-DB validation is pending.

Planned increments, in order:

1. Round-share credit.
2. Player ratings with uncertainty.
3. League offsets linked by international and third-party events.
4. Map strength, shrunk and adjusted for roster continuity.
5. Veto model for map-slot and series prices.

Calibration and market blending follow validated rating improvements.

## Trading rules

League's limits ($250 per order and per fixture, $1k exposure, $2k per day, same Kelly settings) from a $50 seed. No new orders once seed + settled profit − open stakes is $0 or less. Paper trading at VCT 2027 Kickoff before live.

## Data

VLR.gg (primary, scraped politely and cached), bo3.gg (cross-check; a Kalshi settlement source), Kalshi's public API. Backfill: ratings from 2021, benchmarks scored from 2023. Holdout: games from 2026-07-01 on.
