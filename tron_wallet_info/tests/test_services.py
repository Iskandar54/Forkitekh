import pytest
from unittest.mock import MagicMock
from app.services import get_tron_wallet_info
from tronpy.exceptions import AddressNotFound

def test_get_tron_wallet_info_success(monkeypatch):
    mock_tron_client = MagicMock()
    mock_tron_client.is_address.return_value = True
    mock_tron_client.to_base58check_address.return_value = "TVdyt1s88BdiCjKt6a2ZXGtR9G6jM9PZSo"
    mock_tron_client.get_account_balance.return_value = 150_000_000  # 150 TRX в SUN
    mock_tron_client.get_account.return_value = {
        "free_net_limit": 5000,
        "energy_limit": 2000
    }
    
    monkeypatch.setattr("app.services.client", mock_tron_client)
    
    result = get_tron_wallet_info("TVdyt1s88BdiCjKt6a2ZXGtR9G6jM9PZSo")
    
    assert result["balance"] == 150.0

def test_get_tron_wallet_info_invalid_address(monkeypatch):
    mock_client = MagicMock()
    mock_client.is_address.return_value = False
    
    monkeypatch.setattr("app.services.client", mock_client)
    
    with pytest.raises(ValueError, match="Invalid Tron address"):
        get_tron_wallet_info("invalid_address")