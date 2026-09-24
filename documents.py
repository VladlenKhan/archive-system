def check_document(title: str, size: int) -> str:
    """Проверяет корректность данных документа."""
    if title == "":
        return "Ошибка: название документа не указано"

    if size <= 0:
        return "Ошибка: размер документа должен быть больше 0"

    return "Документ прошел проверку"


def get_archive_status(is_archived: bool) -> str:
    """Возвращает статус документа в архиве."""
    if is_archived:
        return "Документ находится в архиве"

    return "Документ не добавлен в архив"


def show_document_info(document: dict) -> None:
    """Выводит информацию о документе."""
    print("\nИнформация о документе:")
    print(f"Название: {document['title']}")
    print(f"Автор: {document['author']}")
    print(f"Категория: {document['category']}")
    print(f"Архив: {document['archive']}")
    print(f"Размер: {document['size']} КБ")
    print(f"Дата добавления: {document['date']}")
    print(f"В архиве: {document['is_archived']}")


def add_document(
    documents: list[dict],
    title: str,
    author: str,
    category: str,
    archive: str,
    size: int,
    date: str,
    is_archived: bool,
) -> bool:
    """Добавляет документ в список документов."""
    result = check_document(title, size)

    if not result == "Документ прошел проверку":
        print(result)
        return False

    document = {
        "title": title,
        "author": author,
        "category": category,
        "archive": archive,
        "size": size,
        "date": date,
        "is_archived": is_archived,
    }

    documents.append(document)
    return True


def search_documents(
    documents: list[dict],
    query: str,
) -> list[dict]:
    """Ищет документы по названию."""
    result = []

    for document in documents:
        if query.lower() in document["title"].lower():
            result.append(document)

    return result


def filter_by_category(
    documents: list[dict],
    category: str,
) -> list[dict]:
    """Возвращает документы указанной категории."""
    result = []

    for document in documents:
        if document["category"].lower() == category.lower():
            result.append(document)

    return result


def sort_documents(
    documents: list[dict],
) -> list[dict]:
    """Сортирует документы по названию."""
    return sorted(
        documents,
        key=lambda document: document["title"].lower(),
    )


def delete_document(
    documents: list[dict],
    title: str,
) -> bool:
    """Удаляет документ по названию."""
    for document in documents:
        if document["title"].lower() == title.lower():
            documents.remove(document)
            return True

    return False