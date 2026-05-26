# Smart Retail Assistant

A starter implementation of a Smart Retail Assistant platform that integrates backend APIs, demand forecasting, document search, and a multi-agent service.

## Project structure

- `backend/` — FastAPI backend, API routes, services, and tests.
- `ml/` — Machine learning pipeline, model training, evaluation, and persistence.
- `agents/` — Agent orchestration, RAG search service, and prompt templates.
- `infra/` — Docker and infrastructure support.
- `.github/workflows/` — GitHub Actions CI pipeline.
- `docs/` — Architecture, deployment, and reflection documentation.

## Quick start

1. Create a Python environment and install dependencies:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

2. Run the API locally:

```bash
uvicorn backend.app.main:app --reload --host 0.0.0.0 --port 8000
```

3. Run tests:

```bash
pytest backend/tests
```

## Notes

- The backend includes endpoints for ingestion, prediction, search, and agent orchestration.
- `ml/` includes starter model code and training / evaluation scripts.
- `agents/` contains a placeholder RAG search service and agent manager for multi-agent orchestration.
- Add Azure deployment configuration and data engineering pipeline details as part of the next development phase.
