#!/bin/sh

until cd /app/myshop
do
    echo "Waiting for myshop server volume>>>"
done

celery -A myshop worker --loglevel=info --concurrency 1 -E

