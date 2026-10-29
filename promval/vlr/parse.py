"""Pure parsers for saved VLR pages. No fetching or filesystem access."""

import re
from dataclasses import dataclass, field
from datetime import UTC, date, datetime
from zoneinfo import ZoneInfo

from bs4 import BeautifulSoup


class ParseError(ValueError):
    def __init__(self, match_id: int, reason: str):
        self.match_id, self.reason = match_id, reason
        super().__init__(f"{match_id}: {reason}")


@dataclass
class ResultRow:
    match_id: int
    slug: str
    day: date


@dataclass
class Team:
    name: str
    team_id: int


@dataclass
class VetoStep:
    step: int
    team_tag: str | None
    action: str
    map: str


@dataclass
class Round:
    number: int
    winner: int
    winner_side: str | None
    win_type: str | None


@dataclass
class PlayerMap:
    player_id: int
    name: str
    team: int
    agents: list[str]
    rating: float | None
    acs: float | None
    kills: int | None
    deaths: int | None
    assists: int | None
    kast: float | None
    adr: float | None
    hs_pct: float | None
    fk: int | None
    fd: int | None


@dataclass
class MapResult:
    order: int
    game_id: int
    map: str
    picked: bool
    score1: int
    score2: int
    team1_atk: int | None
    team1_def: int | None
    team2_atk: int | None
    team2_def: int | None
    overtime: int
    duration: str | None
    players: list[PlayerMap]
    rounds: list[Round]


@dataclass
class Match:
    match_id: int
    event: str
    event_id: int
    stage: str
    start_utc: str
    best_of: int | None
    patch: str | None
    team1: Team
    team2: Team
    score1: int
    score2: int
    winner: int | None  # None for a drawn series (e.g. a 1–1 Bo2)
    veto: list[VetoStep]
    maps: list[MapResult]


@dataclass
class EconomyRound:
    number: int
    buy_type: str | None
    buy: int | None
    bank: int | None


@dataclass
class EconomyTeam:
    team: int
    pistols_won: int | None = None
    pistols_played: int | None = None
    conversions_won: int | None = None
    conversions_played: int | None = None
    bonus_won: int | None = None
    bonus_played: int | None = None
    eco_played: int | None = None
    eco_won: int | None = None
    semi_eco_played: int | None = None
    semi_eco_won: int | None = None
    semi_buy_played: int | None = None
    semi_buy_won: int | None = None
    half_buy_played: int | None = None
    half_buy_won: int | None = None
    full_buy_played: int | None = None
    full_buy_won: int | None = None
    rounds: list[EconomyRound] = field(default_factory=list)


@dataclass
class EconomyMap:
    game_id: int
    teams: list[EconomyTeam]


def _text(node) -> str:
    return " ".join(node.stripped_strings) if node else ""


def _number(node, integer=False):
    value = _text(node).strip().rstrip("%")
    if value in {"", "–", "—", "-"}:
        return None
    return int(value) if integer else float(value)


def _id(node, kind):
    return int(re.search(rf"/{kind}/(\d+)(?:/|$)", node["href"])[1])


def parse_results_page(html: str) -> list[ResultRow]:
    soup = BeautifulSoup(html, "lxml")
    rows, day = [], None
    for node in soup.select(".wf-label.mod-large, a.match-item[href]"):
        if node.name != "a":
            # Ignore the Today/Yesterday badge inside the heading.
            heading = " ".join(
                str(t).strip() for t in node.find_all(string=True, recursive=False)
            )
            day = datetime.strptime(heading.strip(), "%a, %B %d, %Y").date()
        else:
            link = re.fullmatch(r"/(\d+)/([^/?]+)/*", node["href"])
            if link:
                if day is None:
                    raise ValueError("results match has no day heading")
                rows.append(ResultRow(int(link[1]), link[2], day))
    return rows


def _players(game) -> list[PlayerMap]:
    players = []
    for team, table in enumerate(game.select(".ovw-table"), 1):
        for row in table.select(".ovw-row:not(.mod-head)"):
            link = row.select_one('a[href^="/player/"]')
            if not link:
                continue

            def stat(col, integer=False, row=row):
                return _number(row.select_one(f'[data-col="{col}"] .mod-both'), integer)

            players.append(
                PlayerMap(
                    _id(link, "player"),
                    _text(row.select_one(".ovw-player-name")),
                    team,
                    [i.get("alt", "") for i in row.select(".mod-agents img")],
                    stat("rating2"),
                    stat("acs"),
                    stat("kills", True),
                    stat("deaths", True),
                    stat("assists", True),
                    stat("kast"),
                    stat("adr"),
                    stat("hsp"),
                    stat("fb", True),
                    stat("fd", True),
                )
            )
    return players


def _map(game, order, match_id):
    header = game.select_one(".vm-stats-game-header")
    scores = [int(_text(s)) for s in header.select(".score")]
    if len(scores) != 2 or scores[0] == scores[1]:
        raise ParseError(match_id, "invalid map scores")
    rounds = []
    for col in game.select(".vlr-rounds-row-col[title]"):
        squares = col.select(".rnd-sq")
        if not squares:  # Header/side-swap column, not a round.
            continue
        winners = [
            (i, s) for i, s in enumerate(squares, 1) if "mod-win" in s.get("class", [])
        ]
        if len(winners) != 1:
            raise ParseError(match_id, "round has no unique winner")
        winner, square = winners[0]
        classes = square.get("class", [])
        side = "atk" if "mod-t" in classes else "def" if "mod-ct" in classes else None
        icon = square.select_one("img")
        win_type = icon["src"].rsplit("/", 1)[-1].split(".")[0] if icon else None
        if win_type not in {"elim", "boom", "defuse", "time"}:
            win_type = None
        number = int(_text(col.select_one(".rnd-num")))
        rounds.append(Round(number, winner, side, win_type))
    if len(rounds) != sum(scores):
        raise ParseError(match_id, f"rounds {len(rounds)} != score sum {sum(scores)}")
    if [r.number for r in rounds] != list(range(1, len(rounds) + 1)):
        raise ParseError(match_id, "round numbering is not consecutive")
    if [sum(r.winner == t for r in rounds) for t in (1, 2)] != scores:
        raise ParseError(match_id, "round winners disagree with map scores")
    halves = []
    for team in header.select(".team"):
        halves.extend(
            [
                _number(team.select_one("span.mod-t"), True),
                _number(team.select_one("span.mod-ct"), True),
            ]
        )
    name = header.select_one(".map-name")
    # Only direct map-name text, omitting the nested PICK badge.
    map_name = " ".join(
        t.strip()
        for t in name.find_all(string=True)
        if t.parent.get("class", []) == [] and t.strip()
    )
    if not map_name:
        map_name = _text(name).removesuffix(" PICK")
    return MapResult(
        order,
        int(game["data-game-id"]),
        map_name,
        header.select_one(".picked") is not None,
        *scores,
        *halves,
        max(0, sum(scores) - 24),
        _text(header.select_one(".map-duration")) or None,
        _players(game),
        rounds,
    )


def parse_match(html: str, match_id: int) -> Match:
    try:
        soup = BeautifulSoup(html, "lxml")
        header = soup.select_one(".match-header")
        event = header.select_one(".match-header-event")
        stage = event.select_one(".match-header-event-series")
        event_name = _text(event.select_one("div > div"))
        teams = [
            Team(_text(t.select_one(".wf-title-med")), _id(t, "team"))
            for t in header.select("a.match-header-link")
        ]
        stamp = header.select_one(".moment-tz-convert[data-utc-ts]")["data-utc-ts"]
        start = datetime.fromisoformat(stamp).replace(
            tzinfo=ZoneInfo("America/New_York")
        )
        scores = [
            int(_text(t))
            for t in header.select(".sp-hide > span")
            if _text(t).isdigit()
        ]
        if len(scores) != 2:
            raise ParseError(match_id, "missing series score")
        bo = re.search(r"\bBo(\d+)\b", _text(header))
        patch = re.search(r"\bPatch\s+([\d.]+)", _text(header))
        veto = []
        for part in _text(header.select_one(".match-header-note")).split(";"):
            part = part.strip()
            if not part:
                continue
            action = re.fullmatch(r"(.+?)\s+(ban|pick)\s+(.+)", part)
            decider = re.fullmatch(r"(.+?)\s+remains", part)
            if action:
                veto.append(VetoStep(len(veto) + 1, action[1], action[2], action[3]))
            elif decider:
                veto.append(VetoStep(len(veto) + 1, None, "decider", decider[1]))
            else:
                raise ParseError(match_id, f"unrecognized veto: {part}")
        maps = []
        for game in soup.select(".vm-stats-game[data-game-id]"):
            if game["data-game-id"] != "all" and game.select_one(
                ".vm-stats-game-header"
            ):
                maps.append(_map(game, len(maps) + 1, match_id))
        wins = [sum((m.score1 > m.score2) == (t == 1) for m in maps) for t in (1, 2)]
        if wins != scores:
            raise ParseError(match_id, f"series score {scores} != map wins {wins}")
        return Match(
            match_id,
            event_name,
            _id(event, "event"),
            _text(stage),
            start.astimezone(UTC).isoformat().replace("+00:00", "Z"),
            int(bo[1]) if bo else None,
            patch[1] if patch else None,
            *teams,
            *scores,
            None if scores[0] == scores[1] else 1 if scores[0] > scores[1] else 2,
            veto,
            maps,
        )
    except ParseError:
        raise
    except Exception as exc:
        raise ParseError(match_id, f"malformed match page: {exc}") from exc


def _pair(cell):
    values = re.fullmatch(r"(\d+)\s*/\s*(\d+)", _text(cell))
    return (int(values[1]), int(values[2])) if values else (0, 0)


def _money(node):
    value = re.search(r"([\d.]+)k", node.get("title", "")) if node else None
    return round(float(value[1]) * 1000) if value else None


def parse_economy(html: str) -> dict[int, EconomyMap]:
    soup = BeautifulSoup(html, "lxml")
    maps = {}
    for game in soup.select(".vm-stats-game[data-game-id]"):
        if game["data-game-id"] == "all" or not game.select_one(".ecs-wrap"):
            continue
        teams = [EconomyTeam(1), EconomyTeam(2)]
        opening = game.select_one("table.ecm-open")
        if opening:
            for team, row in zip(teams, opening.select("tr")[1:], strict=True):
                for name, cell in zip(
                    ("pistols", "conversions", "bonus"), row.select("td"), strict=True
                ):
                    won, played = _pair(cell)
                    setattr(team, name + "_won", won)
                    setattr(team, name + "_played", played)
        for table in game.select("table.ecm:not(.ecm-open)"):
            label = _text(table.select_one(".ecm-gt-t"))
            category = next(
                (
                    v
                    for k, v in [
                        ("On Eco", "eco"),
                        ("On Half buy", "half_buy"),
                        ("On Full buy", "full_buy"),
                    ]
                    if label.startswith(k)
                ),
                None,
            )
            if category:
                rows = [r for r in table.select("tr") if r.select("td")]
                for team, row in zip(teams, rows, strict=True):
                    pairs = [_pair(c) for c in row.select("td")]
                    setattr(team, category + "_won", sum(p[0] for p in pairs))
                    setattr(team, category + "_played", sum(p[1] for p in pairs))
        for col in game.select(".vlr-rounds-row-col"):
            if not col.select_one(".ecc-sq.mod-win"):
                continue
            for team in teams:
                buy = col.select_one(f".ecc-c.mod-t{team.team}")
                square = buy.select_one(".ecc-sq") if buy else None
                classes = square.get("class", []) if square else []
                category = next(
                    (
                        v
                        for k, v in [
                            ("mod-bp", "pistol"),
                            ("mod-b1", "eco"),
                            ("mod-b2", "half_buy"),
                            ("mod-b3", "full_buy"),
                        ]
                        if k in classes
                    ),
                    None,
                )
                team.rounds.append(
                    EconomyRound(
                        len(team.rounds) + 1,
                        category,
                        _money(buy),
                        _money(col.select_one(f".ecr-bank.mod-t{team.team}")),
                    )
                )
        game_id = int(game["data-game-id"])
        maps[game_id] = EconomyMap(game_id, teams)
    return maps
