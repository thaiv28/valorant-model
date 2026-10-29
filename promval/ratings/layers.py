"""Frozen post-model adjustments fitted exclusively on tuning predictions."""

import pandas as pd


class Layer:
    name: str

    def __init__(self, context=None):
        self.context = context or {}

    def fit(self, frame) -> None:
        raise NotImplementedError

    def apply(self, frame) -> pd.Series:
        raise NotImplementedError


class IdentityLayer(Layer):
    name = "none"

    def fit(self, frame) -> None:
        pass

    def apply(self, frame) -> pd.Series:
        return frame.p.copy()


LAYERS = {"none": IdentityLayer}
