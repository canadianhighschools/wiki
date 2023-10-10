#!/bin/bash
set -o allexport
source ./env/local.env
set +o allexport


if [ "$1" == "-f" ]; then
echo "Flushing database"
python3 project/manage.py flush --no-input
python3 project/manage.py makemigrations
python3 project/manage.py migrate
DJANGO_SUPERUSER_PASSWORD=admin
python3 project/manage.py createsuperuser --no-input --username admin --nickname TheAdmin

else
python3 project/manage.py makemigrations
python3 project/manage.py migrate
fi
python3 project/manage.py runserver 0.0.0.0:8017