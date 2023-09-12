#! /bin/bash

db_host=$(python manage.py diffsettings | grep DB_HOST | awk '{print $3}')
if [[ "$db_host" != "'localhost'" ]]; then
    echo "This script is only available in localhost as DB_HOST."
    exit
fi

python manage.py flush --noinput

declare -a fixtures_backup=(
    "./frontend/upload/fixtures/things.json"
    "./frontend/upload/fixtures/accounts.json"
    "./frontend/upload/fixtures/attachments.json"
    "./frontend/upload/fixtures/token.json"
)

declare -a fixtures=("${fixtures_backup[@]}")

for fixture in "${fixtures[@]}"
do
    if [ -f "$fixture" ]; then
        if [[ "$OSTYPE" == "darwin"* ]]; then
            filesize=$(stat -f%z "$fixture")
        else
            filesize=$(stat -c%s "$fixture")
        fi
        if [ "$filesize" -ge 5 ]; then
            echo "loading $fixture($filesize)..."
            python manage.py loaddata "$fixture" --settings=bbgo.migration_settings
        fi
    fi
done
