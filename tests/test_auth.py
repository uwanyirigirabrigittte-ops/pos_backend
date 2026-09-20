from app.schemas.user import sample_admin, sample_user


def test_full_auth_flow(client, admin_user):
    login_resp = client.post(
        "/users/login",
        json={"username": "testadmin", "password": "AdminPass123!"},
    )
    assert login_resp.status_code == 200
    token = login_resp.json()["access_token"]

    headers = {"Authorization": f"Bearer {token}"}

    list_resp = client.get("/users/", headers=headers)
    assert list_resp.status_code == 200

    create_resp = client.post("/users/", json=sample_user(), headers=headers)
    assert create_resp.status_code == 201

    get_resp = client.get(f"/users/{create_resp.json()['id']}", headers=headers)
    assert get_resp.status_code == 200
    assert get_resp.json()["username"] == "testuser"


def test_cashier_cannot_access_admin_features(client, cashier_headers):
    response = client.post("/users/", json=sample_admin(), headers=cashier_headers)
    assert response.status_code == 403


def test_token_stored_correctly(client, admin_user):
    login_resp = client.post(
        "/users/login",
        json={"username": "testadmin", "password": "AdminPass123!"},
    )
    token = login_resp.json()["access_token"]
    assert token.startswith("ey")


def test_protected_endpoint_with_expired_token(client, admin_user):
    from app.core.security import create_access_token
    import datetime

    expired_expiry = datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(hours=1)
    token = create_access_token({"sub": "1", "role": "admin"}, expire=expired_expiry)

    response = client.post(
        "/users/",
        json={"username": "expiredtest", "first_name": "E", "last_name": "User", "role": "cashier", "is_active": True, "password": "Pass123!"},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 401


def test_login_then_access_protected_routes(client, admin_user):
    login_resp = client.post(
        "/users/login",
        json={"username": "testadmin", "password": "AdminPass123!"},
    )
    assert login_resp.status_code == 200

    token = login_resp.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    products_resp = client.get("/products/", headers=headers)
    assert products_resp.status_code == 200

    categories_resp = client.get("/categories/", headers=headers)
    assert categories_resp.status_code == 200


def test_create_and_delete_user_flow(client, auth_headers):
    user_data = sample_user()
    user_data["username"] = "flowuser"
    create_resp = client.post("/users/", json=user_data, headers=auth_headers)
    assert create_resp.status_code == 201
    user_id = create_resp.json()["id"]

    delete_resp = client.delete(f"/users/{user_id}", headers=auth_headers)
    assert delete_resp.status_code == 204

    get_resp = client.get(f"/users/{user_id}", headers=auth_headers)
    assert get_resp.status_code == 404


def test_full_product_crud_flow(client, auth_headers):
    product_data = {
        "barcode": "FLOW123",
        "name": "Flow Product",
        "cost_price": 5.00,
        "retail_price": 10.00,
        "quantity": 20,
        "category_id": 1,
        "supplier_id": 1,
        "image_url": None,
    }

    create_resp = client.post("/products/", json=product_data, headers=auth_headers)
    assert create_resp.status_code == 201
    product_id = create_resp.json()["id"]

    get_resp = client.get(f"/products/{product_id}", headers=auth_headers)
    assert get_resp.status_code == 200
    assert get_resp.json()["name"] == "Flow Product"

    update_data = {**product_data, "id": product_id, "name": "Flow Updated"}
    update_resp = client.put(f"/products/{product_id}", json=update_data, headers=auth_headers)
    assert update_resp.status_code == 200
    assert update_resp.json()["name"] == "Flow Updated"

    delete_resp = client.delete(f"/products/{product_id}", headers=auth_headers)
    assert delete_resp.status_code == 204


def test_multiple_roles_login(client, admin_user, cashier_user):
    admin_resp = client.post("/users/login", json={"username": "testadmin", "password": "AdminPass123!"})
    assert admin_resp.status_code == 200
    assert admin_resp.json()["token_type"] == "bearer"

    cashier_resp = client.post("/users/login", json={"username": "testcashier", "password": "CashierPass123!"})
    assert cashier_resp.status_code == 200
    assert cashier_resp.json()["token_type"] == "bearer"


def test_create_same_username_twice_fails(client, auth_headers):
    user_data = sample_user()
    user_data["username"] = "uniqueuser"
    first_resp = client.post("/users/", json=user_data, headers=auth_headers)
    assert first_resp.status_code == 201

    second_resp = client.post("/users/", json=user_data, headers=auth_headers)
    assert second_resp.status_code == 400
