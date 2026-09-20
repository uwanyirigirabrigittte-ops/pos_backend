def _sample():
    return {"name": "Test Category", "description": "A test category"}


def test_list_categories_empty(client):
    response = client.get("/categories/")
    assert response.status_code == 200
    assert response.json() == []


def test_list_categories(client, auth_headers):
    client.post("/categories/", json=_sample(), headers=auth_headers)
    response = client.get("/categories/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_category_not_found(client, auth_headers):
    response = client.get("/categories/999")
    assert response.status_code == 404


def test_create_category(client, auth_headers):
    response = client.post("/categories/", json=_sample(), headers=auth_headers)
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Test Category"
    assert "id" in data


def test_create_category_returns_all_fields(client, auth_headers):
    response = client.post("/categories/", json=_sample(), headers=auth_headers)
    assert response.status_code == 201
    data = response.json()
    assert "name" in data
    assert "description" in data
    assert "id" in data


def test_create_category_invalid_data(client, auth_headers):
    response = client.post("/categories/", json={}, headers=auth_headers)
    assert response.status_code == 422


def test_get_category_by_id(client, auth_headers):
    create_resp = client.post("/categories/", json=_sample(), headers=auth_headers)
    cat_id = create_resp.json()["id"]
    response = client.get(f"/categories/{cat_id}")
    assert response.status_code == 200
    assert response.json()["id"] == cat_id


def test_update_category(client, auth_headers):
    create_resp = client.post("/categories/", json=_sample(), headers=auth_headers)
    cat_id = create_resp.json()["id"]
    update_data = {**{"name": "Updated", "description": "updated"}, "id": cat_id}
    response = client.put(f"/categories/{cat_id}", json=update_data, headers=auth_headers)
    assert response.status_code == 200
    assert response.json()["name"] == "Updated"


def test_update_category_not_found(client, auth_headers):
    response = client.put("/categories/999", json=_sample(), headers=auth_headers)
    assert response.status_code == 404


def test_delete_category(client, auth_headers):
    create_resp = client.post("/categories/", json=_sample(), headers=auth_headers)
    cat_id = create_resp.json()["id"]
    response = client.delete(f"/categories/{cat_id}", headers=auth_headers)
    assert response.status_code == 204
    get_resp = client.get(f"/categories/{cat_id}")
    assert get_resp.status_code == 404


def test_delete_category_not_found(client, auth_headers):
    response = client.delete("/categories/999", headers=auth_headers)
    assert response.status_code == 404
