"""Offline execution contract and causal frozen coefficient checks."""

import hashlib
import json
from copy import deepcopy
from datetime import UTC, datetime

import numpy as np
import pandas as pd
import pytest

from promval import blend
from promval.trading import build_blend_artifact, candidates

NOW = datetime(2026, 10, 29, 18, tzinfo=UTC)


def test_monthly_artifact_exact_earlier_only_fits():
    rng = np.random.default_rng(42)
    dates = pd.date_range("2025-08-01", "2026-10-29", freq="8h", tz="UTC")
    p = rng.uniform(0.1, 0.9, len(dates))
    rows = pd.DataFrame(
        {
            "start_utc": dates,
            "p": p,
            "market_p": rng.uniform(0.1, 0.9, len(dates)),
            "won": rng.binomial(1, p),
            "kind": "series",
        }
    )
    # Unknown outcomes and map rows cannot enter a series fit.
    rows.loc[2, "kind"] = "map"
    rows.loc[300, "won"] = np.nan
    artifact = build_blend_artifact(rows, "valorant", "KXVALORANTGAME", NOW)
    assert artifact["version"] == "game-blend-v1" and artifact["clip"] == 0.01
    snapshots = artifact["snapshots"]
    assert snapshots and snapshots[-1]["available_from"] == "2026-11-01T00:00:00+00:00"
    boundaries = [s["available_from"] for s in snapshots]
    assert boundaries == sorted(set(boundaries))
    # September has only 90 eligible series: October's boundary is filtered out.
    assert snapshots[0]["available_from"] == "2026-01-01T00:00:00+00:00"
    for snap in snapshots:
        boundary = pd.Timestamp(snap["available_from"])
        subset = rows[
            (rows.start_utc >= pd.Timestamp("2025-09-01", tz="UTC"))
            & (rows.start_utc < boundary)
            & (rows.kind == "series")
            & rows.won.notna()
        ]
        a, b, n = blend.fit(subset.p, subset.market_p, subset.won)
        assert snap["training_series"] == n >= 300
        assert (snap["market_slope"], snap["gap_slope"]) == (a, b)
        assert (
            pd.Timestamp(snap["trained_through"]) == subset.start_utc.max() < boundary
        )
    # Post-July outcomes are included in later causal snapshots.
    assert snapshots[-1]["training_series"] > snapshots[-5]["training_series"]
    changed = rows.copy()
    changed.loc[changed.start_utc >= "2026-02-01", "won"] = 1
    later = build_blend_artifact(changed, "valorant", "KXVALORANTGAME", NOW)
    assert later["snapshots"][:2] == snapshots[:2]
    assert (
        build_blend_artifact(rows.iloc[:0], "valorant", "KXVALORANTGAME", NOW)[
            "snapshots"
        ]
        == []
    )


@pytest.fixture
def inputs():
    names = ["KRÜ Blaze", "MIBR Female"]
    # Our team one is the second team named in the rules; quotes are irrelevant.
    markets = [
        {
            "status": "active",
            "event_ticker": "KXVALORANTGAME-TEST",
            "yes_sub_title": side,
            "rules_primary": f"If {side} wins the VCT Game Changers Championship 2026: KRÜ Blaze vs. MIBR Female Valorant match originally scheduled for Oct 30, 2026 at 5:00 PM EDT",
        }
        for side in reversed(names)
    ]
    row = {
        "match_id": "42",
        "status": "upcoming",
        "start": "2026-10-30T21:00Z",
        "best_of": 3,
        "international": True,
        "p_game": 0.6,
        "p_series": 0.64,
        "name1": "MIBR GC",
        "name2": "KRU GC",
    }
    return row, {"42": markets}


def test_candidate_orientation_identity_and_validation_shape(inputs):
    row, linked = inputs
    doc = candidates([row], linked, NOW, data_through="2026-10-28")
    assert doc["version"] == 1 and doc["generated"] == "2026-10-29T18:00:00Z"
    record = doc["matches"][0]["execution_candidate"]
    teams = ["KRÜ Blaze", "MIBR Female"]
    assert record["teams"] == teams
    assert record["raw"] == {"MIBR Female": 0.64, "KRÜ Blaze": 0.36}
    assert record["start"] == "2026-10-30T21:00Z"
    assert record["group"] == "valorant-international"
    assert (
        record["fixture_id"]
        == hashlib.sha256(
            json.dumps(
                ["valorant", teams, "KXVALORANTGAME-TEST"],
                separators=(",", ":"),
                ensure_ascii=False,
            ).encode()
        ).hexdigest()
    )
    assert record["provenance"] == {
        "model": "player_round_glicko_rookie_tier_revert",
        "match_id": "42",
        "p_game": 0.6,
        "p_series": 0.64,
        "best_of": 3,
        "data_through": "2026-10-28",
        "names": ["MIBR GC", "KRU GC"],
        "start": row["start"],
    }
    # Mirror saved_candidates' structural requirements without a Prometheus dependency.
    assert record["kind"] == "candidate-v1" and record["schema_version"] == 1
    assert record["game"] == "valorant" and record["series_ticker"] == "KXVALORANTGAME"
    assert isinstance(record["teams"], list) and len(set(record["teams"])) == 2
    assert all(isinstance(t, str) and t for t in record["teams"])
    assert all(
        isinstance(record[k], str) and record[k] for k in ("fixture_id", "event_ticker")
    )
    assert isinstance(record["international"], bool)
    assert isinstance(record["team_homes"], dict) and isinstance(
        record["provenance"], dict
    )
    assert all(
        isinstance(record["raw"][t], (float, int)) and 0 < record["raw"][t] < 1
        for t in teams
    )
    row["international"] = False
    domestic = candidates([row], linked, NOW)["matches"][0]["execution_candidate"]
    assert (
        domestic["group"] == "valorant-domestic" and domestic["international"] is False
    )


@pytest.mark.parametrize(
    "invalid",
    [
        "subtitle",
        "rules_teams",
        "same_side",
        "closed",
        "missing_contract",
        "missing_link",
        "time_gap",
        "started",
        "unknown_best_of",
        "live",
        "kalshi_started",
        "rules_date",
        "event",
        "probability",
    ],
)
def test_invalid_candidates_skipped(inputs, invalid):
    row, linked = deepcopy(inputs)
    pair = linked["42"]
    if invalid == "subtitle":
        pair[0]["yes_sub_title"] = "MIBR GC"
    elif invalid == "rules_teams":
        pair[0]["rules_primary"] = pair[0]["rules_primary"].replace(
            "KRÜ Blaze", "Other"
        )
    elif invalid == "same_side":
        pair[1] = deepcopy(pair[0])
    elif invalid == "closed":
        pair[0]["status"] = "closed"
    elif invalid == "missing_contract":
        pair.pop()
    elif invalid == "missing_link":
        linked.clear()
    elif invalid == "time_gap":
        row["start"] = "2026-10-31T16:00Z"
    elif invalid == "started":
        row["start"] = "2026-10-29T18:00Z"
    elif invalid == "unknown_best_of":
        row["best_of"] = None
    elif invalid == "live":
        row["status"] = "live"
    elif invalid == "kalshi_started":
        row["start"] = "2026-10-29T19:00Z"
        for market in pair:
            market["rules_primary"] = market["rules_primary"].replace(
                "Oct 30, 2026 at 5:00 PM", "Oct 29, 2026 at 1:00 PM"
            )
    elif invalid == "rules_date":
        pair[0]["rules_primary"] = pair[0]["rules_primary"].replace("Oct 30", "Oct 40")
    elif invalid == "event":
        pair[0]["event_ticker"] = "OTHER"
    elif invalid == "probability":
        row["p_series"] = 1
    counts = {}
    assert candidates([row], linked, NOW, counts=counts)["matches"] == []
    assert counts == {"skipped": 1}
