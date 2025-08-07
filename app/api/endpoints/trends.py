from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.depends import get_db, get_tender_service
from app.api.schemas.tender import TenderCreate, TenderRead
from app.services.tender_service import TenderService

router =  APIRouter()

# @router.post("/tenders/", response_model=TenderRead)
# def create(tender: TenderCreate, db: Session = Depends(get_db), service = Depends(get_tender_service)):
#     tender_read: TenderRead = service.create(db, tender)
#     return tender_read
#
# @router.get("/tenders/{number}", response_model=TenderRead)
# def get(number: int, db: Session = Depends(get_db), service: TenderService = Depends(get_tender_service) ):
#     tender = service.get_one(db, number)
#     if not tender:
#         raise HTTPException(status_code=404, detail="Tender not found")
#     return tender


@router.get("/tenders", response_model=list[TenderRead])
def get_all( db: Session = Depends(get_db), service: TenderService = Depends(get_tender_service) ):
    tenders: list[TenderRead] = service.get_all(db)
    return tenders


@router.get("/tenders/load_new", response_model=list[TenderRead])
def load_new( db: Session = Depends(get_db), service: TenderService = Depends(get_tender_service) ):
    tenders: list[TenderRead] = service.get_all(db)
    return tenders