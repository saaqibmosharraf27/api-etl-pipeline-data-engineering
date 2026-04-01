"""Loads raw records into DuckDB as append-only raw tables."""

import os
import json
import logging
from datetime import datetime, timezone
from typing import Iterable

import duckdb
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)

DUCKDB_PATH = os.environ.get("DUCKDB_PATH", "data/warehouse.duckdb")


def get_connection() -> duckdb.DuckDBPyConnection:
    os.makedirs(os.path.dirname(DUCKDB_PATH) or ".", exist_ok=True)
    conn = duckdb.connect(DUCKDB_PATH)
    conn.execute("CREATE SCHEMA IF NOT EXISTS raw")
    return conn


def load_records(table_name: str, records: Iterable[dict]) -> int:
    """Insert `records` into `raw.<table_name>`, creating the table if needed.

    Each row stores the full JSON payload plus an ingestion timestamp.
    Returns the number of rows inserted.
    """
    conn = get_connection()
    _ensure_raw_table(conn, table_name)

    ingested_at = datetime.now(timezone.utc).isoformat()
    rows = [
        (json.dumps(record), ingested_at)
        for record in records
    ]

    if not rows:
        logger.warning("No records to load into raw.%s", table_name)
        return 0

    conn.executemany(
        f"INSERT INTO raw.{table_name} (payload, ingested_at) VALUES (?, ?)",
        rows,
    )
    conn.commit()
    logger.info("Loaded %d rows into raw.%s", len(rows), table_name)
    return len(rows)


def _ensure_raw_table(conn: duckdb.DuckDBPyConnection, table_name: str) -> None:
    conn.execute(f"""
        CREATE TABLE IF NOT EXISTS raw.{table_name} (
            id          INTEGER PRIMARY KEY,
            payload     JSON      NOT NULL,
            ingested_at TIMESTAMP NOT NULL
        )
    """)
