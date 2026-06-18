# E-CON Backend

Enterprise-grade Django backend foundations for the E-CON academic internship SaaS.

## Phase D.2 scope

This repository currently contains only the technical backend foundations:

- modular Django settings;
- PostgreSQL configuration;
- Redis configuration;
- Celery configuration;
- DRF, SimpleJWT, and drf-spectacular configuration;
- reusable abstract models, managers, querysets, mixins, and enums;
- Django app structure for the validated bounded contexts;
- Docker Compose for local development;
- pytest, Ruff, mypy, and Black configuration.

No business models, APIs, serializers, ViewSets, or services are generated in this phase.

## Local commands

```bash
cp .env.example .env
docker compose up --build
```

```bash
python manage.py check
pytest
ruff check .
mypy apps config
black --check .
```
