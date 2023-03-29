import re
from setuptools import setup
from io import open

(__version__,) = re.findall(
    '__version__ = "(.*)"', open("odbcutils/__init__.py").read()
)


def readme():
    with open("README.rst", "r", encoding="utf-8") as f:
        return f.read()


setup(
    name="odbcutils",
    version=__version__,
    description="A small helper library for executing SQL using pyodbc",
    long_description=readme(),
    classifiers=[
        # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.10",
        "Intended Audience :: Developers",
        "Topic :: Database",
    ],
    url="http://github.com/geographika/odbcutils",
    author="Seth Girvin",
    author_email="sethg@geographika.co.uk",
    license="MIT",
    package_data={"odbcutils": ["py.typed"]},
    packages=["odbcutils"],
    install_requires=["pyodbc"],
    zip_safe=False,
)
