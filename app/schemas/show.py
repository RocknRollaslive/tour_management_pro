from pydantic import BaseModel, Field


class ShowCreate(BaseModel):
    tour_id: int
    date: str = Field(..., description="ISO date string, e.g. 2026-08-10")
    city: str = Field(..., min_length=1)
    venue: str = Field(..., min_length=1)
    country: str | None = None


class ShowOut(BaseModel):
    id: int
    tour_id: int
    date: str
    city: str
    venue: str
    country: str | None = None

    model_config = {"from_attributes": True}
