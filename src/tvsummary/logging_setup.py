"""Central logging configuration for tvsummary."""

import logging


def configure_logging(level: str = "INFO") -> None:
    """Configure application logging once."""
    numeric_level = getattr(logging, level.upper(), None)

    if not isinstance(numeric_level, int):
        raise ValueError(f"Invalid logging level: {level}")

    logging.basicConfig(
        level=numeric_level,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
        force=True,
    )
