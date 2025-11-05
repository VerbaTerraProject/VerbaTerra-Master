"""Integration-adaptation hypothesis registry."""

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
            identifier="IA-1",
            statement=(
                "Integration shock triggers adaptation cycles in both ritual tempo "
                "and lexical variance within three epochs."
            ),
        ),
        Hypothesis(
            identifier="IA-2",
            statement=(
                "Communities that co-adapt trade and ritual signals sustain higher "
                "NLIS scores after disruptive events."
            ),
        ),
    ]


__all__ = ["Hypothesis", "catalog"]
