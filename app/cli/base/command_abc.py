from abc import ABC, abstractmethod
from typing import Callable


class Command(ABC):
    """
    Абстрактная команда, которая должна реализовать метод execute.
    """

    @abstractmethod
    def default(self,data=None):
        raise NotImplementedError

    @property
    @abstractmethod
    def name(self) -> str:
        """
        Уникальное имя команды (используется как ключ аргумента).
        """
        raise NotImplementedError


    @property
    def action(self) -> str | None:
        return None

    @abstractmethod
    def execute(self, arg_value: str, data=None):
        """
        Выполняет команду, модифицируя таблицу.

        Args:
            arg_value: Аргумент команды из CLI
            data: Данные необходимые для работы
        Returns:
            Новая таблица с результатом
        """
        raise NotImplementedError