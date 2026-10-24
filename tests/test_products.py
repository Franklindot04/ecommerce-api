def test_list_products_returns_paginated_result(client):
    response = client.get("/products")

    assert response.status_code == 200
    data = response.json()
    assert isinstance(data["items"], list)
    assert data["page"] == 1
    assert data["page_size"] == 20
    assert data["total"] >= 2
    assert data["total_pages"] == 1
    assert len(data["items"]) >= 2


def test_get_single_product(client):
    response = client.get("/products/1")

    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 1
    assert data["name"] == "Keyboard"
