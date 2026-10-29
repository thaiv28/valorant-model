"""Model registry: factories accept keyword parameters; predictions precede updates."""

from functools import partial
from typing import Protocol

from promval.ratings.elo import EloModel


class Model(Protocol):
    def predict(self, row) -> float: ...

    def update(self, row) -> None: ...


class CoinModel:
    def predict(self, row):
        return 0.5

    def update(self, row):
        pass


class TeamEloModel(EloModel):
    """v1 name retained for team/binary Elo without offsets."""


MODELS = {"coin": CoinModel, "team_elo": TeamEloModel}
PARAM_GRIDS = {"coin": {}, "team_elo": {"k": (16, 24, 32, 48, 64, 96)}}
for unit in ("team", "player"):
    for credit in ("binary", "margin", "round"):
        for region in (False, True):
            if (unit, credit, region) == ("team", "binary", False):
                continue
            name = f"{unit}_{credit}" + ("_region" if region else "")
            MODELS[name] = partial(
                EloModel, unit=unit, credit=credit, region_k=16 if region else 0
            )
            grid = {"k": (16, 24, 32, 48, 64, 96)}
            if credit == "margin":
                grid["c"] = (4, 6, 8, 12)
            if credit == "round":
                grid["tau"] = (0.4, 0.5, 0.6, 0.8, 1.0)
            if region:
                grid["region_k"] = (2, 4, 8, 16)
            if unit == "player":
                grid["new_player"] = ("fixed", "teammates")
            PARAM_GRIDS[name] = grid

for region in (False, True):
    name = "player_round" + ("_region" if region else "") + "_glicko"
    MODELS[name] = partial(
        EloModel, unit="player", credit="round", rd=True, region_k=4 if region else 0
    )
    PARAM_GRIDS[name] = {
        "k": (16, 24, 32, 48, 64),
        "tau": (0.4, 0.5, 0.6, 0.8),
        "rd_new": (280, 350, 450, 600),
        "rd_info": (0.125, 0.25, 0.5, 1.0),
        "new_player": ("fixed", "teammates"),
    }
    if region:
        PARAM_GRIDS[name]["region_k"] = (2, 4)

for variant in ("rookie", "moves", "rookie_moves"):
    name = f"player_round_glicko_{variant}"
    MODELS[name] = partial(EloModel, unit="player", credit="round", rd=True)
    grid = {
        "k": (32, 48),
        "tau": (0.4, 0.5),
        "rd_new": (280, 350),
        "rd_info": (0.25,),
        "new_player": ("teammates",),
    }
    if "rookie" in variant:
        grid.update(
            k=(32,),
            rd_new=(280,),
            rookie_penalty=(50, 100, 150, 200, 300),
            rookie_maps=(100, 200, 400, 800),
        )
    if "moves" in variant:
        grid.update(move_up_penalty=(50, 100, 200), move_down_bonus=(0, 50))
    PARAM_GRIDS[name] = grid

for variant in ("maps", "pick", "revert"):
    name = f"player_round_glicko_rookie_{variant}"
    base = {
        "k": 32,
        "tau": 0.5,
        "rd_new": 280,
        "rd_info": 0.25,
        "new_player": "teammates",
        "rookie_penalty": 200,
        "rookie_maps": 400,
    }
    MODELS[name] = partial(EloModel, unit="player", credit="round", rd=True, **base)
    PARAM_GRIDS[name] = {key: (value,) for key, value in base.items()}
    if variant == "revert":
        PARAM_GRIDS[name].update(
            season_revert=(0, 0.1, 0.2, 0.35, 0.5),
            season_month=(1, 11),
            inactive_half_life=(0, 180, 365, 730),
        )
        continue
    PARAM_GRIDS[name].update(
        map_k=(0.5, 1, 2, 4) if variant == "maps" else (0,),
        pick_bonus=(0, 3) if variant == "maps" else (1, 2, 3, 5, 8),
    )
    if variant == "maps":
        PARAM_GRIDS[name]["map_unit"] = ("player", "team")
