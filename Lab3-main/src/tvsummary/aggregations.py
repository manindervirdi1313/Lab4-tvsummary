"""Aggregation classes for TV show summary statistics."""

from collections import defaultdict


class Aggregation:
    """Base class for all aggregations."""

    def __init__(self, shows):
        """Store the cleaned show records."""
        self.shows = shows

    def compute(self):
        """Calculate an aggregation result."""
        raise NotImplementedError("Subclasses must implement compute().")


class GenreAggregation(Aggregation):
    """Count shows in each genre."""

    def compute(self):
        counts = defaultdict(int)

        for show in self.shows:
            for genre in show.genres:
                counts[genre] += 1

        return dict(sorted(counts.items()))


class LanguageRatingAggregation(Aggregation):
    """Calculate average ratings grouped by language."""

    def compute(self):
        ratings = defaultdict(list)

        for show in self.shows:
            if show.language is None or show.rating is None:
                continue

            ratings[show.language].append(show.rating)

        return {
            language: round(sum(values) / len(values), 2)
            for language, values in sorted(ratings.items())
            if values
        }


class PremiereDecadeAggregation(Aggregation):
    """Count shows by premiere decade."""

    def compute(self):
        counts = defaultdict(int)

        for show in self.shows:
            if show.premiered is None:
                continue

            try:
                year = int(show.premiered[:4])
            except ValueError:
                continue

            if not 1 <= year <= 9999:
                continue

            decade = (year // 10) * 10
            counts[f"{decade}s"] += 1

        return dict(sorted(counts.items()))


class UniqueGenresAggregation(Aggregation):
    """Return all unique genre names."""

    def compute(self):
        genres = {genre for show in self.shows for genre in show.genres}

        return sorted(genres)
