#! /bin/bash

find . -name \*.pyc -delete
python manage.py diffsettings | grep DB_NAME
python manage.py runserver
