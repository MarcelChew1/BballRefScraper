# BBallRefScraper

## Overview

BBallRefScraper is a personal project for collecting and viewing NBA player statistics from [Basketball Reference](https://www.basketball-reference.com/). It combines a Python scraping layer with a small Flask API and a React frontend that lets a user enter a player name, request available career stat tables, and view the results in a browser.

This was an earlier personal project and has been documented retroactively to make the intent, architecture, and implementation easier to understand.

## Motivation / Purpose

The project was built to explore how public basketball statistics could be scraped, cached, transformed, and served through a simple web interface. The backend focuses on translating player names into Basketball Reference URLs, extracting tables from player profile and game log pages, and normalizing the results into CSV-backed pandas DataFrames.

It also includes experimental analysis code for questions such as player scoring variance, hot/cold streaks, and relationships between player scoring and opponent defensive rating. Those analysis ideas are present in the codebase, but the main user-facing workflow is the player table lookup UI.

## Features

- Looks up Basketball Reference player profile URLs from first and last name input.
- Scrapes career-level player tables such as per-game, totals, advanced, shooting, play-by-play, career highs, and playoff series data.
- Handles tables that Basketball Reference places inside HTML comments by parsing the commented markup.
- Caches scraped player pages, game logs, team pages, and generated CSV files locally under `Backend/players` and `Backend/teams`.
- Exposes Flask endpoints for creating a player lookup and fetching selected stat tables.
- Provides a React interface for entering a player name and viewing selected stat tables.
- Includes exploratory scripts/classes for team defensive rating data and player scoring analysis.

## Tech Stack

**Backend**

- Python
- Flask and Flask-CORS
- Requests
- Beautiful Soup
- pandas
- NumPy
- SciPy
- Matplotlib
- XlsxWriter support in the older CLI export flow

**Frontend**

- React 18
- Create React App / `react-scripts`
- React Router
- Material UI

**Data storage**

- Local HTML and CSV files generated from scraped Basketball Reference pages.
- No database is used.

## Architecture / How It Works

The project is split into a Python backend and a React frontend.

1. The React home page posts a first and last name to `POST /create_player`.
2. The Flask API creates a `Player` object.
3. `Player` derives the Basketball Reference URL pattern for that name and checks candidate profile URLs until it finds a matching player page.
4. `PlayerOverview` loads the player profile page from the local cache if available; otherwise it fetches the page, saves it, and parses the stat tables.
5. `PlayerIndividual` can fetch season game logs and generate a per-game CSV cache.
6. When the frontend requests `GET /player?name=<player>&type=<table>`, the backend maps the requested table name to a `PlayerOverview` method, returns JSON records, and preserves the DataFrame column order for display.
7. The React player page renders buttons for supported table types and displays the selected table.

Key backend components:

- `Backend/app.py`: Flask API entry point.
- `Backend/Player.py`: Player name normalization, Basketball Reference URL discovery, and object composition.
- `Backend/PlayerOverview.py`: Career/stat table scraping, comment-table handling, and CSV cache generation.
- `Backend/PlayerIndividual.py`: Game log scraping across seasons.
- `Backend/dataFrameManipulation.py`: Beautiful Soup table extraction and DataFrame cleanup helpers.
- `Backend/CalculateStats.py`: Experimental analysis code for scoring variance and opponent defensive rating.
- `Backend/getTeamsScript.py`: Script for scraping team-level Basketball Reference data.

## Getting Started

### Prerequisites

- Python 3.10+ recommended
- Node.js and npm
- Internet access when scraping data that is not already cached locally

### Backend Setup

There is no committed `requirements.txt`, so install the backend dependencies manually:

```bash
cd Backend
python -m venv .venv
.venv\Scripts\activate
python -m pip install flask flask-cors requests beautifulsoup4 pandas "numpy<2" scipy matplotlib XlsxWriter
python app.py
```

The Flask development server runs on `http://localhost:5000` by default.

### Frontend Setup

```bash
cd Frontend/my-new-app
npm install
npm start
```

The React development server runs on `http://localhost:3000` by default and calls the Flask API at `http://localhost:5000`.

## Usage

1. Start the backend from `Backend/app.py`.
2. Start the frontend from `Frontend/my-new-app`.
3. Open `http://localhost:3000`.
4. Enter a player's first and last name.
5. Select one of the available stat table buttons on the player page.

Supported table options in the current UI are:

- Per game
- Total
- Per minute
- Per possession
- Advanced
- Adjusted Shooting
- Play by play
- Shooting
- Career highs
- Playoffs

The backend writes generated files relative to the `Backend` working directory. For the existing paths to resolve correctly, run backend commands from inside `Backend`.

## Testing

The repository does not currently include backend tests.

The frontend contains the default Create React App test file at `Frontend/my-new-app/src/App.test.js`, but it still checks for the original scaffold text (`learn react`) and does not match the current app. As a result, `npm test` is expected to fail until that test is updated or replaced.

Suggested manual smoke test:

```bash
cd Backend
python app.py
```

In a second terminal:

```bash
cd Frontend/my-new-app
npm start
```

Then search for a known cached player such as `LeBron James`, `Stephen Curry`, `James Harden`, or `Paul George` and request one of the stat tables.

## Project Structure

```text
.
|-- Backend/
|   |-- app.py                    # Flask API
|   |-- main.py                   # Older CLI / experimentation entry point
|   |-- Player.py                 # Player URL lookup and composition
|   |-- PlayerOverview.py         # Career table scraping and caching
|   |-- PlayerIndividual.py       # Game log scraping
|   |-- CalculateStats.py         # Experimental analysis utilities
|   |-- dataFrameManipulation.py  # HTML table to DataFrame helpers
|   |-- getTeamsScript.py         # Team data scraping script
|   |-- players/                  # Cached player HTML and CSV data
|   `-- teams/                    # Cached team HTML and CSV data
|-- Frontend/
|   `-- my-new-app/
|       |-- package.json          # React app dependencies and scripts
|       |-- public/
|       `-- src/
|           |-- pages/            # Home and player pages
|           `-- components/       # Reusable table/button components
`-- README.md
```

## Configuration

No environment variables are currently required.

The API base URL is hardcoded in the frontend as `http://localhost:5000`. If the backend runs on a different host or port, update the fetch calls in:

- `Frontend/my-new-app/src/pages/Home.jsx`
- `Frontend/my-new-app/src/pages/PlayerPage.jsx`

## Challenges / Learnings

- Basketball Reference page structure is not always straightforward for scrapers. Some tables are embedded inside HTML comments, so the scraper needs to detect and parse commented markup.
- Player URL discovery requires matching Basketball Reference's naming convention and checking duplicate-name suffixes such as `01`, `02`, and so on.
- Historical team abbreviations need normalization. For example, the code maps legacy or alternate abbreviations such as `BRK` and `NJN` to `BKN`.
- Local caching reduces repeated requests and makes development faster, but it also means cached data can become stale.
- The frontend/backend split made the data flow easier to demonstrate, but the API state is in memory and is not designed for production deployment.

## Known Limitations

- The project depends on Basketball Reference's current HTML structure and may break if the site changes.
- There is no automated backend test coverage.
- The frontend test is still the default scaffold test and should be replaced.
- The backend stores created `Player` objects in an in-memory dictionary, so API state is lost when the Flask server restarts.
- Error handling is limited. For example, a missing player can return an empty response from `POST /create_player`.
- `node_modules`, Python `__pycache__`, and generated `.pyc` files appear to be committed in the repository and should usually be removed from version control.
- Scraped HTML/CSV files are committed as sample/cache data; that may be useful for demonstration, but it also increases repository size and can make data freshness unclear.
- The frontend is still named `my-new-app`, which reflects the original Create React App scaffold rather than the project domain.

## Assumptions / Notes

- Backend setup instructions are based on imports used by the code because the repository does not include a backend dependency file.
- Commands assume a Windows shell because the existing project paths and environment appear to be Windows-based.
- Scraping should be done respectfully and at low volume. Check Basketball Reference's current terms of use and robots guidance before running large scraping jobs.

## Future Improvements

- Add a backend `requirements.txt` or `pyproject.toml`.
- Replace the scaffold frontend test with tests for the actual home page, player lookup flow, and table rendering.
- Add backend unit tests around URL construction, table parsing, CSV caching, and error handling.
- Move the frontend API URL into environment-based configuration.
- Improve API responses for invalid players, missing tables, and Basketball Reference request failures.
- Rename `Frontend/my-new-app` to a project-specific name.
- Remove generated dependency/cache artifacts from version control and add a root `.gitignore`.
- Separate sample data from generated cache files so reviewers can tell what is source code versus local output.
- Consider a small command-line interface for scraping/exporting data independently from the web UI.
