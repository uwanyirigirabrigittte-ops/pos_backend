import datetime
from fastapi import HTTPException, status
from app.core.security import (
    hash_password,
    verify_password,
    create_access_token,
    decode_access_token,
)


# Password hashing tests
def test_hash_password():
    password = "testpassword"
    hashed = hash_password(password)
    assert isinstance(hashed, str)
    assert hashed != password


def test_hash_password_different_hashes():
    hashed1 = hash_password("samepassword")
    hashed2 = hash_password("samepassword")
    assert hashed1 != hashed2


def test_verify_password_correct():
    password = "testpassword"
    hashed = hash_password(password)
    assert verify_password(password, hashed) is True


def test_verify_password_incorrect():
    hashed = hash_password("correctpassword")
    assert verify_password("wrongpassword", hashed) is False


def test_verify_password_empty_string():
    hashed = hash_password("")
    assert verify_password("", hashed) is True
    assert verify_password("nonempty", hashed) is False


# create_access_token tests
def test_create_access_token():
    token = create_access_token({"sub": "1"})
    assert isinstance(token, str)
    parts = token.split(".")
    assert len(parts) == 3


def test_create_access_token_with_role():
    token = create_access_token({"sub": "1", "role": "admin"})
    payload = decode_access_token(token)
    assert payload["sub"] == "1"
    assert payload["role"] == "admin"


def test_create_access_token_with_custom_expiry():
    custom_expiry = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(days=30)
    token = create_access_token({"sub": "1"}, expire=custom_expiry)
    payload = decode_access_token(token)
    assert payload["exp"] is not None


def test_create_access_token_exp_included():
    token = create_access_token({"sub": "1"})
    payload = decode_access_token(token)
    assert "exp" in payload


# decode_access_token tests
def test_decode_access_token_valid():
    token = create_access_token({"sub": "1", "role": "admin"})
    payload = decode_access_token(token)
    assert payload["sub"] == "1"
    assert payload["role"] == "admin"


def test_decode_access_token_invalid():
    try:
        decode_access_token("invalid.token.here")
        assert False, "Should have raised HTTPException"
    except HTTPException as e:
        assert e.status_code == status.HTTP_401_UNAUTHORIZED


def test_decode_access_token_expired():
    expired_expiry = datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(hours=1)
    token = create_access_token({"sub": "1"}, expire=expired_expiry)
    try:
        decode_access_token(token)
        assert False, "Should have raised HTTPException for expired token"
    except HTTPException:
        pass


def test_decode_access_token_missing_sub_key():
    token = create_access_token({"role": "admin"})
    payload = decode_access_token(token)
    assert "sub" not in payload


# get_current_user tests (POST /users/ is the protected endpoint)
def test_get_current_user_no_token(client):
    response = client.post("/users/", json={"username": "test", "first_name": "T", "last_name": "T", "role": "cashier", "is_active": True, "password": "Pass123!"})
    assert response.status_code == 401


def test_get_current_user_invalid_token(client):
    response = client.post(
        "/users/",
        json={"username": "test", "first_name": "T", "last_name": "T", "role": "cashier", "is_active": True, "password": "Pass123!"},
        headers={"Authorization": "Bearer invalid.token.value"},
    )
    assert response.status_code == 401


def test_get_current_user_missing_bearer_prefix(client):
    response = client.post(
        "/users/",
        json={"username": "test", "first_name": "T", "last_name": "T", "role": "cashier", "is_active": True, "password": "Pass123!"},
        headers={"Authorization": "invalid_token"},
    )
    assert response.status_code == 401


def test_get_current_user_valid_token(client, admin_user):
    login_resp = client.post(
        "/users/login",
        json={"username": "testadmin", "password": "AdminPass123!"},
    )
    token = login_resp.json()["access_token"]
    response = client.post(
        "/users/",
        json={"username": "protecteduser", "first_name": "P", "last_name": "User", "role": "cashier", "is_active": True, "password": "Pass123!"},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 201


# require_roles tests
def test_require_roles_admin_can_create_user(client, auth_headers):
    response = client.post("/users/", json={"username": "roleadmin", "first_name": "R", "last_name": "Admin", "role": "admin", "is_active": True, "password": "NewPass123!"}, headers=auth_headers)
    assert response.status_code == 201


def test_require_roles_cashier_cannot_create_user(client, cashier_headers):
    response = client.post("/users/", json={"username": "cashieruser", "first_name": "C", "last_name": "User", "role": "cashier", "is_active": True, "password": "Pass123!"}, headers=cashier_headers)
    assert response.status_code == 403


def test_require_roles_cashier_token_admin_endpoint(client, admin_user):
    login_resp = client.post("/users/login", json={"username": "testadmin", "password": "AdminPass123!"})
    admin_token = login_resp.json()["access_token"]
    assert login_resp.status_code == 200
    assert "access_token" in login_resp.json()


def test_jwt_token_format(client, admin_user):
    login_resp = client.post(
        "/users/login",
        json={"username": "testadmin", "password": "AdminPass123!"},
    )
    token = login_resp.json()["access_token"]
    parts = token.split(".")
    assert len(parts) == 3


def test_hash_password_with_special_chars():
    password = "P@ssw0rd!#$%"
    hashed = hash_password(password)
    assert verify_password(password, hashed) is True
    assert verify_password("wrong", hashed) is False
