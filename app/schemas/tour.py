from typing import Optional
from pydantic import BaseModel


class TourCreate(BaseModel):
    name: str
    band_name: str
    logo_path: Optional[str] = None


class TourOut(BaseModel):
    id: int
    name: str
    band_name: str
    logo_path: Optional[str] = None

    class Config:
        from_attributes = True