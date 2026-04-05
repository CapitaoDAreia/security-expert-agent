FROM python:3.12-slim

# Postgres Driver Dependencies
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# UV
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Copy dependencies
COPY pyproject.toml uv.lock ./

# Sync dependencies
RUN uv sync --frozen

# Copy code, including src and data
COPY . .

# Environment variable for python to find src package 
ENV PYTHONPATH=/app