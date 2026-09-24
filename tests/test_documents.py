from documents import (
    add_document,
    check_document,
    delete_document,
    search_documents,
)


def test_check_document():
    """Проверяет корректность документа."""
    result = check_document("Основы Python", 250)

    assert result == "Документ прошел проверку"


def test_check_document_with_empty_title():
    """Проверяет документ без названия."""
    result = check_document("", 250)

    assert result == "Ошибка: название документа не указано"


def test_add_document():
    """Проверяет добавление документа."""
    documents = []

    result = add_document(
        documents,
        "Основы Python",
        "Хан Владлен",
        "Учебные материалы",
        "Основной архив",
        250,
        "2026-09-23",
        True,
    )

    assert result is True
    assert len(documents) == 1


def test_search_documents():
    """Проверяет поиск документов."""
    documents = [
        {
            "title": "Основы Python",
            "author": "Хан Владлен",
            "category": "Учебные материалы",
            "archive": "Основной архив",
            "size": 250,
            "date": "2026-09-23",
            "is_archived": True,
        }
    ]

    result = search_documents(documents, "Python")

    assert len(result) == 1


def test_delete_document():
    """Проверяет удаление документа."""
    documents = [
        {
            "title": "Основы Python",
            "author": "Хан Владлен",
            "category": "Учебные материалы",
            "archive": "Основной архив",
            "size": 250,
            "date": "2026-09-23",
            "is_archived": True,
        }
    ]

    result = delete_document(documents, "Основы Python")

    assert result is True
    assert len(documents) == 0