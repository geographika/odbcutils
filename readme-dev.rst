Developer Notes
===============

Virtual Environment
-------------------



$VENV_LOCATION = "C:\VirtualEnvs\odbcutils"
$PROJECT_LOCATION = "D:\GitHub\odbcutils"
."$VENV_LOCATION\Scripts\activate.ps1"

cd $PROJECT_LOCATION

pip install -r requirements.txt

black .
flake8 .
mypy odbcutils.py tests

    C:\Python310\python.exe -m pip install --upgrade pip
    C:\Python310\Scripts\pip install virtualenv
    C:\Python310\Scripts\virtualenv C:\VirtualEnvs\odbcutils
    C:\VirtualEnvs\odbcutils\scripts\activate.ps1

    pip install -r D:\GitHub\odbcutils\requirements.txt
    pip install -e D:\GitHub\odbcutils

Testing
-------

.. code-block:: console

    C:\VirtualEnvs\odbcutils\scripts\activate.ps1
    cd D:\GitHub\odbcutils
    black .
    flake8 --max-line-length=120
    py.test tests/

PyPI
----

.. code-block:: console

    C:\VirtualEnvs\odbcutils\Scripts\activate.bat
    cd /D D:\GitHub\odbcutils
    rmdir /s /q dist\
    rmdir /s /q build\
    python setup.py bdist_wheel --universal
    python setup.py sdist
    twine upload dist/* --config-file .pypirc