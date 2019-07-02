"""
Generic functions to load and return records
from SQL Server
"""
import pyodbc
import logging
from collections import OrderedDict


__version__ = "0.1.0"


# set the connection string once globally if required
CONNSTRING = ""


def execute(sql, params=None, connstring=CONNSTRING):

    if params is None:
        params = []

    with pyodbc.connect(connstring) as cnxn:
        cursor = cnxn.cursor()
        cursor.execute(sql, *params)


def _get_single(recs):

    assert len(recs) == 1
    return recs[0][0]  # get the first value from the first record


def get_records(sql, params=None, connstring=CONNSTRING, single_record=False):

    if params is None:
        params = []

    with pyodbc.connect(connstring) as cnxn:
        cursor = cnxn.cursor()
        try:
            recs = cursor.execute(sql, *params).fetchall()
        except pyodbc.ProgrammingError:
            logging.warning(sql)
            raise

    if single_record:
        return _get_single(recs)
    else:
        return recs


def get_records_as_dict(sql, params=None, connstring=CONNSTRING, single_record=False):

    recs = []

    with pyodbc.connect(connstring) as cnxn:
        cursor = cnxn.cursor()

        if params is None:
            params = []

        cursor.execute(sql, *params)

        columns = [column[0] for column in cursor.description]

        for row in cursor.fetchall():
            recs.append(OrderedDict(zip(columns, row)))

    if single_record:
        return _get_single(recs)
    else:
        return recs


def save_records(sql, recs, connstring=CONNSTRING):

    with pyodbc.connect(connstring) as cnxn:
        cursor = cnxn.cursor()
        # see https://github.com/mkleehammer/pyodbc/wiki/Features-beyond-the-DB-API#fast_executemany
        cursor.fast_executemany = True
        recs = cursor.executemany(sql, recs)


def execute_from_file(fn, params=None, connstring=CONNSTRING):

    with open(fn) as f:
        sql = f.read()

    execute(sql, params, connstring)


def select_from_file(fn, params=None, connstring=CONNSTRING, as_dict=False):

    with open(fn) as f:
        sql = f.read()

    if as_dict:
        return get_records_as_dict(sql, params, connstring)
    else:
        return get_records(sql, params, connstring)
