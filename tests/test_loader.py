"""Unit tests for load/loader.py using an in-memory DuckDB."""

import pytest
import duckdb

from load.loader import load_records, _ensure_raw_table


@pytest.fixture
def conn():
    c = duckdb.connect(":memory:")
    c.execute("CREATE SCHEMA IF NOT EXISTS raw")
    return c


def test_ensure_raw_table_creates_table(conn):
    _ensure_raw_table(conn, "test_table")
    tables = conn.execute(
        "SELECT table_name FROM information_schema.tables WHERE table_schema = 'raw'"
    ).fetchall()
    assert ("test_table",) in tables


def test_load_records_inserts_rows(monkeypatch, tmp_path):
    monkeypatch.setenv("DUCKDB_PATH", str(tmp_path / "test.duckdb"))

    count = load_records("events", [{"id": 1, "name": "foo"}, {"id": 2, "name": "bar"}])
    assert count == 2


def test_load_records_empty(monkeypatch, tmp_path):
    monkeypatch.setenv("DUCKDB_PATH", str(tmp_path / "test.duckdb"))

    count = load_records("events", [])
    assert count == 0
