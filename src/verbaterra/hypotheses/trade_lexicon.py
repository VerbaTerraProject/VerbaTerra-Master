"""Trade-lexicon hypothesis space."""

from __future__ import annotations

from dataclasses import dataclass
from typing import List


@dataclass(frozen=True)
class Hypothesis:
    identifier: str
    statement: str


def catalog() -> List[Hypothesis]:
    return [
        Hypothesis(
            identifier="TL-1",
            statement=(
                "Expanded trade networks lead to lexical diversification until "
                "transaction costs dominate cognitive load."
            ),
        ),
        Hypothesis(
            identifier="TL-2",
            statement=(
                "Lexical borrowing spikes immediately after trade route convergence "
                "events in the simulation logs."
            ),
        ),
    ]


__all__ = ["Hypothesis", "catalog"]
