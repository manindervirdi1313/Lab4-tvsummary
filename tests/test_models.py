"""Tests for TVMaze show model validation."""

import pytest

from tvsummary.models import Show


def test_show_cleans_valid_record(sample_show_data: list[dict[str, object]]) -> None:
    """A valid record is cleaned and stored correctly."""
    show = Show(sample_show_data[0])

    assert show.genres == ["Drama"]
    assert show.language == "English"
    assert show.rating == 8.5
    assert show.premiered == "2020-01-01"


def test_missing_genres_become_empty_list() -> None:
    """Missing genres are normalized to an empty list."""
    show = Show({"language": "English"})

    assert show.genres == []


def test_missing_rating_becomes_none() -> None:
    """Missing rating data is normalized to None."""
    show = Show({"genres": ["Drama"]})

    assert show.rating is None


@pytest.mark.parametrize(
    "value",
    [None, "Drama", 123, ["Drama", "", None, " Comedy "]],
)
def test_genres_are_cleaned(value: object) -> None:
    """Invalid genres are removed and valid names are stripped."""
    show = Show({"genres": value})

    if value == ["Drama", "", None, " Comedy "]:
        assert show.genres == ["Drama", "Comedy"]
    else:
        assert show.genres == []


@pytest.mark.parametrize(
    "rating",
    [
        None,
        {},
        {"average": None},
        {"average": -1},
        {"average": 11},
        {"average": True},
        {"average": "8.5"},
    ],
)
def test_invalid_ratings_become_none(rating: object) -> None:
    """Invalid ratings are normalized to None."""
    show = Show({"rating": rating})

    assert show.rating is None


def test_non_dictionary_record_raises_value_error() -> None:
    """A record that is not a dictionary is rejected."""
    with pytest.raises(ValueError, match="must be a dictionary"):
        Show("not a record")  # type: ignore[arg-type]  # Intentionally test invalid input.


def test_text_fields_are_stripped() -> None:
    """Valid text fields have surrounding whitespace removed."""
    show = Show(
        {
            "language": " English ",
            "genres": [" Drama "],
            "premiered": "2020-01-01",
        }
    )

    assert show.language == "English"
    assert show.genres == ["Drama"]


def test_invalid_premiere_date_becomes_none() -> None:
    """An unusable premiere date is normalized to None."""
    show = Show({"premiered": "abcd"})

    assert show.premiered is None
