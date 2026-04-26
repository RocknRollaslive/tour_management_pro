from sqlalchemy import Column, Integer, String
from app.core.db import Base


class Tour(Base):
    __tablename__ = "tours"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    band_name = Column(String, nullable=False)
    logo_path = Column(String, nullable=True)