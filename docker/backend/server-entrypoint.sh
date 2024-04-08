#!/bin/sh


until cd /app/myshop
do
    echo "Waiting for myshop server volume>>>"
done


until python manage.py migrate
do
    echo "Waiting for db to e ready>>>"
    sleep 3
done


python manage.py collectstatic --noinput

gunicorn myshop.wsgi --bind 0.0.0.0:8000 --workers 4 --threads 4
