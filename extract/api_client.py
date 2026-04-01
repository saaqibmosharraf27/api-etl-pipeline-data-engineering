"""REST API client — fetches raw records and yields them as dicts."""

import os
import logging
from typing import Generator

import requests
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)

BASE_URL = os.environ["API_BASE_URL"]
API_KEY = os.environ.get("API_KEY", "")


def _get_headers() -> dict:
    headers = {"Accept": "application/json"}
    if API_KEY:
        headers["Authorization"] = f"Bearer {API_KEY}"
    return headers


def fetch_records(endpoint: str, params: dict | None = None) -> Generator[dict, None, None]:
    """Paginate through `endpoint` and yield each record.

    Assumes the API returns JSON shaped as:
        {"data": [...], "next_page": <url | null>}
    Adjust `_parse_page` if your API differs.
    """
    url = f"{BASE_URL}/{endpoint.lstrip('/')}"
    session = requests.Session()
    session.headers.update(_get_headers())

    while url:
        response = session.get(url, params=params, timeout=30)
        response.raise_for_status()
        payload = response.json()

        records = _parse_page(payload)
        logger.info("Fetched %d records from %s", len(records), url)

        yield from records

        url = payload.get("next_page")
        params = None  # pagination token is embedded in next_page URL


def _parse_page(payload: dict) -> list[dict]:
    """Extract the records list from an API response payload."""
    if isinstance(payload, list):
        return payload
    return payload.get("data", payload.get("results", []))
