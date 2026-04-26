from typing import Optional
from pydantic import BaseModel


class FinanceCreate(BaseModel):
    tour_id: int
    dept: str
    item: str
    rev: float = 0.0
    exp: float = 0.0
    date: str
    city: Optional[str] = None
    venue: Optional[str] = None


class FinanceOut(BaseModel):
    id: int
    tour_id: int
    dept: str
    item: str
    rev: float
    exp: float
    date: str
    city: Optional[str] = None
    venue: Optional[str] = None

    class Config:
        from_attributes = True