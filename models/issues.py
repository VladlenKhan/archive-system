"""Класс выдачи документа и функции работы с выдачами."""

from typing import List, Optional

from .documents import Document
from .users import User


class Issue:
    """Выдача документа пользователю."""

    def __init__(
        self,
        issue_id: int,
        document: Document,
        issue_date: str,
        user: User,
        is_returned: bool = False,
    ) -> None:
        """Создать объект выдачи документа."""
        self.id = issue_id
        self.document = document
        self.issue_date = issue_date
        self.user = user
        self.is_returned = is_returned

    def close(self) -> None:
        """Закрыть выдачу: документ возвращён в архив."""
        self.is_returned = True

    def is_active(self) -> bool:
        """Проверить, что выдача не закрыта."""
        return not self.is_returned

    def to_data(self) -> dict:
        """Вернуть данные выдачи для сохранения в JSON."""
        return {
            "id": self.id,
            "document_id": self.document.id,
            "issue_date": self.issue_date,
            "user_id": self.user.id,
            "is_returned": self.is_returned,
        }

    def __str__(self) -> str:
        """Вернуть строковое представление выдачи."""
        status = "закрыта" if self.is_returned else "активна"
        return (
            f"[{self.id}] {self.document.title} — "
            f"{self.user.name}, {self.issue_date} ({status})"
        )


def get_issue_status(is_available: bool) -> str:
    """Вернуть текстовый статус доступности документа."""
    if is_available:
        return "Документ доступен для выдачи"

    return "Документ уже выдан"


def next_issue_id(issues: List[Issue]) -> int:
    """Вернуть свободный идентификатор выдачи."""
    if not issues:
        return 1

    return max(issue.id for issue in issues) + 1


def is_document_available(
    issues: List[Issue],
    document: Document,
) -> bool:
    """Проверить, свободен ли документ для выдачи."""
    for issue in issues:
        if issue.document.id == document.id and issue.is_active():
            return False

    return True


def create_issue(
    issues: List[Issue],
    document: Document,
    issue_date: str,
    user: User,
) -> Optional[Issue]:
    """Создать выдачу документа и добавить её в коллекцию."""
    if not is_document_available(issues, document):
        return None

    issue = Issue(
        issue_id=next_issue_id(issues),
        document=document,
        issue_date=issue_date,
        user=user,
    )

    issues.append(issue)
    return issue


def close_issue(issues: List[Issue], issue_id: int) -> bool:
    """Закрыть выдачу по идентификатору."""
    for issue in issues:
        if issue.id == issue_id and issue.is_active():
            issue.close()
            return True

    return False


def find_issues_by_user(issues: List[Issue], user: User) -> List[Issue]:
    """Найти выдачи указанного пользователя."""
    result = []

    for issue in issues:
        if issue.user.id == user.id:
            result.append(issue)

    return result


def sort_issues(issues: List[Issue]) -> List[Issue]:
    """Отсортировать выдачи по дате."""
    return sorted(issues, key=lambda issue: issue.issue_date)


def show_issues(issues: List[Issue]) -> None:
    """Вывести список выдач."""
    if not issues:
        print("\nВыдачи отсутствуют.")
        return

    print("\nСписок выдач:")

    for issue in issues:
        print(issue)
