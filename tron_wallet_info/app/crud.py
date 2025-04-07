from sqlalchemy.orm import Session
from . import models, schemas

def create_wallet_request(db: Session, address: str):
    db_wallet_request = models.WalletRequest(address=address)
    db.add(db_wallet_request)
    db.commit()
    db.refresh(db_wallet_request)
    return db_wallet_request

def get_wallet_requests(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.WalletRequest).offset(skip).limit(limit).all()