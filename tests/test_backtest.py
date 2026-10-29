"""Hand cases for after-fee selection, simultaneous stakes, and match bootstrap."""

import numpy as np
import pandas as pd
import pytest

from promval.backtest import (
    LOL_SIZING,
    capped_path,
    fee,
    kelly_path,
    select_bets,
    summarize,
)


def rows(*updates):
    defaults = {
        "match_id": 1,
        "start_utc": "2026-01-01T00:00:00Z",
        "p": 0.8,
        "won": 1,
        "ask": 0.5,
        "bid": 0.4,
    }
    return pd.DataFrame([{**defaults, **update} for update in updates])


def test_fee_edge_fraction_and_flat_profit():
    bet = select_bets(rows({})).iloc[0]
    assert fee(0.5) == pytest.approx(0.0175)
    assert bet["side"] == 1
    assert bet["cost"] == pytest.approx(0.5175)
    assert bet["edge"] == pytest.approx(0.2825)
    assert bet["fraction"] == pytest.approx(0.2825 / 0.4825)
    assert bet["profit"] == pytest.approx(1 / 0.5175 - 1)


def test_side_choice_and_no_positive_edge():
    bets = select_bets(rows({"p": 0.1, "won": 0}, {"p": 0.5}))
    assert len(bets) == 1
    bet = bets.iloc[0]
    assert bet["side"] == 2
    assert bet["price"] == pytest.approx(0.6)
    assert bet["edge"] == pytest.approx(0.9 - 0.6 - fee(0.6))
    assert bet["side_won"] == 1
    crossed = select_bets(rows({"ask": 0.2, "bid": 0.8, "p": 0.4}))
    assert crossed.iloc[0]["side"] == 2


def test_skip_missing_and_boundary_quotes():
    frame = rows(
        {"ask": None},
        {"bid": None},
        {"ask": 0},
        {"bid": 1},
        {"bid": 0},
        {"ask": 1},
        {"ask": "bad"},
        {},
    )
    assert len(select_bets(frame)) == 1
    assert select_bets(frame.drop(columns="bid")).empty
    assert summarize(frame.iloc[:0])["bankroll"] == 50
    empty = summarize(pd.DataFrame())
    assert empty["bets"] == empty["matches"] == 0
    assert empty["bankroll"] == 50
    assert np.isnan(empty["flat_roi"])


def test_same_match_stakes_scaled_from_prematch_bankroll():
    bets = select_bets(rows({}, {}))
    assert bets["fraction"].sum() > 1
    path, drawdown, largest = kelly_path(bets)
    assert largest == pytest.approx(25)
    assert path == pytest.approx([50, 50 / 0.5175])
    assert drawdown == 0


def test_three_match_path_and_drawdown_in_start_order():
    frame = rows(
        {"match_id": 3, "start_utc": "2026-01-03T00:00:00Z"},
        {"match_id": 1},
        {"match_id": 2, "start_utc": "2026-01-02T00:00:00Z", "won": 0},
    )
    fraction = 0.2825 / 0.4825
    gain = 1 + fraction * (1 / 0.5175 - 1)
    expected = [50, 50 * gain, 50 * gain * (1 - fraction)]
    expected.append(expected[-1] * gain)
    path, drawdown, largest = kelly_path(select_bets(frame))
    assert path == pytest.approx(expected)
    assert drawdown == pytest.approx(fraction)
    assert largest == pytest.approx(expected[1] * fraction)
    result = summarize(frame, sizing="full")
    assert result["bankroll"] == pytest.approx(expected[-1])
    assert result["multiple"] == pytest.approx(expected[-1] / 50)
    assert result["matches"] == 3


def test_roi_interval_resamples_whole_matches_deterministically():
    # Unequal match sizes and mixed outcomes distinguish this interval from
    # resampling individual bets.
    updates = [
        {"match_id": match_id, "won": int(match_id % 3 != 0)}
        for match_id in range(10)
        for _ in range(match_id % 4 + 1)
    ]
    frame = rows(*updates)
    first = summarize(frame)
    assert first == summarize(frame)
    win_profit = 1 / 0.5175 - 1
    counts = np.array([match_id % 4 + 1 for match_id in range(10)])
    sums = counts * np.array(
        [win_profit if match_id % 3 != 0 else -1 for match_id in range(10)]
    )
    rng = np.random.default_rng(0)
    expected = []
    for _ in range(2000):
        picks = rng.integers(0, 10, 10)
        expected.append(sums[picks].sum() / counts[picks].sum())
    assert first["flat_roi"] == pytest.approx(sums.sum() / counts.sum())
    assert (first["roi_low"], first["roi_high"]) == pytest.approx(
        np.percentile(expected, [2.5, 97.5])
    )


def test_alternative_probability_selects_and_sizes_blended_bets():
    frame = rows({"p_blend": 0.1}, {"p_blend": 0.5})
    bets = select_bets(frame, probability="p_blend")
    assert len(bets) == 1
    assert bets.iloc[0]["side"] == 2
    expected = frame.copy()
    expected["p"] = frame.p_blend
    assert summarize(frame, probability="p_blend") == summarize(expected)


def _bets(rows):
    """rows: (match_id, start_utc, fraction, profit)."""
    return pd.DataFrame(rows, columns=["match_id", "start_utc", "fraction", "profit"])


def test_capped_path_fixture_cap_and_start_of_day_capital():
    # Full Kelly would stake 40%; the fixture cap is 10% of capital.
    path, _, largest = capped_path(_bets([(1, "2026-03-01T10:00Z", 0.4, 1.0)]))
    assert largest == pytest.approx(5.0)
    assert path[-1] == pytest.approx(55.0)
    # Two matches on one day are both sized from the day's opening capital.
    path, _, _ = capped_path(
        _bets(
            [
                (1, "2026-03-01T10:00Z", 0.1, 1.0),
                (2, "2026-03-01T15:00Z", 0.1, -1.0),
            ]
        )
    )
    assert path == pytest.approx([50.0, 50.0])


def test_capped_path_dollar_caps_and_stop_at_zero():
    big = dict(LOL_SIZING, fixture_fraction=1.0)
    _, _, largest = capped_path(
        _bets([(1, "2026-03-01T10:00Z", 1.0, 0.0)]), initial=10_000, sizing=big
    )
    assert largest == pytest.approx(250.0)  # order and fixture caps
    lose_all = dict(LOL_SIZING, fixture_fraction=1.0)
    path, drawdown, _ = capped_path(
        _bets(
            [
                (1, "2026-03-01T10:00Z", 1.0, -1.0),
                (2, "2026-03-02T10:00Z", 0.5, 1.0),
            ]
        ),
        sizing=lose_all,
    )
    assert path == pytest.approx([50.0, 0.0, 0.0])  # no orders once capital is $0
    assert drawdown == pytest.approx(1.0)
