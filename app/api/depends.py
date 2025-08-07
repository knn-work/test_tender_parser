from app.db import SessionLocal
from app.services.tender_service import TenderService


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_tender_service() -> TenderService:
    yield TenderService()