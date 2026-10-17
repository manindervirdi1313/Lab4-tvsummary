"""Offline tests for the TVMaze data source."""

from unittest.mock import Mock, patch

import pytest
import requests

from tvsummary.errors import DataSourceError, DataValidationError
from tvsummary.sources import TVMazeSource


@patch("tvsummary.sources.requests.get")
def test_fetch_returns_shows(mock_get: Mock) -> None:
    """A successful response is converted into Show objects."""
    mock_response = Mock()
    mock_response.json.return_value = [
        {
            "id": 1,
            "name": "Example Drama",
            "genres": ["Drama"],
            "rating": {"average": 8.5},
            "language": "English",
            "premiered": "2020-01-01",
        }
    ]
    mock_get.return_value = mock_response

    shows = TVMazeSource().fetch()

    mock_get.assert_called_once()
    mock_response.raise_for_status.assert_called_once()
    assert len(shows) == 1
    assert shows[0].genres == ["Drama"]
    assert shows[0].rating == 8.5


@patch("tvsummary.sources.requests.get")
def test_fetch_handles_request_failure(mock_get: Mock) -> None:
    """A network failure is translated into DataSourceError."""
    mock_get.side_effect = requests.exceptions.ConnectionError("offline")

    with pytest.raises(DataSourceError, match="Could not download TVMaze data"):
        TVMazeSource().fetch()


@patch("tvsummary.sources.requests.get")
def test_fetch_handles_invalid_json(mock_get: Mock) -> None:
    """A JSON decoding failure is translated into DataSourceError."""
    mock_response = Mock()
    mock_response.raise_for_status.return_value = None
    mock_response.json.side_effect = ValueError("invalid JSON")
    mock_get.return_value = mock_response

    with pytest.raises(DataSourceError, match="Could not decode TVMaze JSON"):
        TVMazeSource().fetch()


@pytest.mark.parametrize("payload", [{"name": "not a list"}, None, "invalid"])
@patch("tvsummary.sources.requests.get")
def test_fetch_rejects_non_list_response(
    mock_get: Mock, payload: object
) -> None:
    """A response that is not a list is rejected."""
    mock_response = Mock()
    mock_response.json.return_value = payload
    mock_get.return_value = mock_response

    with pytest.raises(DataValidationError, match="response is not a list"):
        TVMazeSource().fetch()


@patch("tvsummary.sources.requests.get")
def test_fetch_rejects_non_dictionary_records(mock_get: Mock) -> None:
    """A list containing invalid records is rejected."""
    mock_response = Mock()
    mock_response.json.return_value = [{"name": "valid"}, "invalid"]
    mock_get.return_value = mock_response

    with pytest.raises(DataValidationError, match="invalid records"):
        TVMazeSource().fetch()
