"""Export the shared website feed; network access is injectable and optional."""

import gzip
import json
import math
import os
import pickle
import sqlite3
import tempfile
import time
from collections import Counter
from datetime import UTC, datetime, timedelta
from pathlib import Path
from types import SimpleNamespace

from promval.evaluation import series_probability
from promval.kalshi.api import Client
from promval.kalshi.quotes import candle_quote
from promval.link import events_from_markets, link, market_row
from promval.ratings.models import MODELS
from promval.ratings.replay import load_lineups, load_maps, replay
from promval.vlr import cache
from promval.vlr.http import Fetcher
from promval.vlr.parse import ParseError, parse_schedule_page, parse_upcoming_match

REPO = Path(__file__).resolve().parents[1]
STATE_VERSION = 1
MODEL = "player_round_glicko_rookie_tier_revert"
SECTIONS = {
    "INTL": "International",
    "VCT": "VCT",
    "GC": "GC",
    "VCL": "VCL",
    "OFF": "Offseason",
    "T3": "T3",
    "COL": "Collegiate",
    "?": "Unknown",
}
SECTION_KEYS = dict(
    zip(
        ("vct", "gc", "vcl", "offseason", "t3", "collegiate"),
        ("VCT", "GC", "VCL", "OFF", "T3", "COL"),
    )
)


def utc(value):
    return datetime.fromisoformat(value.replace("Z", "+00:00")).astimezone(UTC)


def stamp(value):
    return value.astimezone(UTC).strftime("%Y-%m-%dT%H:%MZ")


def atomic_json(path, value):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temporary = tempfile.mkstemp(dir=path.parent, suffix=".tmp")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            json.dump(
                value,
                handle,
                ensure_ascii=False,
                separators=(",", ":"),
                allow_nan=False,
            )
        os.replace(temporary, path)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)


def series_call(p, best_of, temperatures):
    n = best_of if best_of in (1, 3, 5) else 3
    probability = series_probability(p, n)
    temperature = 1 if n == 1 else temperatures.get(str(n), 1)
    if temperature == 1 or probability in (0, 1):
        return probability
    return 1 / (1 + math.exp(-temperature * math.log(probability / (1 - probability))))


def section(event):
    return (
        "INTL"
        if event.get("international")
        else SECTION_KEYS.get(event.get("section"), "?")
    )


def call(match_id, start, best_of, name1, name2, event, key, p, temperatures):
    return {
        "match_id": str(match_id),
        "start": stamp(utc(start)),
        "best_of": best_of,
        "name1": name1,
        "name2": name2,
        "event": event,
        "section": key,
        "p_game": round(float(p), 4),
        "p_series": round(series_call(p, best_of, temperatures), 4),
    }


def feed_match(
    prediction, status, reconstructed=False, score1=None, score2=None, winner=None
):
    fields = (
        "match_id",
        "start",
        "best_of",
        "name1",
        "name2",
        "event",
        "section",
        "p_game",
        "p_series",
    )
    result = {key: prediction[key] for key in fields}
    result.update(
        status=status,
        reconstructed=reconstructed,
        score1=score1,
        score2=score2,
        winner=winner,
        url=f"https://www.vlr.gg/{prediction['match_id']}",
        market=None,
    )
    return result


def upcoming_pages(root, now, no_fetch, fetch):
    """Return parsed pages and listing rows, keeping transient pages outside raw/."""
    directory = root / "upcoming"
    matches, listings, skipped = {}, {}, 0

    def read(match_id, live=False):
        nonlocal skipped
        path = directory / f"{match_id}.html.gz"
        age = now.timestamp() - path.stat().st_mtime if path.exists() else float("inf")
        if no_fetch:
            if age >= 7 * 86400:
                return None
        elif live or age >= 6 * 3600:
            cache.save(path, fetch(f"https://www.vlr.gg/{match_id}"))
        try:
            return parse_upcoming_match(cache.load(path), match_id)
        except ParseError:
            skipped += 1
            return None

    if no_fetch:
        for path in sorted(directory.glob("*.html.gz")):
            if path.name.removesuffix(".html.gz").isdigit():
                match = read(int(path.name.removesuffix(".html.gz")))
                if match is not None:
                    matches[match.match_id] = match
        return matches, listings, skipped
    for page in range(1, 6):
        url = "https://www.vlr.gg/matches" + (f"?page={page}" if page > 1 else "")
        rows = parse_schedule_page(fetch(url))
        if not rows:
            break
        for row in rows:
            if row.match_id in listings:
                continue
            listings[row.match_id] = row
            match = read(row.match_id, row.status == "live")
            if match is None:
                continue
            if utc(match.start_utc) > now + timedelta(days=7):
                return matches, listings, skipped
            matches[match.match_id] = match
    return matches, listings, skipped


def current_prices(aliases, candidates, raw_markets, now, *, linked_markets=None):
    if not candidates or not raw_markets:
        return {}
    rows = [market_row(raw, "KXVALORANTGAME") for raw in raw_markets]
    events = events_from_markets(rows)
    linked = link(events, candidates, initial_aliases=aliases)
    raw_by_ticker = {r["ticker"]: r for r in raw_markets}
    event_by_ticker = {e.event_ticker: e for e in events}
    match_by_id = {m["match_id"]: m for m in candidates}
    prices = {}
    for result in linked.links:
        if result.match_id is None:
            continue
        event = event_by_ticker[result.event_ticker]
        if linked_markets is not None and len(event.markets) == 2:
            ordered = sorted(
                zip(event.markets, result.team_ids),
                key=lambda pair: pair[1] != match_by_id[result.match_id]["team1_id"],
            )
            linked_markets[str(result.match_id)] = [
                raw_by_ticker[market["ticker"]] for market, _ in ordered
            ]
        options = []
        for market, team in zip(
            event_by_ticker[result.event_ticker].markets, result.team_ids
        ):
            raw = raw_by_ticker[market["ticker"]]
            try:
                bid, ask = (
                    float(raw.get(f"yes_{side}_dollars")) for side in ("bid", "ask")
                )
            except (TypeError, ValueError):
                continue
            if not 0 < bid <= ask <= 1 or ask - bid > 0.10 + 1e-9:
                continue
            team1 = team == match_by_id[result.match_id]["team1_id"]
            p = (bid + ask) / 2
            options.append((team1, p if team1 else 1 - p))
        if options:
            _, p = max(options, key=lambda option: option[0])
            prices[str(result.match_id)] = {
                "p": round(p, 4),
                "at": stamp(now),
                "url": market_url(result.event_ticker),
            }
    return prices


def market_url(event_ticker):
    return "https://kalshi.com/markets/kxvalorantgame/" + event_ticker.lower()


def closing_prices(conn, matches, directory):
    tables = {r[0] for r in conn.execute("SELECT name FROM sqlite_master")}
    if not {"kalshi_links", "kalshi_markets", "team_aliases"} <= tables:
        return {}
    prices, preferred = {}, set()
    rows = conn.execute("""SELECT l.match_id, l.event_ticker, k.ticker, a.vlr_team_id
        FROM kalshi_links l JOIN kalshi_markets k USING(event_ticker)
        JOIN team_aliases a USING(competitor_id)
        WHERE l.kind='series' AND l.match_id IS NOT NULL ORDER BY k.ticker""")
    for match_id, event, ticker, team in rows:
        match = matches.get(match_id)
        if match is None or team not in (match["team1_id"], match["team2_id"]):
            continue
        path = directory / "candles" / f"{ticker}.json.gz"
        if not path.exists():
            continue
        with gzip.open(path, "rt") as handle:
            quote = candle_quote(
                json.load(handle), match["start_utc"], with_timestamp=True
            )
        if quote is None:
            continue
        team1 = team == match["team1_id"]
        if match_id in preferred or (not team1 and str(match_id) in prices):
            continue
        bid, ask, timestamp = quote
        p = (bid + ask) / 2
        prices[str(match_id)] = {
            "p": round(p if team1 else 1 - p, 4),
            "at": stamp(datetime.fromtimestamp(timestamp, UTC)),
            "url": market_url(event),
        }
        if team1:
            preferred.add(match_id)
    return prices


def build_state(conn, data_root):
    """Replay DB ratings and capture all inputs needed by a DB-free feed run."""
    root = Path(data_root)
    params = json.loads((REPO / "promval/ratings/elo_weights.json").read_text())[MODEL]
    temperatures = params.get("series_temperature", {})
    params = {
        k: v
        for k, v in params.items()
        if k not in ("fit_through", "series_temperature")
    }
    maps = load_maps(conn)
    model = MODELS[MODEL](lineups=load_lineups(conn), **params)
    predictions = replay(maps, model)
    cursor = conn.execute("SELECT * FROM matches")
    db_matches = {
        row[0]: dict(zip([c[0] for c in cursor.description], row)) for row in cursor
    }
    cursor = conn.execute("SELECT * FROM events")
    events = {
        row[0]: dict(zip([c[0] for c in cursor.description], row)) for row in cursor
    }
    historical, seen, first_seen = {}, set(), {}
    for row in predictions.itertuples(index=False):
        if row.match_id not in historical:
            historical[row.match_id] = (
                row.p,
                row.team1_id in seen and row.team2_id in seen,
            )
        seen.update((row.team1_id, row.team2_id))
        for team in (row.team1_id, row.team2_id):
            first_seen.setdefault(team, utc(row.start_utc))
    matches = {}
    for mid, match in db_matches.items():
        if utc(match["start_utc"]) < datetime(2026, 1, 1, tzinfo=UTC):
            continue
        probability, rated = historical.get(mid, (None, False))
        if not rated:
            continue
        prediction = call(
            mid,
            match["start_utc"],
            match["best_of"] if match["best_of"] in (1, 3, 5) else None,
            match["team1_name"],
            match["team2_name"],
            match["event"],
            section(events.get(match["event_id"], {})),
            probability,
            temperatures,
        )
        matches[str(mid)] = feed_match(
            prediction,
            "final",
            True,
            match["score1"],
            match["score2"],
            match["winner"],
        )
    close = closing_prices(conn, db_matches, root / "kalshi")
    for mid, row in matches.items():
        row["market"] = close.get(mid)
    tables = {r[0] for r in conn.execute("SELECT name FROM sqlite_master")}
    aliases = (
        dict(conn.execute("SELECT competitor_id, vlr_team_id FROM team_aliases"))
        if "team_aliases" in tables
        else {}
    )
    return {
        "version": STATE_VERSION,
        "built": stamp(datetime.now(UTC)),
        "model": model,
        "rated_teams": seen,
        "first_seen": first_seen,
        "temperatures": temperatures,
        "finals": matches,
        "closing_prices": close,
        "db_matches": db_matches,
        "events": events,
        "team_aliases": aliases,
        "data_through": max(
            (m["start_utc"][:10] for m in db_matches.values()), default=None
        ),
    }


def save_state(state, path):
    """Atomically save the trusted ratings snapshot as a compressed pickle."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temporary = tempfile.mkstemp(dir=path.parent, suffix=".tmp")
    try:
        with os.fdopen(fd, "wb") as raw:
            with gzip.GzipFile(fileobj=raw, mode="wb", compresslevel=6) as handle:
                pickle.dump(state, handle, protocol=pickle.HIGHEST_PROTOCOL)
        os.replace(temporary, path)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)


def load_state(path):
    """Load a trusted snapshot, rejecting incompatible state versions."""
    with gzip.open(path, "rb") as handle:
        state = pickle.load(handle)
    if state.get("version") != STATE_VERSION:
        raise ValueError(
            f"Unsupported feed state version {state.get('version')!r}; expected {STATE_VERSION}. Run feed-state again."
        )
    return state


def state_from_db(db=None):
    own_conn = not isinstance(db, sqlite3.Connection)
    conn = (
        sqlite3.connect(f"file:{Path(db or REPO / 'db/valorant.db')}?mode=ro", uri=True)
        if own_conn
        else db
    )
    try:
        return build_state(conn, Path(os.environ.get("PROMVAL_DATA", REPO / "data")))
    finally:
        if own_conn:
            conn.close()


def export(
    out=None,
    *,
    state=None,
    no_fetch=False,
    now=None,
    vlr_fetch=None,
    kalshi_fetch=None,
    db=None,
    candidates_path=None,
):
    """Write and return a feed; existing DB callers build state on demand."""
    started = time.perf_counter()
    now = (now or datetime.now(UTC)).astimezone(UTC)
    root = Path(os.environ.get("PROMVAL_DATA", REPO / "data"))
    out = Path(out) if out is not None else root / "feed" / "valorant.json"
    log_path = root / "predictions.json"
    log = json.loads(log_path.read_text()) if log_path.exists() else {}
    if state is None:
        state = state_from_db(db)
    model = state["model"]
    first_seen = state["first_seen"]
    temperatures = state["temperatures"]
    db_matches = state["db_matches"]
    events = state["events"]
    fetch = None if no_fetch else (vlr_fetch or Fetcher().text)
    upcoming, listings, skipped = upcoming_pages(root, now, no_fetch, fetch)
    # Future calls disappear when removed from the listing; frozen calls persist.
    log = {
        key: value
        for key, value in log.items()
        if utc(value["start"]) <= now or int(key) in upcoming
    }
    matches = {mid: dict(row) for mid, row in state["finals"].items()}
    for mid, match in db_matches.items():
        saved = log.get(str(mid))
        if saved is not None and utc(match["start_utc"]) >= datetime(
            2026, 1, 1, tzinfo=UTC
        ):
            matches[str(mid)] = feed_match(
                saved, "final", False, match["score1"], match["score2"], match["winner"]
            )
    matches = {str(mid): matches[str(mid)] for mid in db_matches if str(mid) in matches}
    candidates = []
    for mid, match in upcoming.items():
        if str(mid) in matches or utc(match.start_utc) > now + timedelta(days=7):
            continue
        saved = log.get(str(mid))
        event = events.get(match.event_id, {})
        if saved is None or utc(saved["start"]) > now:
            if any(
                first_seen.get(team.team_id, datetime.max.replace(tzinfo=UTC))
                >= utc(match.start_utc)
                for team in (match.team1, match.team2)
            ):
                skipped += 1
                continue
            row = SimpleNamespace(
                team1_id=match.team1.team_id,
                team2_id=match.team2.team_id,
                start_utc=match.start_utc,
                section=event.get("section"),
                region=event.get("region"),
                international=event.get("international", 0),
                game_id=None,
                map=None,
                picked_by=None,
            )
            saved = call(
                mid,
                match.start_utc,
                match.best_of if match.best_of in (1, 3, 5) else None,
                match.team1.name,
                match.team2.name,
                match.event,
                section(event),
                model.predict(row),
                temperatures,
            )
            if utc(match.start_utc) > now:
                log[str(mid)] = dict(
                    saved,
                    saved_at=stamp(now),
                    team1_id=match.team1.team_id,
                    team2_id=match.team2.team_id,
                )
        listing = listings.get(mid)
        if listing is not None and listing.status == "live":
            status, score1, score2 = "live", listing.score1, listing.score2
        elif utc(saved["start"]) > now:
            status, score1, score2 = "upcoming", None, None
        else:
            # Frozen entries below implement the elapsed-time fallback.
            continue
        matches[str(mid)] = feed_match(saved, status, score1=score1, score2=score2)
        candidates.append(
            {
                "match_id": mid,
                "start_utc": match.start_utc,
                "team1_id": match.team1.team_id,
                "team2_id": match.team2.team_id,
                "team1_name": match.team1.name,
                "team2_name": match.team2.name,
            }
        )
    for mid, saved in log.items():
        age = now - utc(saved["start"])
        if mid not in matches and timedelta(0) <= age <= timedelta(days=7):
            matches[mid] = feed_match(
                saved, "live" if age < timedelta(hours=6) else "final"
            )
            if age < timedelta(hours=6) and all(
                key in saved for key in ("team1_id", "team2_id")
            ):
                candidates.append(
                    {
                        "match_id": int(mid),
                        "start_utc": saved["start"],
                        "team1_id": saved["team1_id"],
                        "team2_id": saved["team2_id"],
                        "team1_name": saved["name1"],
                        "team2_name": saved["name2"],
                    }
                )
    close = state["closing_prices"]
    prices = {}
    linked_markets = {}
    if not no_fetch:
        client = Client(get=kalshi_fetch) if kalshi_fetch else Client()
        markets = list(
            client.pages(
                "/markets",
                "markets",
                series_ticker="KXVALORANTGAME",
                status="open",
                limit=1000,
            )
        )
        prices = current_prices(
            state["team_aliases"],
            candidates,
            markets,
            now,
            linked_markets=linked_markets,
        )
    for mid, match in matches.items():
        match["market"] = (close if match["status"] == "final" else prices).get(mid)
    present = {m["section"] for m in matches.values()}
    feed = {
        "version": 1,
        "game": "valorant",
        "name": "Valorant",
        "model": "Player round Elo",
        "generated": stamp(now),
        "data_through": state["data_through"],
        "source": {"name": "VLR.gg", "url": "https://www.vlr.gg", "license": None},
        "sections": [
            {"key": key, "label": label, "major": key in ("INTL", "VCT")}
            for key, label in SECTIONS.items()
            if key in present
        ],
        "matches": list(matches.values()),
    }
    from promval.trading import candidates as execution_candidates

    private_rows = [
        dict(
            row,
            international=bool(
                events.get(upcoming[int(mid)].event_id, {}).get("international", 0)
            ),
        )
        for mid, row in matches.items()
        if int(mid) in upcoming
    ]
    candidate_counts = {}
    private = execution_candidates(
        private_rows,
        linked_markets,
        now,
        data_through=state["data_through"],
        counts=candidate_counts,
    )
    atomic_json(candidates_path or root / "feed/candidates.json", private)
    atomic_json(log_path, log)
    atomic_json(out, feed)
    counts = Counter(m["status"] for m in feed["matches"])
    priced = sum(m["market"] is not None for m in feed["matches"])
    print(
        f"upcoming={counts['upcoming']} live={counts['live']} final={counts['final']} kalshi={priced} skipped={skipped} candidates={len(private['matches'])} skipped_candidates={candidate_counts['skipped']} bytes={out.stat().st_size} elapsed={time.perf_counter() - started:.2f}s"
    )
    return feed
