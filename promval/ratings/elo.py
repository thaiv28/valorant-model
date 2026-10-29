"""Team Elo with binary map-win updates."""

from dataclasses import dataclass


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
