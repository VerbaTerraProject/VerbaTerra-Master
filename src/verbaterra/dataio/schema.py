from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Sequence

import pandas as pd


class SchemaError(ValueError):
    """Raised when a DataFrame fails schema validation."""


@dataclass(frozen=True)
class SchemaField:
    name: str
    kind: str = "numeric"
    description: str | None = None

    def validate(self, series: pd.Series) -> None:
        if self.kind == "numeric" and not pd.api.types.is_numeric_dtype(series):
            raise SchemaError(f"Column '{self.name}' must be numeric; received {series.dtype}.")


@dataclass(frozen=True)
class Schema:
    fields: Sequence[SchemaField]

    def names(self) -> Sequence[str]:
        return [field.name for field in self.fields]

    def field_map(self) -> dict[str, SchemaField]:
        return {field.name: field for field in self.fields}


DATASET_SCHEMA = Schema(
    fields=[
        SchemaField("ritual"),
        SchemaField("trade"),
        SchemaField("symbolism"),
        SchemaField("hierarchy"),
        SchemaField("lexical_diversity"),
        SchemaField("syntax_complexity"),
    ]
)


def validate_frame(df: pd.DataFrame, schema: Schema) -> pd.DataFrame:
    missing = [name for name in schema.names() if name not in df.columns]
    if missing:
        raise SchemaError(f"Missing required columns: {missing}")

    for name, field in schema.field_map().items():
        field.validate(df[name])

    return df


def ensure_columns(df: pd.DataFrame, columns: Iterable[str]) -> None:
    missing = [col for col in columns if col not in df.columns]
    if missing:
        raise SchemaError(f"Missing columns: {missing}")
