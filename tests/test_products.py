from app.schemas.product import sample_product


def test_list_products(client, auth_headers):
    response = client.get("/products/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_product_not_found(client, auth_headers):
    response = client.get("/products/999")
    assert response.status_code == 404


def test_create_product(client, auth_headers):
    product_data = sample_product()
    response = client.post("/products/", json=product_data, headers=auth_headers)
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == product_data["name"]
    assert data["barcode"] == product_data["barcode"]
    assert "id" in data


def test_create_product_invalid_data(client, auth_headers):
    response = client.post(
        "/products/", json={"name": "incomplete"}, headers=auth_headers
    )
    assert response.status_code == 422


def test_get_product_by_id(client, auth_headers):
    product_data = sample_product()
    create_resp = client.post("/products/", json=product_data, headers=auth_headers)
    product_id = create_resp.json()["id"]

    response = client.get(f"/products/{product_id}")
    assert response.status_code == 200
    assert response.json()["id"] == product_id


def test_update_product(client, auth_headers):
    product_data = sample_product()
    create_resp = client.post("/products/", json=product_data, headers=auth_headers)
    product_id = create_resp.json()["id"]

    update_data = {**product_data, "id": product_id, "name": "Updated Product"}
    response = client.put(f"/products/{product_id}", json=update_data, headers=auth_headers)
    assert response.status_code == 200
    assert response.json()["name"] == "Updated Product"


def test_update_product_not_found(client, auth_headers):
    product_data = sample_product()
    update_data = {**product_data, "id": 999}
    response = client.put("/products/999", json=update_data, headers=auth_headers)
    assert response.status_code == 404


def test_delete_product(client, auth_headers):
    product_data = sample_product()
    create_resp = client.post("/products/", json=product_data, headers=auth_headers)
    product_id = create_resp.json()["id"]

    response = client.delete(f"/products/{product_id}", headers=auth_headers)
    assert response.status_code == 204

    get_resp = client.get(f"/products/{product_id}")
    assert get_resp.status_code == 404


def test_delete_product_not_found(client, auth_headers):
    response = client.delete("/products/999", headers=auth_headers)
    assert response.status_code == 404
