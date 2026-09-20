def _sample():
    return {"sale_id": 1, "method": "cash", "amount_paid": 100.00}


def test_list_payments_empty(client, auth_headers):
    response = client.get("/payments/")
    assert response.status_code == 200
    assert response.json() == []


def test_list_payments(client, auth_headers):
    response = client.get("/payments/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_payment_not_found(client, auth_headers):
    response = client.get("/payments/999")
    assert response.status_code == 404


def test_create_payment_invalid_data(client, auth_headers):
    response = client.post("/payments/", json={}, headers=auth_headers)
    assert response.status_code == 422


def test_update_payment_not_found(client, auth_headers):
    response = client.put("/payments/999", json=_sample(), headers=auth_headers)
    assert response.status_code == 404


def test_delete_payment_not_found(client, auth_headers):
    response = client.delete("/payments/999", headers=auth_headers)
    assert response.status_code == 404
