"""Data models for TVMaze records."""


class Show:
    """Represent one cleaned TVMaze show record."""

    def __init__(self, data):
        """Create a show and normalize potentially invalid values."""
        if not isinstance(data, dict):
            raise ValueError("A show record must be a dictionary.")

        self.genres = self._clean_genres(data.get("genres"))
        self.language = self._clean_text(data.get("language"))
        self.rating = self._clean_rating(data.get("rating"))
        self.premiered = self._clean_premiered(data.get("premiered"))

    @staticmethod
    def _clean_text(value):
        """Return stripped text, or None for invalid or empty text."""
        if isinstance(value, str) and value.strip():
            return value.strip()
        return None

    @staticmethod
    def _clean_genres(value):
        """Return a list of non-empty genre names."""
        if not isinstance(value, list):
            return []

        return [
            genre.strip() for genre in value if isinstance(genre, str) and genre.strip()
        ]

    @staticmethod
    def _clean_rating(value):
        """Return a valid rating from 0 to 10, or None."""
        if not isinstance(value, dict):
            return None

        rating = value.get("average")

        if isinstance(rating, bool) or not isinstance(rating, (int, float)):
            return None

        if not 0 <= rating <= 10:
            return None

        return rating

    @staticmethod
    def _clean_premiered(value):
        """Return a usable premiere date, or None."""
        if not isinstance(value, str) or len(value) < 4:
            return None

        try:
            year = int(value[:4])
        except ValueError:
            return None

        if not 1 <= year <= 9999:
            return None

        return value

    def __str__(self):
        """Return a readable description of the show."""
        return f"Show(language={self.language!r}, genres={self.genres!r})"
