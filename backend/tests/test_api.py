from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_root():
    response = client.get("/")
    assert response.status_code == 200


def test_register():
    response = client.post(
        "/auth/register",
        json={
            "name": "Test User",
            "email": "testuser@example.com",
            "password": "password123",
        },
    )

    assert response.status_code in [201, 400]


def test_login():
    response = client.post(
        "/auth/login",
        data={
            "username": "testuser@example.com",
            "password": "password123",
        },
    )

    assert response.status_code == 200
    assert "access_token" in response.json()


def test_products():
    response = client.get("/products/")
    assert response.status_code == 200


def test_product_search():
    response = client.get("/products/?search=Java")
    assert response.status_code == 200


def test_cart_without_token():
    response = client.get("/cart/")
    assert response.status_code == 401


def test_orders_without_token():
    response = client.get("/orders/")
    assert response.status_code == 401


def test_admin_without_token():
    response = client.get("/orders/admin/stats")
    assert response.status_code == 401