from typing import Callable

from app.cli.base.command_abc import Command


class MaxCount(Command):
    """Выполняет агрегацию: avg, min или max по одному из столбцов."""

    def __init__(self):
        self.command_name = "max"

    def default(self, data=None):
        return data

    @property
    def name(self) -> str:
        return self.command_name

    def execute(self, arg_value: str, data=None):
        new_data = []
        for count, el in enumerate(data):
            if count >= int(arg_value):
                continue
            new_data.append(el)

        return new_data



