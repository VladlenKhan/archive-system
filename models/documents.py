"""Класс документа и функции работы с коллекцией документов."""

from typing import Iterator, List, Optional


class Document:
    """Электронный документ, хранящийся в архиве."""

    def __init__(
        self,
        document_id: int,
        title: str,
        author: str,
        category: str,
        archive: str,
        size: int,
        date: str,
        is_archived: bool = False,
    ) -> None:
        """Создать объект документа."""
        self.id = document_id
        self.title = title
        self.author = author
        self.category = category
        self.archive = archive
        self.size = size
        self.date = date
        self.is_archived = is_archived

    @staticmethod
    def validate(title: str, size: int) -> bool:
        """Проверить корректность данных документа."""
        return title.strip() != "" and size > 0

    @classmethod
    def from_data(cls, data: dict) -> "Document":
        """Создать документ из набора данных JSON."""
        return cls(
            document_id=data["id"],
            title=data["title"],
            author=data["author"],
            category=data["category"],
            archive=data["archive"],
            size=data["size"],
            date=data["date"],
            is_archived=data["is_archived"],
        )

    def to_data(self) -> dict:
        """Вернуть данные документа для сохранения в JSON."""
        return {
            "id": self.id,
            "title": self.title,
            "author": self.author,
            "category": self.category,
            "archive": self.archive,
            "size": self.size,
            "date": self.date,
            "is_archived": self.is_archived,
        }

    def matches(self, query: str) -> bool:
        """Проверить, встречается ли подстрока в названии."""
        return query.lower() in self.title.lower()

    def is_in_category(self, category: str) -> bool:
        """Проверить принадлежность документа категории."""
        return self.category.lower() == category.lower()

    def is_larger_than(self, min_size: int) -> bool:
        """Проверить, что размер документа не меньше указанного."""
        return self.size >= min_size

    def move_to_archive(self) -> None:
        """Поместить документ в архив."""
        self.is_archived = True

    def __str__(self) -> str:
        """Вернуть строковое представление документа."""
        status = "в архиве" if self.is_archived else "вне архива"
        return (
            f"[{self.id}] {self.title} — {self.author}, "
            f"{self.category}, {self.size} КБ ({status})"
        )


def check_document(title: str, size: int) -> str:
    """Проверить данные документа и вернуть текст результата."""
    if title.strip() == "":
        return "Ошибка: название документа не указано"

    if size <= 0:
        return "Ошибка: размер документа должен быть больше 0"

    return "Документ прошел проверку"


def get_archive_status(document: Document) -> str:
    """Вернуть статус документа в архиве."""
    if document.is_archived:
        return "Документ находится в архиве"

    return "Документ не добавлен в архив"


def next_document_id(documents: List[Document]) -> int:
    """Вернуть свободный идентификатор документа."""
    if not documents:
        return 1

    return max(document.id for document in documents) + 1


def add_document(
    documents: List[Document],
    title: str,
    author: str,
    category: str,
    archive: str,
    size: int,
    date: str,
    is_archived: bool,
) -> Optional[Document]:
    """Создать документ и добавить его в коллекцию."""
    if not Document.validate(title, size):
        print(check_document(title, size))
        return None

    document = Document(
        document_id=next_document_id(documents),
        title=title,
        author=author,
        category=category,
        archive=archive,
        size=size,
        date=date,
        is_archived=is_archived,
    )

    documents.append(document)
    return document


def find_documents(
    documents: List[Document],
    query: str,
) -> List[Document]:
    """Найти документы по подстроке названия."""
    result = []

    for document in documents:
        if document.matches(query):
            result.append(document)

    return result


def find_document_by_id(
    documents: List[Document],
    document_id: int,
) -> Optional[Document]:
    """Найти документ по идентификатору."""
    for document in documents:
        if document.id == document_id:
            return document

    return None


def filter_by_category(
    documents: List[Document],
    category: str,
) -> List[Document]:
    """Отобрать документы указанной категории."""
    result = []

    for document in documents:
        if document.is_in_category(category):
            result.append(document)

    return result


def filter_documents_by_size(
    documents: List[Document],
    min_size: int,
) -> Iterator[Document]:
    """Отобрать документы не меньше указанного размера."""
    return (
        document
        for document in documents
        if document.is_larger_than(min_size)
    )


def sort_documents(documents: List[Document]) -> List[Document]:
    """Отсортировать документы по названию."""
    return sorted(
        documents,
        key=lambda document: document.title.lower(),
    )


def delete_document(documents: List[Document], title: str) -> bool:
    """Удалить документ по названию."""
    for document in documents:
        if document.title.lower() == title.lower():
            documents.remove(document)
            return True

    return False


def show_documents(documents: List[Document]) -> None:
    """Вывести список документов."""
    if not documents:
        print("\nДокументы отсутствуют.")
        return

    print("\nСписок документов:")

    for document in documents:
        print(document)


def show_document_info(document: Document) -> None:
    """Вывести подробную информацию о документе."""
    print("\nИнформация о документе:")
    print(f"Идентификатор: {document.id}")
    print(f"Название: {document.title}")
    print(f"Автор: {document.author}")
    print(f"Категория: {document.category}")
    print(f"Архив: {document.archive}")
    print(f"Размер: {document.size} КБ")
    print(f"Дата добавления: {document.date}")
    print(get_archive_status(document))
