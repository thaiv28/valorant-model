# Product

## Goal

Price Valorant matches before each map well enough to beat Kalshi's prices after fees, then trade them. Pages and in-game odds come later. Full design: `docs/design_plan.pdf`.

## Markets

- `KXVALORANTGAME`: series winner. Listed from Sep 2025.
- `KXVALORANTMAP`: map winner by slot ("map 1", "map 2"). Listed from Feb 2026, about two days before the match, so before the veto. Maps 3–4 are rarely listed. An unplayed map settles at the fair market price.
- Tiers traded: tier 1, Challengers/VCL, Ascension, Game Changers and third-party events.

## Where the edge comes from

From a better rating model, as in Prometheus: not from speed. Kalshi's map prices react to the veto immediately, so post-veto latency is not an edge to pursue.

## Model (planned)

1. Player-based round Elo: ratings belong to players and update on round share; Glicko-style uncertainty; region offsets linked by international and third-party events.
2. Map layer: team-by-map deviation, shrunk, decayed and scaled by roster continuity.
3. Veto model: conditional logit per ban/pick; every veto order enumerated for map-slot and series prices.
4. Calibration (temperature, Bo1/LAN/region) and a market blend as in Prometheus.

## Trading rules

League's limits ($250 per order and per fixture, $1k exposure, $2k per day, same Kelly settings) from a $50 seed. No new orders once seed + settled profit − open stakes is $0 or less. Paper trading at VCT 2027 Kickoff before live.

## Data

VLR.gg (primary, scraped politely and cached), bo3.gg (cross-check; a Kalshi settlement source), Kalshi's public API. Backfill: ratings from 2021, benchmarks scored from 2023. Holdout: games from 2026-07-01 on.
