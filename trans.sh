#! /bin/bash

django-admin makemessages -a -i ".tox" -i "frontend/wc" -i "frontend/upload"
django-admin compilemessages -i ".tox" -i "frontend/wc" -i "frontend/upload"
