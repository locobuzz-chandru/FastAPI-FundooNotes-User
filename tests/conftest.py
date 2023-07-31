import json

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from core.database import Base, get_db
from main import api

engine = create_engine("postgresql://postgres:99999@localhost:5432/fastapifundoouser1")
session_local = sessionmaker(bind=engine, autoflush=False, autocommit=False)
Base.metadata.create_all(bind=engine)


@pytest.fixture
def override_get_db():
    Base.metadata.create_all(bind=engine)
    db = session_local()
    try:
        yield db
    finally:
        Base.metadata.drop_all(bind=engine)
        db.close()


@pytest.fixture
def client(override_get_db):
    def override_db():
        try:
            yield override_get_db
        finally:
            override_get_db.close()

    api.dependency_overrides[get_db] = override_db
    yield TestClient(api)


@pytest.fixture
def user_data():
    return {"username": "user", "password": "user", "first_name": "a", "last_name": "b", "email": "a@gmail.com",
            "is_verified": False}


@pytest.fixture
def user_data_error():
    return {"username": "user", "password": "user", "first_namec": "a", "last_name": "b", "email": "a@gmail.com",
            "is_verified": False}
