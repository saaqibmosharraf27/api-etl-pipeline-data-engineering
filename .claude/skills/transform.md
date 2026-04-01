# /transform — Run dbt models

Runs dbt transformations inside the `transform/` directory.

## What to do

1. Change into the `transform/` directory.
2. Run the appropriate dbt command based on any argument the user passed:
   - No argument → `dbt run`
   - `staging` → `dbt run --select staging`
   - `marts` → `dbt run --select marts`
   - A specific model name → `dbt run --select <name>`
   - `test` → `dbt test`
   - `fresh` → `dbt run --full-refresh`
3. Show a concise summary: how many models passed/failed/skipped.
4. If any model failed, show the error from the dbt logs and suggest a fix (bad SQL, missing source table, type mismatch, etc.).

## Command

```bash
cd /c/Users/saaqi/my_etl_project/transform && dbt run
```

## Arguments

`/transform [staging|marts|<model-name>|test|fresh]`

Examples:
- `/transform` — run all models
- `/transform staging` — run only staging layer
- `/transform stg_events` — run one model
- `/transform test` — run dbt tests
- `/transform fresh` — full-refresh rebuild
