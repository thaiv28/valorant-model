"""Model registry: factories accept keyword parameters; predictions precede updates."""

from typing import Protocol

from promval.ratings.elo import EloConfig, TeamElo


class Model(Protocol):
    def predict(self, row) -> float: ...

    def update(self, row) -> None: ...


class CoinModel:
    def predict(self, row):
        return 0.5

    def update(self, row):
        pass


class TeamEloModel:
    def __init__(self, **params):
        self.elo = TeamElo(EloConfig(**params))

    def predict(self, row):
        return self.elo.expected(row.team1_id, row.team2_id)

    def update(self, row):
        self.elo.update(row.team1_id, row.team2_id, row.won)


MODELS = {"coin": CoinModel, "team_elo": TeamEloModel}
