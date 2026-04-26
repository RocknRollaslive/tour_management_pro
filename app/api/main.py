from fastapi import Depends, FastAPI
from fastapi.responses import Response
from sqlalchemy.orm import Session

from app.core.db import Base, engine, get_db
from app.schemas.finance import FinanceCreate, FinanceOut
from app.schemas.tour import TourCreate, TourOut
from app.services.finance_service import (
    create_finance,
    get_finance_summary,
    get_finances_for_tour,
)
from app.services.pdf_service import generate_call_sheet_pdf
from app.services.tour_service import create_tour, get_all_tours

# Ensure models are imported before create_all
from app.models.finance import Finance  # noqa: F401
from app.models.tour import Tour  # noqa: F401
from app.models.schedule import ScheduleItem  # noqa: F401

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Tour Management Pro API")


@app.get("/")
def health() -> dict:
    return {"status": "ok"}


@app.post("/tours", response_model=TourOut)
def api_create_tour(tour: TourCreate, db: Session = Depends(get_db)) -> TourOut:
    return create_tour(db, tour)


@app.get("/tours", response_model=list[TourOut])
def api_get_tours(db: Session = Depends(get_db)) -> list[TourOut]:
    return get_all_tours(db)


@app.post("/finances", response_model=FinanceOut)
def api_create_finance(
    finance: FinanceCreate,
    db: Session = Depends(get_db),
) -> FinanceOut:
    return create_finance(db, finance)


@app.get("/tours/{tour_id}/finances", response_model=list[FinanceOut])
def api_get_finances(tour_id: int, db: Session = Depends(get_db)) -> list[FinanceOut]:
    return get_finances_for_tour(db, tour_id)


@app.get("/tours/{tour_id}/summary")
def api_get_summary(tour_id: int, db: Session = Depends(get_db)) -> list[dict]:
    return get_finance_summary(db, tour_id)


@app.post("/call-sheet")
def api_generate_call_sheet(payload: dict) -> Response:
    tour_name = payload.get("tour_name", "Unknown Tour")
    venue = payload.get("venue", "")
    schedule_text = payload.get("schedule_text", "")

    pdf_bytes = generate_call_sheet_pdf(tour_name, venue, schedule_text)

    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={"Content-Disposition": "attachment; filename=call_sheet.pdf"},
    )
# --- SHOWS SECTION ---
from app.models.show import Show

@app.get("/shows")
def get_all_shows(db: Session = Depends(get_db)):
    return db.query(Show).all()

# ADD THIS: This is what the Home page is looking for!
@app.get("/tours/{tour_id}/shows")
def get_shows_for_tour(tour_id: int, db: Session = Depends(get_db)):
    shows = db.query(Show).filter(Show.tour_id == tour_id).all()
    return shows

@app.post("/shows")
def create_show(show: dict, db: Session = Depends(get_db)):
    # Basic cleanup: remove tour_id from dict if it's there to avoid double-passing
    db_show = Show(**show)
    db.add(db_show)
    db.commit()
    db.refresh(db_show)
    return db_show
@app.get("/shows/{show_id}/schedule")
def get_schedule(show_id: int, db: Session = Depends(get_db)):
    return db.query(ScheduleItem).filter(ScheduleItem.show_id == show_id).order_by(ScheduleItem.time).all()

@app.post("/schedule")
def create_schedule_item(item: dict, db: Session = Depends(get_db)):
    db_item = ScheduleItem(**item)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item    