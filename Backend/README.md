# Backend Notes

The main project documentation lives in the repository root `README.md`. This file is a short backend-specific reference for the Python scraping and API code.

## Entry Points

- `app.py`: Flask API used by the React frontend.
- `main.py`: Older experimentation/CLI entry point. Much of the original interactive flow is currently commented out.
- `getTeamsScript.py`: Scrapes Basketball Reference team pages and writes cached CSV files under `teams/`.

## Core Modules

- `Player.py`: Builds Basketball Reference player URLs from first and last names and wires together the scraper/analysis classes.
- `PlayerOverview.py`: Scrapes career/stat tables from a player's main Basketball Reference profile page.
- `PlayerIndividual.py`: Scrapes season game logs and writes per-game CSV data.
- `dataFrameManipulation.py`: Converts parsed HTML tables into pandas DataFrames and writes CSV output.
- `CalculateStats.py`: Experimental analysis code for scoring variance and opponent defensive rating comparisons.

## Runtime Notes

- Run backend commands from this `Backend` directory. Several paths are relative, including `players/` and `teams/`.
- There is no committed backend dependency file yet. See the root `README.md` for the dependency list inferred from imports.
- Cached HTML and CSV files are stored locally to reduce repeated Basketball Reference requests.
