from datetime import datetime, timedelta

from asserts import read_table
from data_generator import DATE_FORMAT, generate_dates
from elementary.clients.dbt.dbt_runner import DbtRunner
from run_dbt_test import run_dbt_test

TIMESTAMP_COLUMN = "updated_at"
DBT_TEST_NAME = "elementary.volume_anomalies"
DBT_TEST_ARGS = {"timestamp_column": TIMESTAMP_COLUMN}


def read_status(dbt_runner: DbtRunner, test_id: str):
    results = read_table(
        dbt_runner,
        "elementary_test_results",
        where=f"table_name = '{test_id}'",
        column_names=["status"],
    )
    return results


def test_anomalyless_table_volume_anomalies(request, dbt_runner: DbtRunner):
    test_id = request.node.name
    data = [
        {TIMESTAMP_COLUMN: date.strftime(DATE_FORMAT)}
        for date in generate_dates(base_date=datetime.now())
        for _ in range(10)
    ]
    run_dbt_test(dbt_runner, data, test_id, DBT_TEST_NAME, DBT_TEST_ARGS)
    assert all(
        result["status"] == "pass" for result in read_status(dbt_runner, test_id)
    )


def test_full_drop_table_volume_anomalies(request, dbt_runner: DbtRunner):
    test_id = request.node.name
    data = [
        {TIMESTAMP_COLUMN: date.strftime(DATE_FORMAT)}
        for date in generate_dates(base_date=datetime.now())
        for _ in range(10)
        if date < datetime.now() - timedelta(days=2)
    ]
    run_dbt_test(dbt_runner, data, test_id, DBT_TEST_NAME, DBT_TEST_ARGS)
    assert all(
        result["status"] == "fail" for result in read_status(dbt_runner, test_id)
    )


def test_partial_drop_table_volume_anomalies(request, dbt_runner: DbtRunner):
    test_id = request.node.name
    data = [
        {TIMESTAMP_COLUMN: date.strftime(DATE_FORMAT)}
        for date in generate_dates(base_date=datetime.now())
        for _ in range(10 if date < datetime.now() - timedelta(days=2) else 1)
    ]
    run_dbt_test(dbt_runner, data, test_id, DBT_TEST_NAME, DBT_TEST_ARGS)
    assert all(
        result["status"] == "fail" for result in read_status(dbt_runner, test_id)
    )


def test_spike_table_volume_anomalies(request, dbt_runner: DbtRunner):
    test_id = request.node.name
    data = [
        {TIMESTAMP_COLUMN: date.strftime(DATE_FORMAT)}
        for date in generate_dates(base_date=datetime.now())
        for _ in range(10 if date < datetime.now() - timedelta(days=2) else 100)
    ]
    run_dbt_test(dbt_runner, data, test_id, DBT_TEST_NAME, DBT_TEST_ARGS)
    assert all(
        result["status"] == "fail" for result in read_status(dbt_runner, test_id)
    )
