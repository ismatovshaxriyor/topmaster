# TopMaster — Backend API

TopMaster is a services marketplace for Uzbekistan (Uzbek-Latin UI) connecting
clients (**mijoz**) with verified tradespeople / masters (**usta**). Clients
post jobs (buyurtmalar), masters send proposals (takliflar), the two chat in
real time, work gets done, and clients leave reviews (sharhlar).

This repository is the **Django REST + Channels** backend: a JSON API under
`/api/v1/`, real-time chat and notifications over WebSockets, background jobs on
Celery, and S3-compatible media storage via MinIO.

> **Payments are intentionally excluded.** There is **no** payment processing,
> escrow, or money movement anywhere in this backend. Price fields on jobs and
> proposals are *informational only* — they record what a client offers / a
> master quotes. The 10% platform commission is a display constant, not a
> transaction. Any payment UI in the design system is out of scope here.

## Stack

- **Python 3.12**, **Django 5.1** + **Django REST Framework**
- **SimpleJWT** for auth (access/refresh tokens, refresh blacklisting)
- **Channels 4 + Daphne/uvicorn** for WebSockets, backed by **Redis**
- **Celery + Redis** for background tasks (job matching, FCM push), with
  `django-celery-beat` + `django-celery-results`
- **PostgreSQL 16** database
- **MinIO** (S3-compatible) media storage via `django-storages` / `boto3`
- **drf-spectacular** for the OpenAPI schema + Swagger UI
- **Firebase Admin** for FCM push (optional; gracefully disabled when unset)
- **pytest** + `pytest-django` for tests

## Project layout

```
config/            settings (base/dev/prod), urls, asgi/wsgi, routing, celery
apps/
  common/          shared base models, permissions, pagination, seed_demo
  accounts/        custom User (email login), settings, devices, JWT WS auth
  catalog/         cities + service categories (reference data)
  masters/         master profiles, skills, portfolio, verification
  jobs/            client job orders + lifecycle timeline
  proposals/       master proposals on jobs
  reviews/         client reviews of masters (rating aggregates via signals)
  chat/            1:1 conversations + messages (REST + WebSocket)
  notifications/   in-app notifications (WebSocket + FCM), notify() service
  favorites/       saved / favourite masters
  support/         help center (FAQ topics + entries)
```

## Quickstart (Docker)

Everything runs in Docker Compose (Postgres, Redis, MinIO, web, Celery
worker/beat, Mailpit).

```bash
cp .env.example .env
docker compose up --build
```

On first boot the web container's entrypoint waits for Postgres + Redis, runs
migrations, collects static files, and seeds reference data
(`seed_catalog`, `seed_support`). The API is then available at
`http://localhost:8000`.

Create a superuser for the admin:

```bash
docker compose run --rm web python manage.py createsuperuser
```

## Key URLs

| URL | What |
| --- | --- |
| `http://localhost:8000/api/v1/` | API root (all endpoints live under here) |
| `http://localhost:8000/api/docs/` | Swagger UI (interactive API docs) |
| `http://localhost:8000/api/schema/` | OpenAPI 3 schema (raw) |
| `http://localhost:8000/admin/` | Django admin |
| `http://localhost:8000/health/` | Health check |
| `http://localhost:9001/` | MinIO console (user/pass from `.env`: `topmaster` / `topmaster-secret`) |
| `http://localhost:8025/` | Mailpit (captured outbound email, dev profile) |

API areas: `auth/`, `catalog/`, `masters/`, `jobs/`, `proposals/`,
`reviews/`, `chat/`, `notifications/`, `favorites/`, `support/` — all under
`/api/v1/`.

## Seed data

Reference data is seeded automatically on first boot. To (re-)run manually —
all three commands are idempotent and safe to re-run:

```bash
docker compose run --rm web python manage.py seed_catalog   # cities + categories
docker compose run --rm web python manage.py seed_support   # FAQ topics + entries
docker compose run --rm web python manage.py seed_demo      # demo users/jobs/chat/...
```

**Order matters:** `seed_demo` depends on cities + categories, so run
`seed_catalog` (and `seed_support`) **before** `seed_demo`.

`seed_demo` mirrors the frontend mock data and creates:

- one client: **Bekzod Murodov** — `bekzod@topmaster.uz`
- ~6 master users (Akmal, Dilnoza, Sardor, Gulnora, Jasur, Nodira) with
  profiles, categories, and (for Akmal) skills + portfolio items
- several jobs (open + in_progress), a couple of proposals, a review on a
  completed job, one conversation with messages, a handful of notifications,
  and saved-master rows for the client

All seeded users share the password **`topmaster123`**.

## Running tests

```bash
docker compose run --rm web pytest
```

Tests use pytest + `pytest-django` (config in `pyproject.toml`,
`DJANGO_SETTINGS_MODULE=config.settings.dev`). The root `conftest.py` provides
shared `api_client`, `make_client`, and `make_master` fixtures; most app tests
are otherwise self-contained.

## WebSockets

WebSocket endpoints are served by Channels and authenticated with the **JWT
access token** passed as a `?token=<access>` query parameter (the same token
issued by `POST /api/v1/auth/login/`). A bare `Authorization: Bearer` header is
also accepted.

| Endpoint | Purpose |
| --- | --- |
| `ws://localhost:8000/ws/chat/<conversation_id>/?token=<access>` | Live chat for one conversation |
| `ws://localhost:8000/ws/notifications/?token=<access>` | Per-user notification stream |

**Chat** (`/ws/chat/<id>/`) — client sends JSON actions:

```json
{ "action": "message", "text": "Salom" }
{ "action": "typing" }
{ "action": "read" }
```

The server broadcasts `message`, `typing`, and `read` events to the
conversation group; new messages also trigger a notification to the recipient.

**Notifications** (`/ws/notifications/`) — the server pushes `notification` and
`unread` events; the client is not expected to send anything. On connect the
current unread count is delivered immediately.

## Configuration

All configuration is environment-driven (`django-environ`); see
`.env.example` for the full list. Notable toggles:

- `USE_S3` — when `true` (default), media goes to MinIO/S3; when `false`,
  media is served from the local filesystem and `/media/` is served by Django
  in `DEBUG`.
- `FIREBASE_CREDENTIALS_FILE` — path to an FCM service-account JSON. When
  unset, push delivery is skipped gracefully (logged, never raised).
- Redis uses separate logical DBs for Channels / Celery broker / cache.

## Note on payments

To restate the project boundary: this backend performs **no payment
processing**. There is no payment gateway integration, no escrow logic, and no
money ever changes hands through the API. This is by design.
