"""Offline Elo selection and benchmark against coin and cached Kalshi prices."""

import argparse
import gzip
import json
import math
import os
import sqlite3
import sys
import time
from concurrent.futures import ProcessPoolExecutor
from dataclasses import dataclass
from itertools import product
from pathlib import Path

import numpy as np
import pandas as pd

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))

from promval.backtest import summarize
from promval.blend import walk_forward
from promval.evaluation import (
    HOLDOUT_START,
    ece,
    game_losses,
    paired_bootstrap,
    series_probability,
)
from promval.kalshi.collect import data_dir
from promval.ratings.models import MODELS, PARAM_GRIDS
from promval.ratings.regions import macro_region
from promval.ratings.replay import load_lineups, load_maps, replay


@dataclass(frozen=True)
class QuoteRule:
    """Which hourly quote stands for the price a bot could have traded.

    `tradeable` (the default for reports): the first candle ending at least
    `open_delay_minutes` after the market opened, no later than `buffer_hours` before the
    scheduled start (so no veto or lineup news), whose bid/ask spread is at most
    `max_spread`. `prestart`: the last candle ending at or before the start,
    which can already price the veto.
    """

    mode: str = "prestart"
    max_spread: float = 0.06
    open_delay_minutes: float = 30.0
    buffer_hours: float = 2.0


PRESTART = QuoteRule()
TRADEABLE = QuoteRule("tradeable")


def candle_quote(candles, start_utc, open_time=None, rule=PRESTART):
    """(bid, ask) closes in dollars under `rule`, or None when no candle qualifies."""
    if isinstance(candles, dict):
        candles = candles.get("candlesticks", [])
    start = pd.Timestamp(start_utc)
    if rule.mode == "tradeable":
        if open_time is None:
            return None
        delay = pd.Timedelta(minutes=rule.open_delay_minutes)
        earliest = (pd.Timestamp(open_time) + delay).timestamp()
        cutoff = (start - pd.Timedelta(hours=rule.buffer_hours)).timestamp()
    else:
        earliest, cutoff = float("-inf"), start.timestamp()
    valid = []
    for candle in candles:
        end = candle.get("end_period_ts")
        if end is None or end > cutoff or end < earliest:
            continue
        closes = []
        for side in ("yes_bid", "yes_ask"):
            quote = candle.get(side) or {}
            value = quote.get("close_dollars")
            if value is None:
                value = quote.get("close")
            try:
                value = float(value)
            except (TypeError, ValueError):
                break
            if not math.isfinite(value) or not 0 <= value <= 1:
                break
            closes.append(value)
        if len(closes) == 2:
            if rule.mode == "tradeable" and not (
                0 < closes[0] < closes[1] < 1
                and closes[1] - closes[0] <= rule.max_spread + 1e-9
            ):
                continue
            valid.append((end, tuple(closes)))
    if not valid:
        return None
    pick = min if rule.mode == "tradeable" else max
    return pick(valid, key=lambda item: item[0])[1]


def candle_mid(candles, start_utc):
    quote = candle_quote(candles, start_utc)
    return sum(quote) / 2 if quote is not None else None


def series_rows(maps):
    """Use the first map's pre-update chance and the recorded series winner."""
    first = maps.drop_duplicates("match_id").copy()
    first = first[
        first.best_of.notna()
        & (first.best_of > 0)
        & (first.best_of % 2 == 1)
        & first.series_won.notna()
    ].copy()
    first["p"] = [series_probability(p, int(n)) for p, n in zip(first.p, first.best_of)]
    first["won"] = first.series_won.astype(int)
    return first


def kalshi_rows(conn, maps, series, directory, rule=PRESTART):
    """One usable market per event, preferring the team1-side contract."""
    tables = {r[0] for r in conn.execute("SELECT name FROM sqlite_master")}
    if not {"kalshi_links", "kalshi_markets", "team_aliases"} <= tables:
        return pd.DataFrame()
    markets = pd.read_sql(
        """SELECT l.event_ticker, l.match_id, l.game_id, l.kind,
                  k.ticker, k.open_time, a.vlr_team_id
           FROM kalshi_links l JOIN kalshi_markets k USING (event_ticker)
           JOIN team_aliases a USING (competitor_id)
           WHERE l.match_id IS NOT NULL ORDER BY k.ticker""",
        conn,
    )
    map_index = maps.set_index("game_id")
    # Kalshi quotes are taken before the match, so maps are compared with the
    # model's pre-match chance (the first map's), not one updated on earlier maps.
    prematch = maps.sort_values(["match_id", "order"]).groupby("match_id").p.first()
    series_index = series.set_index("match_id")
    candidates = []
    for market in markets.itertuples(index=False):
        index = series_index if market.kind == "series" else map_index
        key = market.match_id if market.kind == "series" else market.game_id
        if key not in index.index:
            continue
        row = index.loc[key]
        if market.kind == "map" and row.match_id != market.match_id:
            continue
        if market.vlr_team_id not in (row.team1_id, row.team2_id):
            continue
        path = directory / "candles" / f"{market.ticker}.json.gz"
        if not path.exists():
            continue
        with gzip.open(path, "rt") as handle:
            quote = candle_quote(
                json.load(handle), row.start_utc, market.open_time, rule
            )
        if quote is None:
            continue
        bid, ask = quote
        mid = (bid + ask) / 2
        team1 = market.vlr_team_id == row.team1_id
        candidate = row.to_dict()
        if market.kind == "map":
            candidate["p"] = prematch[market.match_id]
        candidate.update(
            match_id=market.match_id,
            kind=market.kind,
            event_ticker=market.event_ticker,
            market_p=mid if team1 else 1 - mid,
            team1_side=team1,
            ask=ask if team1 else 1 - bid,
            bid=bid if team1 else 1 - ask,
        )
        candidates.append(candidate)
    if not candidates:
        return pd.DataFrame()
    return (
        pd.DataFrame(candidates)
        .sort_values("team1_side", ascending=False, kind="stable")
        .drop_duplicates("event_ticker")
        .reset_index(drop=True)
    )


def sections(frame):
    yield "all", frame
    for name in ("vct", "vcl", "gc", "t3", "collegiate", "offseason", "unknown"):
        yield name, frame[frame.section == name]
    for flag in (1, 0):
        yield f"international={flag}", frame[frame.international == flag]


def metrics_table(frame, model):
    lines = [
        "| Model | Section | Rows | Log loss | Brier | Accuracy | ECE |",
        "|---|---|---:|---:|---:|---:|---:|",
    ]
    for name, rows in sections(frame):
        if rows.empty:
            lines.append(f"| {model} | {name} | 0 | — | — | — | — |")
            continue
        scores = game_losses(rows.p, rows.won).mean()
        lines.append(
            f"| {model} | {name} | {len(rows)} | {scores.log_loss:.6f} | "
            f"{scores.brier:.6f} | {scores.accuracy:.6f} | {ece(rows.p, rows.won):.6f} |"
        )
    return "\n".join(lines)


def comparison_table(frame, other, label, model="team_elo", by_section=True):
    lines = [
        f"| Section | Rows | {model} log loss | {label} log loss | Difference | 95% interval | Significant |",
        "|---|---:|---:|---:|---:|---|---|",
    ]
    for name, rows in sections(frame) if by_section else [("all", frame)]:
        if rows.empty:
            continue
        model_loss = game_losses(rows.p, rows.won).log_loss
        other_p = rows[other] if other in rows else np.full(len(rows), 0.5)
        other_loss = game_losses(other_p, rows.won).log_loss
        mean, low, high = paired_bootstrap(
            model_loss, other_loss, clusters=rows.match_id
        )
        significant = "yes" if low > 0 or high < 0 else "no"
        lines.append(
            f"| {name} | {len(rows)} | {model_loss.mean():.6f} | "
            f"{other_loss.mean():.6f} | {mean:.6f} | [{low:.6f}, {high:.6f}] | {significant} |"
        )
    return "\n".join(lines)


def market_slices(frame):
    for kind in ("series", "map"):
        subset = frame[frame.kind == kind] if not frame.empty else frame
        yield kind, "all", subset
        for section in ("vct", "vcl", "gc", "t3", "collegiate", "offseason"):
            yield (
                kind,
                section,
                subset[subset.section == section] if not subset.empty else subset,
            )
        for flag in (1, 0):
            yield (
                kind,
                f"international={flag}",
                subset[subset.international == flag] if not subset.empty else subset,
            )


def market_tables(frame, probability="p"):
    if probability == "p_blend":
        frame = frame[frame.blend_fitted]
    loss_lines = [
        "| Kind | Slice | Rows | Model log loss | Kalshi log loss | Difference [95% interval] | Significant |",
        "|---|---|---:|---:|---:|---|---|",
    ]
    bet_lines = [
        "| Kind | Slice | Bets | Matches | Mean edge | Flat ROI [95% interval] | Kelly, LoL caps ($50 start) | Multiple | Max drawdown | Largest stake |",
        "|---|---|---:|---:|---:|---|---:|---:|---:|---:|",
    ]
    for kind, label, rows in market_slices(frame):
        if rows.empty:
            loss_lines.append(f"| {kind} | {label} | 0 | — | — | — | — |")
        else:
            model_loss = game_losses(rows[probability], rows.won).log_loss
            market_loss = game_losses(rows.market_p, rows.won).log_loss
            diff, low, high = paired_bootstrap(
                model_loss, market_loss, clusters=rows.match_id
            )
            significant = "yes" if low > 0 or high < 0 else "no"
            loss_lines.append(
                f"| {kind} | {label} | {len(rows)} | {model_loss.mean():.6f} | "
                f"{market_loss.mean():.6f} | {diff:.6f} [{low:.6f}, {high:.6f}] | {significant} |"
            )
        stats = summarize(rows, probability=probability)
        edge = f"{stats['mean_edge']:.4f}" if stats["bets"] else "—"
        roi = (
            f"{stats['flat_roi']:.2%} [{stats['roi_low']:.2%}, {stats['roi_high']:.2%}]"
            if stats["bets"]
            else "—"
        )
        bet_lines.append(
            f"| {kind} | {label} | {stats['bets']} | {stats['matches']} | {edge} | {roi} | "
            f"${stats['bankroll']:.2f} | {stats['multiple']:.3f}× | "
            f"{stats['max_drawdown']:.2%} | ${stats['largest_stake']:.2f} |"
        )
    # Prometheus caps apply per fixture across its series and map markets.
    stats = summarize(frame, probability=probability)
    if stats["bets"]:
        bet_lines.append(
            f"| series+map | all | {stats['bets']} | {stats['matches']} | "
            f"{stats['mean_edge']:.4f} | {stats['flat_roi']:.2%} "
            f"[{stats['roi_low']:.2%}, {stats['roi_high']:.2%}] | "
            f"${stats['bankroll']:.2f} | {stats['multiple']:.3f}× | "
            f"{stats['max_drawdown']:.2%} | ${stats['largest_stake']:.2f} |"
        )
    return "\n".join(loss_lines), "\n".join(bet_lines)


def summary_table(markets):
    labels = [
        f"{kind}{suffix} {metric}"
        for suffix in ("", " blended")
        for kind in ("Series", "Map")
        for metric in ("Δ log loss", "flat ROI", "Kelly (LoL caps) $")
    ]
    lines = ["| Model | " + " | ".join(labels) + " |", "|---|" + "---:|" * len(labels)]
    for name, frame in markets.items():
        cells = [name]
        for probability in ("p", "p_blend"):
            for kind in ("series", "map"):
                rows = frame[frame.kind == kind] if not frame.empty else frame
                if probability == "p_blend":
                    rows = rows[rows.blend_fitted]
                stats = summarize(rows, probability=probability)
                diff = (
                    (
                        game_losses(rows[probability], rows.won).log_loss.mean()
                        - game_losses(rows.market_p, rows.won).log_loss.mean()
                    )
                    if not rows.empty
                    else None
                )
                cells.extend(
                    [
                        f"{diff:.6f}" if diff is not None else "—",
                        f"{stats['flat_roi']:.2%}" if stats["bets"] else "—",
                        f"${stats['bankroll']:.2f}",
                    ]
                )
        lines.append("| " + " | ".join(cells) + " |")
    return "\n".join(lines)


def scored_rows(frame, score_from, holdout=False):
    """Scoring windows never overlap; rating warmup is handled by replay."""
    dates = pd.to_datetime(frame.start_utc, utc=True)
    boundary = pd.Timestamp(HOLDOUT_START, tz="UTC")
    mask = dates >= pd.Timestamp(score_from, tz="UTC")
    return frame[mask & ((dates >= boundary) if holdout else (dates < boundary))]


def parameter_grid(model, k_grid=None):
    grid = dict(PARAM_GRIDS[model])
    if k_grid is not None and "k" in grid:
        grid["k"] = k_grid
    return [dict(zip(grid, values)) for values in product(*grid.values())]


def initialize_worker(maps, lineups, score_from):
    global _WORKER_MAPS, _WORKER_LINEUPS, _WORKER_SCORE_FROM
    _WORKER_MAPS, _WORKER_LINEUPS, _WORKER_SCORE_FROM = maps, lineups, score_from


def tune_candidate(task):
    """Return just a scalar score, avoiding retention of all candidate replays."""
    name, params = task
    candidate = replay(_WORKER_MAPS, MODELS[name](lineups=_WORKER_LINEUPS, **params))
    tuning = scored_rows(candidate, _WORKER_SCORE_FROM)
    return name, params, float(game_losses(tuning.p, tuning.won).log_loss.mean())


def mean_loss(frame):
    return float(game_losses(frame.p, frame.won).log_loss.mean())


def main(argv=None):
    started = time.perf_counter()
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--db", type=Path, default=Path("db/valorant.db"))
    parser.add_argument("--out", type=Path, default=Path("docs/elo_backtest.md"))
    parser.add_argument("--models", default=",".join(n for n in MODELS if n != "coin"))
    parser.add_argument(
        "--report-models",
        help="comma list; default team_elo, best three, both Glicko variants",
    )
    parser.add_argument("--jobs", type=int, default=min(os.cpu_count() or 1, 8))
    parser.add_argument("--k-grid", help="optional K grid override for every model")
    parser.add_argument("--score-from", default="2023-01-01")
    parser.add_argument("--blend-min", type=int, default=100)
    parser.add_argument(
        "--quote",
        choices=("tradeable", "prestart"),
        default="tradeable",
        help="Kalshi price: first tight quote ≥30 min after listing and ≥2 h "
        "before start (default), or the last candle before start",
    )
    parser.add_argument("--max-spread", type=float, default=0.06)
    parser.add_argument("--holdout", action="store_true")
    parser.add_argument("--write-weights", action="store_true")
    args = parser.parse_args(argv)
    quote_rule = QuoteRule(args.quote, max_spread=args.max_spread)
    try:
        k_grid = (
            None
            if args.k_grid is None
            else tuple(float(k) for k in args.k_grid.split(","))
        )
        if k_grid is not None and (
            not k_grid or any(not math.isfinite(k) or k <= 0 for k in k_grid)
        ):
            raise ValueError
        score_start = pd.Timestamp(args.score_from, tz="UTC")
        if (
            score_start >= pd.Timestamp(HOLDOUT_START, tz="UTC")
            or args.jobs < 1
            or args.blend_min < 1
        ):
            raise ValueError
    except (ValueError, TypeError):
        parser.error(
            "use positive finite K values, --jobs >= 1, --blend-min >= 1 and --score-from before 2026-07-01"
        )
    requested = [name.strip() for name in args.models.split(",")]
    if any(name not in MODELS for name in requested):
        parser.error("unknown model in --models")
    report_names = (
        None
        if args.report_models is None
        else list(dict.fromkeys(name.strip() for name in args.report_models.split(",")))
    )
    if report_names is not None and any(
        name not in MODELS or name == "coin" for name in report_names
    ):
        parser.error("unknown rating model in --report-models")
    extras = (
        report_names
        if report_names is not None
        else ["player_round_glicko", "player_round_region_glicko"]
    )
    names = list(
        dict.fromkeys(["team_elo", *(n for n in requested if n != "coin"), *extras])
    )
    if not args.db.is_file():
        parser.error(f"database does not exist: {args.db}")
    with sqlite3.connect(args.db) as conn:
        maps = load_maps(conn)
        if not args.holdout:
            maps = maps[pd.to_datetime(maps.start_utc, utc=True) < HOLDOUT_START]
        tuning_maps = scored_rows(maps, args.score_from)
        if tuning_maps.empty:
            parser.error("no tuning maps in the requested scoring window")
        lineups = load_lineups(conn)
        tasks = [
            (name, params) for name in names for params in parameter_grid(name, k_grid)
        ]
        best_params, losses = {}, {}
        if args.jobs == 1:
            initialize_worker(maps, lineups, args.score_from)
            for name, params, loss in map(tune_candidate, tasks):
                if name not in losses or loss < losses[name]:
                    best_params[name], losses[name] = params, loss
        else:
            with ProcessPoolExecutor(
                max_workers=args.jobs,
                initializer=initialize_worker,
                initargs=(maps, lineups, args.score_from),
            ) as pool:
                for name, params, loss in pool.map(tune_candidate, tasks, chunksize=1):
                    if name not in losses or loss < losses[name]:
                        best_params[name], losses[name] = params, loss
        ranked = sorted(names, key=losses.get)
        detailed = (
            report_names
            if report_names is not None
            else list(
                dict.fromkeys(
                    [
                        "team_elo",
                        *ranked[:3],
                        "player_round_glicko",
                        "player_round_region_glicko",
                    ]
                )
            )
        )
        winners = {
            name: replay(maps, MODELS[name](lineups=lineups, **best_params[name]))
            for name in names
        }
        coin = replay(maps, MODELS["coin"]())
        fit_through = tuning_maps.start_utc.max()[:10]
        unknown = sum(macro_region(code) is None for code in maps.region)
        report = [
            "# Elo variants benchmark",
            "Parameters minimize tuning map log loss across all sections. Replay predicts before update; "
            "2021–22 seed ratings only. "
            f"Scoring starts {args.score_from}; tuning ends before {HOLDOUT_START}. "
            "Holdout is scored only with --holdout and never selects parameters. "
            "Series use the first map prediction and independent maps in an odd best-of; "
            "missing/even best-of or unknown results are skipped. "
            "Accuracy gives 0.5 predictions half credit; ECE uses 10 equal-width bins. "
            "Log loss clips probabilities at 1e-6. Paired bootstrap uses 2,000 resamples, "
            "seed 0, clustered by match_id. Differences are the named model minus its comparator; "
            "negative favors the model. Significance requires a 95% percentile interval excluding zero. "
            "Tuning scores are selection diagnostics, not independent evidence of improvement.",
            f"Fit through {fit_through}. Unknown host-region map rows: {unknown} (including missing/un).",
            "## Leaderboard (tuning only)\n\n"
            "| Model | Best params | Map log loss | Series log loss | Rows |\n"
            "|---|---|---:|---:|---:|\n"
            + "\n".join(
                f"| {name} | {json.dumps(best_params[name], sort_keys=True)} | {losses[name]:.6f} | "
                f"{mean_loss(series_rows(scored_rows(winners[name], args.score_from))):.6f} | {len(tuning_maps)} |"
                for name in ranked
            ),
            (
                f"Kalshi uses the first hourly bid/ask (midpoint for log loss, ask/bid for bets) "
                f"ending ≥30 min after the market opened and ≥2 h before the scheduled start, "
                f"with a spread ≤ {args.max_spread:.2f}: a price a bot could trade before any veto. "
                "Markets without such a quote are skipped. "
                if args.quote == "tradeable"
                else "Kalshi uses the last valid hourly bid/ask midpoint ending at or before "
                "match start (can already price the veto). "
            )
            + "oriented to team1 using aliases. One contract per event, preferring team1. "
            "Compare identical rows; map predictions use the first map's pre-match chance. "
            "Missing links, aliases or candles are skipped. Backtests are in-sample on the tuning window "
            "(parameters were selected there). Fills are assumed at the hourly candle’s ask/bid with "
            "no depth limit or slippage; unplayed maps are not in the rows. "
            "Kalshi taker fees use unrounded f(c)=0.07×c×(1−c) per contract. Buy the larger positive "
            "after-fee edge, otherwise skip; require a two-sided quote with both buy costs in (0,1). "
            "Full Kelly uses fraction (q−c′)/(1−c′), c′=c+f(c). All bets in a match use its starting "
            "bankroll, scaling fractions to sum to at most one, then settle together. Each kind/slice "
            "runs its own $50 path. Drawdown uses settled match balances. Flat stakes are $1 all-in "
            "per bet; ROI intervals resample whole matches 2,000 times, seed 0.",
        ]
        blended_markets, monthly_fits = {}, {}
        for name in detailed:
            source = winners[name]
            source = source[pd.to_datetime(source.start_utc, utc=True) >= score_start]
            market = kalshi_rows(
                conn, source, series_rows(source), data_dir(), quote_rule
            )
            blended_markets[name], monthly_fits[name] = walk_forward(
                market, args.score_from, args.blend_min
            )
        windows = [("Tuning", False)]
        if args.holdout:
            windows.append(("Holdout", True))
        for title, holdout in windows:
            report.append(f"## {title}")
            selected = {
                name: scored_rows(frame, args.score_from, holdout)
                for name, frame in winners.items()
            }
            coin_rows = scored_rows(coin, args.score_from, holdout)
            for kind in ("Maps", "Series"):
                frames = (
                    selected
                    if kind == "Maps"
                    else {n: series_rows(f) for n, f in selected.items()}
                )
                coin_frame = coin_rows if kind == "Maps" else series_rows(coin_rows)
                report.extend([f"### {kind}", metrics_table(coin_frame, "coin")])
                for name in detailed:
                    report.append(metrics_table(frames[name], name))
                    report.append(f"{name} − coin (paired log loss):")
                    report.append(
                        comparison_table(frames[name], "coin_p", "coin", name)
                    )
                for name in names:
                    if name == "team_elo":
                        continue
                    frame = frames[name].merge(
                        frames["team_elo"][["game_id", "p"]].rename(
                            columns={"p": "baseline_p"}
                        ),
                        on="game_id",
                        validate="one_to_one",
                    )
                    report.append(f"{name} − team_elo (paired log loss):")
                    report.append(
                        comparison_table(
                            frame, "baseline_p", "team_elo", name, by_section=False
                        )
                    )
            markets = {
                name: scored_rows(frame, args.score_from, holdout)
                if not frame.empty
                else frame
                for name, frame in blended_markets.items()
            }
            if not holdout:
                top_summary = summary_table(markets)
                report.insert(
                    1, "## Combined summary (tuning, all sections)\n\n" + top_summary
                )
            for name, market in markets.items():
                report.append(f"### {name}: Kalshi comparison and returns")
                if market.empty:
                    report.append("no linked markets (rows: 0)")
                loss_table, bet_table = market_tables(market)
                report.extend(
                    [
                        "#### Log loss vs Kalshi",
                        loss_table,
                        "#### Full-Kelly returns",
                        bet_table,
                    ]
                )
                excluded = int((~market.blend_fitted).sum())
                loss_table, bet_table = market_tables(market, probability="p_blend")
                fits = monthly_fits[name]
                fit_lines = [
                    "| Month | Kind | n | a | b | Status |",
                    "|---|---|---:|---:|---:|---|",
                ]
                for row in fits.itertuples(index=False):
                    fit_lines.append(
                        f"| {row.month} | {row.kind} | {row.n} | {row.a:.6f} | {row.b:.6f} | "
                        + ("fitted |" if row.fitted else "unfitted |")
                    )
                report.extend(
                    [
                        "#### Monthly market blend fits",
                        f"UTC monthly fits use earlier rows of the same kind from {args.score_from}, "
                        f"excluding holdout; minimum {args.blend_min} rows. "
                        "logit(p_blend) = a·logit(mid) + b·(logit(p_model) − logit(mid)); "
                        "inputs clipped to [0.01, 0.99], no intercept, ridge 1e-6. "
                        f"Unfitted rows use mid unchanged; excluded from blended tables: {excluded} rows. "
                        "Rating parameters remain selected on the tuning window.",
                        "\n".join(fit_lines),
                        "#### Log loss vs Kalshi (blended)",
                        loss_table,
                        "#### Full-Kelly returns (blended)",
                        bet_table,
                    ]
                )
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text("\n\n".join(report) + "\n")
    if args.write_weights:
        path = REPO / "promval/ratings/elo_weights.json"
        path.write_text(
            json.dumps(
                {
                    name: {**params, "fit_through": fit_through}
                    for name, params in best_params.items()
                },
                indent=2,
            )
            + "\n"
        )
    print(top_summary)
    print(f"Report: {args.out}")
    print(f"Total wall time: {time.perf_counter() - started:.2f}s")
    return best_params


if __name__ == "__main__":
    main()
