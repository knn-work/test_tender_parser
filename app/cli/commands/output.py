import csv
import os

from app.cli.base.command_abc import Command


class Output(Command):
    """Команда CLI для сохранения данных Tender в CSV-файл."""

    def __init__(self):
        """Инициализация команды."""
        self.command_name = "output"

    def default(self, data=None):
        """Выводит данные в консоль.

        Args:
            data: Список объектов Tender или другие данные для отображения.
        """
        print(*[x.__dict__ for x in data], sep="\n")
        return

    @property
    def name(self):
        """Возвращает имя команды.

        Returns:
            str: Имя команды.
        """
        return self.command_name

    def execute(self, file_name, data=None):
        """Сохраняет список объектов Tender в CSV-файл.

        Args:
            file_name: Имя выходного файла с расширением .csv.
            data: Список объектов Tender для записи.

        Returns:
            list: Те же данные, что были переданы на вход.
        """
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

        print(f"[✓] Записано {file_name}")
        return data
