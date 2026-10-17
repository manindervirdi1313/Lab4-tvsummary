"""Deterministic selection of featured TV shows."""

import random
from typing import TypeVar

T = TypeVar("T")


def select_featured(
    records: list[T],
    sample_size: int,
    seed: int,
) -> list[T]:
    """Select a reproducible sample without modifying the input."""
    if sample_size < 0:
        raise ValueError("sample_size must be non-negative")

    generator = random.Random(seed)
    return generator.sample(records, k=min(sample_size, len(records)))
