import os
import sys

import pytest
from pyspark.sql import SparkSession
from pyspark.sql.types import DoubleType, StringType, StructField, StructType

from pyspark_job import clean_data

# Make Spark use the same Python as pytest (avoids "python3 not found" on Windows)
os.environ["PYSPARK_PYTHON"] = sys.executable
os.environ["PYSPARK_DRIVER_PYTHON"] = sys.executable

SCHEMA = StructType([
    StructField("name", StringType(), True),
    StructField("amount", DoubleType(), True),
])


@pytest.fixture(scope="module")
def spark():
    session = (
        SparkSession.builder.master("local[1]")
        .appName("clean-data-tests")
        .config("spark.sql.shuffle.partitions", "1")
        .getOrCreate()
    )
    yield session
    session.stop()


def test_valid_records_are_kept(spark):
    df = spark.createDataFrame([("Alice", 100.0), ("Bob", 50.0)], SCHEMA)
    result = clean_data(df)
    assert result.count() == 2


def test_amount_less_or_equal_zero_removed(spark):
    df = spark.createDataFrame(
        [("Alice", 100.0), ("Bob", 0.0), ("Carol", -5.0)], SCHEMA
    )
    result = clean_data(df).collect()
    assert [r["name"] for r in result] == ["Alice"]


def test_null_names_removed(spark):
    df = spark.createDataFrame([("Alice", 100.0), (None, 80.0)], SCHEMA)
    result = clean_data(df).collect()
    assert len(result) == 1
    assert result[0]["name"] == "Alice"


def test_amount_with_tax_calculated_correctly(spark):
    df = spark.createDataFrame([("Alice", 100.0), ("Bob", 50.0)], SCHEMA)
    result = {r["name"]: r["amount_with_tax"] for r in clean_data(df).collect()}
    assert result["Alice"] == pytest.approx(120.0)
    assert result["Bob"] == pytest.approx(60.0)