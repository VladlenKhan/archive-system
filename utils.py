"""Вспомогательные функции безопасного ввода данных."""

from datetime import date, datetime

DATE_FORMAT = "%Y-%m-%d"


def input_int(message: str) -> int:
    """Запросить у пользователя целое число."""
    while True:
        try:
            return int(input(message))
        except ValueError:
            print("Ошибка: необходимо ввести целое число.")


def input_bool(message: str) -> bool:
    """Запросить у пользователя ответ да или нет."""
    while True:
        value = input(message).strip().lower()

        if value in ("да", "д", "yes", "y"):
            return True

        if value in ("нет", "н", "no", "n"):
            return False

        print("Введите да или нет.")


def input_date(message: str) -> str:
    """Запросить дату в формате ГГГГ-ММ-ДД."""
    while True:
        value = input(message).strip()

        if value == "":
            return str(date.today())

        try:
            parsed = datetime.strptime(value, DATE_FORMAT)
            return parsed.strftime(DATE_FORMAT)
        except ValueError:
            print("Ошибка: введите дату в формате ГГГГ-ММ-ДД.")
