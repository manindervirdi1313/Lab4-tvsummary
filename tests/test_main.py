
"""Tests for the command-line entry point."""

from tvsummary.main import main


def test_main_accepts_valid_config() -> None:
    """Valid settings should return success."""
    assert main(["--config", "config/tvsummary.toml"]) == 0


def test_main_handles_missing_config(capsys) -> None:
    """Missing settings should return an error without a traceback."""
    result = main(["--config", "config/does-not-exist.toml"])

    captured = capsys.readouterr()

    assert result == 1
    assert captured.err.startswith("Error:")
    assert "Traceback" not in captured.err
