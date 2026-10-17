"""Central configuration for the TV summary package."""

from pathlib import Path

API_URL = "https://api.tvmaze.com/shows?page=0"
TIMEOUT_SECONDS = 15

PROJECT_ROOT = Path(__file__).resolve().parents[2]
OUTPUT_FILE = PROJECT_ROOT / "data" / "processed" / "summary.json"
