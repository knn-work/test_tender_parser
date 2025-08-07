from app.cli.base.command_abc import Command
from app.db import SessionLocal
from app.services.tender_parser_service import TenderParserService
from app.services.tender_service import TenderService


class GetNew(Command):

    def __init__(self):
        self.command_name = "get_new"
        self.service = TenderService()

    @property
    def name(self) -> str:
        return self.command_name

    @property
    def action(self) -> str | None:
        return "store_true"

    def default(self, data=None):
        return self.service.get_all(db=SessionLocal())

    def execute(self, arg_value: str, data=None):
        session = SessionLocal()
        TenderParserService(self.service).fetch_and_sync_tenders(session,100)
        return self.service.get_all(db=session)