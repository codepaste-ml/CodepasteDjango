#!/bin/sh
set -ex
python manage.py collectstatic --no-input
python manage.py migrate --no-input
gunicorn Codepaste.wsgi -b 0.0.0.0:8000 --preload
