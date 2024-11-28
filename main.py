from taskmanager import TaskManager

if __name__ == "__main__":
    manager = TaskManager()

    while True:

        print("1. прсмотр задач")
        print("2.добавить задачу")
        print("3. Редактировать задачу")
        print("4. Удалить задачу")
        print("5. Поиск задач")

        cur = input("Выберите действие: ")

        if cur == "1":
            tasks = manager.list_tasks()
            for task in tasks:
                print(task)

        elif cur == "2":
            title = input("Название задачи: ")
            description = input("Описание задачи: ")
            category = input("Категория: ")
            due_date = input("Срок выполнения (YYYY-MM-DD): ")
            priority = input("Приоритет (Низкий, Средний, Высокий): ")
            try:
                manager.add_task(title, description, category, due_date, priority)
                print("Задача добавлена!")
            except Exception:
                print("Ошибка при добавленрии ")

        elif cur == "3":
            task_id = int(input("Введите ID задачи для редактирования: "))
            title = input("Новое название (или Enter для пропуска): ")
            description = input("Новое описание (или Enter для пропуска): ")
            category = input("Новая категория (или Enter для пропуска): ")
            due_date = input(
                "Новый срок выполнения (YYYY-MM-DD) (или Enter для пропуска): "
            )
            priority = input("Новый приоритет (или Enter для пропуска): ")
            try:
                manager.edit_task(
                    task_id, title, description, category, due_date, priority
                )
                print("Задача обновлена!")
            except ValueError as e:
                print(e)

        elif cur == "4":
            task_id = int(input("Введите ID задачи для удаления: "))
            manager.delete_task(task_id)
            print("Задача удалена!")

        elif cur == "5":
            filters = {}
            print("Параметры поиска (оставьте пустым для пропуска):")
            filters["title"] = input("Название: ")
            filters["description"] = input("Описание: ")
            filters["category"] = input("Категория: ")
            filters["due_date"] = input("Срок выполнения (YYYY-MM-DD): ")
            filters["priority"] = input("Приоритет: ")
            filters["status"] = input("Статус (Выполнена/Не выполнена): ")
            filters = {k: v for k, v in filters.items() if v}
            result = manager.search_tasks(**filters)
            for task in result:
                print(task.to_dict())

        else:
            break
