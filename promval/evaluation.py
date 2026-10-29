"""Benchmark helpers ported from Prometheus, prometheus/evaluation.py (1–165).

Accuracy gives an exactly 50% prediction half credit. Bootstrap intervals use
paired losses, with whole matches as clusters in the benchmark harness.
"""

from math import comb, exp, log

import numpy as np
import pandas as pd

EPS = 1e-6
HOLDOUT_START = "2026-07-01"


def game_losses(p, won):
    """Per-game accuracy, Brier score and log loss for predicted probabilities."""
    p = np.clip(np.asarray(p, dtype=float), EPS, 1 - EPS)
    won = np.asarray(won, dtype=int)
    # A pick of exactly 50% counts as half right.
    correct = np.where(p == 0.5, 0.5, ((p > 0.5) == (won == 1)).astype(float))
    return pd.DataFrame(
        {
            "accuracy": correct,
            "brier": (p - won) ** 2,
            "log_loss": -(won * np.log(p) + (1 - won) * np.log(1 - p)),
        }
    )


def resamples(units, n_resamples=2000, seed=0):
    """Bootstrap resamples, as arrays of row positions: `units` is a row count
    (rows drawn with replacement) or a list of row-position arrays, one per
    cluster (whole clusters drawn with replacement, their rows kept together).
    Every resample draws once from one generator seeded with `seed`, so a caller
    gets the same draws as the loops this replaced."""
    rng = np.random.default_rng(seed)
    clusters = None if isinstance(units, (int, np.integer)) else list(units)
    n = units if clusters is None else len(clusters)
    for _ in range(n_resamples):
        pick = rng.integers(0, n, n)
        yield pick if clusters is None else np.concatenate([clusters[i] for i in pick])


def interval(values):
    """The 95% percentile interval of bootstrap values: (low, high)."""
    return np.percentile(values, 2.5), np.percentile(values, 97.5)


def ece(p, won, bins=10):
    """Expected calibration error: over equal-width bins of the chance `p`, the
    share of rows in each bin times the gap between its mean chance and its win
    rate."""
    p, won = np.asarray(p, dtype=float), np.asarray(won, dtype=float)
    idx = np.minimum((p * bins).astype(int), bins - 1)
    return sum(
        (idx == b).mean() * abs(p[idx == b].mean() - won[idx == b].mean())
        for b in range(bins)
        if (idx == b).any()
    )


def paired_bootstrap(loss_a, loss_b, n_resamples=2000, seed=0, clusters=None):
    """Mean of (loss_a - loss_b) and its 95% bootstrap interval.

    Both metrics are scored on the same games, so resampling games (not each
    metric separately) gives a much tighter, fairer comparison. Games in a
    series share rating errors, so game-level intervals are too narrow; pass
    series labels as `clusters` to resample whole series together.
    """
    diff = np.asarray(loss_a, dtype=float) - np.asarray(loss_b, dtype=float)
    if clusters is None:
        means = [diff[i].mean() for i in resamples(len(diff), n_resamples, seed)]
    else:
        if len(clusters) != len(diff):
            raise ValueError("clusters and losses must have equal length")
        codes, labels = pd.factorize(np.asarray(clusters))
        sums = np.bincount(codes, weights=diff)
        counts = np.bincount(codes)
        means = [
            sums[pick].sum() / counts[pick].sum()
            for pick in resamples(len(labels), n_resamples, seed)
        ]
    return (diff.mean(), *interval(means))


def _validate_series(p, best_of):
    if best_of < 1 or best_of % 2 != 1:
        raise ValueError("best_of must be a positive odd integer")
    if not 0 <= p <= 1:
        raise ValueError("p must be between 0 and 1")


def _map_chain(p, best_of, m):
    """Propagate live (wins, losses, previous winner) states, absorbing finishes."""
    target = best_of // 2 + 1
    if p in (0, 1):
        return p, [p] * best_of
    z = log(p / (1 - p))
    after = {side: 1 / (1 + exp(-(z + m * side))) for side in (-1, 1)}
    states = {(0, 0, 0): 1.0}
    series_win, slots = 0.0, []
    for _ in range(best_of):
        played = sum(states.values())
        win_mass = sum(
            mass * (p if side == 0 else after[side])
            for (_, _, side), mass in states.items()
        )
        slots.append(win_mass / played)
        following = {}
        for (wins, losses, side), mass in states.items():
            q = p if side == 0 else after[side]
            for won, chance in ((1, q), (0, 1 - q)):
                w, l = wins + won, losses + 1 - won
                weight = mass * chance
                if w == target:
                    series_win += weight
                elif l < target:
                    key = (w, l, 1 if won else -1)
                    following[key] = following.get(key, 0.0) + weight
        states = following
    return series_win, slots


def series_probability(p, best_of, m=0.0):
    """Exact odd best-of win chance with previous-map winner logit bonus m."""
    _validate_series(p, best_of)
    if m != 0:
        return _map_chain(p, best_of, m)[0]
    return sum(
        comb(best_of, wins) * p**wins * (1 - p) ** (best_of - wins)
        for wins in range(best_of // 2 + 1, best_of + 1)
    )


def slot_probabilities(p, best_of, m=0.0) -> list[float]:
    """Pre-match P(team1 wins slot k | slot k is played), for every map slot."""
    _validate_series(p, best_of)
    return [p] * best_of if m == 0 else _map_chain(p, best_of, m)[1]


def fit_momentum(frame) -> float:
    """Bounded MLE using first-map p and the immediately previous map winner."""
    first = frame[frame["order"] == 1].set_index("match_id").p
    previous = frame[["match_id", "order", "won"]].copy()
    previous["order"] += 1
    rows = frame[frame["order"] >= 2].merge(
        previous, on=["match_id", "order"], suffixes=("", "_previous")
    )
    rows["p0"] = rows.match_id.map(first)
    rows = rows.dropna(subset=["p0", "won", "won_previous"])
    if len(rows) < 100:
        return 0.0
    p = np.clip(rows.p0.to_numpy(), EPS, 1 - EPS)
    z = np.log(p / (1 - p))
    x, y = 2 * rows.won_previous.to_numpy() - 1, rows.won.to_numpy()
    # Convex likelihood: bisect the monotone derivative, including boundary optima.
    low, high = -1.0, 1.0
    for _ in range(60):
        m = (low + high) / 2
        q = 1 / (1 + np.exp(-(z + m * x)))
        if np.sum(x * (q - y)) > 0:
            high = m
        else:
            low = m
    return float((low + high) / 2)
