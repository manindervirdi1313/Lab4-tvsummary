# TVMaze Show Summary

## Overview

This Python project downloads TV show records from the TVMaze API and generates summary statistics. It demonstrates modular Python development, data validation, object-oriented programming, aggregation, automated testing, and package installation.

## Features

* Downloads TV show records from TVMaze.
* Validates and cleans show data.
* Counts shows by genre.
* Calculates average ratings by language.
* Counts shows by premiere decade.
* Lists unique genres.
* Saves the summary as formatted JSON.
* Handles download and data errors with clear messages.
* Includes network-free unit tests.

## Project Structure

```text
week03-lab03/
├── data/
│   ├── raw/
│   │   └── .gitkeep
│   └── processed/
│       └── summary.json
├── src/
│   └── tvsummary/
│       ├── __init__.py
│       ├── config.py
│       ├── models.py
│       ├── sources.py
│       ├── aggregations.py
│       └── report.py
├── tests/
│   └── test_aggregations.py
├── lab2.py
├── main.py
├── environment.yml
├── pyproject.toml
├── requirements.txt
├── .gitignore
└── README.md
```

## Requirements

* Python 3.11
* pip
* requests

## Setup

Create the Conda environment:

```powershell
conda env create -f environment.yml
```

Activate the environment:

```powershell
conda activate tvsummary
```

Install dependencies:

```powershell
python -m pip install -r requirements.txt
```

Install the package in editable mode:

```powershell
python -m pip install -e .
```

## Run the Application

From the project root, run:

```powershell
python main.py
```

The program retrieves TVMaze data and writes the report to `data/processed/summary.json`. Internet access is required to retrieve live data.

## Run Tests

Run the network-free unit tests with:

```powershell
python -m unittest discover -s tests -v
```

The tests verify genre counts, average ratings by language, premiere-decade counts, and unique genres without making API requests.

## What Moved Where

| Original responsibility                             | New module        |
| --------------------------------------------------- | ----------------- |
| API URL, timeout, output path                       | `config.py`       |
| Show data validation and cleaning                   | `models.py`       |
| API requests and response validation                | `sources.py`      |
| Genre, rating, decade and unique-genre calculations | `aggregations.py` |
| Summary assembly and JSON output                    | `report.py`       |
| Application entry point                             | `main.py`         |

## Design Choices

* **Separation of concerns:** Configuration, data access, models, calculations, and reporting are separated into modules.
* **Data validation:** The `Show` model normalizes genres, language, ratings, and premiere dates.
* **Polymorphism:** Aggregation subclasses implement their own `compute()` methods, called through a common interface.
* **Testability:** Aggregations are tested with sample data and do not require network access.
* **Centralized configuration:** The API URL, timeout, and output location are defined in one module.
* **Dependency management:** `pyproject.toml` defines package metadata and dependencies; `requirements.txt` pins the requests dependency.

## Lab 02 Comparison

The original Lab 02 script is preserved as `lab2.py`. The refactored package retains the same summary categories and JSON output structure while organizing the functionality into separate modules.
