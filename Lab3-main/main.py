"""Entry point for the TV show summary application."""

from tvsummary.config import OUTPUT_FILE
from tvsummary.report import build_summary, write_summary
from tvsummary.sources import TVMazeSource


def main():
    """Run the TVMaze aggregation workflow."""
    try:
        shows = TVMazeSource().fetch()
        summary = build_summary(shows)
        write_summary(summary)

        print(f"Processed {summary['records_processed']} TV shows.")
        print(f"Summary written to {OUTPUT_FILE.resolve()}")

    except (RuntimeError, OSError, ValueError) as error:
        print(f"Error: {error}")


if __name__ == "__main__":
    main()
