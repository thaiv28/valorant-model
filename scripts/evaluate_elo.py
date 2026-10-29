"""Offline Elo selection and benchmark against coin and cached Kalshi prices."""

import argparse
import gzip
import json
import math
import sqlite3
import sys
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
from promval.ratings.models import MODELS
from promval.ratings.replay import load_maps, replay


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


def comparison_table(frame, other, label):
    lines = [
        f"| Section | Rows | team_elo log loss | {label} log loss | Difference | 95% interval | Significant |",
        "|---|---:|---:|---:|---:|---|---|",
    ]
    for name, rows in sections(frame):
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


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--db", type=Path, default=Path("db/valorant.db"))
    parser.add_argument("--out", type=Path, default=Path("docs/elo_backtest.md"))
    parser.add_argument("--k-grid", default="16,24,32,40,48,64")
    parser.add_argument("--score-from", default="2023-01-01")
    parser.add_argument("--holdout", action="store_true")
    parser.add_argument("--write-weights", action="store_true")
    args = parser.parse_args(argv)
    try:
        grid = [float(k) for k in args.k_grid.split(",")]
        if not grid or any(not math.isfinite(k) or k <= 0 for k in grid):
            raise ValueError
        score_start = pd.Timestamp(args.score_from, tz="UTC")
        if score_start >= pd.Timestamp(HOLDOUT_START, tz="UTC"):
            raise ValueError
    except (ValueError, TypeError):
        parser.error("use positive finite K values and --score-from before 2026-07-01")
    if not args.db.is_file():
        parser.error(f"database does not exist: {args.db}")
    with sqlite3.connect(args.db) as conn:
        maps = load_maps(conn)
        if not args.holdout:
            maps = maps[pd.to_datetime(maps.start_utc, utc=True) < HOLDOUT_START]
        coin = replay(maps, MODELS["coin"]())
        candidates, losses = {}, {}
        for k in grid:
            candidate = replay(maps, MODELS["team_elo"](k=k))
            tuning = scored_rows(candidate, args.score_from)
            if tuning.empty:
                parser.error("no tuning maps in the requested scoring window")
            candidates[k] = candidate
            losses[k] = game_losses(tuning.p, tuning.won).log_loss.mean()
        best_k = min(grid, key=losses.get)
        best = candidates[best_k]
        fit_through = scored_rows(best, args.score_from).start_utc.max()[:10]
        report = [
            "# Elo v1 benchmark",
            "One global team Elo pool; initial rating 1500, scale 400, binary map wins. "
            "Replay order: match start (UTC), match ID, map order; predict before update. "
            "2021–22 seed ratings only. Selection minimizes map log loss over all tuning sections. "
            f"Scoring starts {args.score_from}; tuning ends before {HOLDOUT_START}. "
            "Holdout is scored only with --holdout and never selects K. "
            "Series use the first map's prediction, independent maps, and an odd best-of; "
            "missing/even best-of and unknown series results are skipped. "
            "Accuracy gives 0.5 predictions half credit; ECE uses 10 equal-width bins. "
            "Log loss clips probabilities at 1e-6. "
            "Paired bootstrap: 2,000 resamples, seed 0, whole matches clustered by match_id. "
            "Differences are team_elo minus comparator; negative favors Elo. "
            "Significance means the 95% percentile interval excludes zero. "
            "Tuning scores are selection diagnostics, not independent evidence of improvement.",
            f"Selected K: {best_k:g}; fit through {fit_through}.",
            "## K grid (tuning only)\n\n| K | Map log loss |\n|---:|---:|\n"
            + "\n".join(f"| {k:g} | {losses[k]:.6f} |" for k in grid),
            "Kalshi: use the last valid hourly bid/ask midpoint ending at or before VLR "
            "match start; orient to team1 through competitor aliases. One contract per event, "
            "preferring team1, otherwise complementing team2. Compare on identical rows. "
            "Like the market quotes, map predictions here are pre-match (the first map's "
            "chance), so they never use earlier maps of the same match. "
            "Missing links, aliases or candles are skipped. This measures predictive loss, "
            "without fees or execution assumptions.",
        ]
        windows = [("Tuning", False)]
        if args.holdout:
            windows.append(("Holdout", True))
        for title, holdout in windows:
            selected = scored_rows(best, args.score_from, holdout)
            baseline = scored_rows(coin, args.score_from, holdout)
            model_series = series_rows(selected)
            report.append(f"## {title}")
            for kind, frame, coin_frame in (
                ("Maps", selected, baseline),
                ("Series", model_series, series_rows(baseline)),
            ):
                report.extend(
                    [
                        f"### {kind}",
                        metrics_table(frame, "team_elo"),
                        metrics_table(coin_frame, "coin"),
                        "team_elo − coin (paired log loss):",
                        comparison_table(frame, "coin_p", "coin"),
                    ]
                )
            market = kalshi_rows(conn, selected, model_series, data_dir())
            for kind in ("series", "map"):
                report.append(f"### Kalshi {kind}")
                subset = market[market.kind == kind] if not market.empty else market
                report.append(
                    "no linked markets (rows: 0)"
                    if subset.empty
                    else comparison_table(subset, "market_p", "Kalshi")
                )
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text("\n\n".join(report) + "\n")
    if args.write_weights:
        path = REPO / "promval/ratings/elo_weights.json"
        path.write_text(
            json.dumps(
                {"team_elo": {"k": best_k, "fit_through": fit_through}}, indent=2
            )
            + "\n"
        )
    print(f"Selected team_elo K={best_k:g}; tuning log loss={losses[best_k]:.6f}")
    print(
        f"Tuning maps={len(scored_rows(best, args.score_from))}; fit through {fit_through}"
    )
    if args.holdout:
        print(f"Holdout maps={len(scored_rows(best, args.score_from, True))}")
    print(f"Report: {args.out}")
    return best_k


if __name__ == "__main__":
    main()
