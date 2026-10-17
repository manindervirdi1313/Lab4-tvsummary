"""TVMaze show summary package."""

from .aggregations import (
    Aggregation,
    GenreAggregation,
    LanguageRatingAggregation,
    PremiereDecadeAggregation,
    UniqueGenresAggregation,
)
from .models import Show
from .report import build_summary, write_summary
from .sources import TVMazeSource

__all__ = [
    "Aggregation",
    "GenreAggregation",
    "LanguageRatingAggregation",
    "PremiereDecadeAggregation",
    "Show",
    "TVMazeSource",
    "UniqueGenresAggregation",
    "build_summary",
    "write_summary",
]
