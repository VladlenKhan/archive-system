def input_int(message: str) -> int:
    """Запрашивает у пользователя целое число."""
    while True:
        try:
            return int(input(message))
        except ValueError:
            print("Ошибка: необходимо ввести целое число.")


def input_bool(message: str) -> bool:
    """Запрашивает у пользователя значение True или False."""
    while True:
        value = input(message).strip().lower()

        if value in ("да", "д", "yes", "y"):
            return True

        if value in ("нет", "н", "no", "n"):
            return False

        print("Введите да или нет.")