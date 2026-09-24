"""Тесты класса Issue и функций работы с выдачами документов."""

from models import Document, Issue, User
from models.issues import (
    close_issue,
    create_issue,
    find_issues_by_user,
    get_issue_status,
    is_document_available,
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


def make_user() -> User:
    """Создать тестового пользователя."""
    return User(1, "Хан Владлен", "vladlen@example.com")


def test_issue_creation():
    """Проверяет создание выдачи и связь с объектами."""
    document = make_document()
    user = make_user()

    issue = Issue(1, document, "2026-09-24", user)

    assert issue.id == 1
    assert issue.document is document
    assert issue.user is user
    assert issue.issue_date == "2026-09-24"
    assert issue.is_returned is False


def test_issue_str():
    """Проверяет строковое представление выдачи."""
    issue = Issue(1, make_document(), "2026-09-24", make_user())

    assert "Основы Python" in str(issue)
    assert "активна" in str(issue)


def test_issue_close():
    """Проверяет закрытие выдачи."""
    issue = Issue(1, make_document(), "2026-09-24", make_user())

    issue.close()

    assert issue.is_returned is True
    assert issue.is_active() is False


def test_issue_to_data():
    """Проверяет сохранение выдачи по идентификаторам связей."""
    issue = Issue(1, make_document(), "2026-09-24", make_user())

    data = issue.to_data()

    assert data["document_id"] == 1
    assert data["user_id"] == 1
    assert data["is_returned"] is False


def test_is_document_available():
    """Проверяет доступность документа без выдач."""
    issues: list = []

    assert is_document_available(issues, make_document())


def test_get_issue_status():
    """Проверяет текстовый статус доступности документа."""
    assert get_issue_status(True) == "Документ доступен для выдачи"
    assert get_issue_status(False) == "Документ уже выдан"


def test_duplicate_issue_forbidden():
    """Проверяет запрет повторной выдачи документа."""
    issues: list = []
    document = make_document()
    user = make_user()

    create_issue(issues, document, "2026-09-24", user)
    second = create_issue(issues, document, "2026-09-25", user)

    assert second is None
    assert len(issues) == 1
    assert not is_document_available(issues, document)


def test_closed_issue_does_not_block_document():
    """Проверяет, что закрытая выдача не блокирует документ."""
    issues: list = []
    document = make_document()
    user = make_user()

    first = create_issue(issues, document, "2026-09-24", user)
    first.close()

    second = create_issue(issues, document, "2026-09-25", user)

    assert second is not None
    assert second.id == 2
    assert len(issues) == 2


def test_close_issue():
    """Проверяет закрытие выдачи по идентификатору."""
    issues: list = []
    create_issue(issues, make_document(), "2026-09-24", make_user())

    assert close_issue(issues, 1) is True
    assert close_issue(issues, 1) is False


def test_find_issues_by_user():
    """Проверяет поиск выдач пользователя."""
    issues: list = []
    user = make_user()
    create_issue(issues, make_document(), "2026-09-24", user)

    assert len(find_issues_by_user(issues, user)) == 1
    assert len(find_issues_by_user(issues, User(2, "Анна", "a@b.ru"))) == 0
