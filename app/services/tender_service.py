from typing import Optional

from sqlalchemy.orm import Session

from app.api.schemas.tender import TenderCreate, TenderRead
from app.db.models import Tender
from app.repositories import TenderRepository


class TenderService:
    """Сервисный слой для работы с тендерами."""
    def __init__(self, repo: type = TenderRepository) -> None:
        self.repo: TenderRepository = repo()

    def create(self, db: Session, tender_create: TenderCreate) -> TenderRead | None:
        """
        Создает новый тендер, если он еще не существует.

        Args:
            db: Сессия базы данных.
            tender_create: Данные тендера для создания.

        Returns:
            Объект TenderRead, если тендер был создан. Иначе None.
        """
        if self.repo.exists(db, tender_create.number):
            return None

        tender: Tender = self.repo.create(
            db,
            Tender(**tender_create.model_dump())
        )
        return TenderRead.model_validate(tender)

    def get_one(self, db: Session, number: int) -> TenderRead:
        """
        Получает тендер по его номеру.

        Args:
            db: Сессия базы данных.
            number: Номер тендера.

        Returns:
            Объект TenderRead.
        """
        tender_model: Tender = self.repo.get_one(db, number)
        return TenderRead.model_validate(tender_model)

    def get_all(self, db: Session) -> list[TenderRead]:
        """
        Возвращает список всех тендеров.

        Args:
            db: Сессия базы данных.

        Returns:
            Список объектов TenderRead.
        """
        return [
            TenderRead.model_validate(tender)
            for tender in self.repo.get_all(db)
        ]

    def delete_all(self, db: Session) -> None:
        """
        Удаляет все тендеры из базы.

        Args:
            db: Сессия базы данных.
        """
        self.repo.delete_all(db)

    def delete_not_in(self, db: Session, numbers: list[int]) -> None:
        """
        Удаляет все тендеры, номера которых не входят в переданный список.

        Args:
            db: Сессия базы данных.
            numbers: Список номеров тендеров, которые нужно оставить.
        """
        self.repo.delete_not_in(db, numbers)


    def get_one_or_none(self, db: Session, number: int) -> Optional[TenderRead]:
        """
           Возвращает тендер по номеру или None, если он не найден.

           Args:
               db: Сессия базы данных.
               number: Номер тендера.

           Returns:
               Объект TenderRead или None.
           """
        tender_model: Optional[Tender] = self.repo.get_one(db, number)
        if tender_model:
            return TenderRead.model_validate(tender_model)
        return None
