from datetime import datetime


def _sample_sale(user_id: int, customer_id: int | None = None):
    return {
        "sale_date": datetime.now().isoformat(),
        "sub_total": 100.00,
        "tax_amount": 10.00,
        "discount": 0.00,
        "grand_total": 110.00,
        "user_id": user_id,
        "customer_id": customer_id,
        "items": [],
    }


def test_list_sales(client, auth_headers, admin_user):
    response = client.get("/sales/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_sale_not_found(client, auth_headers):
    response = client.get("/sales/999")
    assert response.status_code == 404


def test_create_sale_invalid_data(client, auth_headers):
    response = client.post("/sales/", json={"sale_date": datetime.now().isoformat()}, headers=auth_headers)
    assert response.status_code == 422


def test_update_sale_not_found(client, auth_headers):
    response = client.put("/sales/999", json=_sample_sale(1), headers=auth_headers)
    assert response.status_code == 404


def test_delete_sale_not_found(client, auth_headers):
    response = client.delete("/sales/999", headers=auth_headers)
    assert response.status_code == 404
