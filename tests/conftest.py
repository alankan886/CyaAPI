import os
from typing import Optional, List

import pytest
from dotenv import load_dotenv
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy_utils import database_exists, create_database, drop_database
from app.db.db import Base, get_db

from app import app

load_dotenv('.env')
SQLALCHEMY_DATABASE_URL = os.environ.get('TEST_DB')

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)


def get_test_db():
    SessionLocal = sessionmaker(bind=engine)
    test_db = SessionLocal()

    try:
        yield test_db
    finally:
        test_db.close()


@pytest.fixture(scope="session", autouse=True)
def create_test_database():
    if database_exists(SQLALCHEMY_DATABASE_URL):
        drop_database(SQLALCHEMY_DATABASE_URL)
    create_database(SQLALCHEMY_DATABASE_URL)

    # Create the tables.
    Base.metadata.create_all(engine)
    app.dependency_overrides[get_db] = get_test_db
    yield
    drop_database(SQLALCHEMY_DATABASE_URL)


@pytest.fixture
def test_db_session():
    SessionLocal = sessionmaker(bind=engine)

    session = SessionLocal()
    yield session
    # Drop all data after each test
    for tbl in reversed(Base.metadata.sorted_tables):
        # Delete all rows in the table
        engine.execute(tbl.delete())

    # put back the connection to the connection pool
    session.close()


@pytest.fixture(scope="module")
def test_client():
    client = TestClient(app)
    yield client


def add_commit_refresh(test_db_session: Session, *args: Optional[List[object]]):
    for arg in args:
        test_db_session.add(arg)

    test_db_session.commit()

    for arg in args:
        test_db_session.refresh(arg)
