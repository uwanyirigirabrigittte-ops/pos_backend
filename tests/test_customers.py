from app.schemas.customer import CustomerCreate, CustomerUpdate


def _sample():
    return {
        "first_name": "Jane",
        "last_name": "Doe",
        "phone": "555-5678",
        "loyalty_points": 50,
    }


def test_list_customers_empty(client):
    response = client.get("/customers/")
    assert response.status_code == 200
    assert response.json() == []


def test_list_customers(client, auth_headers):
    client.post("/customers/", json=_sample(), headers=auth_headers)
    response = client.get("/customers/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_customer_not_found(client, auth_headers):
    response = client.get("/customers/999")
    assert response.status_code == 404


def test_create_customer(client, auth_headers):
    response = client.post("/customers/", json=_sample(), headers=auth_headers)
    assert response.status_code == 201
    data = response.json()
    assert data["first_name"] == "Jane"
    assert data["loyalty_points"] == 50
    assert "id" in data


def test_create_customer_default_loyalty_points(client, auth_headers):
    data = _sample()
    del data["loyalty_points"]
    response = client.post("/customers/", json=data, headers=auth_headers)
    assert response.status_code == 201
    assert response.json()["loyalty_points"] == 0


def test_create_customer_invalid_data(client, auth_headers):
    response = client.post("/customers/", json={}, headers=auth_headers)
    assert response.status_code == 422


def test_get_customer_by_id(client, auth_headers):
    create_resp = client.post("/customers/", json=_sample(), headers=auth_headers)
    cust_id = create_resp.json()["id"]
    response = client.get(f"/customers/{cust_id}")
    assert response.status_code == 200
    assert response.json()["id"] == cust_id


def test_update_customer(client, auth_headers):
    create_resp = client.post("/customers/", json=_sample(), headers=auth_headers)
    cust_id = create_resp.json()["id"]
    update_data = {**{"first_name": "Updated", "last_name": "Smith"}, "id": cust_id}
    response = client.put(f"/customers/{cust_id}", json=update_data, headers=auth_headers)
    assert response.status_code == 200
    assert response.json()["first_name"] == "Updated"


def test_update_customer_not_found(client, auth_headers):
    response = client.put("/customers/999", json=_sample(), headers=auth_headers)
    assert response.status_code == 404


def test_delete_customer(client, auth_headers):
    create_resp = client.post("/customers/", json=_sample(), headers=auth_headers)
    cust_id = create_resp.json()["id"]
    response = client.delete(f"/customers/{cust_id}", headers=auth_headers)
    assert response.status_code == 204
    get_resp = client.get(f"/customers/{cust_id}")
    assert get_resp.status_code == 404


def test_delete_customer_not_found(client, auth_headers):
    response = client.delete("/customers/999", headers=auth_headers)
    assert response.status_code == 404
