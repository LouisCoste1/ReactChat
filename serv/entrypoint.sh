#!/bin/bash
if [ "$1" = "test" ]; then
    echo "Starting Gunicorn in background..."
    . /venv/bin/activate
    gunicorn --bind 0.0.0.0:5000 app:app --workers 4 --threads 2 &
    
    # Wait briefly to ensure the server starts up
    sleep 10
    
    echo "Running tests..."
    pytest
    
    # Bring the server back to the foreground
    fg %1
else
    echo "Starting Gunicorn..."
    exec gunicorn --bind 0.0.0.0:5000 app:app --workers 4 --threads 2
fi
