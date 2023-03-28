import odbcutils
import pytest
import logging
import os

log = logging.getLogger("odbcutils")
log.setLevel(logging.DEBUG)

console_handler = logging.StreamHandler()
log.addHandler(console_handler)

if "TEST_CONN" in os.environ:
    TEST_CONN = os.environ["TEST_CONN"]
    log.info(f"Using test connection string {TEST_CONN}")
else:
    TEST_CONN = r"DRIVER={ODBC Driver 17 for SQL Server};SERVER=localhost;DATABASE=tempdb;uid=sa;pwd=dbatools.I0"


@pytest.fixture
def setup_db():
    odbcutils.execute(
        TEST_CONN, sql="CREATE TABLE test ([MyKey] [int], [MyValue] [nvarchar])"
    )
    odbcutils.execute(TEST_CONN, sql="INSERT INTO test VALUES (1, 'A')")
    odbcutils.execute(TEST_CONN, sql="INSERT INTO test VALUES (2, 'B')")
    odbcutils.execute(TEST_CONN, sql="INSERT INTO test VALUES (3, 'C')")
    yield
    odbcutils.execute(TEST_CONN, sql="DROP TABLE test;")


@pytest.mark.usefixtures("setup_db")
def test_execute():
    sql = "INSERT INTO test VALUES (4, 'D')"
    odbcutils.execute(TEST_CONN, sql=sql)

    recs = odbcutils.get_records(TEST_CONN, "SELECT * FROM test")
    assert len(recs) == 4


@pytest.mark.usefixtures("setup_db")
def test_execute_with_params():
    sql = "INSERT INTO test VALUES (?, ?)"
    odbcutils.execute(TEST_CONN, sql=sql, params=[5, "E"])

    recs = odbcutils.get_records(TEST_CONN, "SELECT * FROM test")
    assert len(recs) == 4


@pytest.mark.usefixtures("setup_db")
def test_get_records():
    recs = odbcutils.get_records(TEST_CONN, "SELECT * FROM test")
    assert len(recs) == 3


@pytest.mark.usefixtures("setup_db")
def test_get_records_with_params():
    recs = odbcutils.get_records(TEST_CONN, "SELECT * FROM test WHERE MyKey = ?", [3])
    assert len(recs) == 1


@pytest.mark.usefixtures("setup_db")
def test_get_records_single_value():
    val = odbcutils.get_records(
        TEST_CONN, "SELECT MyValue FROM test WHERE MyKey = ?", [3], single_value=True
    )
    assert val == "C"


@pytest.mark.usefixtures("setup_db")
def test_get_records_as_dict():
    recs = odbcutils.get_records_as_dict(
        TEST_CONN, "SELECT MyKey, MyValue FROM test ORDER BY MyKey ASC"
    )
    assert len(recs) == 3
    assert recs[0]["MyKey"] == 1
    assert recs[0]["MyValue"] == "A"


@pytest.mark.usefixtures("setup_db")
def test_get_records_as_dict_with_params():
    recs = odbcutils.get_records_as_dict(
        TEST_CONN, "SELECT MyKey, MyValue FROM test WHERE MyKey = ?", params=[2]
    )
    assert len(recs) == 1
    assert recs[0]["MyKey"] == 2
    assert recs[0]["MyValue"] == "B"


# @pytest.mark.usefixtures("setup_db")
# def test_get_records_as_dict_single_value():
#    res = odbcutils.get_records_as_dict(
#        TEST_CONN,
#        "SELECT MyValue FROM test WHERE MyKey = ?",
#        params=[2],
#        single_record=True,
#    )
#    assert res == "B"


if __name__ == "__main__":
    # when using fixtures we need to invoke pytest
    # we cannot simply call test_execute(setup_db)
    # pytest.main(['-vv', './tests/test_odbcutils.py::test_execute'])
    pytest.main(["-vv", "./tests/test_odbcutils.py"])

    print("Done!")
