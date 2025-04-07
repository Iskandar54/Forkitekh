from fastapi import APIRouter
from fastapi.testclient import TestClient
from app.main import app
from app.schemas import WalletInfo 

router = APIRouter()
client = TestClient(app)

@router.get("/wallet-requests/", response_model=list[WalletInfo])
def get_wallet_requests(skip: int = 0, limit: int = 100):
    test_data = [
        {"address": "addr1", "balance": 100.0, "bandwidth": 1000, "energy": 500},
        {"address": "addr2", "balance": 200.0, "bandwidth": 2000, "energy": 600},
        {"address": "addr3", "balance": 300.0, "bandwidth": 3000, "energy": 700}
    ]
    
    for item in test_data:
        client.post("/wallet-info/", json=item)

    # Тест пагинации
    response = client.get("/wallet-requests/", params={"skip": 0, "limit": 2})
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    
    # Проверка структуры данных
    for item in data:
        assert all(key in item for key in ["address", "balance", "bandwidth", "energy", "request_id"])
    
    # Проверка сортировки (если предполагается по request_id)
    assert data[0]["request_id"] < data[1]["request_id"]
    
    # Проверка второй страницы
    response = client.get("/wallet-requests/", params={"skip": 2, "limit": 1})
    assert len(response.json()) == 1