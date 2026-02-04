# GeoSamples – Architecture & Technical Documentation

## 1. Purpose

GeoSamples is designed as a production-grade geo-spatial data platform.
The primary goals of the architecture are:

- Clear separation of concerns
- Reliable geo-spatial querying using PostGIS
- Predictable deployment via Docker
- Testability with real infrastructure (no mocks)
- Simplicity over unnecessary abstractions

This document explains **how the system is built and why design decisions were made**.

---

## 2. High-Level Architecture

```
Client (Browser)
      |
      v
Nginx (Reverse Proxy + Static Assets)
      |
      +--> /api/*  ---> FastAPI Application
      |
      +--> SPA (Vue)

FastAPI
      |
      v
PostgreSQL 16 + PostGIS 3.4
```

### Key Characteristics
- Single-origin deployment
- Backend is stateless
- Database is the single source of persistence
- Reverse proxy hides internal topology

---

## 3. Component Responsibilities

### Nginx
- Serves frontend static assets
- Acts as a reverse proxy for `/api/*`
- Unifies frontend and backend under the same origin
- Enables production-ready caching and security headers

### Frontend (Vue)
- Consumes the API exclusively through `/api`
- No direct knowledge of backend hostnames
- Stateless client application

### Backend (FastAPI)
- Input validation and request routing
- Business logic encapsulated in service layer
- Database interaction via SQLAlchemy + GeoAlchemy2
- Geometry generation handled at application layer

### Database (PostgreSQL + PostGIS)
- Stores raw attributes and spatial geometry
- Executes spatial queries efficiently
- Enforces data integrity constraints

---

## 4. Backend Internal Architecture

```
app/
├── api/
│   ├── routes/        # HTTP endpoints
│   └── schemas/       # Pydantic models
├── service/           # Business logic
├── db/
│   ├── models/        # ORM models
│   └── session.py     # DB session management
├── core/
│   ├── settings.py    # Environment-based config
│   └── logging.py     # Logging setup
└── main.py
```

### Architectural Pattern
- Layered architecture
- API → Service → DB
- No business logic in routes
- No HTTP knowledge in services

---

## 5. Data Model & Spatial Design

### Table: samples

| Column          | Type                    | Description                         |
|-----------------|-------------------------|-------------------------------------|
| id              | UUID (PK)               | Sample identifier                   |
| latitude        | DOUBLE PRECISION        | Latitude (-90..90)                  |
| longitude       | DOUBLE PRECISION        | Longitude (-180..180)               |
| signal_strength | DOUBLE PRECISION        | Signal value                        |
| timestamp       | TIMESTAMPTZ             | Sample timestamp (UTC)              |
| geom            | GEOMETRY(Point, 4326)   | Spatial representation              |

### Spatial Decisions
- SRID 4326 (WGS84) for compatibility
- Geometry generated at application layer
- GIST index on `geom` for fast spatial queries

---

## 6. Geometry Source of Truth

The application generates `geom` explicitly using:

- `ST_MakePoint(longitude, latitude)`
- `ST_SetSRID(..., 4326)`

### Rationale
- Single source of truth
- Full control over geometry creation
- Avoids hidden DB triggers or side effects
- Easier to test and reason about

---

## 7. Query Flow Example (Polygon Filter)

1. Client sends GeoJSON polygon
2. API validates structure and coordinates
3. Service layer constructs spatial query
4. PostGIS executes `ST_Within`
5. Results returned in descending timestamp order

All spatial computation is delegated to PostGIS.

---

## 8. Testing Strategy

### Test Types
- Integration tests (API + DB)
- Spatial query validation
- Time-based filtering

### Characteristics
- Real PostgreSQL + PostGIS instance
- Dedicated test database (`db_test`)
- Tables truncated between tests
- No mocking of spatial logic

### Why No Mocks?
Spatial correctness depends on PostGIS behavior.
Mocking would reduce confidence instead of increasing it.

---

## 9. Configuration & Environments

- Configuration via environment variables
- `Settings` object cached for performance
- Separate databases for runtime and tests
- No hard-coded environment values

---

## 10. Deployment Model

- Stateless backend containers
- Horizontal scalability ready
- Reverse proxy as single entry point
- Suitable for Docker Swarm / Kubernetes

---

## 11. Design Trade-offs

### Chosen
- Explicit geometry generation
- Real DB testing
- Minimal abstractions

### Avoided
- ORMs hiding spatial logic
- Trigger-based geometry creation
- Mock-heavy testing
- Multi-origin frontend/backend setup

---

## 12. Future Extensions

- Authentication / authorization layer
- Background ingestion workers
- Spatial aggregation queries
- Streaming ingestion (Kafka / Kinesis)
- CI pipeline with automated spatial tests

---

## 13. Summary

GeoSamples prioritizes:
- Correctness over cleverness
- Transparency over magic
- Production realism over demo simplicity

The architecture is intentionally boring — and therefore reliable.
