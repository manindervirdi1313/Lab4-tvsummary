"""Build and write the TV show summary report."""

import json

from .aggregations import (
    GenreAggregation,
    LanguageRatingAggregation,
    PremiereDecadeAggregation,
    UniqueGenresAggregation,
)
from .config import API_URL, OUTPUT_FILE


def build_summary(shows):
    """Build the complete summary without writing a file."""

    aggregations = [
        ("shows_per_genre", GenreAggregation(shows)),
        (
            "average_rating_by_language",
            LanguageRatingAggregation(shows),
        ),
        (
            "shows_per_premiere_decade",
            PremiereDecadeAggregation(shows),
        ),
        ("unique_genres", UniqueGenresAggregation(shows)),
    ]

    summary = {
        "source_url": API_URL,
        "records_processed": len(shows),
    }

    # Polymorphism: each object uses its own compute() implementation.
    for name, aggregation in aggregations:
        summary[name] = aggregation.compute()

    return summary


def write_summary(summary, output_file=OUTPUT_FILE):
    """Write the summary dictionary to a readable JSON file."""

    output_file.parent.mkdir(parents=True, exist_ok=True)

    with output_file.open("w", encoding="utf-8") as file:
        json.dump(summary, file, indent=4, ensure_ascii=False)
        file.write("\n")
