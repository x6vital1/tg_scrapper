FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1

ENV PYTHONUNBUFFERED=1

RUN pip3 install poetry==1.8.4

WORKDIR /app
COPY . /app

RUN adduser -u 5678 --disabled-password --gecos "" appuser && chown -R appuser /app
USER appuser
RUN chmod +x entrypoint.sh

ENTRYPOINT ["/app/entrypoint.sh"]

