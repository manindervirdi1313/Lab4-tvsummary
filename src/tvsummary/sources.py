"""Data sources for TV show records."""

import logging

import requests

from tvsummary.config import API_URL, TIMEOUT_SECONDS
from tvsummary.errors import DataSourceError, DataValidationError
from tvsummary.models import Show

logger = logging.getLogger(__name__)


class TVMazeSource:
    """Fetch TVMaze records and convert them into Show objects."""

    def __init__(
        self,
        url: str = API_URL,
        timeout: float = TIMEOUT_SECONDS,
    ) -> None:
        """Configure the source URL and request timeout."""
        self.url = url
        self.timeout = timeout

    def fetch(self) -> list[Show]:
        """Download, validate and return cleaned show records."""
        logger.info("Fetching shows from %s", self.url)

        try:
            response = requests.get(self.url, timeout=self.timeout)
            response.raise_for_status()
            records = response.json()
        except requests.exceptions.RequestException as error:
            raise DataSourceError(f"Could not download TVMaze data: {error}") from error
        except ValueError as error:
            raise DataSourceError(f"Could not decode TVMaze JSON: {error}") from error

        if not isinstance(records, list):
            raise DataValidationError("The API response is not a list.")

        if not all(isinstance(record, dict) for record in records):
            raise DataValidationError("The API response contains invalid records.")

        try:
            shows = [Show(record) for record in records]
        except (KeyError, TypeError, ValueError) as error:
            raise DataValidationError(
                f"The API response contains an invalid show: {error}"
            ) from error

        logger.info("Fetched %s show records", len(shows))
        return shows
