from app.core.security import (
    hash_password,
    verify_password,
    create_access_token,
    decode_access_token,
)


def test_hash_password():
    password = "testpassword"
    hashed = hash_password(password)
    assert isinstance(hashed, str)
    assert hashed != password


def test_verify_password_correct():
    password = "testpassword"
    hashed = hash_password(password)
    assert verify_password(password, hashed) is True


def test_verify_password_incorrect():
    hashed = hash_password("correctpassword")
    assert verify_password("wrongpassword", hashed) is False


def test_create_access_token():
    token = create_access_token({"sub": "1"})
    assert isinstance(token, str)
    parts = token.split(".")
    assert len(parts) == 3


def test_decode_access_token_valid():
    token = create_access_token({"sub": "1", "role": "admin"})
    payload = decode_access_token(token)
    assert payload["sub"] == "1"
    assert payload["role"] == "admin"


def test_decode_access_token_invalid():
    from fastapi import HTTPException, status

    try:
        decode_access_token("invalid.token.here")
        assert False, "Should have raised HTTPException"
    except HTTPException as e:
        assert e.status_code == status.HTTP_401_UNAUTHORIZED


def test_get_current_user_unauthorized(client):
    response = client.post("/users/", json={"username": "test", "password": "test", "first_name": "T", "last_name": "T", "role": "admin"})
    assert response.status_code == 401
