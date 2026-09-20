from app.schemas.user import sample_user, sample_admin
from app.models.user import User
from app.core.security import hash_password


def test_root(client):
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()


def test_health(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_list_users(client, admin_user):
    response = client.get("/users/")
    assert response.status_code == 200


def test_get_user(client, auth_headers):
    user_data = sample_user()
    user_data["username"] = "getuser"
    create_resp = client.post("/users/", json=user_data, headers=auth_headers)
    assert create_resp.status_code == 201
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


def test_create_user_cashier_forbidden(client, cashier_headers):
    response = client.post("/users/", json=sample_user(), headers=cashier_headers)
    assert response.status_code == 403


def test_create_user_duplicate(client, auth_headers):
    user_data = sample_admin()
    user_data["username"] = "dupuser"
    client.post("/users/", json=user_data, headers=auth_headers)
    response = client.post("/users/", json=user_data, headers=auth_headers)
    assert response.status_code == 400


def test_login_success(client, admin_user):
    response = client.post(
        "/users/login",
        json={"username": "testadmin", "password": "AdminPass123!"},
    )
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


def test_update_user(client, auth_headers):
    user_data = sample_user()
    user_data["username"] = "updateme"
    create_resp = client.post("/users/", json=user_data, headers=auth_headers)
    assert create_resp.status_code == 201
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
    user_data = sample_user()
    user_data["username"] = "deleteuser"
    create_resp = client.post("/users/", json=user_data, headers=auth_headers)
    assert create_resp.status_code == 201
    user_id = create_resp.json()["id"]

    response = client.delete(f"/users/{user_id}", headers=auth_headers)
    assert response.status_code == 204

    get_resp = client.get(f"/users/{user_id}", headers=auth_headers)
    assert get_resp.status_code == 404


def test_delete_user_not_found(client, auth_headers):
    response = client.delete("/users/999", headers=auth_headers)
    assert response.status_code == 404