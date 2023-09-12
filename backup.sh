#!/bin/bash

PYTHON=
PRJ_DIR=
OUT_DIR=
DB=default
today=$(date +"%F")

$PYTHON $PRJ_DIR/manage.py dumpdata --database $DB -a things --exclude=things.Attachment --indent 4 -o $OUT_DIR/things.json
$PYTHON $PRJ_DIR/manage.py dumpdata --database $DB -a things.Attachment --indent 4 -o $OUT_DIR/attachments.json
$PYTHON $PRJ_DIR/manage.py dumpdata --database $DB -a accounts --indent 4 -o $OUT_DIR/accounts.json
$PYTHON $PRJ_DIR/manage.py dumpdata --database $DB -a authtoken.Token --indent 4 -o $OUT_DIR/token.json

cd $OUT_DIR
tar -C . -cvzf $today.tar.gz *.json --remove-files
