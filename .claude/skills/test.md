# /test — Run the full test suite

Runs pytest unit tests and dbt schema tests for the ETL project.

## What to do

1. Run pytest from the project root:
   ```bash
   cd /c/Users/saaqi/my_etl_project && python -m pytest tests/ -v
   ```
2. Then run dbt tests:
   ```bash
   cd /c/Users/saaqi/my_etl_project/transform && dbt test
   ```
3. Report a combined summary:
   - pytest: X passed, Y failed, Z errors
   - dbt tests: X passed, Y failed
4. For any failure, show the failing test name and the error. If it's a pytest test, show the relevant assert. If it's a dbt test, show the model and the constraint that failed.

## Arguments

`/test [pytest|dbt|<test-file>]`

- No argument → run both pytest and dbt tests
- `pytest` → pytest only
- `dbt` → dbt test only
- A file path like `tests/test_extract.py` → run that file only
