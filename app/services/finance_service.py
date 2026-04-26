from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.finance import Finance
from app.schemas.finance import FinanceCreate


def create_finance(db: Session, finance_data: FinanceCreate) -> Finance:
    finance = Finance(**finance_data.model_dump())
    db.add(finance)
    db.commit()
    db.refresh(finance)
    return finance


def get_finances_for_tour(db: Session, tour_id: int) -> list[Finance]:
    return (
        db.query(Finance)
        .filter(Finance.tour_id == tour_id)
        .order_by(Finance.id.desc())
        .all()
    )


def get_finance_summary(db: Session, tour_id: int) -> list[dict]:
    rows = (
        db.query(
            Finance.dept,
            func.sum(Finance.rev).label("total_rev"),
            func.sum(Finance.exp).label("total_exp"),
        )
        .filter(Finance.tour_id == tour_id)
        .group_by(Finance.dept)
        .all()
    )

    return [
        {
            "dept": row.dept,
            "total_rev": float(row.total_rev or 0),
            "total_exp": float(row.total_exp or 0),
            "profit": float((row.total_rev or 0) - (row.total_exp or 0)),
        }
        for row in rows
    ]
