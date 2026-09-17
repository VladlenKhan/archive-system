from datetime import date as dt

document_title = "Основы Python"
author_name = "Хан Владлен"
category_name = "Учебные материалы"
archive_name = "Основной архив"
document_size = 250
is_archived = True


def check_document(title, size):
    if title == "":
        return "Ошибка: название документа не указано"

    if size <= 0:
        return "Ошибка: размер документа должен быть больше 0"

    return "Документ прошел проверку"


def get_archive_status(is_archived):
    if is_archived:
        return "Документ находится в архиве"

    return "Документ не добавлен в архив"


def show_document_info(title, author, category, archive, size):
    print("\nИнформация о документе:")
    print(f"Название: {title}")
    print(f"Автор: {author}")
    print(f"Категория: {category}")
    print(f"Архив: {archive}")
    print(f"Размер: {size} КБ")
    print(f"Дата добавления: {dt.today()}")


print("Система электронного архива")
print("--------------------------")

print(check_document(document_title, document_size))
print(get_archive_status(is_archived))

show_document_info(
    document_title, author_name, category_name, archive_name, document_size
)