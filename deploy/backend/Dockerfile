# Base stage

FROM ghcr.io/astral-sh/uv:python3.12-bookworm AS base

ENV UV_COMPILE_BYTECODE=1
ENV UV_LINK_MODE=copy
ENV PATH="/app/.venv/bin:$PATH"

RUN mkdir -p /app
WORKDIR /app

# Preproduction stage

FROM base AS preproduction

COPY backend ./backend

RUN --mount=type=cache,target=/root/.cache/uv \
  --mount=type=bind,source=uv.lock,target=uv.lock \
  --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
  uv sync --frozen --no-install-project --no-dev


# Predevelopment stage

FROM base AS predevelopment

RUN --mount=type=cache,target=/root/.cache/uv \
  --mount=type=bind,source=uv.lock,target=uv.lock \
  --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
  uv sync --frozen --no-install-project


# Development stage

FROM predevelopment AS development

CMD ["fastapi", "dev", "backend/app.py", "--host", "0.0.0.0", "--port", "80"]


# Testing stage

FROM predevelopment AS testing

COPY ./pyproject.toml ./
CMD ["pytest"]


# Production stage

FROM python:3.12-slim-bookworm AS production

ENV PATH="/app/.venv/bin:$PATH"
WORKDIR /app

COPY --from=preproduction /app /app

CMD ["fastapi", "run", "backend/app.py", "--port", "80", "--workers", "4", "--workers", "4"]
