# TVMaze Show Summary — Lab 04

## Overview

This project is a Python package that retrieves TV show records from the TVMaze API, validates and cleans the records, calculates summary statistics, and writes JSON reports.

Lab 04 focuses on package hardening, configuration validation, error handling, logging, reproducible sampling, automated tests, type checking, and code quality.

## Features

- Loads application settings from `config/tvsummary.toml`.
- Retrieves TV show records from the configured TVMaze endpoint.
- Validates API responses and normalizes show data.
- Calculates show counts by genre and premiere decade.
- Calculates average ratings by language.
- Lists unique genres.
- Selects featured shows reproducibly using a configured random seed.
- Writes `summary.json` and `run_info.json` to the configured output folder.
- Uses custom exceptions and clear command-line error messages.
- Includes offline automated tests, static type checking, and Ruff linting.

## Project Structure

```text
.
├── config/
│   └── tvsummary.toml
├── data/
│   ├── raw/
│   │   └── .gitkeep
│   └── processed/
│       ├── summary.json
│       └── run_info.json
├── src/
│   └── tvsummary/
│       ├── __init__.py
│       ├── py.typed
│       ├── aggregations.py
│       ├── config.py
│       ├── errors.py
│       ├── featured.py
│       ├── logging_setup.py
│       ├── main.py
│       ├── models.py
│       ├── report.py
│       └── sources.py
├── tests/
│   ├── conftest.py
│   ├── test_aggregations.py
│   ├── test_config.py
│   ├── test_featured.py
│   ├── test_main.py
│   ├── test_models.py
│   └── test_sources.py
├── .gitignore
├── environment.yml
├── pyproject.toml
├── requirements.txt
└── README.md
```

## Setup

### Requirements

- Python 3.11
- Conda, or another Python environment manager
- Internet access to retrieve live TVMaze data

### Create the environment

For a new environment, run:

```powershell
conda env create -f environment.yml
conda activate tvsummary
```

If the `tvsummary` environment already exists, activate it and install the pinned dependencies:

```powershell
conda activate tvsummary
python -m pip install -r requirements.txt
```

Install the package in editable mode:

```powershell
python -m pip install -e .
```

## Check it

Run the offline tests:

```powershell
python -m pytest -v
```

Check static types:

```powershell
python -m mypy src tests
```

Check lint rules:

```powershell
python -m ruff check .
```

Verify formatting:

```powershell
python -m ruff format --check .
```

All four checks should pass before submission.

## Run the application

From the project root:

```powershell
python -m tvsummary.main
```

To specify a different configuration file:

```powershell
python -m tvsummary.main --config config/tvsummary.toml
```

The application uses the configured API URL and timeout, builds the summary, selects featured shows using the configured seed, and writes the output files to the configured output folder.

Expected output files:

- `data/processed/summary.json` — summary statistics and featured shows.
- `data/processed/run_info.json` — configuration settings, Python version, and available pytest, mypy, and Ruff versions.

Running the application requires network access. The automated tests should not depend on a live API.

## Settings

Edit `config/tvsummary.toml` to change the application settings:

```toml
[app]
source_url = "https://api.tvmaze.com/shows?page=0"
timeout = 15
output_folder = "data/processed"
seed = 42
sample_size = 5
log_level = "INFO"
```

| Setting | Purpose |
| --- | --- |
| `source_url` | HTTPS endpoint used to retrieve show records |
| `timeout` | Maximum request wait time, in seconds |
| `output_folder` | Directory for generated JSON reports |
| `seed` | Random seed for reproducible featured-show selection |
| `sample_size` | Number of featured shows to select |
| `log_level` | Logging level, such as `INFO` or `DEBUG` |

Configuration is validated when the application starts. Missing or invalid settings should produce a clear error rather than an unhandled traceback.

## Errors and exit codes

| Exit code | Meaning |
| --- | --- |
| `0` | Application completed successfully |
| `1` | An expected configuration, data-source, validation, or report-writing error occurred |

Expected application errors are reported with an `Error:` message on standard error. Logs provide additional diagnostic information.

## Reproducing a run

To reproduce the featured-show selection:

1. Keep the same input records.
2. Keep the same `seed` and `sample_size` values in `config/tvsummary.toml`.
3. Run the application again.
4. Compare the featured-show selection in `summary.json`.

The random seed makes sampling reproducible for the same input records and sampling parameters. Live API data can change, so the entire summary may differ between runs.

The `run_info.json` file records settings and environment information to help document each run.

## What tests cover

The test suite covers:

- Cleaning and validation of show records.
- Aggregation calculations for genres, ratings, decades, and unique genres.
- Configuration loading and missing configuration errors.
- Data-source success, request failures, invalid JSON, and malformed API responses.
- Reproducible featured-show selection.
- Command-line success and expected error handling.

Tests should use fixtures, temporary paths, and mocks where appropriate so they can run without relying on the live TVMaze API.

## Known limitations

- Live data retrieval requires internet access and depends on TVMaze availability.
- The default endpoint retrieves one configured page of records; it does not necessarily represent every TVMaze show.
- Summary statistics reflect the records returned by the endpoint.
- Reproducibility of the full report depends on receiving the same input records and using the same settings.
- `run_info.json` records environment information but is not a complete lockfile for every transitive dependency.

## Design choices

- **Separation of concerns:** Configuration, data access, models, aggregation, reporting, and command-line behavior live in separate modules.
- **Error handling:** Expected failures use package-specific exceptions.
- **Logging:** Application diagnostics use centralized logging.
- **Reproducibility:** Featured-show selection uses a dedicated seeded random generator.
- **Testability:** Automated tests validate behavior without requiring live API calls.
- **Code quality:** Ruff and mypy help maintain consistent formatting, linting, and type annotations.
