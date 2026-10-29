"""Pure catalog parsing, conservative team matching and settlement checks."""

import re
import unicodedata
from bisect import bisect_left, bisect_right
from collections import defaultdict
from dataclasses import dataclass
from datetime import UTC, datetime, timedelta, timezone
from difflib import SequenceMatcher
from itertools import permutations


def normalize(name):
    """Return accent-insensitive team tokens, retaining regional qualifiers."""
    name = "".join(
        c
        for c in unicodedata.normalize("NFKD", name).casefold()
        if not unicodedata.combining(c)
    )
    tokens = re.findall(r"[^\W_]+", name)
    return tuple(
        "gc" if t in {"female", "women", "gc"} else t
        for t in tokens
        if t not in {"esports", "esport", "gaming", "team", "club", "the"}
    )


def scheduled_utc(rules_primary):
    """Read the advertised Eastern time using its explicit EDT/EST offset."""
    found = re.search(
        r"originally scheduled for (\w+ \d{1,2}, \d{4}) at "
        r"(\d{1,2}:\d{2} [AP]M) (EDT|EST)",
        rules_primary or "",
    )
    if not found:
        return None
    try:
        date = datetime.strptime(f"{found[1]} {found[2]}", "%b %d, %Y %I:%M %p")
    except ValueError:
        return None
    offset = -4 if found[3] == "EDT" else -5
    return (
        date.replace(tzinfo=timezone(timedelta(hours=offset)))
        .astimezone(UTC)
        .isoformat()
        .replace("+00:00", "Z")
    )


def market_row(raw, series):
    """Project a raw market without deriving dates from its ticker."""
    event = raw["event_ticker"]
    kind = "map" if series == "KXVALORANTMAP" else "series"
    suffix = event.rsplit("-", 1)[-1]
    event_name = re.search(r"\b(?:in|wins) the (.+?):", raw.get("rules_primary") or "")
    return {
        "ticker": raw["ticker"],
        "series": series,
        "event_ticker": event,
        "kind": kind,
        "map_number": int(suffix) if kind == "map" and suffix.isdigit() else None,
        "team_code": raw["ticker"].rsplit("-", 1)[-1],
        "team_name": raw.get("yes_sub_title", ""),
        "competitor_id": (raw.get("custom_strike") or {}).get("esports_competitor"),
        "scheduled_utc": scheduled_utc(raw.get("rules_primary")),
        "event_name": event_name[1] if event_name else None,
        "status": raw.get("status"),
        "result": raw.get("result", ""),
        "volume": float(raw.get("volume_fp") or raw.get("volume") or 0),
        "open_time": raw.get("open_time"),
        "close_time": raw.get("close_time"),
    }


@dataclass(frozen=True)
class Event:
    event_ticker: str
    markets: tuple[dict, ...]
    kind: str = "series"
    map_number: int | None = None

    @property
    def series_ticker(self):
        if self.kind == "series":
            return self.event_ticker
        return self.event_ticker.rsplit("-", 1)[0].replace(
            "KXVALORANTMAP-", "KXVALORANTGAME-", 1
        )


def events_from_markets(rows):
    groups = defaultdict(list)
    for row in rows:
        groups[row["event_ticker"]].append(dict(row))
    return [
        Event(ticker, tuple(markets), markets[0]["kind"], markets[0]["map_number"])
        for ticker, markets in sorted(groups.items())
    ]


@dataclass(frozen=True)
class Alias:
    competitor_id: str
    kalshi_name: str
    kalshi_code: str
    vlr_team_id: int
    vlr_name: str
    events: int


@dataclass(frozen=True)
class Link:
    event_ticker: str
    match_id: int | None
    game_id: int | None
    kind: str
    method: str | None
    reason: str | None
    # Event market order -> VLR team id, retained for result checks.
    team_ids: tuple[int | None, ...] = ()


@dataclass
class LinkResult:
    links: list[Link]
    aliases: list[Alias]


def _time(value):
    if not value:
        return None
    try:
        date = datetime.fromisoformat(value.replace("Z", "+00:00"))
        return date if date.tzinfo else None
    except ValueError:
        return None


def _similar(a, b):
    a, b = sorted(set(normalize(a))), sorted(set(normalize(b)))
    return (
        bool(a and b) and SequenceMatcher(None, " ".join(a), " ".join(b)).ratio() >= 0.8
    )


def _orientations(event, match, method, aliases):
    if len(event.markets) != 2:
        return []
    choices = []
    for sides in permutations((1, 2)):
        valid = True
        for market, side in zip(event.markets, sides):
            name, team_id = match[f"team{side}_name"], match[f"team{side}_id"]
            if method == "exact":
                valid &= bool(normalize(name)) and normalize(
                    market["team_name"]
                ) == normalize(name)
            elif method == "alias":
                valid &= aliases.get(market["competitor_id"]) == team_id
            else:
                valid &= _similar(market["team_name"], name)
        if valid:
            choices.append(tuple(match[f"team{s}_id"] for s in sides))
    return choices


def link(kalshi_events, vlr_matches):
    """Link series in three passes, then inherit their matches for map events.

    Matches are dictionaries; optional ``maps`` holds played map dictionaries.
    A map-only catalog supplies a representative event for the absent series.
    """
    events, matches = list(kalshi_events), list(vlr_matches)
    timed = sorted(
        ((start, m) for m in matches if (start := _time(m["start_utc"]))),
        key=lambda row: row[0],
    )
    starts = [start for start, _ in timed]
    representatives = {}
    for event in sorted(events, key=lambda e: e.kind != "series"):
        representatives.setdefault(event.series_ticker, event)
    candidates, reasons = {}, {}
    for key, event in representatives.items():
        scheduled = next(
            (date for m in event.markets if (date := _time(m.get("scheduled_utc")))),
            None,
        )
        opened = next(
            (date for m in event.markets if (date := _time(m.get("open_time")))),
            None,
        )
        target = scheduled or (opened + timedelta(hours=24) if opened else None)
        window = timedelta(hours=30)
        candidates[key] = (
            [
                m
                for _, m in timed[
                    bisect_left(starts, target - window) : bisect_right(
                        starts, target + window
                    )
                ]
            ]
            if target
            else []
        )
        reasons[key] = (
            "missing scheduled/open time"
            if target is None
            else "no candidate within 30h"
            if not candidates[key]
            else "no team match"
        )
    resolved, evidence = {}, defaultdict(list)
    aliases = {}
    for method in ("exact", "alias", "fuzzy"):
        for key, event in representatives.items():
            if key in resolved:
                continue
            if len(event.markets) != 2:
                reasons[key] = "expected two competitor markets"
                continue
            if method == "alias" and not all(
                m.get("competitor_id") in aliases for m in event.markets
            ):
                continue
            found = []
            for match in candidates[key]:
                orientations = _orientations(event, match, method, aliases)
                if orientations:
                    found.append((match, orientations))
            if len(found) == 1 and len(found[0][1]) == 1:
                match, orientations = found[0]
                team_ids = orientations[0]
                resolved[key] = (match, method, team_ids)
                if method == "exact":
                    for market, team_id in zip(event.markets, team_ids):
                        if market.get("competitor_id"):
                            side = 1 if team_id == match["team1_id"] else 2
                            evidence[market["competitor_id"]].append(
                                (market, team_id, match[f"team{side}_name"], key)
                            )
            elif found:
                reasons[key] = f"ambiguous {method} candidates"
        if method == "exact":
            aliases = {
                cid: rows[0][1]
                for cid, rows in evidence.items()
                if len({r[1] for r in rows}) == 1
            }
    learned = [
        Alias(
            cid,
            rows[0][0]["team_name"],
            rows[0][0]["team_code"],
            aliases[cid],
            rows[0][2],
            len({r[3] for r in rows}),
        )
        for cid, rows in sorted(evidence.items())
        if cid in aliases
    ]
    links = []
    for event in events:
        key = event.series_ticker
        if key not in resolved:
            links.append(
                Link(event.event_ticker, None, None, event.kind, None, reasons[key])
            )
            continue
        match, method, team_ids = resolved[key]
        representative = representatives[key]
        identity = {
            m["competitor_id"]: tid
            for m, tid in zip(representative.markets, team_ids)
            if m.get("competitor_id")
        }
        names = {
            normalize(m["team_name"]): tid
            for m, tid in zip(representative.markets, team_ids)
        }
        mapped = tuple(
            identity.get(m.get("competitor_id"), names.get(normalize(m["team_name"])))
            for m in event.markets
        )
        game_id, reason = None, None
        if event.kind == "map":
            if event.map_number is None:
                reason = "invalid map number"
            else:
                game = next(
                    (
                        g
                        for g in match.get("maps", [])
                        if g["order"] == event.map_number
                    ),
                    None,
                )
                game_id = game["game_id"] if game else None
                reason = None if game else "unplayed"
        links.append(
            Link(
                event.event_ticker,
                match["match_id"],
                game_id,
                event.kind,
                method,
                reason,
                mapped,
            )
        )
    return LinkResult(links, learned)


@dataclass
class CrossCheck:
    agreements: int
    checked: int
    mismatches: list[str]


def cross_check(events, links, matches):
    """Check each binary settled market; skip scalar and unknown VLR winners."""
    by_event = {e.event_ticker: e for e in events}
    by_match = {m["match_id"]: m for m in matches}
    agreements, checked, mismatches = 0, 0, []
    for linked in links:
        if linked.match_id is None or linked.reason:
            continue
        match = by_match[linked.match_id]
        winner = match.get("winner")
        if linked.kind == "map":
            game = next(g for g in match["maps"] if g["game_id"] == linked.game_id)
            winner = (
                1
                if game["score1"] > game["score2"]
                else 2
                if game["score2"] > game["score1"]
                else None
            )
        if winner not in (1, 2):
            continue
        winner_id = match[f"team{winner}_id"]
        for market, team_id in zip(
            by_event[linked.event_ticker].markets, linked.team_ids
        ):
            if market.get("result") not in ("yes", "no") or team_id is None:
                continue
            checked += 1
            expected = "yes" if team_id == winner_id else "no"
            if market["result"] == expected:
                agreements += 1
            else:
                mismatches.append(
                    f"{market['ticker']}: Kalshi={market['result']} VLR={expected} "
                    f"match_id={linked.match_id} game_id={linked.game_id}"
                )
    return CrossCheck(agreements, checked, mismatches)
