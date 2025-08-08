import re
from datetime import datetime
from typing import Optional

import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

from app.api.schemas.tender import TenderCreate

BASE_URL = "https://rostender.info"
SEARCH_URL_TEMPLATE = BASE_URL + "/extsearch?page={}"


class RosTenderParser:
    """Класс для парсинга сайта rostender.info и получения данных о тендерах."""

    ua = UserAgent()

    def get_tender_links(self, page_number: int) -> list[str]:
        """
        Получает список ссылок на тендеры с указанной страницы.

        Args:
            page_number: Номер страницы поиска.

        Returns:
            Список полных URL-адресов тендеров.
        """
        url = SEARCH_URL_TEMPLATE.format(page_number)
        print(f"Получение ссылок из {url}",end = " - ")
        resp = requests.get(url, headers={"User-Agent": self.ua.random})
        soup = BeautifulSoup(resp.text, "html.parser")
        anchors = soup.find_all("a", class_="tender-info__link")
        lincs = [BASE_URL + a["href"] for a in anchors if a.get("href")]
        print(f"Получено {len(lincs)} ссылок")
        # print(lincs)
        return lincs

    def parse_tender_page(self, url: str) -> Optional[TenderCreate]:
        """
        Парсит страницу тендера и возвращает объект TenderCreate.

        Args:
            url: URL страницы тендера.

        Returns:
            Объект TenderCreate или None в случае ошибки.
        """
        try:
            resp = requests.get(url, headers={"User-Agent": self.ua.random})
            soup = BeautifulSoup(resp.text, "html.parser")

            number_block = soup.find("div", class_="tender-info-header-number")
            number = int(re.search(r"\d+", number_block.text).group()) if number_block else None

            title_block = soup.find("h1", class_="tender-header__h4")
            title = title_block.text.strip()[:100] if title_block else "Без названия"

            price_block = soup.find("span", class_="tender-body__text")
            start_price = self.parse_price(price_block.text) if price_block else None

            place_block = soup.find("span", class_="tender-info__text")
            place_of_delivery = place_block.text.strip() if place_block else "Не указано"

            date_block = soup.find("div", class_="n4")
            if date_block:
                date_text = date_block.find("span", class_="black").text.strip()
                time_text = date_block.find("span", class_="gray-text-small")
                if time_text is None:
                    time_text = "00:00"
                else:
                    time_text = time_text.text.strip()
                end_time = self.parse_datetime(date_text, time_text)
            else:
                end_time = datetime.now()

            return TenderCreate(
                number=number,
                title=title,
                start_price=start_price,
                place_of_delivery=place_of_delivery,
                url=url,
                end_time=end_time,
            )
        except Exception as e:
            print(f"[!] Ошибка при парсинге {url}: {e}")
            return None

    @staticmethod
    def parse_datetime(date_str: str, time_str: str) -> Optional[datetime]:
        """
        Преобразует строковые дату и время в объект datetime.

        Args:
            date_str: Дата в формате "дд.мм.гггг".
            time_str: Время в формате "чч:мм".

        Returns:
            Объект datetime или None, если произошла ошибка.
        """
        try:
            return datetime.strptime(f"{date_str.strip()} {time_str.strip()}", "%d.%m.%Y %H:%M")
        except Exception:
            return None

    @staticmethod
    def parse_price(price_str: str) -> Optional[float]:
        """
        Преобразует строку с ценой в число с плавающей точкой.

        Args:
            price_str: Строка с ценой (может содержать пробелы, символы валюты и т.п.).

        Returns:
            Цена в виде float или None, если не удалось распарсить.
        """
        try:
            return float(re.sub(r"[^\d.]", "", price_str.replace(",", ".")))
        except ValueError:
            return None
