import json


def load_documents(filename: str) -> list[dict]:
    """Загружает документы из JSON-файла."""
    try:
        with open(filename, "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        print("Файл с документами не найден.")
        return []
    except json.JSONDecodeError:
        print("Ошибка: файл содержит некорректный JSON.")
        return []


def save_documents(
    filename: str,
    documents: list[dict],
) -> None:
    """Сохраняет документы в JSON-файл."""
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(
            documents,
            file,
            ensure_ascii=False,
            indent=4,
        )