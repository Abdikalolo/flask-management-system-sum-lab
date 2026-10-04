import pytest

from app import app


@pytest.fixture
def client():
    app.config["TESTING"] = True

    with app.test_client() as client:
        yield client

def test_get_inventory(client):
    response = client.get("/inventory")

    assert response.status_code == 200
    assert isinstance(response.get_json(), list)

def test_get_single_inventory_item(client):
    response = client.get("/inventory/1")

    assert response.status_code == 200
    assert response.get_json()["id"] == 1

def test_get_missing_inventory_item(client):
    response = client.get("/inventory/999")

    assert response.status_code == 404

def test_add_inventory_item(client):
    new_item = {
        "barcode": "123456789",
        "product_name": "Test Juice",
        "brands": "Test Brand",
        "ingredients_text": "Orange juice",
        "quantity": 10,
        "price": 200
    }

    response = client.post("/inventory", json=new_item)

    assert response.status_code == 201
    assert response.get_json()["product_name"] == "Test Juice"

def test_add_inventory_missing_field(client):
    new_item = {
        "product_name": "Test Juice"
    }

    response = client.post("/inventory", json=new_item)

    assert response.status_code == 400

def test_update_inventory_item(client):
    update_data = {
        "quantity": 20,
        "price": 250
    }

    response = client.patch("/inventory/1", json=update_data)

    assert response.status_code == 200
    assert response.get_json()["quantity"] == 20
    assert response.get_json()["price"] == 250

def test_delete_inventory_item(client):
    response = client.delete("/inventory/1")

    assert response.status_code == 200
    assert response.get_json()["message"] == "Item deleted successfully"

def test_delete_nonexistent_inventory_item(client):
    response = client.delete("/inventory/999")

    assert response.status_code == 404
    assert response.get_json()["error"] == "Item not found"

def test_delete_missing_inventory_item(client):
    response = client.delete("/inventory/999")

    assert response.status_code == 404

def test_openfoodfacts_barcode_search(client, monkeypatch):
    class FakeResponse:
        status_code = 200

        def raise_for_status(self):
            pass

        def json(self):
            return {
                "status": 1,
                "product": {
                    "code": "3017620422003",
                    "product_name": "Nutella",
                    "brands": "Ferrero",
                    "ingredients_text": "Sugar, hazelnuts, cocoa"
                }
            }

    def fake_get(*args, **kwargs):
        return FakeResponse()

    monkeypatch.setattr("app.requests.get", fake_get)

    response = client.get("/external-products/barcode/3017620422003")

    assert response.status_code == 200
    assert response.get_json()["product_name"] == "Nutella"


def test_openfoodfacts_product_not_found(client, monkeypatch):
    class FakeResponse:
        status_code = 200

        def raise_for_status(self):
            pass

        def json(self):
            return {
                "status": 0
            }

    def fake_get(*args, **kwargs):
        return FakeResponse()

    monkeypatch.setattr("app.requests.get", fake_get)

    response = client.get("/external-products/barcode/9999999999999")

    assert response.status_code == 404


def test_openfoodfacts_name_search(client, monkeypatch):
    class FakeResponse:
        status_code = 200

        def json(self):
            return {
                "products": [
                    {
                        "code": "3017620422003",
                        "product_name": "Nutella",
                        "brands": "Ferrero",
                        "ingredients_text": "Sugar, hazelnuts, cocoa"
                    }
                ]
            }

    def fake_get(*args, **kwargs):
        return FakeResponse()

    monkeypatch.setattr("app.requests.get", fake_get)

    response = client.get("/external-products/search?name=Nutella")

    print(response.get_json())

    assert response.status_code == 200
    assert response.get_json()["total"] == 1
    assert response.get_json()["products"][0]["product_name"] == "Nutella"

def test_openfoodfacts_name_search_failure(client, monkeypatch):
    class FakeResponse:
        status_code = 503

    def fake_get(*args, **kwargs):
        return FakeResponse()

    monkeypatch.setattr("app.requests.get", fake_get)

    response = client.get("/external-products/search?name=Nutella")

    assert response.status_code == 500


def test_import_openfoodfacts_product(client, monkeypatch):
    class FakeResponse:
        status_code = 200

        def raise_for_status(self):
            pass

        def json(self):
            return {
                "status": 1,
                "product": {
                    "code": "3017620422003",
                    "product_name": "Nutella",
                    "brands": "Ferrero",
                    "ingredients_text": "Sugar, hazelnuts, cocoa"
                }
            }

    def fake_get(*args, **kwargs):
        return FakeResponse()

    monkeypatch.setattr("app.requests.get", fake_get)

    response = client.post(
        "/inventory/import",
        json={
            "barcode": "3017620422003",
            "quantity": 10,
            "price": 500
        }
    )

    assert response.status_code == 201
    assert response.get_json()["product_name"] == "Nutella"
    assert response.get_json()["quantity"] == 10
    assert response.get_json()["price"] == 500