# spark-project

A small PySpark project with automated testing through GitHub Actions.

## What it does

`clean_data(df)` in `pyspark_job.py` cleans a Spark DataFrame that has `name` and `amount` columns:

- removes rows where `amount <= 0`
- removes rows where `name` is NULL
- adds a column `amount_with_tax` = `amount * 1.20`

## Tests

`test_pyspark_job.py` has four pytest tests, one for each rule:

- valid records are kept
- records with `amount <= 0` are removed
- records with NULL names are removed
- `amount_with_tax` is calculated correctly

## CI

`.github/workflows/ci.yml` runs on every Pull Request (opened, updated or reopened). It sets up Java 17 and Python 3.11, installs `requirements.txt`, and runs `pytest -v`.

## Run locally

```
pip install -r requirements.txt
pytest -v
```

Requires Python 3.9 to 3.11 and Java 8, 11 or 17.

## Structure

```
spark-project/
├── .github/workflows/ci.yml
├── pyspark_job.py
├── test_pyspark_job.py
└── requirements.txt
```
