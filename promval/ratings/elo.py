"""Composable Elo variants and the original binary team Elo reference."""

from dataclasses import dataclass
from math import exp, log, tanh

from promval.ratings.regions import macro_region
from promval.ratings.rounds import map_win


@dataclass(frozen=True)
class EloConfig:
    k: float = 32.0
    init: float = 1500.0
    scale: float = 400.0


class TeamElo:
    def __init__(self, config=None):
        self.config = config or EloConfig()
        self.ratings = {}

    def expected(self, a, b):
        rating_a = self.ratings.get(a, self.config.init)
        rating_b = self.ratings.get(b, self.config.init)
        return 1 / (1 + 10 ** ((rating_b - rating_a) / self.config.scale))

    def update(self, a, b, score_a):
        delta = self.config.k * (score_a - self.expected(a, b))
        self.ratings[a] = self.ratings.get(a, self.config.init) + delta
        self.ratings[b] = self.ratings.get(b, self.config.init) - delta


class EloModel:
    """Composable credit, rating unit and macro-region offsets.

    predict may initialize starters, but only update records lineup/home history.
    Home counts have four buckets, so all history maintenance is constant time.
    """

    def __init__(
        self,
        *,
        unit="team",
        credit="binary",
        k=32.0,
        c=4.0,
        tau=1.0,
        region_k=0.0,
        new_player="fixed",
        lineups=None,
        init=1500.0,
        scale=400.0,
    ):
        if unit not in {"team", "player"} or credit not in {
            "binary",
            "margin",
            "round",
        }:
            raise ValueError("unknown Elo unit or credit")
        if new_player not in {"fixed", "teammates"}:
            raise ValueError("unknown new_player mode")
        if k <= 0 or c <= 0 or tau <= 0 or region_k < 0 or scale <= 0:
            raise ValueError("Elo parameters must be positive (region_k may be zero)")
        self.unit, self.credit = unit, credit
        self.k, self.c, self.tau = k, c, tau
        self.region_k, self.new_player = region_k, new_player
        self.init, self.scale = init, scale
        self.lineups = lineups if lineups is not None else {}
        self.ratings = {}
        self.last_lineups = {}
        self.homes = {}
        self.home_counts = {}
        self.offsets = {}
        # Preserve the v1 public rating accessor.
        self.elo = self

    def _units(self, row, side):
        team = getattr(row, f"team{side}_id")
        if self.unit == "team":
            return (team,)
        starters = self.lineups.get(row.game_id, ((), ()))[side - 1]
        if starters:
            return starters
        return self.last_lineups.get(team, (("team", team),))

    def _strength(self, units):
        known = [self.ratings[p] for p in units if p in self.ratings]
        initial = (
            sum(known) / len(known)
            if known and self.new_player == "teammates"
            else self.init
        )
        for player in units:
            self.ratings.setdefault(player, initial)
        return sum(self.ratings[p] for p in units) / len(units)

    def _state(self, row):
        a, b = self._units(row, 1), self._units(row, 2)
        home_a, home_b = self.homes.get(row.team1_id), self.homes.get(row.team2_id)
        strength_a, strength_b = self._strength(a), self._strength(b)
        if self.region_k:
            strength_a += self.offsets.get(home_a, 0)
            strength_b += self.offsets.get(home_b, 0)
        # Stable logistic, algebraically the original base-ten Elo formula.
        x = (strength_a - strength_b) / self.scale
        if abs(x) < 300:
            expected = 1 / (1 + 10 ** (-x))
        else:
            expected = 1.0 if x > 0 else 0.0
        return a, b, home_a, home_b, expected

    def predict(self, row):
        expected = self._state(row)[-1]
        if self.credit != "round":
            return expected
        p = map_win(expected)
        if p in (0, 1):
            return p
        log_odds = self.tau * (log(p) - log(1 - p))
        if log_odds >= 0:
            return 1 / (1 + exp(-log_odds))
        odds = exp(log_odds)
        return odds / (1 + odds)

    def score(self, row):
        if self.credit == "binary":
            return row.won
        if self.credit == "round":
            return row.score1 / (row.score1 + row.score2)
        magnitude = 0.5 * tanh(abs(row.score1 - row.score2) / self.c)
        return 0.5 + (magnitude if row.won else -magnitude)

    def update(self, row):
        a, b, home_a, home_b, expected = self._state(row)
        error = self.score(row) - expected
        delta = self.k * error
        for units, change in ((a, delta), (b, -delta)):
            for player in units:
                self.ratings[player] += change
        if (
            self.region_k
            and home_a is not None
            and home_b is not None
            and home_a != home_b
        ):
            change = self.region_k * error
            self.offsets[home_a] = self.offsets.get(home_a, 0) + change
            self.offsets[home_b] = self.offsets.get(home_b, 0) - change
        region = macro_region(getattr(row, "region", None))
        for side, units in ((1, a), (2, b)):
            team = getattr(row, f"team{side}_id")
            if self.unit == "player":
                self.last_lineups[team] = units
            if (
                self.region_k
                and region is not None
                and not getattr(row, "international", False)
            ):
                counts = self.home_counts.setdefault(team, {})
                counts[region] = counts.get(region, 0) + 1
                previous = self.homes.get(team)
                # The incremented bucket is the only possible new leader.
                if counts[region] > counts.get(previous, 0):
                    self.homes[team] = region
