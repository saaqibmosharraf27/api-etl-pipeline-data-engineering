# ETL Project — Claude Instructions

## Project Overview
Python ETL pipeline that ingests data from a REST API, stores raw JSON in DuckDB, transforms it with dbt, and exposes clean mart tables.

## Architecture
```
REST API → extract/api_client.py → load/loader.py → DuckDB (raw) → dbt → DuckDB (marts)
```

## Stack
- **Python 3.11+** — extraction and loading
- **DuckDB** — local analytical database (file: `data/warehouse.duckdb`)
- **dbt-duckdb** — SQL transformations
- **requests** — HTTP client
- **pytest** — testing

## Key Conventions
- Raw tables are prefixed `raw_` and live in the `raw` schema
- Staging models (`stg_*`) clean and cast raw data, one-to-one with sources
- Mart models (`mart_*`) are business-level, joined/aggregated views
- Never mutate raw tables after load — treat them as append-only

## Running the Pipeline
```bash
# 1. Extract + Load raw data
python -m extract.api_client | python -m load.loader

# 2. Transform with dbt
cd transform && dbt run

# 3. Run tests
pytest tests/
cd transform && dbt test
```

## Environment Variables
| Variable | Description |
|---|---|
| `API_BASE_URL` | Base URL of the source REST API |
| `API_KEY` | Auth token for the API |
| `DUCKDB_PATH` | Path to DuckDB file (default: `data/warehouse.duckdb`) |
