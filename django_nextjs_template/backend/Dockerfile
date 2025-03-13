FROM python:3.13.0-slim

ENV PYTHONUNBUFFERED=1
ENV POETRY_VIRTUALENVS_CREATE=false

WORKDIR /app

COPY pyproject.toml /app/

RUN python -mpip install --upgrade pip --root-user-action=ignore
RUN python -mpip install poetry && poetry install

WORKDIR /app/src

CMD python -m uvicorn --reload --lifespan off --host 0.0.0.0 --port 8000 application.asgi:application