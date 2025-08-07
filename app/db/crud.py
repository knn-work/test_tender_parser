from sqlalchemy.orm import Session

from app.api.schemas.tender import TenderCreate

from .models import Tender


def create_tender(db: Session, tender_in: TenderCreate) -> Tender:
    tender = Tender(**tender_in.model_dump())
    db.add(tender)
    db.commit()
    db.refresh(tender)
    return tender

def get_tender(db: Session, number: int) -> Tender | None:
    return db.query(Tender).filter(Tender.number == number).first()
