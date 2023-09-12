#! /bin/bash

db_host=$(python manage.py diffsettings | grep DB_HOST | awk '{print $3}')
if [[ "$db_host" != "'localhost'" ]]; then
    echo "This script is only available in localhost as DB_HOST."
    exit
fi

python manage.py flush --noinput
