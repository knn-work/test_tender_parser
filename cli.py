import argparse

from app.cli.base.command_abc import Command
from app.cli.commands import *
from app.core import app_config


def main() -> None:
    """
    Основная точка входа для CLI-инструмента.

    Парсит аргументы командной строки, выполняет соответствующие команды и
    последовательно передаёт данные между ними.
    """
    parser = argparse.ArgumentParser(
        prog=app_config.project_name,
        description='CLI-инструмент / ' + app_config.description,
    )

    commands: list = [
        GetNew(),
        MaxCount(),
        Output(),
    ]

    # Добавление аргументов команд
    for command in commands:
        parser.add_argument(
            f'--{command.name.replace("_", "-")}',
            dest=command.name,
            help=command.__doc__,
            action=command.action
        )

    try:
        args = parser.parse_args()
    except Exception:
        print("Ошибка: указан несуществующий аргумент. Используйте --help для списка опций.")
        return

    if getattr(args, "file", None) is not None:
        print("Ошибка: необходимо указать файл как параметр. \n\tПример: --file filename.csv")
        return

    data = None
    for command in commands:
        arg_value = getattr(args, command.name, None)
        if arg_value is None or bool(arg_value) is False:
            data = command.default(data)
            continue
        data = command.execute(arg_value, data=data)


if __name__ == '__main__':
    main()
