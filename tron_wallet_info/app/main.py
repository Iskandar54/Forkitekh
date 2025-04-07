from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List, Optional
from . import models, schemas, services, crud
from .database import SessionLocal, engine

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
async def read_root():
    return {"message": "Tron Wallet Info Service"}

@app.post("/wallet-info/", response_model=schemas.WalletInfoResponse)
async def get_wallet_info(wallet: schemas.WalletRequest, db: Session = Depends(get_db)):
    try:
        wallet_info = await services.get_tron_wallet_info(wallet.address)
        
        db_wallet_request = crud.create_wallet_request(db, wallet.address)
        
        return {
            "address": wallet.address,
            "balance": wallet_info["balance"],
            "bandwidth": wallet_info["bandwidth"],
            "energy": wallet_info["energy"],
            "request_id": db_wallet_request.id
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/wallet-requests/", response_model=List[schemas.WalletRequestDB])
async def get_wallet_requests(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    db_requests = crud.get_wallet_requests(db, skip=skip, limit=limit)
    return [schemas.WalletRequestDB.from_orm(request) for request in db_requests]
