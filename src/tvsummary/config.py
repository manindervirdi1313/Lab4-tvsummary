
"""Load and validate application settings from TOML."""

import logging
import tomllib
from dataclasses import dataclass
from pathlib import Path

from tvsummary.errors import SettingsError

logger = logging.getLogger(__name__)

# Backward-compatible defaults for the original Lab 03 modules.
API_URL = "https://api.tvmaze.com/shows?page=0"
TIMEOUT_SECONDS = 15
OUTPUT_FILE = Path("data/processed/summary.json")


@dataclass(frozen=True)
class AppConfig:
    """Immutable application configuration."""

    source_url: str
    timeout: float
    output_folder: Path
    seed: int
    sample_size: int
    log_level: str


def load_config(config_path: str | Path) -> AppConfig:
    """Load and validate settings from a TOML file."""
    path = Path(config_path)

    try:
        with path.open("rb") as file:
            document = tomllib.load(file)
    except FileNotFoundError as error:
        raise SettingsError(
            f"Configuration file not found: {path}"
        ) from error
    except tomllib.TOMLDecodeError as error:
        raise SettingsError(
            f"Invalid TOML configuration: {path}"
        ) from error
    except OSError as error:
        raise SettingsError(
            f"Cannot read configuration file: {path}"
        ) from error

    app = document.get("app")
    if not isinstance(app, dict):
        raise SettingsError("Configuration must contain an [app] section.")

    required = {
        "source_url",
        "timeout",
        "output_folder",
        "seed",
        "sample_size",
        "log_level",
    }
    missing = required - app.keys()
    if missing:
        raise SettingsError(
            f"Missing configuration settings: {', '.join(sorted(missing))}"
        )

    source_url = app["source_url"]
    timeout = app["timeout"]
    output_folder = app["output_folder"]
    seed = app["seed"]
    sample_size = app["sample_size"]
    log_level = app["log_level"]

    if not isinstance(source_url, str) or not source_url.startswith("https://"):
        raise SettingsError("source_url must be an HTTPS URL.")

    if isinstance(timeout, bool) or not isinstance(timeout, (int, float)):
        raise SettingsError("timeout must be a positive number.")
    if timeout <= 0:
        raise SettingsError("timeout must be a positive number.")

    if not isinstance(output_folder, str) or not output_folder.strip():
        raise SettingsError("output_folder must be a non-empty string.")

    if isinstance(seed, bool) or not isinstance(seed, int):
        raise SettingsError("seed must be an integer.")

    if isinstance(sample_size, bool) or not isinstance(sample_size, int):
        raise SettingsError("sample_size must be a positive integer.")
    if sample_size < 1:
        raise SettingsError("sample_size must be a positive integer.")

    valid_levels = {"DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"}
    if not isinstance(log_level, str) or log_level.upper() not in valid_levels:
        raise SettingsError("log_level must be a valid logging level.")

    logger.debug("Loaded configuration from %s", path)

    return AppConfig(
        source_url=source_url,
        timeout=float(timeout),
        output_folder=Path(output_folder),
        seed=seed,
        sample_size=sample_size,
        log_level=log_level.upper(),
    )
