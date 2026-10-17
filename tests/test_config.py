
"""Tests for configuration loading."""

import pytest

from tvsummary.config import load_config
from tvsummary.errors import SettingsError


def test_load_config_reads_settings() -> None:
    """Load the supplied configuration."""
    config = load_config("config/tvsummary.toml")

    assert config.seed == 42
    assert config.sample_size == 5
    assert config.log_level == "INFO"


def test_missing_config_raises_settings_error(tmp_path) -> None:
    """Reject a missing configuration file."""
    missing_file = tmp_path / "missing.toml"

    with pytest.raises(SettingsError, match="Configuration file not found"):
        load_config(missing_file)
