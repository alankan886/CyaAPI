import os
from typing import Generator

import pytest
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient

from app.main import app
from app.db import Base, get_db


load_dotenv(".env")
SQLALCHEMY_DATABASE_URL = os.environ.get("TEST_DB_URI")

engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
session = TestingSessionLocal()


def override_get_db():
    try:
        db = session
        yield db
    finally:
        db.close()


@pytest.fixture()
def test_client():
    app.dependency_overrides[get_db] = override_get_db
    return TestClient(app)


@pytest.fixture()
def test_db():
    # drop before create, pytest has problems tearing down the database last in a fixture
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)


@pytest.fixture()
def test_session():
    return session
