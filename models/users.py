"""Класс пользователя и функции работы с коллекцией пользователей."""

from typing import List, Optional


class User:
    """Пользователь электронного архива."""

    def __init__(
        self,
        user_id: int,
        name: str,
        email: str,
    ) -> None:
        """Создать объект пользователя."""
        self.id = user_id
        self.name = name
        self.email = email

    @classmethod
    def from_data(cls, data: dict) -> "User":
        """Создать пользователя из набора данных JSON."""
        return cls(
            user_id=data["id"],
            name=data["name"],
            email=data["email"],
        )

    def to_data(self) -> dict:
        """Вернуть данные пользователя для сохранения в JSON."""
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
        }

    def matches(self, query: str) -> bool:
        """Проверить совпадение по имени или адресу почты."""
        value = query.lower()
        return value in self.name.lower() or value in self.email.lower()

    def __str__(self) -> str:
        """Вернуть строковое представление пользователя."""
        return f"[{self.id}] {self.name} ({self.email})"


def next_user_id(users: List[User]) -> int:
    """Вернуть свободный идентификатор пользователя."""
    if not users:
        return 1

    return max(user.id for user in users) + 1


def add_user(
    users: List[User],
    name: str,
    email: str,
) -> Optional[User]:
    """Создать пользователя и добавить его в коллекцию."""
    if name.strip() == "":
        print("Ошибка: имя пользователя не указано")
        return None

    if "@" not in email:
        print("Ошибка: некорректный адрес электронной почты")
        return None

    user = User(
        user_id=next_user_id(users),
        name=name,
        email=email,
    )

    users.append(user)
    return user


def find_users(users: List[User], query: str) -> List[User]:
    """Найти пользователей по имени или адресу почты."""
    result = []

    for user in users:
        if user.matches(query):
            result.append(user)

    return result


def find_user_by_id(users: List[User], user_id: int) -> Optional[User]:
    """Найти пользователя по идентификатору."""
    for user in users:
        if user.id == user_id:
            return user

    return None


def show_users(users: List[User]) -> None:
    """Вывести список пользователей."""
    if not users:
        print("\nПользователи отсутствуют.")
        return

    print("\nСписок пользователей:")

    for user in users:
        print(user)
