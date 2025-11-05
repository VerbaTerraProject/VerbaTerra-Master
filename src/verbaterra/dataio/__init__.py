"""Data loading and schema utilities."""

from .schema import DATASET_SCHEMA, Schema, SchemaError, SchemaField, ensure_columns, validate_frame


def load_sample_dataset():
    from .loaders import load_sample_dataset as _load_sample_dataset

    return _load_sample_dataset()


def load_vsion_config(name: str = "default"):
    from .loaders import load_vsion_config as _load_vsion_config

    return _load_vsion_config(name=name)


__all__ = [
    "load_sample_dataset",
    "load_vsion_config",
    "DATASET_SCHEMA",
    "Schema",
    "SchemaError",
    "SchemaField",
    "ensure_columns",
    "validate_frame",
]
