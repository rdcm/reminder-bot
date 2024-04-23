FROM python:3.12.3-alpine3.19 AS build
WORKDIR /app
RUN pip install poetry==1.8.2
ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_VIRTUALENVS_CREATE=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache
COPY pyproject.toml poetry.lock ./
RUN poetry install --no-root --without dev --no-ansi
COPY src/ /app/src

FROM python:3.12.3-alpine3.19 AS final
WORKDIR /app
ENV VIRTUAL_ENV=/app/.venv
ENV PATH="/app/.venv/bin:$PATH"
COPY --from=build /app /app
ENTRYPOINT ["python", "src/reminder_bot/main.py"]