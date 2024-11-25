FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN pip install poetry

WORKDIR /app

COPY poetry.lock pyproject.toml /app/

RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi

COPY . /app

RUN adduser -u 5678 --disabled-password --gecos "" appuser && chown -R appuser /app

USER appuser