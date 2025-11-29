#!/bin/bash
set -e

echo "Running database migrations..."
flask db upgrade

echo "Starting gunicorn server..."
exec gunicorn run:app
