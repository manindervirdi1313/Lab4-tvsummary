"""Shared fixtures for tvsummary tests."""

import pytest


@pytest.fixture
def sample_show_data() -> list[dict[str, object]]:
    """Provide sample TVMaze-style show records."""
    return [
        {
            "id": 1,
            "name": "Example Drama",
            "genres": ["Drama"],
            "rating": {"average": 8.5},
            "language": "English",
            "premiered": "2020-01-01",
        },
        {
            "id": 2,
            "name": "Example Comedy",
            "genres": ["Comedy"],
            "rating": {"average": 7.5},
            "language": "English",
            "premiered": "2015-06-01",
        },
        {
            "id": 3,
            "name": "Example Mystery",
            "genres": [],
            "rating": {"average": None},
            "language": "French",
            "premiered": None,
        },
    ]
