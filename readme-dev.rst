Developer Notes
===============

Virtual Environment
-------------------

.. code-block:: console

    C:\Python27\scripts\virtualenv C:\VirtualEnvs\odbcutils
    C:\VirtualEnvs\odbcutils\scripts\activate.bat
    pip install -r D:\GitHub\odbcutils\requirements-dev.txt
    pip install -e D:\GitHub\odbcutils

Testing
-------

.. code-block:: console

    C:\VirtualEnvs\odbcutils\scripts\activate.bat
    cd /D D:\GitHub\odbcutils
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