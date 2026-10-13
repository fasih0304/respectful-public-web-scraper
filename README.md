# Respectful Public Web Scraper

A beginner-friendly Python project that extracts the title, readable text, and links from one public web page.

## Features
- Fetches one HTTP/HTTPS page
- Checks `robots.txt` before fetching
- Uses a descriptive User-Agent and request timeout
- Extracts title, visible text, and links
- Saves output as JSON
- Includes unit tests

## Ethical use
Use only on pages you are allowed to access. Respect site terms and `robots.txt`. This tool does not bypass logins, CAPTCHAs, anti-bot protections, or rate limits.

## Setup
Python 3.10+ is recommended.

```bash
python -m venv .venv
```

Activate it, then install dependencies:

```bash
pip install -r requirements.txt
```

## Run

```bash
python scraper.py https://example.com --output result.json
```

If the site's `robots.txt` cannot be verified or disallows scraping, the tool stops.

## Tests

```bash
python -m unittest discover -s tests -v
```

## Structure
- `scraper.py` — scraper and CLI
- `requirements.txt` — dependencies
- `tests/test_parser.py` — parser tests
- `LICENSE` — MIT license

## Before publishing
Add your GitHub username and contact details here. Test the project locally and make sure you understand the code before submitting it to a community moderator.
