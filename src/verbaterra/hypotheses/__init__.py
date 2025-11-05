"""Hypothesis registries grouped by theme."""

from .integration_adaptation import catalog as integration_catalog
from .ritual_syntax import catalog as ritual_syntax_catalog
from .symbolism_semantics import catalog as symbolism_catalog
from .trade_lexicon import catalog as trade_catalog

__all__ = [
    "integration_catalog",
    "ritual_syntax_catalog",
    "symbolism_catalog",
    "trade_catalog",
]
