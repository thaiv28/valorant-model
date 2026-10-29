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


def select_bets(frame):
    """Choose the larger positive after-fee edge; skip incomplete quotes.

    Returned ``cost`` includes fees, ``fraction`` is full Kelly, and ``profit``
    is realized profit for a flat $1 all-in stake.
    """
    bets = frame.copy()
    for name in ("ask", "bid", "p", "won", "match_id", "start_utc"):
        if name not in bets:
            bets[name] = np.nan
    ask = pd.to_numeric(bets["ask"], errors="coerce")
    other_ask = 1 - pd.to_numeric(bets["bid"], errors="coerce")
    valid = ask.between(0, 1, inclusive="neither") & other_ask.between(
        0, 1, inclusive="neither"
    )
    bets = bets.loc[valid].copy()
    ask, other_ask = ask.loc[valid], other_ask.loc[valid]
    p = bets["p"].astype(float)
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


def summarize(frame, n_resamples=2000, seed=0):
    """Flat ROI with whole-match bootstrap and a separate full-Kelly path."""
    bets = select_bets(frame)
    path, drawdown, largest = kelly_path(bets)
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
