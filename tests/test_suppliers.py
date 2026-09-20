from fastapi.testclient import TestClient


def _sample():
    return {
        "company_name": "Test Supplier Co",
        "contact_name": "John Doe",
        "phone": "555-1234",
        "email": "john@test.com",
    }


def test_list_suppliers(client, auth_headers):
    response = client.get("/suppliers/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_supplier_not_found(client, auth_headers):
    response = client.get("/suppliers/999")
    assert response.status_code == 404


def test_create_supplier(client, auth_headers):
    response = client.post("/suppliers/", json=_sample(), headers=auth_headers)
    assert response.status_code == 201
    data = response.json()
    assert data["company_name"] == "Test Supplier Co"
    assert "id" in data


def test_create_supplier_invalid(client, auth_headers):
    response = client.post("/suppliers/", json={}, headers=auth_headers)
    assert response.status_code == 422


def test_get_supplier_by_id(client, auth_headers):
    create_resp = client.post("/suppliers/", json=_sample(), headers=auth_headers)
    sup_id = create_resp.json()["id"]
    response = client.get(f"/suppliers/{sup_id}")
    assert response.status_code == 200
    assert response.json()["id"] == sup_id


def test_update_supplier(client, auth_headers):
    create_resp = client.post("/suppliers/", json=_sample(), headers=auth_headers)
    sup_id = create_resp.json()["id"]
    update_data = _sample()
    update_data["company_name"] = "Updated Supplier"
    response = client.put(f"/suppliers/{sup_id}", json=update_data, headers=auth_headers)
    assert response.status_code == 200
    assert response.json()["company_name"] == "Updated Supplier"


def test_update_supplier_not_found(client, auth_headers):
    response = client.put("/suppliers/999", json=_sample(), headers=auth_headers)
    assert response.status_code == 404


def test_delete_supplier(client, auth_headers):
    create_resp = client.post("/suppliers/", json=_sample(), headers=auth_headers)
    sup_id = create_resp.json()["id"]
    response = client.delete(f"/suppliers/{sup_id}", headers=auth_headers)
    assert response.status_code == 204
    get_resp = client.get(f"/suppliers/{sup_id}")
    assert get_resp.status_code == 404


def test_delete_supplier_not_found(client, auth_headers):
    response = client.delete("/suppliers/999", headers=auth_headers)
    assert response.status_code == 404
