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

## Local backend startup

### Docker Compose

```bash
cp .env.example .env
docker compose up --build
```

### Direct local runserver

Use the local settings module. For a quick local startup without requiring PostgreSQL or Redis, enable SQLite and the in-memory cache:

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
python -m pip install -r requirements.txt
cp .env.example .env
DJANGO_USE_SQLITE=true DJANGO_USE_LOCMEM_CACHE=true python manage.py migrate
DJANGO_USE_SQLITE=true DJANGO_USE_LOCMEM_CACHE=true python manage.py check
DJANGO_USE_SQLITE=true DJANGO_USE_LOCMEM_CACHE=true python manage.py runserver
```

The backend then listens on `http://127.0.0.1:8000/`.

Celery is intentionally not imported during Django startup. Start a worker explicitly from the Celery module when needed:

```bash
celery -A config.celery worker -l info
```

## Local checks

```bash
python manage.py check
pytest
ruff check .
mypy apps config
black --check .
```
