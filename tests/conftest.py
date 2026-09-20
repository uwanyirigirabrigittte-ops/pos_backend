import os

os.environ['DATABASE_URL'] = 'sqlite://'

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.database import Base, get_db, engine
from app.main import app
from app.models.user import User
from app.core.security import hash_password

TestingSessionLocal = sessionmaker(bind=engine)


def _create_user(db, username, password, role="admin", **kwargs):
    user = User(
        username=username,
        password=hash_password(password),
        role=role,
        is_active=True,
        **kwargs,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@pytest.fixture
def client():
    Base.metadata.create_all(bind=engine)

    def override_get_db():
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)

    app.dependency_overrides.clear()
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def db(client):
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture
def admin_user(client):
    db = TestingSessionLocal()
    try:
        return _create_user(
            db, "testadmin", "AdminPass123!", "admin",
            first_name="Test", last_name="Admin",
        )
    finally:
        db.close()


@pytest.fixture
def cashier_user(client):
    db = TestingSessionLocal()
    try:
        return _create_user(
            db, "testcashier", "CashierPass123!", "cashier",
            first_name="Test", last_name="Cashier",
        )
    finally:
        db.close()


@pytest.fixture
def admin_token(client, admin_user):
    response = client.post(
        "/users/login",
        json={"username": "testadmin", "password": "AdminPass123!"},
    )
    return response.json()["access_token"]


@pytest.fixture
def cashier_token(client, cashier_user):
    response = client.post(
        "/users/login",
        json={"username": "testcashier", "password": "CashierPass123!"},
    )
    return response.json()["access_token"]


@pytest.fixture
def auth_headers(admin_token):
    return {"Authorization": f"Bearer {admin_token}"}


@pytest.fixture
def cashier_headers(cashier_token):
    return {"Authorization": f"Bearer {cashier_token}"}
