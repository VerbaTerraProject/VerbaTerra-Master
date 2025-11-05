from __future__ import annotations

import logging
from typing import Optional


def setup_logging(level: int = logging.INFO, *, name: Optional[str] = None) -> logging.Logger:
    logger = logging.getLogger(name)
    if not logger.handlers:
        handler = logging.StreamHandler()
        handler.setFormatter(logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s"))
        logger.addHandler(handler)
    logger.setLevel(level)
    return logger


__all__ = ["setup_logging"]
