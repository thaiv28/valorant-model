# Tech

## Stack

Python ≥ 3.12 with uv; SQLite rebuilt from raw caches; raw SQL; Typer CLI (`promval`); BeautifulSoup + lxml for HTML; ruff; pytest (offline, fixtures in `tests/fixtures/`).

## Layout

| Path | Purpose |
|---|---|
| `promval/ratings/` | Team Elo, model registry, chronological map replay; optional `elo_weights.json` |
| `promval/evaluation.py`, `scripts/evaluate_elo.py` | Scoring helpers and offline benchmark report |
| `tests/test_elo.py`, `tests/test_evaluation.py` | Ratings, leakage, candle formats and synthetic-DB benchmark checks |
| `promval/main.py` | CLI entry; mounts the `kalshi` and `vlr` command groups |
| `promval/kalshi/api.py` | Public HTTP client, pacing, retries and pagination |
| `promval/kalshi/collect.py` | Raw catalog, trade, candle and book files |
| `promval/kalshi/cli.py` | Collector, manifest and book-loop commands |
| `tests/test_kalshi_collect.py` | Offline fixture-based collector and CLI tests |
| `promval/vlr/` | VLR.gg crawler, raw cache and parsers |
| `scripts/001_create_tables.sql`, `002_load_vlr.py`, `003_events.py`, `004_map_pool.py`, `setup_db.sh` | Rebuild SQLite from VLR cache |
| `promval/link.py` | Pure team normalization, event linking and settlement checks |
| `scripts/005_load_kalshi.py`, `006_link_kalshi.py` | Load catalogs, learn aliases and link Kalshi to VLR |
| `tests/test_link.py` | Offline linking and catalog-to-DB checks |
| `scripts/work_log.py`, `.githooks/` | Work-log tooling |
| `tests/test_vlr_*.py` | Offline parser, crawl and DB checks |
| `tests/test_steering.py` | Doc guard |
| `tests/fixtures/` | Saved Kalshi JSON and gzipped VLR pages |

## Kalshi collector

`promval kalshi collect [--no-books] [--limit N]` refreshes both Valorant series (`KXVALORANTGAME`, `KXVALORANTMAP`), saves final-market histories and snapshots active books. `--limit` caps new trade/candle fetches combined (each file attempt counts separately). `promval kalshi books --every 60 --minutes 60` refreshes active tickers each pass; pass summaries include failures. GitHub Actions collects every six hours (see Deployment).

Public base: `https://api.elections.kalshi.com/trade-api/v2`. Paginate `/markets` and `/historical/markets` by series; merge by ticker, preferring `/markets`. Historical-catalog markets use `/historical/trades?ticker=T` and `/historical/markets/T/candlesticks`; recent markets use `/markets/trades?ticker=T` and `/series/S/markets/T/candlesticks`. Trades paginate with `limit=1000`; hourly candles use market open/close unix timestamps and `period_interval=60`. Preserve raw fields. Books use `/markets/T/orderbook`; the books loop discovers tickers through `/markets?series_ticker=S&status=open`.

Under `data/kalshi/` (or `$PROMVAL_DATA/kalshi/`):

- `markets/<SERIES>.json`: raw market list sorted by ticker, refreshed each run.
- `trades/<TICKER>.jsonl.gz`: raw full tape sorted by (`created_time`, `trade_id`).
- `candles/<TICKER>.json.gz`: raw candlesticks list.
- `books/<YYYY-MM-DD>/<YYYYMMDDTHHMMSSZ>.jsonl.gz`: one new gzip file per pass, one line per snapshot with `at` (UTC ISO Z, second precision), `ticker` and raw `orderbook_fp`. No appends; zero snapshots write no file. Local timestamp collisions advance the filename by a second.
- `manifest.json`: version 1 with sorted `trades` and `candles` ticker arrays. Skip histories present locally or listed here; runners download only this manifest, never the history archive.

New files and refreshed catalogs use temporary files plus atomic rename. Only finalized/settled markets get histories; existing trade/candle files are never rewritten. Empty tapes with positive `volume_fp` (or `volume`) and empty candle lists report errors without writing files, allowing retries. Zero-volume empty tapes are saved as complete. Other markets continue after failures; failed catalogs skip that series. After collection, atomically rewrite the manifest as the union of its old entries and all local histories, including newly saved files. A missing manifest starts empty. `promval kalshi manifest` rebuilds it from local history files only, for seeding S3. Books are written atomically once per pass.

The standard-library client uses a repository User-Agent, 30-second timeout and at least 0.06 seconds between requests. HTTP 429/5xx, URL errors and timeouts retry up to five attempts with 1/2/4/8-second backoff. First-run estimate: about 10k final markets × two requests at ~0.06-second spacing plus latency, roughly an hour; pagination and retries can add time.

## VLR scraper

`uv run promval vlr events` refreshes all tier lists: 60 VCT, 61 VCL, 62 T3, 63 GC, 64 Collegiate, 67 Offseason. Pages stop at the first empty list; `raw/events/tier<T>_p<N>.html.gz` is overwritten each run, obsolete trailing pages removed. Cost: ≈63 pages ≈2 min at 2 s/request. `003_events.py` builds the union into `events` (event_id, slug, name, primary vlr_tier, section, JSON tiers, international, status, dates, region, prize); no cache creates an empty table. Primary priority: 60, 63, 61, 67, 62, 64; sections: vct, gc, vcl, offseason, t3, collegiate. International (`is_international`): a vct, gc or offseason event, not a qualifier, whose name matches Masters followed by a city, Valorant Champions <year>, Champions Tour <year>: Champions, LOCK//IN, Esports World Cup or a Game Changers Championship. Regional names ending in Masters and T3/collegiate "Masters" cups do not match. `promval/vlr/event_overrides.json` applies international/section overrides by event ID last.

`004_map_pool.py` builds `veto_pools` (match_id, start_utc, sorted comma-joined pool) from exactly seven distinct veto maps. `map_pool_periods` (pool, first_utc, last_utc, matches) merges consecutive pools in VCT start order (all matches only when events is empty). Runs shorter than three join the preceding stable pool, or the next at the start; without a stable run, use the longest run's pool. View `map_pool` merges each map's adjacent active spans. Endpoints are inclusive observed times, not patch dates.

Run `uv run promval vlr crawl --since 2021-01-01`; options: `--economy-since 2023-01-01`, `--max-matches N`, `--min-interval 2.0`, `--workers N` (parallel fetches; `--min-interval` caps the total rate and a 429/5xx pauses all workers), `--full` (walk back to `--since` past cached pages; use it to resume an interrupted backfill, since a normal run stops after 3 pages with nothing new). Build offline with `bash scripts/setup_db.sh`; it deletes and rebuilds `db/valorant.db` in numeric script order. Failures roll back one match, continue, and log to `db/parse_errors.txt`.

Cache: `${PROMVAL_DATA:-data}/vlr/raw/matches/<id>.html.gz` and `<id>_economy.html.gz`. Writes use atomic gzip replacement. Parsed `(match, economy)` pickles are atomically gzip-cached in `vlr/parsed/v<PARSER_VERSION>/<id>.pkl.gz`; valid only when newer than both existing raw pages. Errors are not cached. Bump `promval.vlr.parse.PARSER_VERSION` whenever any parser's output changes. The loader parses misses in up to eight worker processes (CPU count capped at eight); `002_load_vlr.py --jobs N` or `PROMVAL_JOBS=N` overrides this (1 is serial). SQLite inserts stay in ascending match ID order in the main process, one transaction per match, using table batches. Results listings are uncached. Never re-fetch cached match pages; missing economy tabs can be retried independently. Skip same-day matches until tomorrow (Eastern date). Stop at empty/older pages, three consecutive pages without new work, or the match limit.

Requests start at least 2 seconds apart. User-Agent: `valorant-model/0.1 (+https://github.com/thaiv28/valorant-model)`. Retry 429, 5xx, URL errors and timeouts up to five attempts, sleeping 5/10/20/40 seconds. Fetching is injectable; parsers never fetch.

Results parser extracts IDs, slugs and day headings. Match parser extracts event/stage, team IDs/names, best-of, patch, UTC start, series score/winner, ordered veto (short tags; “remains” is decider), played maps, picks, scores, side totals, duration, overtime beyond 24 rounds, players/agents/stats, and round winners/sides/types. Skip unplayed maps. Missing stats are null. Reject inconsistent round counts, round wins or series map wins. An 11–13 score is 24 regulation rounds, not overtime. Map order is taken from the numbered map tabs, not the order of the stat sections. A drawn series (1–1 Bo2) has a null winner. The economy tab omits overtime rounds, so its per-round rows cover regulation only.

Economy fixtures (2020–2026) show pistol/conversion/bonus won/played, eco (<10k), half buy (10–18k), full buy (18k+) matchup counts, plus per-round team equipment and bank amounts (displayed in thousands). Summary grids exclude each half’s first three rounds; aggregate their counts by own buy category. Preserve every round’s category/buy/bank. Separate semi-eco and semi-buy are absent, stored null; half buy stays separate. Unavailable values remain null.

Tables: `matches` (match_id), `vetoes` (match_id/step), `maps` (game_id), `rounds` (game_id/round), `player_maps` (game_id/player_id), `economy` (game_id/team); declared foreign keys connect them. Agents and economy round details use JSON text; other fields are scalar SQL columns.

Time gotcha: VLR `data-utc-ts` is America/New_York local time, despite its name. Convert with zoneinfo (EST/EDT) to ISO UTC ending Z.

Backfill estimate: roughly 590 results pages back to 2021, about 29k matches; approximately two requests per match from 2023 and one before, at 2 seconds, roughly a day of crawling. Not run against the live site.

## Kalshi ↔ VLR links

The numbered DB build loads `kalshi_markets` from `collect.data_dir()/markets/{KXVALORANTGAME,KXVALORANTMAP}.json`; missing catalogs load zero rows with a message. Rules supply scheduled EDT/EST times (UTC Z) and event names; ticker suffixes supply team codes and map numbers.

`team_aliases` maps consistent competitor UUIDs to VLR team IDs, with names, codes and confident-series evidence counts; conflicting UUIDs are permanently dropped. `kalshi_links` stores one row per event, match/game IDs, kind, method and failure reason.

Candidates start within ±30 hours of the advertised schedule (otherwise open time +24 hours), allowing a one-day slip. Exact → alias → anchor passes repeat until no new link is made, re-deriving aliases from every confident link. Exact matching accepts either the outside name or the alternate inside a trailing parenthetical. Alias matching requires both UUIDs. An anchor requires one exact/aliased team appearing in only one candidate match; the other name must share normalized tokens, match team-code initials/a token, or have difflib similarity ≥0.6. Prefer an exact other-side name present in the window over a looser subteam name; competing matches remain ambiguous. Finally both fuzzy name similarities must reach 0.8, without overriding that preference. Normalization removes accents and generic organization words and equates female/women/GC. Map events inherit their series match (map-only catalogs use a representative map event), then select the played map by order; missing rows are `unplayed`.

Cross-check each linked binary settled market against the series/map winner; skip scalar settlements and unknown winners. `db/link_report.txt` lists unlinked events/unplayed maps with team names, schedule, event name and reason; anchor name mappings; and mismatched tickers with VLR IDs. The linker prints linked/total series and maps, aliases, market agreements/checked and mismatches. Re-runs replace derived rows. The Aug 18–Oct 27, 2026 catalog window linked 194/252 series against 233 cached matches before anchor/variant improvements. Settlement checks agreed on 1256/1264; eight disagreements came from the subsequently fixed VLR map ordering bug. Updated coverage is pending.

## Model change rules

```bash
uv run python scripts/evaluate_elo.py --out docs/elo_backtest.md               # two-stage benchmark, all models (~2–10 min)
uv run python scripts/evaluate_elo.py --layers none,regional,form --out docs/elo_backtest.md
uv run python scripts/evaluate_elo.py --write-weights                          # also store each model's stage-1 parameters
```

- **Stages.** Stage 1 (tuning): 2023-01-01 to 2025-09-01, match outcomes only; every parameter, grid choice and layer fit is selected here. Stage 2 (validation): 2025-09-01 to 2026-07-01, the frozen models against outcomes and against Kalshi (log loss, blend, returns). Holdout: 2026-07-01 on, never used for selection or fitting; opened once, for the final verdict, with `--holdout`.
- **Adopt a change only on a significant stage-1 gain.** The paired-bootstrap 95% interval of the per-map log-loss difference against the current best model, resampling whole matches, must exclude 0 on the sections the change targets (all, or a section such as vct, vcl, gc or international), and no guarded section (all, vct, vcl, gc, international) may be significantly worse. An added parameter, feature or layer also needs a gain of at least 0.0005.
- **Then confirm on stage 2.** Stage-2 outcome log loss and blended log loss vs Kalshi must not be significantly worse than the current best. A stage-2 gain is reported but is not a reason to adopt a change that failed stage 1; tuning on stage 2 to pass it is not allowed.
- **Removals** ship when every guarded section's interval stays below +0.0005 on both stages (non-inferior).
- **Every test goes in the ledger,** adopted or not, with its numbers: `docs/research/README.md`. Count the tests run against stage 2; many tries against one validation window make a lucky winner likely, so prefer ideas with a stage-1 case.
- **Trading results are reported, not gates:** the returns tables (raw and blended, LoL-capped Kelly, monthly breakdown) are in-sample for the blend's earliest months and assume fills at hourly quotes; a single month driving a result is called out.
- **Data fixes** (which data a model uses: a link, alias, tier, parser bug) are not model changes: they ship when they are correct and the benchmark doesn't get significantly worse.

## Ratings and benchmark

Kalshi price (`--quote`): `tradeable` (default) = first hourly bid/ask ending ≥30 min after the market opened and ≥2 h before the scheduled start with spread ≤ `--max-spread` (0.06), i.e. a price a bot could trade before any veto; markets without one are skipped. `prestart` = last candle before start (can price the veto; comparison only). Returns use Prometheus's pregame caps (`LOL_SIZING`): full Kelly, ≤10% of capital and ≤$250 per fixture, $250 per order, $1k exposure, $2k per day, day bets sized from opening capital; `sizing="full"` is uncapped.

Built: `coin` (0.5), v1 `team_elo`, 11 composable variants `<unit>_<credit>[_region]`, two player RD combinations and three rookie/move variants; `team_binary` is named `team_elo`. Initial ratings 1500, scale 400. Replay by (match start UTC, match_id, map order), predict before update. Chronologically loaded replays take O(maps); lineup/home history uses bounded work per map. Factories receive `load_lineups` starters; `load_maps` includes round scores and event host/international fields.

Three dimensions:

- Credit: binary S=win (1/0); margin winner S=0.5+0.5·tanh(abs(score1−score2)/c), loser 1−S; round S=score1/(score1+score2). Expected e=1/(1+10^(−Δ/400)); all units update ±K·(S−e). Binary/margin predict e. Round predicts σ(τ·logit(map_win(e))); first-to-13 DP, at 12–12 e²/(e²+(1−e)²), cache e rounded to four decimals.
- Unit: team ID or mean starter rating. Every starter moves equally unless RD is enabled. New players start fixed at 1500 or at the mean of already-rated teammates (1500 if none). Missing starters use that team's latest earlier lineup, then a namespaced team pseudo-player. Accept any nonempty lineup size.
- Regions: strength adds the team's home offset. Home is the earlier-map majority of known non-international event hosts; ties retain the previous home. Offsets start zero; only known, differing homes move ±region_k·(S−e). Record the current host after updating, preventing leakage.

Host country → macro region (`ratings/regions.py`):

| Region | Codes |
|---|---|
| Americas | us ca mx br ar cl co pe uy ve py bo ec cr gt pa pr do na latam north-america north_america south-america south_america |
| EMEA | eu gb de fr es it pt nl be se no dk fi pl cz at ch tr ru ua by kz sa ae eg ma za il gr ro hu rs hr bg ie lt lv ee me mena cis |
| Pacific | kr jp ph id th vn sg my au nz in tw hk mo kh mm pk bd lk np mn |
| China | cn |

`sa` means Saudi Arabia; use explicit South America aliases. Other codes (including un/missing) are unknown; benchmark summaries count unknown map rows.

Grids: K={16,24,32,48,64,96}; margin c={4,6,8,12}; round τ={0.4,0.5,0.6,0.8,1}; regional region_k={2,4,8,16} (otherwise 0); players new_player={fixed,teammates}. Replay starts at the first map unless `--seed-from` restricts it. Stage 1 selects parameters by map outcome log loss on [`--tune-from` (2023-01-01), `--tune-to` (2025-09-01)); no Kalshi data enters selection. Stage 2 validates frozen parameters on [`--validate-from` (2025-09-01), `HOLDOUT_START` (2026-07-01)). Require tune-from < tune-to ≤ validate-from ≤ holdout; earlier maps seed ratings. Winning models replay continuously; optional July 2026+ holdout never selects parameters or fits blends. Series use the first map's probability and independent maps; skip missing/even best-of and unknown winners.

Player RD (off by default; ignored for teams) adds `player_round_glicko` and `player_round_region_glicko`. New variance = rd_new²; before each map grow by rd_growth² × days since the player's last map start, capped at rd_new². Scale the usual player move by variance/rd_floor², then store max(rd_floor², 1/(1/variance + rd_info·(ln(10)/scale)²·E·(1−E))). E is the update expectation (round share for round credit). Only updates record variance/dates. Defaults: rd_new=280, rd_floor=140, rd_growth=10 per √day, rd_info=0.125. Glicko grids: K={16,24,32,48,64}, τ={0.4,0.5,0.6,0.8}, rd_new={280,350,450,600}, rd_info={0.125,0.25,0.5,1.0}, new_player={fixed,teammates}; regional region_k={2,4}. Floor/growth fixed (1,920 RD candidates).

Player-only rookie/tier adjustments default off: rookie_penalty=move_up_penalty=move_down_bonus=0, rookie_maps=30, move_maps=20. Effective rating subtracts rookie_penalty·(1−log1p(n)/log1p(rookie_maps)) for n<rookie_maps prior maps. Tier ranks: collegiate=0, t3=1, vcl=2, vct=3; gc/offseason/unknown neither apply moves nor change homes. Home is the prior ranked-map majority, retaining ties. Above/below home, add −move_up_penalty/+move_down_bonus times max(0,1−prior_maps_at_rank/move_maps). Both affect prediction and update expectations, never directly lower stored ratings; only update records counts. `player_round_glicko_{rookie,moves,rookie_moves}` grids: K={32,48}, τ={0.4,0.5}, rd_new={280,350}, rd_info={0.25}, new_player={teammates}; where used, rookie_penalty={50,100,200}, rookie_maps={30,100}, move_up_penalty={50,100,200}, move_down_bonus={0,50}. Not yet benchmarked.

Leaderboard retains selected params and tuning map/series losses; vs-v1 tables use paired log-loss differences, 2,000 match-clustered resamples, seed 0. Intervals excluding zero indicate significance. Coin metrics remain. Tuning comparisons are selection diagnostics.

Kalshi rows use cached last valid hourly yes bid/ask closes ending by match start (`close_dollars` or historical `close`, dollars). Prefer team1's contract; team2 contracts orient ask=1−bid, bid=1−ask. Compare identical linked rows; map predictions use first-map pre-match chances. Missing links/aliases/candles are skipped.

`backtest.py` buys team1 at ask or team2 at 1−bid, whichever has larger positive after-fee edge q−c−f(c). Require both buy prices in (0,1). Unrounded taker fee f(c)=0.07·c·(1−c). Full Kelly fraction=(q−c′)/(1−c′), c′=c+f(c); size every match's bets from its starting bankroll, scale total fractions down to one, then settle together. Each reported slice starts independently at $50. Flat stakes use $1 all-in per bet; ROI=profit/staked, 95% interval from 2,000 whole-match resamples, seed 0. Report bets, matches, mean edge, flat ROI interval, Kelly final/multiple, settled-path maximum drawdown and largest stake. Returns use frozen stage-1 parameters on validation rows; hourly ask/bid fills assume unlimited depth, no slippage; unplayed maps excluded.

`blend.py`: logit(p_blend)=a·logit(mid)+b·(logit(p_model)−logit(mid)), inputs clipped to [0.01,0.99]. No intercept; numpy Newton MLE with ridge 1e-6. Freeze separate series/map fits each UTC calendar month using earlier match starts at/after `--validate-from`, never holdout. Below `--blend-min` (100 default), use mid unchanged and flag unfitted; exclude these rows from blended tables and state their count. Report monthly (month,kind,n,a,b,status) snapshots. Rating parameters still use the tuning window.

Report starts with a validation summary, then Stage 1 outcome leaderboard/params and all-section vs-v1 bootstrap, Stage 2 outcome losses by section and vs-v1 bootstrap, then Stage 2 Kalshi tables. The summary has one row per reported model: all-section series/map model−Kalshi log loss, flat ROI and Kelly final. Blended columns repeat these metrics on fitted rows. Each model has raw and blended log-loss and return tables by kind (series/map), slice (all, vct/vcl/gc/t3/collegiate/offseason, international=1/0). `--report-models` overrides defaults: `team_elo`, `player_round_glicko`, best two by stage-1 map loss, deduplicated, plus their layers. Explicit report models are tuned even if absent from `--models`. Monthly breakdowns list kind, month, rows, model/blended/Kalshi losses and raw/blended flat ROI (bets) on identical linked rows; unfitted blend months show dashes and retain row counts.

`ratings/layers.py` defines `Layer.name`, `fit(frame) -> None`, `apply(frame) -> pd.Series`; factories receive `context={"conn": connection, "lineups": lineups}`. Frames include p, won, match/event/section/region/international/team IDs. Each reported frozen model fits each requested layer on stage-1 rows only, applies it to validation/holdout, and reports `<model>+<layer>` alongside its base. `LAYERS = {"none": IdentityLayer}`; `--layers none` is default and reproduces base probabilities.

Run `uv run python scripts/evaluate_elo.py --tune-from 2023-01-01 --tune-to 2025-09-01 --validate-from 2025-09-01 --layers none`; flags: `--db`, `--out`, `--models` comma list (default all except coin), `--jobs` (default min(cpu,8)), optional `--k-grid` override, `--seed-from`, `--tune-from`, `--tune-to`, `--validate-from`, `--layers`, `--holdout`, `--write-weights`. Process pool tunes (model,params); summaries print wall time in ≤20 lines. Weights store selected models' parameters and fit date in `ratings/elo_weights.json`. Full-data two-stage benchmark and holdout pending.
