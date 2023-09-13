#!/bin/bash
set -o allexport
source ./env/.local.env
set +o allexport

# python3 project/manage.py flush --no-input
python3 project/manage.py makemigrations
python3 project/manage.py migrate
# python3 project/manage.py createsuperuser
python3 project/manage.py runserver 0.0.0.0:8017