from app.cli.base.command_abc import Command
from app.core import app_config
from app.db import SessionLocal
from app.services.tender_parser_service import TenderParserService
from app.services.tender_service import TenderService


class GetNew(Command):
    """Команда CLI для получения и синхронизации новых тендеров."""

    def __init__(self):
        """Инициализация команды и сервиса для работы с тендерами."""
        self.command_name = "get_new"
        self.service = TenderService()

    @property
    def name(self):
        """Возвращает имя команды.

        Returns:
            str: Имя команды.
        """
        return self.command_name

    @property
    def action(self):
        """Возвращает действие для argparse.

        Returns:
            str | None: Строка для настройки аргумента в argparse.
        """
        return "store_true"

    def default(self, data=None):
        """Выполняет действие по умолчанию — получает все тендеры из базы.

        Args:
            data: Входные данные от предыдущей команды.

        Returns:
            list: Список тендеров.
        """
        return self.service.get_all(db=SessionLocal())

    def execute(self, arg_value, data=None):
        """Выполняет команду — получает и синхронизирует новые тендеры.

        Args:
            arg_value: Значение аргумента, переданного в CLI.
            data: Входные данные от предыдущей команды.

        Returns:
            list: Список всех тендеров после синхронизации.
        """

        session = SessionLocal()
        TenderParserService(self.service).fetch_and_sync_tenders(session, app_config.count_tender)
        return self.service.get_all(db=session)
