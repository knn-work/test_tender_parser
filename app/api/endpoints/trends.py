from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.depends import get_db, get_tender_service
from app.api.schemas.tender import TenderRead
from app.services.tender_service import TenderService

router =  APIRouter()

@router.get("/tenders", response_model=list[TenderRead])
def get_all( db: Session = Depends(get_db), service: TenderService = Depends(get_tender_service) ):
    tenders: list[TenderRead] = service.get_all(db)
    return tenders


@router.get("/tenders/count", response_model=int)
def load_new( db: Session = Depends(get_db), service: TenderService = Depends(get_tender_service) ):
    tenders: list[TenderRead] = service.get_all(db)
    return len(tenders)