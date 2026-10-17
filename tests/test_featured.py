
"""Tests for featured-show selection."""

import pytest

from tvsummary.featured import select_featured


def test_same_seed_produces_same_selection() -> None:
    """A fixed seed produces a reproducible sample."""
    records = list(range(20))

    first = select_featured(records, sample_size=5, seed=42)
    second = select_featured(records, sample_size=5, seed=42)

    assert first == second
    assert len(first) == 5


def test_sample_does_not_change_input() -> None:
    """Sampling leaves the original records unchanged."""
    records = list(range(10))
    original = records.copy()

    select_featured(records, sample_size=4, seed=42)

    assert records == original


def test_negative_sample_size_is_rejected() -> None:
    """A negative sample size is invalid."""
    with pytest.raises(ValueError, match="non-negative"):
        select_featured([1, 2, 3], sample_size=-1, seed=42)
