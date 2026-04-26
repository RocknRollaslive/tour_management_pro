from sqlalchemy.orm import Session

from app.models.tour import Tour
from app.schemas.tour import TourCreate


def create_tour(db: Session, tour_data: TourCreate) -> Tour:
    tour = Tour(**tour_data.model_dump())
    db.add(tour)
    db.commit()
    db.refresh(tour)
    return tour


def get_all_tours(db: Session) -> list[Tour]:
    return db.query(Tour).order_by(Tour.id.desc()).all()
