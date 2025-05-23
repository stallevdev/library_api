import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session, sessionmaker

from alembic.command import downgrade, upgrade
from alembic.config import Config
from app.core.config import settings
from app.core.db import get_db
from app.core.security import create_access_token
from app.main import app
from app.models.user import User

TEST_DATABASE_URL = settings.DATABASE_URL
ALEMBIC_CONFIG_PATH = "alembic.ini"

engine: Engine = create_engine(TEST_DATABASE_URL, echo=False)
TestingSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine)


def create_test_database():
    alembic_config = Config(ALEMBIC_CONFIG_PATH)
    alembic_config.set_main_option("sqlalchemy.url", TEST_DATABASE_URL)
    upgrade(alembic_config, "head")


def drop_test_database():
    alembic_config = Config(ALEMBIC_CONFIG_PATH)
    alembic_config.set_main_option("sqlalchemy.url", TEST_DATABASE_URL)
    downgrade(alembic_config, "base")


@pytest.fixture(scope="session", autouse=True)
def prepare_database():
    create_test_database()
    yield
    drop_test_database()


@pytest.fixture(scope="session")
def db() -> Session:
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture(scope="session")
def override_get_db(db: Session):
    def _get_db():
        try:
            yield db
        finally:
            pass

    app.dependency_overrides[get_db] = _get_db


@pytest.fixture(scope="session")
def client(override_get_db):
    with TestClient(app) as client:
        yield client


@pytest.fixture(scope="session")
def librarian_token(db):
    user = User(email="librarian@test.com", hashed_password="fakehashed")
    db.add(user)
    db.commit()
    return create_access_token(data={"sub": user.email})
