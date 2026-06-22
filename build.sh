#!/bin/bash
set -e

pip3 install --upgrade -r requirements.txt
python3 manage.py collectstatic --noinput
