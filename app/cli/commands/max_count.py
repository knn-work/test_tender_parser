from typing import Callable

from app.cli.base.command_abc import Command


class MaxCount(Command):
    """Команда CLI для ограничения количества элементов в выводе."""

    def __init__(self):
        """Инициализация команды."""
        self.command_name = "max"

    def default(self, data=None):
        """Возвращает данные без изменений.

        Args:
            data: Входные данные от предыдущей команды.

        Returns:
            Любой тип данных, переданный на вход.
        """
        return data

    @property
    def name(self):
        """Возвращает имя команды.

        Returns:
            str: Имя команды.
        """
        return self.command_name

    def execute(self, arg_value, data=None):
        """Ограничивает количество элементов, переданных в данных.

        Args:
            arg_value: Максимальное количество элементов для отображения.
            data: Входные данные (итерируемая последовательность).

        Returns:
            list: Ограниченный по количеству список элементов.
        """
        new_data = []
        for count, el in enumerate(data):
            if count >= int(arg_value):
                continue
            new_data.append(el)
        return new_data
