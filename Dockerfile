# Multi-stage Dockerfile for Hispanie Backend
# Supports: development and production API

# ============================================================================
# BASE STAGE - Common dependencies for all variants
# ============================================================================
FROM python:3.12-slim-bookworm AS base

WORKDIR /app

# Install common system dependencies
RUN apt-get update -y && \
    apt-get install -y --no-install-recommends \
    libmagic1 && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Copy dependency files for better layer caching
COPY pyproject.toml README.md ./

# ============================================================================
# DEPENDENCIES STAGE - Install Python dependencies
# ============================================================================
FROM base AS dependencies

# Upgrade pip
RUN --mount=type=cache,target=/root/.cache/pip \
    pip install --upgrade pip

# Install base Python dependencies
RUN --mount=type=cache,target=/root/.cache/pip \
    pip install --editable .

# ============================================================================
# DEV STAGE - Development environment with hot reload
# ============================================================================
FROM dependencies AS dev

# Copy source code
COPY . .

EXPOSE 3201

# Default command for API dev server with hot reload and debug logging
CMD ["uvicorn", "hispanie.api.api:app", "--host", "0.0.0.0", "--port", "3201", "--log-level", "debug", "--reload"]

# ============================================================================
# API PRODUCTION STAGE - Production API
# ============================================================================
FROM dependencies AS api

# Copy only necessary files for API
COPY hispanie/ ./hispanie/
COPY alembic/ ./alembic/
COPY config.ini ./
COPY scripts/start-api.sh ./scripts/

# Make startup script executable
RUN chmod +x ./scripts/start-api.sh

# Create non-root user for security
RUN useradd -m -u 1000 appuser && \
    chown -R appuser:appuser /app

USER appuser

EXPOSE 3201

# Production API server with automatic migrations
CMD ["./scripts/start-api.sh"]
