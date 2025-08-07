from typing import Type

from sqlalchemy.orm import Session

from app.api.schemas.tender import TenderRead
from app.db.models import Tender


class TenderRepository:
    @staticmethod
    def create(db: Session, tender: Tender) -> Tender:
        db.add(tender)
        db.commit()
        db.refresh(tender)
        return tender

    @staticmethod
    def get_one(db: Session, number: int) -> Tender:
        tender: Tender | None = db.get(Tender, number)
        return tender


    @staticmethod
    def exists(db: Session, number: int) -> bool:
        return db.query(Tender).filter(Tender.number == number).first() is not None


    @staticmethod
    def get_all(db: Session ) -> list[TenderRead]:
        tenders: list[Type[Tender]] = db.query(Tender).all()

        return tenders

    @staticmethod
    def delete_all(db: Session) -> None:
        db.query(Tender).delete()
        db.commit()

    @staticmethod
    def delete_not_in(db: Session, numbers: list[int]) -> None:
        db.query(Tender).filter(Tender.number.notin_(numbers)).delete(synchronize_session=False)
        db.commit()