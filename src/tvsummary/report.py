"""Build and write the TV show summary report."""

import json
import logging
from pathlib import Path
from typing import Any

from tvsummary.aggregations import (
    GenreAggregation,
    LanguageRatingAggregation,
    PremiereDecadeAggregation,
    UniqueGenresAggregation,
)
from tvsummary.config import API_URL, OUTPUT_FILE
from tvsummary.errors import ReportError
from tvsummary.models import Show

logger = logging.getLogger(__name__)


def build_summary(
    shows: list[Show],
    source_url: str = API_URL,
) -> dict[str, Any]:
    """Build the complete summary without writing a file."""
    aggregations = [
        ("shows_per_genre", GenreAggregation(shows)),
        ("average_rating_by_language", LanguageRatingAggregation(shows)),
        ("shows_per_premiere_decade", PremiereDecadeAggregation(shows)),
        ("unique_genres", UniqueGenresAggregation(shows)),
    ]

    summary: dict[str, Any] = {
        "source_url": source_url,
        "records_processed": len(shows),
    }

    for name, aggregation in aggregations:
        summary[name] = aggregation.compute()

    logger.info("Built summary for %s records", len(shows))
    return summary


def write_summary(
    summary: dict[str, Any],
    output_file: Path = OUTPUT_FILE,
) -> None:
    """Write the summary dictionary to a readable JSON file."""
    try:
        output_file.parent.mkdir(parents=True, exist_ok=True)
        with output_file.open("w", encoding="utf-8") as file:
            json.dump(summary, file, indent=4, ensure_ascii=False)
            file.write("\n")
    except OSError as error:
        raise ReportError(
            f"Could not write summary to {output_file}: {error}"
        ) from error

    logger.info("Wrote summary to %s", output_file)
