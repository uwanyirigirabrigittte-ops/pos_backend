from datetime import datetime


def test_list_receipts(client, auth_headers):
    response = client.get("/receipts/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_receipt_not_found(client, auth_headers):
    response = client.get("/receipts/999")
    assert response.status_code == 404


def test_create_receipt_invalid_data(client, auth_headers):
    response = client.post("/receipts/", json={}, headers=auth_headers)
    assert response.status_code == 422


def test_update_receipt_not_found(client, auth_headers):
    response = client.put("/receipts/999", json={"receipt_no": "REC001", "sale_id": 1, "issue_date": datetime.now().isoformat()}, headers=auth_headers)
    assert response.status_code == 404


def test_delete_receipt_not_found(client, auth_headers):
    response = client.delete("/receipts/999", headers=auth_headers)
    assert response.status_code == 404
