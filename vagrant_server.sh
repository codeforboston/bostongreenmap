#!/bin/sh
cd bostongreenmap
. ../virtualenv/bin/activate
python manage.py runserver 0.0.0.0:8000
