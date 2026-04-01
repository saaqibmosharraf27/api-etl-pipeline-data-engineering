"""Unit tests for extract/api_client.py."""

import pytest
import responses
import requests

from extract.api_client import fetch_records, _parse_page


# --- _parse_page ---

def test_parse_page_list():
    assert _parse_page([{"id": 1}]) == [{"id": 1}]


def test_parse_page_data_key():
    assert _parse_page({"data": [{"id": 2}]}) == [{"id": 2}]


def test_parse_page_results_key():
    assert _parse_page({"results": [{"id": 3}]}) == [{"id": 3}]


def test_parse_page_empty():
    assert _parse_page({}) == []


# --- fetch_records (mocked HTTP) ---

@responses.activate
def test_fetch_records_single_page(monkeypatch):
    monkeypatch.setenv("API_BASE_URL", "https://api.example.com")
    monkeypatch.setenv("API_KEY", "test-key")

    responses.add(
        responses.GET,
        "https://api.example.com/events",
        json={"data": [{"id": 1, "name": "foo"}, {"id": 2, "name": "bar"}], "next_page": None},
        status=200,
    )

    records = list(fetch_records("events"))
    assert len(records) == 2
    assert records[0]["name"] == "foo"


@responses.activate
def test_fetch_records_pagination(monkeypatch):
    monkeypatch.setenv("API_BASE_URL", "https://api.example.com")
    monkeypatch.setenv("API_KEY", "test-key")

    responses.add(
        responses.GET,
        "https://api.example.com/events",
        json={"data": [{"id": 1}], "next_page": "https://api.example.com/events?page=2"},
        status=200,
    )
    responses.add(
        responses.GET,
        "https://api.example.com/events",
        json={"data": [{"id": 2}], "next_page": None},
        status=200,
    )

    records = list(fetch_records("events"))
    assert len(records) == 2


@responses.activate
def test_fetch_records_http_error(monkeypatch):
    monkeypatch.setenv("API_BASE_URL", "https://api.example.com")

    responses.add(
        responses.GET,
        "https://api.example.com/events",
        status=401,
    )

    with pytest.raises(requests.HTTPError):
        list(fetch_records("events"))
