from datetime import date

from documents import (
    add_document,
    delete_document,
    filter_by_category,
    search_documents,
    show_document_info,
    sort_documents,
)
from storage import load_documents, save_documents
from utils import input_bool, input_int


DATA_FILE = "data/documents.json"


def show_documents(documents: list[dict]) -> None:
    """Выводит список всех документов."""
    if not documents:
        print("\nДокументы отсутствуют.")
        return

    print("\nСписок документов:")

    for number, document in enumerate(documents, start=1):
        print(f"{number}. {document['title']}")


def main() -> None:
    """Запускает систему электронного архива."""
    documents = load_documents(DATA_FILE)

    while True:
        print("\n=== Система электронного архива ===")
        print("1. Показать документы")
        print("2. Добавить документ")
        print("3. Найти документ")
        print("4. Показать информацию о документе")
        print("5. Найти документы по категории")
        print("6. Отсортировать документы")
        print("7. Удалить документ")
        print("8. Сохранить данные")
        print("0. Выход")

        choice = input("\nВыберите действие: ")

        if choice == "1":
            show_documents(documents)

        elif choice == "2":
            title = input("Название документа: ")
            author = input("Автор: ")
            category = input("Категория: ")
            archive = input("Архив: ")
            size = input_int("Размер документа в КБ: ")
            is_archived = input_bool("Документ находится в архиве? ")

            added = add_document(
                documents,
                title,
                author,
                category,
                archive,
                size,
                str(date.today()),
                is_archived,
            )

            if added:
                print("Документ успешно добавлен.")

        elif choice == "3":
            query = input("Введите название для поиска: ")

            found_documents = search_documents(
                documents,
                query,
            )

            if found_documents:
                for document in found_documents:
                    show_document_info(document)
            else:
                print("Документы не найдены.")

        elif choice == "4":
            title = input("Введите название документа: ")

            found_documents = search_documents(
                documents,
                title,
            )

            if found_documents:
                show_document_info(found_documents[0])
            else:
                print("Документ не найден.")

        elif choice == "5":
            category = input("Введите категорию: ")

            found_documents = filter_by_category(
                documents,
                category,
            )

            if found_documents:
                for document in found_documents:
                    show_document_info(document)
            else:
                print("Документы данной категории не найдены.")

        elif choice == "6":
            documents = sort_documents(documents)
            print("Документы отсортированы по названию.")

        elif choice == "7":
            title = input("Введите название документа для удаления: ")

            deleted = delete_document(
                documents,
                title,
            )

            if deleted:
                print("Документ удалён.")
            else:
                print("Документ не найден.")

        elif choice == "8":
            save_documents(DATA_FILE, documents)
            print("Данные успешно сохранены.")

        elif choice == "0":
            save_documents(DATA_FILE, documents)
            print("Данные сохранены. Программа завершена.")
            break

        else:
            print("Ошибка: выберите существующий пункт меню.")


if __name__ == "__main__":
    main()