import pytest
import odbcutils


def test_global_connectionstring():

    assert odbcutils.CONNSTRING == ""
    odbcutils.CONNSTRING = "DRIVER={SQL Server};SERVER=Test;DATABASE=Test;UID=Test;PWD=Test;"

    connstring = "DRIVER={SQL Server};SERVER=Test;DATABASE=Test;UID=Test;PWD=Test;"
    odbcutils.CONNSTRING = connstring
    assert odbcutils.CONNSTRING == connstring
