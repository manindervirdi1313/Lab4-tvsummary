
"""Network-free tests for TV summary aggregations."""

import unittest

from tvsummary.aggregations import (
    GenreAggregation,
    LanguageRatingAggregation,
    PremiereDecadeAggregation,
    UniqueGenresAggregation,
)
from tvsummary.models import Show


class TestAggregations(unittest.TestCase):
    """Test aggregation results using sample records."""

    def setUp(self):
        """Create sample shows without making network requests."""
        self.shows = [
            Show({
                "genres": ["Drama", "Comedy"],
                "language": "English",
                "rating": {"average": 8.0},
                "premiered": "1995-01-01",
            }),
            Show({
                "genres": ["Drama"],
                "language": "English",
                "rating": {"average": 6.0},
                "premiered": "2005-03-10",
            }),
            Show({
                "genres": ["Comedy"],
                "language": "French",
                "rating": {"average": 9.0},
                "premiered": "1998-06-20",
            }),
        ]

    def test_genre_counts(self):
        result = GenreAggregation(self.shows).compute()

        self.assertEqual(result, {"Comedy": 2, "Drama": 2})

    def test_average_rating_by_language(self):
        result = LanguageRatingAggregation(self.shows).compute()

        self.assertEqual(result, {"English": 7.0, "French": 9.0})

    def test_premiere_decade_counts(self):
        result = PremiereDecadeAggregation(self.shows).compute()

        self.assertEqual(result, {"1990s": 2, "2000s": 1})

    def test_unique_genres(self):
        result = UniqueGenresAggregation(self.shows).compute()

        self.assertEqual(result, ["Comedy", "Drama"])


if __name__ == "__main__":
    unittest.main()