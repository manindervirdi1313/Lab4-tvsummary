
"""
TV Show Aggregator
Downloads TVMaze show records and creates summary statistics.
"""

import json
from collections import defaultdict
from pathlib import Path

import requests


def get_unique_genres(shows):
    """Return all distinct, non-empty genre names."""
    genres = set()

    for show in shows:
        show_genres = show.get("genres")

        if not isinstance(show_genres, list):
            continue

        for genre in show_genres:
            if isinstance(genre, str) and genre.strip():
                genres.add(genre.strip())

    return sorted(genres)


API_URL = "https://api.tvmaze.com/shows?page=0"
OUTPUT_FILE = Path("summary.json")
TIMEOUT_SECONDS = 15


def fetch_shows(url=API_URL):
    """Download show records from TVMaze and validate the response."""
    try:
        response = requests.get(url, timeout=TIMEOUT_SECONDS)
        response.raise_for_status()
        shows = response.json()

        if not isinstance(shows, list):
            raise ValueError("The API response is not a list.")

        if not all(isinstance(show, dict) for show in shows):
            raise ValueError("The API response contains invalid records.")

        return shows

    except requests.exceptions.RequestException as error:
        raise RuntimeError(f"Could not download TVMaze data: {error}") from error
    except (ValueError, json.JSONDecodeError) as error:
        raise RuntimeError(f"Could not read valid JSON data: {error}") from error


def count_shows_by_genre(shows):
    """Count shows in each genre."""
    genre_counts = defaultdict(int)

    for show in shows:
        genres = show.get("genres", [])

        if not isinstance(genres, list):
            continue

        for genre in genres:
            if isinstance(genre, str) and genre.strip():
                genre_counts[genre.strip()] += 1

    return dict(sorted(genre_counts.items()))


def average_rating_by_language(shows):
    """Calculate average ratings for shows grouped by language."""
    ratings = defaultdict(list)

    for show in shows:
        language = show.get("language")
        rating_data = show.get("rating")

        if not isinstance(language, str) or not language.strip():
            continue

        if not isinstance(rating_data, dict):
            continue

        rating = rating_data.get("average")

        # Exclude missing, non-numeric, and invalid rating values.
        if isinstance(rating, bool) or not isinstance(rating, (int, float)):
            continue

        if not 0 <= rating <= 10:
            continue

        ratings[language.strip()].append(rating)

    return {
        language: round(sum(values) / len(values), 2)
        for language, values in sorted(ratings.items())
        if values
    }


def count_shows_by_decade(shows):
    """Count shows by premiere decade using their premiere dates."""
    decade_counts = defaultdict(int)

    for show in shows:
        premiere_date = show.get("premiered")

        if not isinstance(premiere_date, str) or len(premiere_date) < 4:
            continue

        try:
            year = int(premiere_date[:4])

            if year < 1 or year > 9999:
                continue

            decade = (year // 10) * 10
            decade_counts[f"{decade}s"] += 1

        except ValueError:
            continue

    return dict(sorted(decade_counts.items()))


def get_unique_genres(shows):
    """Return all distinct, non-empty genre names."""
    genres = {
        genre.strip()
        for show in shows
        for genre in show.get("genres", [])
        if isinstance(show.get("genres"), list)
        and isinstance(genre, str)
        and genre.strip()
    }

    return sorted(genres)


def build_summary(shows):
    """Build the complete summary without writing any files."""
    return {
        "source_url": API_URL,
        "records_processed": len(shows),
        "shows_per_genre": count_shows_by_genre(shows),
        "average_rating_by_language": average_rating_by_language(shows),
        "shows_per_premiere_decade": count_shows_by_decade(shows),
        "unique_genres": get_unique_genres(shows),
    }


def write_summary(summary, output_file=OUTPUT_FILE):
    """Write the summary dictionary to a readable JSON file."""
    with output_file.open("w", encoding="utf-8") as file:
        json.dump(summary, file, indent=4, ensure_ascii=False)
        file.write("\n")


def main():
    """Run the data aggregation workflow."""
    try:
        shows = fetch_shows()
        summary = build_summary(shows)
        write_summary(summary)

        print(f"Processed {summary['records_processed']} TV shows.")
        print(f"Summary written to {OUTPUT_FILE.resolve()}")

    except (RuntimeError, OSError, ValueError) as error:
        print(f"Error: {error}")


if __name__ == "__main__":
    main()