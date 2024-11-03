#!/bin/bash
if [ "$1" = "test" ]; then
    echo "Running tests..."
    . /venv/bin/activate
    pytest
else
    echo "Starting Gunicorn..."
    exec gunicorn --bind 0.0.0.0:5000 app:app --workers 4 --threads 2
fi
