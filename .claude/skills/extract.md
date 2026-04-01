# /extract — Run API extraction and load raw data

Runs the full extract → load pipeline for this ETL project.

## What to do

1. Check that `.env` exists (copy from `.env.example` if not). If `API_BASE_URL` is unset, ask the user for it before proceeding.
2. Run the extract + load step from the project root:
   ```bash
   cd /c/Users/saaqi/my_etl_project
   python -c "
   import logging, os
   logging.basicConfig(level=logging.INFO)
   from extract.api_client import fetch_records
   from load.loader import load_records
   endpoint = os.environ.get('ETL_ENDPOINT', 'events')
   rows = load_records(endpoint, fetch_records(endpoint))
   print(f'Loaded {rows} rows into raw.{endpoint}')
   "
   ```
3. Report how many rows were loaded and into which table.
4. If the run fails, show the traceback and suggest the likely fix (missing env var, bad endpoint, network error, etc.).

## Arguments

The user can pass an endpoint name as an argument, e.g. `/extract orders`.  
Default endpoint is `events` if none is given.
