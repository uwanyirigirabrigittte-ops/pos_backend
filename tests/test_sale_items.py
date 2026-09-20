def _sample():
    return {
        "product_id": 1,
        "quantity": 2,
        "unit_price": 10.00,
    }


def _sample_update():
    return {
        "sale_id": 1,
        "product_id": 1,
        "quantity": 2,
        "unit_price": 10.00,
        "line_total": 20.00,
    }


def test_list_sale_items_empty(client, auth_headers):
    response = client.get("/sale-items/")
    assert response.status_code == 200
    assert response.json() == []


def test_list_sale_items(client, auth_headers):
    response = client.get("/sale-items/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_sale_item_not_found(client, auth_headers):
    response = client.get("/sale-items/999")
    assert response.status_code == 404


def test_create_sale_item_invalid_data(client, auth_headers):
    response = client.post("/sale-items/", json={}, headers=auth_headers)
    assert response.status_code == 422


def test_update_sale_item_not_found(client, auth_headers):
    response = client.put("/sale-items/999", json=_sample_update(), headers=auth_headers)
    assert response.status_code == 404


def test_delete_sale_item_not_found(client, auth_headers):
    response = client.delete("/sale-items/999", headers=auth_headers)
    assert response.status_code == 404
