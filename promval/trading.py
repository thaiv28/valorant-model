"""Frozen blend coefficients and private, unblended execution inputs."""

import hashlib
import json
import math
import os
import re
import sqlite3
from datetime import UTC, datetime, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo

import pandas as pd

from promval import blend

GAME = "valorant"
SERIES = "KXVALORANTGAME"
VALIDATE_FROM = "2025-09-01"
MODEL = "player_round_glicko_rookie_tier_revert"
RULES = re.compile(
    r"^If (?P<side>.+?) wins the (?P<event>.+): (?P<team1>.+?) vs\.? "
    r"(?P<team2>.+?) Valorant match originally scheduled for "
    r"(?P<day>\w{3} \d{1,2}, \d{4}) at (?P<time>\d{1,2}:\d{2} [AP]M) E[DS]T"
)


def build_blend_artifact(rows, game, series_ticker, now):
    """Fit each monthly snapshot using only known outcomes before its boundary."""
    snapshots = []
    if not rows.empty:
        dates = pd.to_datetime(rows.start_utc, utc=True)
        eligible = rows.loc[
            (rows.kind == "series")
            & rows.won.notna()
            & (dates >= pd.Timestamp(VALIDATE_FROM, tz="UTC"))
        ].copy()
        eligible["start_utc"] = dates.loc[eligible.index]
        if not eligible.empty:
            first = eligible.start_utc.min().normalize().replace(
                day=1
            ) + pd.offsets.MonthBegin(1)
            last = pd.Timestamp(now).tz_convert("UTC").normalize().replace(
                day=1
            ) + pd.offsets.MonthBegin(1)
            for boundary in pd.date_range(first, last, freq="MS"):
                training = eligible[eligible.start_utc < boundary]
                if len(training) < 300:
                    continue
                a, b, n = blend.fit(training.p, training.market_p, training.won)
                snapshots.append(
                    {
                        "available_from": boundary.isoformat(),
                        "trained_through": training.start_utc.max().isoformat(),
                        "training_series": n,
                        "market_slope": a,
                        "gap_slope": b,
                    }
                )
    return {
        "version": "game-blend-v1",
        "game": game,
        "series_ticker": series_ticker,
        "clip": 0.01,
        "protocol": f"Tradeable quotes, no intercept, monthly earlier-only fits from {VALIDATE_FROM}, adopted {MODEL} model with stage-1 series temperature.",
        "snapshots": snapshots,
    }


def export_blend_artifact(out):
    """Replay adopted frozen weights and reuse the report's exact market rows."""
    from promval.benchmark_rows import benchmark_market_rows, with_series_temperature
    from promval.feed import REPO
    from promval.ratings.models import MODELS
    from promval.ratings.replay import load_lineups, load_maps, replay

    params = json.loads((REPO / "promval/ratings/elo_weights.json").read_text())[
        MODEL
    ].copy()
    temperatures = {int(k): v for k, v in params.pop("series_temperature").items()}
    params.pop("fit_through", None)
    root = Path(os.environ.get("PROMVAL_DATA", REPO / "data"))
    with sqlite3.connect(f"file:{REPO / 'db/valorant.db'}?mode=ro", uri=True) as conn:
        source = replay(
            load_maps(conn), MODELS[MODEL](lineups=load_lineups(conn), **params)
        )
        source = with_series_temperature(source, temperatures)
        rows = benchmark_market_rows(conn, source, root / "kalshi")
    artifact = build_blend_artifact(rows, GAME, SERIES, datetime.now(UTC))
    out = Path(out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(artifact, indent=2, allow_nan=False) + "\n")
    latest = artifact["snapshots"][-1] if artifact["snapshots"] else None
    print(
        f"snapshots={len(artifact['snapshots'])}"
        + (
            f" latest={latest['available_from']} a={latest['market_slope']:.9f} b={latest['gap_slope']:.9f} n={latest['training_series']}"
            if latest
            else " latest=none"
        )
    )
    return artifact


def _utc(value):
    return datetime.fromisoformat(value.replace("Z", "+00:00")).astimezone(UTC)


def _contract_pair(markets):
    if len(markets) != 2 or any(
        m.get("status") not in ("open", "active") for m in markets
    ):
        return None
    parsed = [RULES.match(m.get("rules_primary") or "") for m in markets]
    if not all(parsed):
        return None
    names = [tuple(p[k].strip() for k in ("team1", "team2")) for p in parsed]
    sides = [p["side"].strip() for p in parsed]
    if (
        set(names[0]) != set(names[1])
        or names[0][0] == names[0][1]
        or set(sides) != set(names[0])
        or any(
            m.get("yes_sub_title", "").strip() != side
            for m, side in zip(markets, sides)
        )
        or not markets[0].get("event_ticker")
        or markets[0]["event_ticker"] != markets[1].get("event_ticker")
    ):
        return None
    try:
        starts = [
            datetime.strptime(f"{p['day']} {p['time']}", "%b %d, %Y %I:%M %p")
            .replace(tzinfo=ZoneInfo("America/New_York"))
            .astimezone(UTC)
            for p in parsed
        ]
    except ValueError:
        return None
    if starts[0] != starts[1] or parsed[0]["event"] != parsed[1]["event"]:
        return None
    return sides, starts[0]


def candidates(feed_rows, linked_markets, now, *, data_through=None, counts=None):
    """Export raw series chances; linked contracts are ordered to our team one."""
    now = now.astimezone(UTC)
    at = now.strftime("%Y-%m-%dT%H:%M:%SZ")
    records, skipped = [], 0
    for row in feed_rows:
        if (
            row["status"] != "upcoming"
            or _utc(row["start"]) <= now
            or row["best_of"] is None
        ):
            skipped += 1
            continue
        markets = linked_markets.get(str(row["match_id"]))
        if markets is None:
            skipped += 1
            continue
        parsed = _contract_pair(markets)
        if parsed is None:
            skipped += 1
            continue
        sides, start = parsed
        p = row["p_series"]
        raw = {sides[0]: round(p, 6), sides[1]: round(1 - p, 6)}
        if (
            abs(start - _utc(row["start"])) > timedelta(hours=18)
            or start <= now
            or any(not math.isfinite(v) or not 0 < v < 1 for v in raw.values())
        ):
            skipped += 1
            continue
        teams = sorted(sides)
        event = markets[0]["event_ticker"]
        fixture = hashlib.sha256(
            json.dumps(
                [GAME, teams, event], separators=(",", ":"), ensure_ascii=False
            ).encode()
        ).hexdigest()
        international = bool(row["international"])
        records.append(
            {
                "execution_candidate": {
                    "kind": "candidate-v1",
                    "schema_version": 1,
                    "game": GAME,
                    "series_ticker": SERIES,
                    "at": at,
                    "fixture_id": fixture,
                    "event_ticker": event,
                    "teams": teams,
                    "team_homes": {},
                    "international": international,
                    "group": "valorant-international"
                    if international
                    else "valorant-domestic",
                    "start": start.strftime("%Y-%m-%dT%H:%MZ"),
                    "raw": raw,
                    "provenance": {
                        "model": MODEL,
                        "match_id": row["match_id"],
                        "p_game": row["p_game"],
                        "p_series": p,
                        "best_of": row["best_of"],
                        "data_through": data_through,
                        "names": [row["name1"], row["name2"]],
                        "start": row["start"],
                    },
                }
            }
        )
    if counts is not None:
        counts["skipped"] = skipped
    return {"version": 1, "game": GAME, "generated": at, "matches": records}
