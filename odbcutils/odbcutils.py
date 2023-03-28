"""
Generic functions to load and return records
from SQL Server
"""
import pyodbc
import logging
from collections import OrderedDict
import typing

log = logging.getLogger("odbcutils")


def execute(connstring: str = "", sql: str = "", params: list | None = None) -> None:
    """
    Execute a SQL statement on the database
    """

    if params is None:
        params = []

    with pyodbc.connect(connstring) as cnxn:
        cursor = cnxn.cursor()
        cursor.execute(sql, *params)


def _get_single(recs):
    assert len(recs) == 1
    return recs[0][0]  # get the first value from the first record


def get_records(
    connstring: str = "",
    sql: str = "",
    params: list | None = None,
    single_value: bool = False,
) -> typing.Any:  # list[pyodbc.Row] | typing.Any
    """
    Execute the SQL on the database and return the results
    """

    if params is None:
        params = []

    with pyodbc.connect(connstring) as cnxn:
        cursor = cnxn.cursor()
        try:
            if single_value:
                recs = cursor.execute(sql, params).fetchone()
            else:
                recs = cursor.execute(sql, *params).fetchall()
        except pyodbc.ProgrammingError:
            log.error(sql)
            raise

    if single_value:
        return _get_single(recs)
    else:
        return recs


def get_records_as_dict(
    connstring: str = "",
    sql: str = "",
    params: list | None = None,
    # single_record: bool = False,
) -> typing.Any:
    """
    Execute SQL and return the resultset in a dictionary
    format of FieldName: Value
    """
    recs = []

    with pyodbc.connect(connstring) as cnxn:
        cursor = cnxn.cursor()

        if params is None:
            params = []

        cursor.execute(sql, *params)

        columns = [column[0] for column in cursor.description]

        for row in cursor.fetchall():
            recs.append(OrderedDict(zip(columns, row)))

    # if single_record:
    #    return _get_single(recs)
    # else:
    #    return recs

    return recs


def save_records(connstring: str = "", sql: str = "", recs: list | None = None) -> None:
    """
    Save records to the database, using fast_executemany
    """

    with pyodbc.connect(connstring) as cnxn:
        cursor = cnxn.cursor()
        # see https://github.com/mkleehammer/pyodbc/wiki/Features-beyond-the-DB-API#fast_executemany
        cursor.fast_executemany = True
        recs = cursor.executemany(sql, recs)


def execute_from_file(
    connstring: str = "", fn: str = "", params: list | None = None
) -> None:
    """
    Execute SQL statements stored in a file
    """

    with open(fn) as f:
        sql = f.read()

    execute(connstring, sql, params)


def select_from_file(
    connstring: str = "",
    fn: str = "",
    params: list | None = None,
    as_dict: bool = False,
) -> typing.Any:
    """
    Run SQL statements stored in a file, returning the
    resulting records
    """

    with open(fn) as f:
        sql = f.read()

    if as_dict:
        return get_records_as_dict(connstring, sql, params)
    else:
        return get_records(connstring, sql, params)
