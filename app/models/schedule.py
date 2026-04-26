from sqlalchemy import Column, Integer, String, ForeignKey
from app.core.db import Base

class ScheduleItem(Base):
    __tablename__ = "schedules"

    id = Column(Integer, primary_key=True, index=True)
    show_id = Column(Integer, ForeignKey("shows.id"))
    time = Column(String)  # e.g., "10:00 AM"
    event = Column(String) # e.g., "Production Load-in"
    notes = Column(String, nullable=True)