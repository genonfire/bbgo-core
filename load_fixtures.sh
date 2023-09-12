#! /bin/bash

db_host=$(python manage.py diffsettings | grep DB_HOST | awk '{print $3}')
if [[ "$db_host" != "'localhost'" ]]; then
    echo "This script is only available in localhost as DB_HOST."
    exit
fi

declare -a fixtures_things=(
)

declare -a fixtures_accounts=(
)

declare -a fixtures_test=(
    "accounts_test.json"
)

declare -a fixtures=()

if [ $# -eq 0 ]; then
    declare -a fixtures=(
        "${fixtures_things[@]}"
        "${fixtures_accounts[@]}"
    )
else
    for argval in "$@"
    do
        if [ "$argval" == "things" ]; then
            fixtures+=("${fixtures_things[@]}")
        fi
        if [ "$argval" == "accounts" ]; then
            fixtures+=("${fixtures_accounts[@]}")
        fi
        if [ "$argval" == "test" ]; then
            fixtures+=("${fixtures_test[@]}")
        fi
    done
fi
echo "# loading following fixtures: ${fixtures[@]}"

for fixture in "${fixtures[@]}"
do
    echo " $fixture..."
    SECONDS=0
    python manage.py loaddata "$fixture" --settings=bbgo.migration_settings
    duration=$SECONDS
    if [ $? -eq 0 ]; then
        echo "# successfully loaded" "$fixture" "in $duration seconds."
    else
        echo "# error while loading" "$fixture"
        break
    fi
done
