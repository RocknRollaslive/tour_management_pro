from sqlalchemy.orm import Session

from app.models.show import Show
from app.schemas.show import ShowCreate


def create_show(db: Session, show_data: ShowCreate) -> Show:
    show = Show(**show_data.model_dump())
    db.add(show)
    db.commit()
    db.refresh(show)
    return show


def get_shows_for_tour(db: Session, tour_id: int) -> list[Show]:
    return (
        db.query(Show)
        .filter(Show.tour_id == tour_id)
        .order_by(Show.date.asc(), Show.city.asc(), Show.venue.asc())
        .all()
    )


def get_show(db: Session, show_id: int) -> Show | None:
    return db.query(Show).filter(Show.id == show_id).first()
