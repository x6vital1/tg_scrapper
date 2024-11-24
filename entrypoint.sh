#!/bin/bash
set -e

echo "Starting the Telegram Channel Parser..."
echo $PWD
poetry lock --no-update
poetry install
echo "Telegram Channel Parser started successfully."
exec "$@"