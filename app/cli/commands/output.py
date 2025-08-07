import csv
import os
from typing import List

from app.cli.base.command_abc import Command
from app.db.models import Tender


class Output(Command):
    """Сохраняет данные Tender в файл с расширением .csv"""

    def __init__(self):
        self.command_name = "output"

    def default(self, data=None):
        print(*[x.__dict__ for x in data], sep ="\n")
        return


    @property
    def name(self) -> str:
        return self.command_name

    def execute(self, file_name: str, data: List[Tender] = None):
        if not file_name.endswith('.csv'):
            print("Ошибка: файл должен иметь расширение .csv")
            return data

        if not data:
            print("Нет данных для записи.")
            return data

        # Гарантируем, что директория существует
        os.makedirs(os.path.dirname(file_name) or ".", exist_ok=True)

        with open(file_name, mode='w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow([
                "number", "title", "start_price",
                "place_of_delivery", "url", "end_time"
            ])
            for tender in data:
                writer.writerow([
                    tender.number,
                    tender.title,
                    tender.start_price,
                    tender.place_of_delivery,
                    tender.url,
                    tender.end_time.isoformat() if tender.end_time else "",
                ])

        print(f"Записано {file_name}")
        return data
