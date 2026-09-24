"""Точка запуска системы электронного архива."""

from datetime import date
from typing import List

from models import Document, Issue, User
from models.documents import (
    add_document,
    delete_document,
    filter_by_category,
    filter_documents_by_size,
    find_document_by_id,
    find_documents,
    show_document_info,
    show_documents,
    sort_documents,
)
from models.issues import (
    close_issue,
    create_issue,
    find_issues_by_user,
    get_issue_status,
    is_document_available,
    show_issues,
    sort_issues,
)
from models.users import (
    add_user,
    find_user_by_id,
    find_users,
    show_users,
)
from storage import (
    load_documents,
    load_issues,
    load_users,
    save_documents,
    save_issues,
    save_users,
)
from utils import input_bool, input_date, input_int

DOCUMENTS_FILE = "data/documents.json"
USERS_FILE = "data/users.json"
ISSUES_FILE = "data/issues.json"

MENU = """
=== Система электронного архива ===
1. Показать документы
2. Добавить документ
3. Найти документ по названию
4. Показать информацию о документе
5. Найти документы по категории
6. Отобрать документы по размеру
7. Отсортировать документы
8. Удалить документ
9. Показать пользователей
10. Добавить пользователя
11. Найти пользователя
12. Проверить доступность документа
13. Выдать документ
14. Закрыть выдачу
15. Показать выдачи
16. Сохранить данные
0. Выход
"""


def create_new_document(documents: List[Document]) -> None:
    """Запросить данные и добавить новый документ."""
    title = input("Название документа: ")
    author = input("Автор: ")
    category = input("Категория: ")
    archive = input("Архив: ")
    size = input_int("Размер документа в КБ: ")
    is_archived = input_bool("Документ находится в архиве? ")

    document = add_document(
        documents,
        title,
        author,
        category,
        archive,
        size,
        str(date.today()),
        is_archived,
    )

    if document is not None:
        print(f"Документ успешно добавлен: {document}")


def create_new_user(users: List[User]) -> None:
    """Запросить данные и добавить нового пользователя."""
    name = input("Имя пользователя: ")
    email = input("Электронная почта: ")

    user = add_user(users, name, email)

    if user is not None:
        print(f"Пользователь добавлен: {user}")


def create_new_issue(
    issues: List[Issue],
    documents: List[Document],
    users: List[User],
) -> None:
    """Выдать документ пользователю."""
    document_id = input_int("Идентификатор документа: ")
    document = find_document_by_id(documents, document_id)

    if document is None:
        print("Документ не найден.")
        return

    user_id = input_int("Идентификатор пользователя: ")
    user = find_user_by_id(users, user_id)

    if user is None:
        print("Пользователь не найден.")
        return

    issue_date = input_date("Дата выдачи (ГГГГ-ММ-ДД): ")
    issue = create_issue(issues, document, issue_date, user)

    if issue is None:
        print(get_issue_status(False))
        return

    print(f"Выдача создана: {issue}")


def close_existing_issue(issues: List[Issue]) -> None:
    """Закрыть выдачу по идентификатору."""
    issue_id = input_int("Идентификатор выдачи: ")

    if close_issue(issues, issue_id):
        print("Выдача закрыта, документ возвращён в архив.")
    else:
        print("Активная выдача с таким идентификатором не найдена.")


def check_availability(
    issues: List[Issue],
    documents: List[Document],
) -> None:
    """Проверить доступность документа для выдачи."""
    document_id = input_int("Идентификатор документа: ")
    document = find_document_by_id(documents, document_id)

    if document is None:
        print("Документ не найден.")
        return

    print(f"\n{document}")
    print(get_issue_status(is_document_available(issues, document)))


def search_documents_by_title(documents: List[Document]) -> None:
    """Найти и вывести документы по названию."""
    query = input("Введите название для поиска: ")
    found = find_documents(documents, query)

    if not found:
        print("Документы не найдены.")
        return

    for document in found:
        print(document)


def show_selected_document(documents: List[Document]) -> None:
    """Вывести подробную информацию о документе."""
    document_id = input_int("Идентификатор документа: ")
    document = find_document_by_id(documents, document_id)

    if document is None:
        print("Документ не найден.")
        return

    show_document_info(document)


def show_documents_by_category(documents: List[Document]) -> None:
    """Вывести документы выбранной категории."""
    category = input("Введите категорию: ")
    found = filter_by_category(documents, category)

    if not found:
        print("Документы данной категории не найдены.")
        return

    for document in found:
        print(document)


def show_documents_by_size(documents: List[Document]) -> None:
    """Вывести документы не меньше указанного размера."""
    min_size = input_int("Минимальный размер в КБ: ")
    found = list(filter_documents_by_size(documents, min_size))

    if not found:
        print("Подходящие документы не найдены.")
        return

    for document in found:
        print(document)


def remove_document(documents: List[Document]) -> None:
    """Удалить документ по названию."""
    title = input("Введите название документа для удаления: ")

    if delete_document(documents, title):
        print("Документ удалён.")
    else:
        print("Документ не найден.")


def search_users(users: List[User], issues: List[Issue]) -> None:
    """Найти пользователей и показать их выдачи."""
    query = input("Введите имя или почту для поиска: ")
    found = find_users(users, query)

    if not found:
        print("Пользователи не найдены.")
        return

    for user in found:
        print(f"\n{user}")

        for issue in find_issues_by_user(issues, user):
            print(f"  {issue}")


def save_all(
    documents: List[Document],
    users: List[User],
    issues: List[Issue],
) -> None:
    """Сохранить все коллекции проекта в JSON-файлы."""
    save_documents(DOCUMENTS_FILE, documents)
    save_users(USERS_FILE, users)
    save_issues(ISSUES_FILE, issues)


def main() -> None:
    """Запустить систему электронного архива."""
    documents = load_documents(DOCUMENTS_FILE)
    users = load_users(USERS_FILE)
    issues = load_issues(ISSUES_FILE, documents, users)

    while True:
        print(MENU)
        choice = input("Выберите действие: ").strip()

        if choice == "1":
            show_documents(documents)

        elif choice == "2":
            create_new_document(documents)

        elif choice == "3":
            search_documents_by_title(documents)

        elif choice == "4":
            show_selected_document(documents)

        elif choice == "5":
            show_documents_by_category(documents)

        elif choice == "6":
            show_documents_by_size(documents)

        elif choice == "7":
            documents = sort_documents(documents)
            print("Документы отсортированы по названию.")

        elif choice == "8":
            remove_document(documents)

        elif choice == "9":
            show_users(users)

        elif choice == "10":
            create_new_user(users)

        elif choice == "11":
            search_users(users, issues)

        elif choice == "12":
            check_availability(issues, documents)

        elif choice == "13":
            create_new_issue(issues, documents, users)

        elif choice == "14":
            close_existing_issue(issues)

        elif choice == "15":
            show_issues(sort_issues(issues))

        elif choice == "16":
            save_all(documents, users, issues)
            print("Данные успешно сохранены.")

        elif choice == "0":
            save_all(documents, users, issues)
            print("Данные сохранены. Программа завершена.")
            break

        else:
            print("Ошибка: выберите существующий пункт меню.")


if __name__ == "__main__":
    main()
