FROM python:3.12.1-slim

ENV PYTHONUNBUFFERED=1
ENV POETRY_VIRTUALENVS_CREATE=false

WORKDIR /app

COPY pyproject.toml /app/

RUN python -mpip install --upgrade pip
RUN python -mpip install poetry && poetry install

WORKDIR /app/src
