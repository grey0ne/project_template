FROM grey0ne/dev-environment:0.6.9

ENV PYTHONUNBUFFERED=1
ENV POETRY_VIRTUALENVS_CREATE=false

WORKDIR /app

COPY backend/pyproject.toml /app/
RUN poetry install

COPY spa/package.json /app/
RUN npm install

RUN chown -R greyone:greyone /app

ENV NODE_ENV development
ENV NODE_PATH /app/node_modules

WORKDIR /app/src
