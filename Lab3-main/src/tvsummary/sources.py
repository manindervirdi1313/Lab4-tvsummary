
"""Data sources for TV show records."""

import json

import requests

from .config import API_URL, TIMEOUT_SECONDS
from .models import Show


class TVMazeSource:
    """Fetch TVMaze records and convert them into Show objects."""

    def __init__(self, url=API_URL, timeout=TIMEOUT_SECONDS):
        """Configure the source URL and request timeout."""
        self.url = url
        self.timeout = timeout

    def fetch(self):
        """Download, validate and return cleaned show records."""
        try:
            response = requests.get(self.url, timeout=self.timeout)
            response.raise_for_status()
            records = response.json()

            if not isinstance(records, list):
                raise ValueError("The API response is not a list.")

            if not all(isinstance(record, dict) for record in records):
                raise ValueError("The API response contains invalid records.")

            return [Show(record) for record in records]

        except requests.exceptions.RequestException as error:
            raise RuntimeError(
                f"Could not download TVMaze data: {error}"
            ) from error

        except (ValueError, json.JSONDecodeError) as error:
            raise RuntimeError(
                f"Could not read valid JSON data: {error}"
            ) from error