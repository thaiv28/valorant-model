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
from itertools import product
from pathlib import Path

import numpy as np
import pandas as pd

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))

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


def candle_mid(candles, start_utc):
    """Last valid bid/ask close at or before match start, in dollar units."""
    if isinstance(candles, dict):
        candles = candles.get("candlesticks", [])
    cutoff = pd.Timestamp(start_utc).timestamp()
    valid = []
    for candle in candles:
        end = candle.get("end_period_ts")
        if end is None or end > cutoff:
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
            valid.append((end, sum(closes) / 2))
    return max(valid, key=lambda item: item[0])[1] if valid else None


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


def kalshi_rows(conn, maps, series, directory):
    """One usable market per event, preferring the team1-side contract."""
    tables = {r[0] for r in conn.execute("SELECT name FROM sqlite_master")}
    if not {"kalshi_links", "kalshi_markets", "team_aliases"} <= tables:
        return pd.DataFrame()
    markets = pd.read_sql(
        """SELECT l.event_ticker, l.match_id, l.game_id, l.kind,
                  k.ticker, a.vlr_team_id
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
            mid = candle_mid(json.load(handle), row.start_utc)
        if mid is None:
            continue
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
    for flag in (0, 1):
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
    parser.add_argument("--jobs", type=int, default=min(os.cpu_count() or 1, 8))
    parser.add_argument("--k-grid", help="optional K grid override for every model")
    parser.add_argument("--score-from", default="2023-01-01")
    parser.add_argument("--holdout", action="store_true")
    parser.add_argument("--write-weights", action="store_true")
    args = parser.parse_args(argv)
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
        if score_start >= pd.Timestamp(HOLDOUT_START, tz="UTC") or args.jobs < 1:
            raise ValueError
    except (ValueError, TypeError):
        parser.error(
            "use positive finite K values, --jobs >= 1 and --score-from before 2026-07-01"
        )
    requested = [name.strip() for name in args.models.split(",")]
    if any(name not in MODELS for name in requested):
        parser.error("unknown model in --models")
    names = list(dict.fromkeys(["team_elo", *(n for n in requested if n != "coin")]))
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
        detailed = ["team_elo", *[name for name in ranked if name != "team_elo"][:3]]
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
            "Kalshi uses the last valid hourly bid/ask midpoint ending at or before match start, "
            "oriented to team1 using aliases. One contract per event, preferring team1. "
            "Compare identical rows; map predictions use the first map's pre-match chance. "
            "Missing links, aliases or candles are skipped; fees and execution are excluded.",
        ]
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
            for name in detailed:
                frame = selected[name]
                market = kalshi_rows(conn, frame, series_rows(frame), data_dir())
                for kind in ("series", "map"):
                    report.append(f"### Kalshi {kind}: {name}")
                    subset = market[market.kind == kind] if not market.empty else market
                    report.append(
                        "no linked markets (rows: 0)"
                        if subset.empty
                        else comparison_table(subset, "market_p", "Kalshi", name)
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
    for name in ranked:
        print(
            f"{name}: {json.dumps(best_params[name], sort_keys=True)}; tuning map log loss={losses[name]:.6f}"
        )
    print(
        f"Tuning maps={len(tuning_maps)}; fit through {fit_through}; unknown region rows={unknown}"
    )
    print(f"Report: {args.out}")
    print(f"Total wall time: {time.perf_counter() - started:.2f}s")
    return best_params


if __name__ == "__main__":
    main()
