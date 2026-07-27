#!/usr/bin/env bash
# Render build script
set -e  # exit on error

pip install -r requirements.txt
python manage.py collectstatic --noinput
python manage.py migrate --run-syncdb
python seed_data.py
