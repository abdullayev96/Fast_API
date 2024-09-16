from pydantic import BaseModel
from typing import Optional

class ItemCreate(BaseModel):
    name: str
    price: float

class ItemRead(BaseModel):
    id: int
    name: str
    price: float

    class Config:
        orm_mode = True