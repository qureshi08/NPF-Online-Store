#!/bin/bash
set -e

echo "Running database migrations..."
python -m flask db upgrade

echo "Starting gunicorn server..."
exec gunicorn run:app --preload
