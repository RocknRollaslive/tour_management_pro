from sqlalchemy import Column, Integer, String, ForeignKey
from app.core.db import Base


class Show(Base):
    __tablename__ = "shows"

    id = Column(Integer, primary_key=True, index=True)
    tour_id = Column(Integer, ForeignKey("tours.id"))
    date = Column(String, nullable=False)
    city = Column(String, nullable=False)
    venue = Column(String, nullable=False)
    country = Column(String, nullable=True)
    notes = Column(String, nullable=True)
    type = Column(String, nullable=True)