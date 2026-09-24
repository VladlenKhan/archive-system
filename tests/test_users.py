"""Тесты класса User и функций работы с пользователями."""

from models import User
from models.users import add_user, find_user_by_id, find_users


def test_user_creation():
    """Проверяет создание объекта пользователя."""
    user = User(1, "Хан Владлен", "vladlen@example.com")

    assert user.id == 1
    assert user.name == "Хан Владлен"
    assert user.email == "vladlen@example.com"


def test_user_str():
    """Проверяет строковое представление пользователя."""
    user = User(1, "Хан Владлен", "vladlen@example.com")

    assert "Хан Владлен" in str(user)
    assert "vladlen@example.com" in str(user)


def test_user_from_data():
    """Проверяет создание пользователя из набора данных."""
    data = {
        "id": 2,
        "name": "Анна Смирнова",
        "email": "anna@example.com",
    }

    user = User.from_data(data)

    assert user.id == 2
    assert user.name == "Анна Смирнова"
    assert user.to_data() == data


def test_add_user():
    """Проверяет добавление пользователя в коллекцию."""
    users: list = []

    user = add_user(users, "Хан Владлен", "vladlen@example.com")

    assert isinstance(user, User)
    assert user.id == 1
    assert len(users) == 1


def test_add_user_with_invalid_email():
    """Проверяет отказ в добавлении пользователя без почты."""
    users: list = []

    user = add_user(users, "Хан Владлен", "vladlen")

    assert user is None
    assert len(users) == 0


def test_find_users():
    """Проверяет поиск пользователей по имени и почте."""
    users = [User(1, "Хан Владлен", "vladlen@example.com")]

    assert len(find_users(users, "владлен")) == 1
    assert len(find_users(users, "example.com")) == 1
    assert len(find_users(users, "Пётр")) == 0


def test_find_user_by_id():
    """Проверяет поиск пользователя по идентификатору."""
    users = [User(1, "Хан Владлен", "vladlen@example.com")]

    assert find_user_by_id(users, 1) is users[0]
    assert find_user_by_id(users, 99) is None
