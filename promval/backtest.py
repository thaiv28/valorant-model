"""Kalshi taker backtest with unrounded fees and match-level settlement.

Quotes are oriented to VLR team1. Fills assume the last pre-start hourly ask/bid,
with unlimited depth and no slippage. Each summary is an independent $50 path.
"""

import numpy as np
import pandas as pd

from promval.evaluation import interval, resamples


def fee(cost):
    """Unrounded Kalshi taker fee per contract: 0.07 * c * (1 - c)."""
    return 0.07 * cost * (1 - cost)


def select_bets(frame, probability="p"):
    """Choose the larger positive after-fee edge; skip incomplete quotes.

    Returned ``cost`` includes fees, ``fraction`` is full Kelly, and ``profit``
    is realized profit for a flat $1 all-in stake.
    """
    bets = frame.copy()
    for name in ("ask", "bid", probability, "won", "match_id", "start_utc"):
        if name not in bets:
            bets[name] = np.nan
    ask = pd.to_numeric(bets["ask"], errors="coerce")
    other_ask = 1 - pd.to_numeric(bets["bid"], errors="coerce")
    valid = ask.between(0, 1, inclusive="neither") & other_ask.between(
        0, 1, inclusive="neither"
    )
    bets = bets.loc[valid].copy()
    ask, other_ask = ask.loc[valid], other_ask.loc[valid]
    p = bets[probability].astype(float)
    first_edge = p - ask - fee(ask)
    second_edge = 1 - p - other_ask - fee(other_ask)
    first = first_edge >= second_edge
    bets["side"] = np.where(first, 1, 2)
    bets["price"] = np.where(first, ask, other_ask)
    bets["cost"] = bets["price"] + fee(bets["price"])
    bets["edge"] = np.where(first, first_edge, second_edge)
    bets = bets.loc[bets["edge"] > 0].copy()
    bets["fraction"] = bets["edge"] / (1 - bets["cost"])
    bets["side_won"] = np.where(bets["side"] == 1, bets["won"], 1 - bets["won"])
    bets["profit"] = bets["side_won"] / bets["cost"] - 1
    return bets.reset_index(drop=True)


def kelly_path(bets, initial=50.0):
    """Settle each match together, sizing all its bets from pre-match capital.

    Returns the settled bankroll path (including initial capital), maximum
    fractional drawdown, and largest single all-in stake in dollars.
    """
    bankroll = float(initial)
    path = [bankroll]
    largest = 0.0
    if not bets.empty:
        ordered = bets.sort_values("start_utc", kind="stable")
        for _, match in ordered.groupby("match_id", sort=False):
            fractions = match["fraction"].to_numpy(dtype=float)
            fractions = fractions / max(1.0, fractions.sum())
            stakes = bankroll * fractions
            largest = max(largest, float(stakes.max()))
            bankroll += float(np.dot(stakes, match["profit"]))
            # Prevent tiny negative balances from floating-point cancellation.
            bankroll = max(0.0, bankroll)
            path.append(bankroll)
    values = np.asarray(path)
    peaks = np.maximum.accumulate(values)
    drawdown = float(np.max((peaks - values) / peaks))
    return path, drawdown, largest


# Prometheus's pregame execution limits (LoL, 2026-10-28): full Kelly, at most
# 10% of capital per fixture, $250 per order and per fixture, $1k exposure,
# $2k per UTC day, from a $50 seed; no orders once capital is $0.
LOL_SIZING = {
    "kelly_fraction": 1.0,
    "fixture_fraction": 0.10,
    "order_cap": 250.0,
    "fixture_cap": 250.0,
    "exposure_cap": 1000.0,
    "day_cap": 2000.0,
}


def capped_path(bets, initial=50.0, sizing=LOL_SIZING):
    """Kelly with Prometheus-style caps, sized from start-of-day capital.

    Matches on one UTC day overlap, so every bet that day is sized from the
    capital at the day's start and the day's stakes (open exposure) are capped;
    all settle at the end of the day. Returns the same tuple as `kelly_path`.
    """
    bankroll = float(initial)
    path = [bankroll]
    largest = 0.0
    if not bets.empty:
        ordered = bets.assign(
            day=pd.to_datetime(bets["start_utc"], utc=True).dt.strftime("%Y-%m-%d")
        ).sort_values("start_utc", kind="stable")
        day_limit = min(sizing["day_cap"], sizing["exposure_cap"])
        for _, day in ordered.groupby("day", sort=True):
            capital = bankroll
            if capital <= 0:
                path.append(bankroll)
                continue
            spent, result = 0.0, 0.0
            for _, match in day.groupby("match_id", sort=False):
                stakes = (
                    capital
                    * sizing["kelly_fraction"]
                    * match["fraction"].to_numpy(dtype=float)
                )
                stakes = np.minimum(stakes, sizing["order_cap"])
                fixture_limit = min(
                    sizing["fixture_fraction"] * capital, sizing["fixture_cap"]
                )
                limit = min(fixture_limit, day_limit - spent)
                total = stakes.sum()
                if total <= 0 or limit <= 0:
                    continue
                if total > limit:
                    stakes = stakes * (limit / total)
                spent += float(stakes.sum())
                largest = max(largest, float(stakes.max()))
                result += float(np.dot(stakes, match["profit"]))
            bankroll = max(0.0, bankroll + result)
            path.append(bankroll)
    values = np.asarray(path)
    peaks = np.maximum.accumulate(values)
    with np.errstate(invalid="ignore", divide="ignore"):
        drawdown = float(np.nanmax(np.where(peaks > 0, (peaks - values) / peaks, 0)))
    return path, drawdown, largest


def summarize(frame, n_resamples=2000, seed=0, probability="p", sizing="lol"):
    """Flat ROI with whole-match bootstrap and a Kelly path (`lol` caps or `full`)."""
    bets = select_bets(frame, probability=probability)
    path, drawdown, largest = capped_path(bets) if sizing == "lol" else kelly_path(bets)
    low = high = roi = mean_edge = float("nan")
    if not bets.empty:
        profits = bets["profit"].to_numpy()
        codes, labels = pd.factorize(bets["match_id"])
        sums = np.bincount(codes, weights=profits)
        counts = np.bincount(codes)
        draws = [
            sums[pick].sum() / counts[pick].sum()
            for pick in resamples(len(labels), n_resamples, seed)
        ]
        low, high = interval(draws)
        roi = float(profits.mean())
        mean_edge = float(bets["edge"].mean())
    return {
        "bets": len(bets),
        "matches": bets["match_id"].nunique() if not bets.empty else 0,
        "mean_edge": mean_edge,
        "flat_roi": roi,
        "roi_low": float(low),
        "roi_high": float(high),
        "bankroll": path[-1],
        "multiple": path[-1] / 50.0,
        "max_drawdown": drawdown,
        "largest_stake": largest,
    }
