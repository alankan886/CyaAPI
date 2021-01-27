import os

import pytest
from dotenv import load_dotenv
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app import app

load_dotenv('.env')
SQLALCHEMY_DATABASE_URL = os.environ.get('TEST_DB')

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)


@pytest.fixture(scope="module")
def test_client():
    client = TestClient(app)
    yield client


@pytest.fixture(scope="module")
def get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()