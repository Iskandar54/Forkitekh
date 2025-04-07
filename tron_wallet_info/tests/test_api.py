from fastapi.testclient import TestClient
from app.main import app
from app.database import SessionLocal, engine
from app import models

client = TestClient(app)

def setup_module(module):
    models.Base.metadata.create_all(bind=engine)

def teardown_module(module):
    models.Base.metadata.drop_all(bind=engine)

def test_get_wallet_info():
    test_address = "TLa2f6VPqDgRE67v1736s7bJ8Ray5wYjU7"  # Binance Cold Wallet
    response = client.post(
        "/wallet-info/",
        json={"address": test_address},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["address"] == test_address
    assert isinstance(data["balance"], float)
    assert isinstance(data["bandwidth"], int)
    assert isinstance(data["energy"], int)
    assert isinstance(data["request_id"], int)

def test_get_wallet_requests():
    test_addresses = ["TXsmKpEuW7qWnXzJLGP9eDLvWq4W8b3QHf", "TNPeeaaFB7K9cmo4uQpcU32zGK8G1NYqeL"]
    for addr in test_addresses:
        client.post("/wallet-info/", json={"address": addr})

    response = client.get("/wallet-requests/", params={"skip": 0, "limit": 2})
    assert response.status_code == 200
    data = response.json()
    
    assert isinstance(data, list)
    for item in data:
        assert "id" in item
        assert "address" in item
        assert "created_at" in item