"""Тесты класса Document и функций работы с документами."""

from models import Document
from models.documents import (
    add_document,
    check_document,
    delete_document,
    filter_by_category,
    filter_documents_by_size,
    find_document_by_id,
    find_documents,
    get_archive_status,
    sort_documents,
)


def make_document() -> Document:
    """Создать тестовый документ."""
    return Document(
        document_id=1,
        title="Основы Python",
        author="Хан Владлен",
        category="Учебные материалы",
        archive="Основной архив",
        size=250,
        date="2026-09-23",
        is_archived=True,
    )


def test_document_creation():
    """Проверяет создание объекта документа."""
    document = make_document()

    assert document.id == 1
    assert document.title == "Основы Python"
    assert document.author == "Хан Владлен"
    assert document.size == 250
    assert document.is_archived is True


def test_document_str():
    """Проверяет строковое представление документа."""
    document = make_document()

    assert "Основы Python" in str(document)
    assert "в архиве" in str(document)


def test_document_matches():
    """Проверяет поиск по подстроке названия."""
    document = make_document()

    assert document.matches("python")
    assert not document.matches("Django")


def test_document_is_larger_than():
    """Проверяет сравнение размера документа."""
    document = make_document()

    assert document.is_larger_than(100)
    assert not document.is_larger_than(500)


def test_document_move_to_archive():
    """Проверяет перевод документа в архив."""
    document = make_document()
    document.is_archived = False

    document.move_to_archive()

    assert document.is_archived is True


def test_document_validate():
    """Проверяет статический метод проверки данных."""
    assert Document.validate("Основы Python", 250)
    assert not Document.validate("", 250)
    assert not Document.validate("Основы Python", 0)


def test_document_from_data_and_to_data():
    """Проверяет преобразование документа из JSON и обратно."""
    data = make_document().to_data()
    document = Document.from_data(data)

    assert document.id == 1
    assert document.title == "Основы Python"
    assert document.to_data() == data


def test_check_document():
    """Проверяет корректность документа."""
    result = check_document("Основы Python", 250)

    assert result == "Документ прошел проверку"


def test_check_document_with_empty_title():
    """Проверяет документ без названия."""
    result = check_document("", 250)

    assert result == "Ошибка: название документа не указано"


def test_get_archive_status():
    """Проверяет статус документа в архиве."""
    document = make_document()

    assert get_archive_status(document) == "Документ находится в архиве"

    document.is_archived = False

    assert get_archive_status(document) == "Документ не добавлен в архив"


def test_add_document():
    """Проверяет добавление документа в коллекцию."""
    documents: list = []

    document = add_document(
        documents,
        "Основы Python",
        "Хан Владлен",
        "Учебные материалы",
        "Основной архив",
        250,
        "2026-09-23",
        True,
    )

    assert isinstance(document, Document)
    assert document.id == 1
    assert len(documents) == 1


def test_add_document_with_invalid_size():
    """Проверяет отказ в добавлении документа с нулевым размером."""
    documents: list = []

    document = add_document(
        documents,
        "Основы Python",
        "Хан Владлен",
        "Учебные материалы",
        "Основной архив",
        0,
        "2026-09-23",
        True,
    )

    assert document is None
    assert len(documents) == 0


def test_find_documents():
    """Проверяет поиск документов по названию."""
    documents = [make_document()]

    result = find_documents(documents, "Python")

    assert len(result) == 1
    assert result[0].title == "Основы Python"


def test_find_document_by_id():
    """Проверяет поиск документа по идентификатору."""
    documents = [make_document()]

    assert find_document_by_id(documents, 1) is documents[0]
    assert find_document_by_id(documents, 99) is None


def test_filter_by_category():
    """Проверяет отбор документов по категории."""
    documents = [make_document()]

    assert len(filter_by_category(documents, "учебные материалы")) == 1
    assert len(filter_by_category(documents, "Отчёты")) == 0


def test_filter_documents_by_size():
    """Проверяет отбор документов по размеру."""
    documents = [make_document()]

    result = list(filter_documents_by_size(documents, 200))

    assert len(result) == 1


def test_sort_documents():
    """Проверяет сортировку документов по названию."""
    first = make_document()
    second = make_document()
    second.id = 2
    second.title = "Аналитическая записка"

    result = sort_documents([first, second])

    assert result[0].title == "Аналитическая записка"


def test_delete_document():
    """Проверяет удаление документа."""
    documents = [make_document()]

    assert delete_document(documents, "Основы Python") is True
    assert len(documents) == 0
