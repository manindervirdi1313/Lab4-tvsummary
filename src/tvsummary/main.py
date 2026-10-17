
"""Command-line entry point for tvsummary."""

import argparse
import logging
import sys
from collections.abc import Sequence

from tvsummary.config import load_config
from tvsummary.errors import TVSummaryError
from tvsummary.logging_setup import configure_logging

logger = logging.getLogger(__name__)


def main(argv: Sequence[str] | None = None) -> int:
    """Load settings and run the application."""
    parser = argparse.ArgumentParser(
        description="Generate a TV show summary."
    )
    parser.add_argument(
        "--config",
        default="config/tvsummary.toml",
        help="Path to the TOML configuration file.",
    )
    args = parser.parse_args(argv)

    try:
        config = load_config(args.config)
        configure_logging(config.log_level)
        logger.info("Configuration loaded successfully.")
        return 0
    except TVSummaryError as error:
        logger.error("%s", error)
        print(f"Error: {error}", file=sys.stderr)
        return 1
    except ValueError as error:
        logger.error("%s", error)
        print(f"Error: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
