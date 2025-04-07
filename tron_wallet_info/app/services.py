from tronpy import Tron
from tronpy.providers import HTTPProvider
from tronpy.exceptions import AddressNotFound
import httpx

provider = HTTPProvider("https://api.trongrid.io")
client = Tron(provider)

client.api_key = "42d8b2be-97d6-4155-a745-081fefab5f6a"  # Замените на ваш ключ

async def get_tron_wallet_info(address: str) -> dict:
    try:
        if not client.is_address(address):
            raise ValueError("Invalid Tron address")
        
        addr = client.to_base58check_address(address)
        
        balance = client.get_account_balance(addr) / 1_000_000
        
        account = client.get_account(addr)
        if not account:
            raise AddressNotFound("Account not found")
        bandwidth = account.get("free_net_limit", 0)
        energy = account.get("energy_limit", 0)
        
        return {
            "balance": balance,
            "bandwidth": bandwidth,
            "energy": energy
        }
    except Exception as e:
        raise ValueError(f"Error getting wallet info: {str(e)}")
