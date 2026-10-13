"""Respectful single-page scraper for public web pages."""
import argparse
import json
import sys
from urllib.parse import urlparse, urljoin
from urllib.robotparser import RobotFileParser

import requests
from bs4 import BeautifulSoup

USER_AGENT = "RespectfulPublicWebScraper/1.0 (open-source learning project)"


def validate_url(url):
    parsed = urlparse(url)
    if parsed.scheme not in {"http", "https"} or not parsed.netloc:
        raise ValueError("Please provide a full http:// or https:// URL.")
    return url


def robots_allows(url, timeout=10):
    parsed = urlparse(url)
    robots_url = f"{parsed.scheme}://{parsed.netloc}/robots.txt"
    response = requests.get(
        robots_url, headers={"User-Agent": USER_AGENT}, timeout=timeout
    )
    if response.status_code >= 400:
        return False
    parser = RobotFileParser()
    parser.set_url(robots_url)
    parser.parse(response.text.splitlines())
    return parser.can_fetch(USER_AGENT, url)


def parse_html(html, page_url):
    soup = BeautifulSoup(html, "html.parser")
    for element in soup(["script", "style", "noscript", "template"]):
        element.decompose()

    title = soup.title.get_text(" ", strip=True) if soup.title else ""
    text = " ".join(soup.get_text(" ", strip=True).split())

    links, seen = [], set()
    for anchor in soup.find_all("a", href=True):
        href = anchor["href"].strip()
        if not href or href.startswith(("javascript:", "mailto:", "tel:")):
            continue
        absolute = urljoin(page_url, href)
        if absolute not in seen:
            seen.add(absolute)
            links.append({"text": anchor.get_text(" ", strip=True), "url": absolute})

    return {"url": page_url, "title": title, "text": text, "links": links}


def scrape(url, timeout=10):
    url = validate_url(url)
    if not robots_allows(url, timeout):
        raise PermissionError(
            "robots.txt could not be verified or does not allow this request. "
            "Choose a page whose robots.txt permits scraping."
        )

    response = requests.get(
        url,
        headers={"User-Agent": USER_AGENT, "Accept": "text/html,application/xhtml+xml"},
        timeout=timeout,
    )
    response.raise_for_status()
    content_type = response.headers.get("Content-Type", "")
    if "html" not in content_type.lower():
        raise ValueError(f"Expected HTML, received Content-Type: {content_type}")
    return parse_html(response.text, response.url)


def main():
    parser = argparse.ArgumentParser(
        description="Extract title, text, and links from one permitted public page."
    )
    parser.add_argument("url", help="Full public HTTP(S) URL")
    parser.add_argument("--output", default="result.json", help="Output JSON filename")
    parser.add_argument("--timeout", type=int, default=10, help="Timeout in seconds")
    args = parser.parse_args()

    try:
        result = scrape(args.url, args.timeout)
        with open(args.output, "w", encoding="utf-8") as output:
            json.dump(result, output, ensure_ascii=False, indent=2)
        print(f"Saved results to {args.output}")
        print(f"Title: {result['title'] or '(no title found)'}")
        print(f"Extracted {len(result['links'])} links.")
        return 0
    except (requests.RequestException, ValueError, PermissionError) as error:
        print(f"Error: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
