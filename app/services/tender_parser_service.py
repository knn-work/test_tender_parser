import random
import time
from typing import List

from app.api.schemas.tender import TenderCreate
from app.services.ros_tender_parser import RosTenderParser
from app.services.tender_service import TenderService


class TenderParserService:

    def __init__(self, tender_service: TenderService):
        self.tender_parser:RosTenderParser = RosTenderParser()
        self.tender_service: TenderService = tender_service

    def __parse_links(self, max_count: int = 100):
        # Сначала парсим до max_count уникальных ссылок
        links = []
        page = 1
        seen = set()
        while len(links) < max_count:

            page_links = self.tender_parser.get_tender_links(page)
            if not page_links:
                break

            for link in page_links:
                if link not in seen:
                    links.append(link)
                    seen.add(link)
                if len(links) >= max_count:
                    break
            page += 1

            time.sleep(random.uniform(1.2, 3.4))
        return links

    def fetch_and_sync_tenders(self, db_session, max_count: int = 100) -> List[TenderCreate]:
        """
        Парсит и синхронизирует тендеры: удаляет устаревшие, добавляет новые (без дубликатов).
        """
        print("[*] Загрузка свежих тендеров...")

        # 1. Получаем до max_count уникальных ссылок
        links = self.__parse_links(max_count)

        # 2. Парсим каждую ссылку в TenderCreate
        tenders: List[TenderCreate] = []
        for url in links:
            tender = self.tender_parser.parse_tender_page(url)
            time.sleep(random.uniform(1.2, 3.4))
            if tender:
                tenders.append(tender)

        # 3. Удаляем устаревшие тендеры (те, которых нет в новых данных)
        print("[*] Удаление устаревших тендеров...")
        numbers_from_site = [t.number for t in tenders]
        self.tender_service.delete_not_in(db_session, numbers_from_site)

        # 4. Добавляем новые тендеры (только если их ещё нет)
        print(f"[*] Добавление {len(tenders)} тендеров (только новых)...")
        for tender_schema in tenders:
            existing = self.tender_service.get_one_or_none(db_session, tender_schema.number)
            if not existing:
                created = self.tender_service.create(db_session, tender_schema)
                print(f"[+] Добавлен тендер: {created.number}")
            else:
                print(f"[=] Уже существует: {tender_schema.number}")

        print("[✓] Синхронизация завершена.")
        return tenders
