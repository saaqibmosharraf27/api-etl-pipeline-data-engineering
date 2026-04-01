# /pipeline — Run the complete ETL pipeline end-to-end

Runs extract → load → dbt transform in sequence, then reports overall status.

## What to do

Run each step in order. Stop and report clearly if any step fails — do not continue to the next step after a failure.

### Step 1 — Extract & Load
```bash
cd /c/Users/saaqi/my_etl_project
python -c "
import logging, os
logging.basicConfig(level=logging.INFO)
from extract.api_client import fetch_records
from load.loader import load_records
endpoint = os.environ.get('ETL_ENDPOINT', 'events')
rows = load_records(endpoint, fetch_records(endpoint))
print(f'EXTRACT: loaded {rows} rows into raw.{endpoint}')
"
```

### Step 2 — Transform
```bash
cd /c/Users/saaqi/my_etl_project/transform && dbt run
```

### Step 3 — Report
Print a pipeline summary:
```
Pipeline complete
  Extract : OK — N rows loaded into raw.events
  Transform: OK — N models, 0 errors
```

If any step fails, print:
```
Pipeline FAILED at <step>
  Error: <message>
```

## Arguments

`/pipeline [endpoint]` — optionally specify the API endpoint to extract from (default: `events`).
