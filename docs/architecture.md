# Architecture Overview

## Core layers

- `backend/` — FastAPI REST API, request validation, and service orchestration.
- `ml/` — Data cleaning, feature engineering, model training, persistence, and evaluation.
- `agents/` — Prompt templates, document search, and multi-agent orchestration.
- `infra/` — Deployment configuration and containerization files.

## Data flow

1. Data ingestion through `POST /api/ingest`.
2. Model prediction via `POST /api/predict`.
3. Document search through `POST /api/search`.
4. Agent orchestration via `POST /api/agent`.

## Deployment targets

- Local development with `uvicorn`.
- Containerized deployment using Docker and `docker-compose`.
- CI pipeline using GitHub Actions.
