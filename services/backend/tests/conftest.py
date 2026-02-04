import os
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

from app.main import create_app
from app.db.session import get_db

TEST_DATABASE_URL = os.getenv(
    "TEST_DATABASE_URL",
    "postgresql+psycopg://geouser:geopass@db_test:5432/geosamples_test",
)

engine = create_engine(TEST_DATABASE_URL, pool_pre_ping=True)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="session", autouse=True)
def ensure_db_ready():
    with engine.begin() as conn:
        conn.execute(text("SELECT PostGIS_Version();"))
        conn.execute(text("SELECT 1 FROM information_schema.tables WHERE table_name='samples';"))
    yield


@pytest.fixture(autouse=True)
def cleanup_samples():
    with engine.begin() as conn:
        conn.execute(text("TRUNCATE TABLE samples;"))
    yield


@pytest.fixture()
def client():
    app = create_app()

    def override_get_db():
        db = TestingSessionLocal()
        try:
            yield db
            db.commit()
        except Exception:
            db.rollback()
            raise
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as c:
        yield c
