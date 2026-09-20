from app.schemas.user import sample_user, sample_admin
from app.models.user import User
from app.core.security import hash_password, decode_access_token


def test_root(client):
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()


def test_health(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_list_users_empty(client):
    response = client.get("/users/")
    assert response.status_code == 200
    assert response.json() == []


def test_list_users_with_user(client, admin_user):
    response = client.get("/users/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 1


def test_get_user_by_id(client, auth_headers):
    create_resp = client.post("/users/", json=sample_user(), headers=auth_headers)
    user_id = create_resp.json()["id"]
    response = client.get(f"/users/{user_id}", headers=auth_headers)
    assert response.status_code == 200
    assert response.json()["id"] == user_id


def test_get_user_not_found(client, auth_headers):
    response = client.get("/users/999", headers=auth_headers)
    assert response.status_code == 404


def test_create_user_requires_auth(client):
    response = client.post("/users/", json=sample_user())
    assert response.status_code == 401


def test_create_user_success(client, auth_headers):
    user_data = sample_admin()
    user_data["username"] = "newadmin"
    response = client.post("/users/", json=user_data, headers=auth_headers)
    assert response.status_code == 201
    data = response.json()
    assert data["username"] == "newadmin"
    assert data["role"] == "admin"
    assert "id" in data


def test_create_user_returns_all_fields(client, auth_headers):
    user_data = sample_user()
    response = client.post("/users/", json=user_data, headers=auth_headers)
    assert response.status_code == 201
    data = response.json()
    assert "username" in data
    assert "first_name" in data
    assert "last_name" in data
    assert "role" in data
    assert "is_active" in data


def test_create_user_cashier_forbidden(client, cashier_headers):
    response = client.post("/users/", json=sample_user(), headers=cashier_headers)
    assert response.status_code == 403


def test_create_user_duplicate(client, auth_headers):
    user_data = sample_admin()
    user_data["username"] = "dupadmin"
    client.post("/users/", json=user_data, headers=auth_headers)
    response = client.post("/users/", json=user_data, headers=auth_headers)
    assert response.status_code == 400


def test_login_success(client, admin_user):
    login_data = {"username": "testadmin", "password": "AdminPass123!"}
    response = client.post("/users/login", json=login_data)
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_login_wrong_password(client, admin_user):
    response = client.post(
        "/users/login",
        json={"username": "testadmin", "password": "wrong"},
    )
    assert response.status_code == 401


def test_login_user_not_found(client):
    response = client.post(
        "/users/login",
        json={"username": "nobody", "password": "pass"},
    )
    assert response.status_code == 401


def test_login_inactive_user(client, db):
    user = User(
        username="inactiveuser",
        first_name="Inactive",
        last_name="User",
        role="admin",
        is_active=False,
        password=hash_password("Inactive123!"),
    )
    db.add(user)
    db.commit()
    response = client.post(
        "/users/login",
        json={"username": "inactiveuser", "password": "Inactive123!"},
    )
    assert response.status_code == 401


def test_login_missing_username(client):
    response = client.post("/users/login", json={"password": "pass"})
    assert response.status_code == 422


def test_login_missing_password(client):
    response = client.post("/users/login", json={"username": "test"})
    assert response.status_code == 422


def test_update_user(client, auth_headers):
    create_resp = client.post("/users/", json=sample_user(), headers=auth_headers)
    user_id = create_resp.json()["id"]
    update_data = {
        "username": "updateduser",
        "first_name": "Updated",
        "last_name": "User",
        "role": "cashier",
        "is_active": True,
        "password": "NewPassword123!",
    }
    response = client.put(f"/users/{user_id}", json=update_data, headers=auth_headers)
    assert response.status_code == 200
    assert response.json()["username"] == "updateduser"


def test_update_user_not_found(client, auth_headers):
    response = client.put("/users/999", json=sample_user(), headers=auth_headers)
    assert response.status_code == 404


def test_delete_user(client, auth_headers):
    create_resp = client.post("/users/", json=sample_user(), headers=auth_headers)
    user_id = create_resp.json()["id"]
    response = client.delete(f"/users/{user_id}", headers=auth_headers)
    assert response.status_code == 204
    get_resp = client.get(f"/users/{user_id}", headers=auth_headers)
    assert get_resp.status_code == 404


def test_delete_user_not_found(client, auth_headers):
    response = client.delete("/users/999", headers=auth_headers)
    assert response.status_code == 404


def test_create_user_role_stored(client, auth_headers):
    user_data = sample_user()
    user_data["role"] = "cashier"
    user_data["username"] = "rolestored"
    response = client.post("/users/", json=user_data, headers=auth_headers)
    assert response.status_code == 201
    assert response.json()["role"] == "cashier"


def test_login_empty_credentials(client):
    response = client.post("/users/login", json={})
    assert response.status_code == 422


def test_create_user_missing_fields(client, auth_headers):
    response = client.post("/users/", json={"username": "t"}, headers=auth_headers)
    assert response.status_code == 422


def test_token_contains_user_id_and_role(client, admin_user):
    resp = client.post("/users/login", json={"username": "testadmin", "password": "AdminPass123!"})
    token = resp.json()["access_token"]
    payload = decode_access_token(token)
    assert payload["sub"] == str(admin_user.id)
    assert payload["role"] == "admin"


def test_login_twice_returns_valid_tokens(client, admin_user):
    resp1 = client.post("/users/login", json={"username": "testadmin", "password": "AdminPass123!"})
    token1 = resp1.json()["access_token"]
    resp2 = client.post("/users/login", json={"username": "testadmin", "password": "AdminPass123!"})
    token2 = resp2.json()["access_token"]
    assert token1 is not None
    assert token2 is not None
    assert resp1.status_code == 200
    assert resp2.status_code == 200


def test_create_user_returns_no_password(client, auth_headers):
    user_data = sample_user()
    user_data["username"] = "nopassuser"
    response = client.post("/users/", json=user_data, headers=auth_headers)
    assert response.status_code == 201
    assert "password" not in response.json()


def test_create_user_with_long_username(client, auth_headers):
    user_data = sample_user()
    user_data["username"] = "x" * 200
    response = client.post("/users/", json=user_data, headers=auth_headers)
    assert response.status_code == 201
    assert response.json()["username"] == "x" * 200


def test_get_nonexistent_user_returns_404(client, auth_headers):
    response = client.get("/users/99999", headers=auth_headers)
    assert response.status_code == 404
