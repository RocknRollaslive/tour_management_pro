from sqlalchemy import Column, Float, ForeignKey, Integer, String
from app.core.db import Base


class Finance(Base):
    __tablename__ = "finances"

    id = Column(Integer, primary_key=True, index=True)
    tour_id = Column(Integer, ForeignKey("tours.id"), nullable=False)
    dept = Column(String, nullable=False)
    item = Column(String, nullable=False)
    rev = Column(Float, default=0.0)
    exp = Column(Float, default=0.0)
    date = Column(String, nullable=False)
    city = Column(String, nullable=True)
    venue = Column(String, nullable=True)
