# bbgo-core
[![API](https://github.com/genonfire/bbgo-core/actions/workflows/backend.yml/badge.svg?branch=master)](https://github.com/genonfire/bbgo-core/actions/workflows/backend.yml)
[![CodeQL](https://github.com/genonfire/bbgo-core/actions/workflows/codeql.yml/badge.svg)](https://github.com/genonfire/bbgo-core/actions/workflows/codeql.yml)
[![codecov](https://codecov.io/gh/genonfire/bbgo-core/branch/master/graph/badge.svg)](https://codecov.io/gh/genonfire/bbgo-core)

Total bbs system made by django

bbgo-ui: https://github.com/genonfire/bbgo-ui


# Create database before setup

    $ psql
    postgres=# create user <DB_USER>;
    postgres=# alter user <DB_USER> with password '<DB_PASSWORD>';
    postgres=# create database <DB_NAME> owner <DB_USER>;


# Getting started with bbgo
[Create Python + virtualenv and activate it](https://docs.python.org/3.10/library/venv.html)

    $ pip install -r requirements.txt
    $ python manage.py migrate
    $ ./serve.sh


# Docker
    TBD


# unittest

    $ ./runtest.sh flake8  # run flake8 only
    $ ./runtest.sh  # run all unit tests + flake8
    $ ./runtest.sh --clean  # without --keepdb option
    $ ./runtest.sh case [case name]  # run a specific unit test in debug-mode


# Swagger

    http://localhost:8000/redoc/
    http://localhost:8000/swagger/

- Available on localserver
- [API Docs in Korean](https://gencode.notion.site/API-docs-5f522b59ba254f218afe4934771b4772)
