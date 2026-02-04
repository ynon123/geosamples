# GeoSamples – Geo-Spatial Data Platform

GeoSamples is a production-ready full-stack project that demonstrates ingestion, storage, querying, and visualization of geo-spatial samples using PostGIS.

The system is designed with clean architecture principles and realistic production considerations: reverse proxying, spatial indexing, environment separation, and automated testing with a real PostGIS database.

---

## Overview

GeoSamples allows clients to:
- Ingest geo-spatial samples (latitude, longitude, signal strength, timestamp)
- Query samples by time range
- Perform spatial filtering using GeoJSON polygons
- Serve a modern frontend and API from a single origin

---

## Architecture

```
Browser
  |
  v
Nginx (Frontend + Reverse Proxy)
  |
  +--> /api/*  ---> FastAPI (Backend)
  |
  +--> Static SPA (Vue)

FastAPI
  |
  v
PostgreSQL + PostGIS
```

- Frontend and backend are served under the same origin
- Nginx handles reverse proxying and static assets
- No CORS is required in production

---

## Technology Stack

### Backend
- FastAPI
- SQLAlchemy 2.x
- GeoAlchemy2
- PostgreSQL 16 + PostGIS 3.4

### Frontend
- Vue (Vite build)
- Nginx

### DevOps & Tooling
- Docker & Docker Compose
- pytest (integration tests with real PostGIS)
- httpx

---

## Project Structure (Backend)

```
services/backend/
├── app/
│   ├── api/        # API routes and schemas
│   ├── core/       # Settings and logging
│   ├── db/         # DB session and models
│   ├── service/    # Business logic
│   └── main.py
├── tests/
├── Dockerfile
├── pytest.ini
└── requirements.txt
```

---

## Running the Project (Local)

### Prerequisites
- Docker
- Docker Compose

### Build and Run
```bash
cp .env.example .env
docker compose build
docker compose up -d
```

### Access
- Frontend: http://localhost:3000
- API Health: http://localhost:3000/api/health

---

## API Endpoints

### POST /api/samples
Ingest one or multiple samples.

### GET /api/samples
List samples with pagination and optional time filtering.

### POST /api/samples/filter
Filter samples using:
- GeoJSON polygon
- Time range
- Pagination parameters

---

## Testing

The project includes automated tests that run against a dedicated PostGIS test database.

### Run Tests
```bash
docker compose up -d db_test
docker compose run --rm api pytest
```

### Notes
- Tests use a real PostgreSQL + PostGIS instance
- Tables are truncated between tests
- No mocks are used for spatial queries

---

## Design Notes

- Geometry (`geom`) is generated at the application layer to maintain a single source of truth
- Spatial queries use GIST indexes for performance
- The system is structured to support production deployment and CI pipelines

---

## Deployment Considerations

- Single-origin deployment via Nginx
- Environment variables control configuration
- Stateless backend containers
- Ready for CI/CD integration

---