#!/bin/bash
set -e

echo "Starting the Telegram Channel Parser..."

# Запускает скрипт, но не завершает контейнер
poetry lock --no-update
poetry install
echo "Telegram Channel Parser started successfully."

# Здесь добавляем команду для запуска оболочки или вашего основного процесса
exec "$@"