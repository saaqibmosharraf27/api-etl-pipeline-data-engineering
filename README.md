# api-etl-pipeline — Data Engineering

A production-ready Python ETL pipeline that extracts data from REST APIs, stores raw JSON in DuckDB, and transforms it into clean analytical mart tables using dbt.

```
REST API → extract/ → load/ → DuckDB (raw) → dbt → DuckDB (marts)
```

---

## Stack

| Layer | Technology |
|---|---|
| Extraction | Python 3.11+, `requests` |
| Storage | DuckDB (local analytical database) |
| Transformation | dbt-duckdb |
| Orchestration | Prefect (optional) |
| Testing | pytest, `responses` (HTTP mocking) |
| Config | python-dotenv |

---

## Project Structure

```
api-etl-pipeline-data-engineering/
├── extract/
│   └── api_client.py        # REST API client with pagination & auth
├── load/
│   └── loader.py            # DuckDB raw loader (append-only)
├── transform/
│   ├── dbt_project.yml      # dbt project config
│   ├── profiles.yml         # DuckDB connection profile
│   └── models/
│       ├── staging/
│       │   ├── sources.yml          # Raw source definitions
│       │   ├── stg_events.sql       # Parse + cast raw JSON
│       │   └── stg_events.yml       # Column tests
│       └── marts/
│           ├── mart_events_daily.sql  # Daily aggregation
│           └── mart_events_daily.yml  # Column tests
├── tests/
│   ├── test_extract.py      # Unit tests for API client
│   └── test_loader.py       # Unit tests for loader
├── .env.example             # Environment variable template
└── requirements.txt         # Python dependencies
```

---

## Quickstart

### 1. Clone and install dependencies

```bash
git clone https://github.com/saaqibmosharraf27/api-etl-pipeline-data-engineering.git
cd api-etl-pipeline-data-engineering
pip install -r requirements.txt
```

### 2. Configure environment variables

```bash
cp .env.example .env
```

Edit `.env` with your values:

```env
API_BASE_URL=https://api.example.com
API_KEY=your-api-key-here
DUCKDB_PATH=data/warehouse.duckdb
```

### 3. Run the full pipeline

```bash
# Step 1 — Extract from API and load into DuckDB raw schema
python -m extract.api_client | python -m load.loader

# Step 2 — Transform raw data with dbt
cd transform && dbt run

# Step 3 — Run all tests
pytest tests/
cd transform && dbt test
```

---

## How It Works

### Extract — `extract/api_client.py`

Fetches records from a paginated REST API and yields them as Python dicts.

- Follows `next_page` URLs automatically until all pages are consumed
- Supports Bearer token authentication via `API_KEY`
- Flexible response parsing — handles `{"data": [...]}`, `{"results": [...]}`, or raw list responses
- Uses `requests.Session` for connection pooling and a 30-second timeout per request

```python
from extract.api_client import fetch_records

for record in fetch_records("events"):
    print(record)
```

### Load — `load/loader.py`

Inserts extracted records into DuckDB's `raw` schema as append-only tables.

- Auto-creates the `raw.<table_name>` table if it doesn't exist
- Stores the full JSON payload alongside a UTC ingestion timestamp
- Safe to re-run — never mutates existing rows

```python
from load.loader import load_records

count = load_records("events", records)
print(f"Loaded {count} rows")
```

**Raw table schema:**

```sql
CREATE TABLE raw.events (
    id          INTEGER PRIMARY KEY,
    payload     JSON      NOT NULL,
    ingested_at TIMESTAMP NOT NULL
)
```

### Transform — `transform/models/`

Two-layer dbt transformation built on DuckDB:

#### Staging — `stg_events` (view)

Parses raw JSON fields into strongly-typed columns. One row in = one row out.

| Column | Type | Source |
|---|---|---|
| `event_id` | VARCHAR | `payload->>'$.id'` |
| `event_name` | VARCHAR | `payload->>'$.name'` |
| `created_at` | TIMESTAMP | `payload->>'$.created_at'` |
| `amount` | DOUBLE | `payload->>'$.amount'` |
| `status` | VARCHAR | `payload->>'$.status'` |

#### Mart — `mart_events_daily` (table)

Daily aggregation of events for dashboards and reporting.

| Column | Description |
|---|---|
| `event_date` | Date of the events |
| `status` | Event status group |
| `event_count` | Number of events that day |
| `total_amount` | Sum of amounts (2 dp) |
| `avg_amount` | Average amount (2 dp) |

**dbt lineage:**

```
raw.events → stg_events → mart_events_daily
```

### Tests — `tests/`

| Test file | Covers |
|---|---|
| `test_extract.py` | Single-page fetch, pagination, HTTP error handling, response parsing |
| `test_loader.py` | Table creation, row insertion, empty-record handling |

Run all tests:

```bash
pytest tests/ -v
```

---

## Environment Variables

| Variable | Required | Default | Description |
|---|---|---|---|
| `API_BASE_URL` | Yes | — | Base URL of the source REST API |
| `API_KEY` | No | `""` | Bearer token for API authentication |
| `DUCKDB_PATH` | No | `data/warehouse.duckdb` | Path to the DuckDB database file |

---

## Design Principles

- **Append-only raw layer** — raw tables are insert-only; re-runs add new data without overwriting history
- **Generator-based extraction** — records are yielded lazily to keep memory usage flat regardless of dataset size
- **Environment-driven config** — no secrets or paths hardcoded anywhere in the codebase
- **Two-layer dbt modeling** — staging cleans once, marts aggregate for business use
- **Data quality enforced by dbt** — `not_null`, `unique`, and `accepted_values` tests on every key column

---

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature`
3. Run the test suite: `pytest tests/`
4. Commit your changes and open a pull request

---

## License

MIT
