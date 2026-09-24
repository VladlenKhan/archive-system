"""Загрузка и сохранение данных архива в JSON-файлах."""

import json
from typing import List

from models import Document, Issue, User
from models.documents import find_document_by_id
from models.users import find_user_by_id


def read_data(filename: str) -> list:
    """Прочитать список данных из JSON-файла."""
    try:
        with open(filename, "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"Файл {filename} не найден, будет создан новый.")
        return []
    except json.JSONDecodeError:
        print(f"Ошибка: файл {filename} содержит некорректный JSON.")
        return []


def write_data(filename: str, data: list) -> None:
    """Записать список данных в JSON-файл."""
    try:
        with open(filename, "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)
    except OSError:
        print(f"Ошибка: не удалось сохранить файл {filename}.")


def load_documents(filename: str) -> List[Document]:
    """Загрузить документы из JSON-файла в объекты Document."""
    documents = []

    for data in read_data(filename):
        try:
            documents.append(Document.from_data(data))
        except KeyError:
            print("Ошибка: пропущена запись документа без поля данных.")

    return documents


def save_documents(filename: str, documents: List[Document]) -> None:
    """Сохранить объекты Document в JSON-файл."""
    write_data(filename, [document.to_data() for document in documents])


def load_users(filename: str) -> List[User]:
    """Загрузить пользователей из JSON-файла в объекты User."""
    users = []

    for data in read_data(filename):
        try:
            users.append(User.from_data(data))
        except KeyError:
            print("Ошибка: пропущена запись пользователя без поля данных.")

    return users


def save_users(filename: str, users: List[User]) -> None:
    """Сохранить объекты User в JSON-файл."""
    write_data(filename, [user.to_data() for user in users])


def load_issues(
    filename: str,
    documents: List[Document],
    users: List[User],
) -> List[Issue]:
    """Загрузить выдачи и восстановить связи с документами."""
    issues = []

    for data in read_data(filename):
        try:
            document = find_document_by_id(documents, data["document_id"])
            user = find_user_by_id(users, data["user_id"])
            issue_id = data["id"]
            issue_date = data["issue_date"]
            is_returned = data["is_returned"]
        except KeyError:
            print("Ошибка: пропущена запись выдачи без поля данных.")
            continue

        if document is None or user is None:
            print(f"Ошибка: выдача {issue_id} ссылается на чужие данные.")
            continue

        issues.append(
            Issue(
                issue_id=issue_id,
                document=document,
                issue_date=issue_date,
                user=user,
                is_returned=is_returned,
            )
        )

    return issues


def save_issues(filename: str, issues: List[Issue]) -> None:
    """Сохранить объекты Issue в JSON-файл."""
    write_data(filename, [issue.to_data() for issue in issues])
