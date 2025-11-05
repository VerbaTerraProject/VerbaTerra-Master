"""Ritual-syntax hypothesis definitions."""

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
            identifier="RS-1",
            statement="Ritual intensity positively correlates with syntax complexity when hierarchical norms remain moderate.",
        ),
        Hypothesis(
            identifier="RS-2",
            statement="Communities with oscillatory ritual schedules experience periodic syntax contractions followed by rebounds.",
        ),
    ]


__all__ = ["Hypothesis", "catalog"]
