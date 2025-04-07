from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List

class WalletRequest(BaseModel):
    address: str

class WalletInfoResponse(BaseModel):
    address: str
    balance: float
    bandwidth: int
    energy: int
    request_id: int

class WalletRequestDB(BaseModel):
    id: int
    address: str
    created_at: datetime

    class Config:
        orm_mode = True  

class WalletInfo(BaseModel):
    address: str
    balance: float
    bandwidth: int
    energy: int
    request_id: int

    class Config:
        orm_mode = True