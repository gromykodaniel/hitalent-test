import json
from datetime import datetime
from typing import List, Dict, Any

from task import Task


class TaskManager:
    def __init__(self, storage_file: str = "tasks.json"):
        self.storage_file = storage_file
        self.tasks = self.load_tasks()

    def save_tasks(self) -> None:
        with open(self.storage_file, "w", encoding="utf-8") as file:
            json.dump(
                [task.__dict__ for task in self.tasks],
                file,
                ensure_ascii=False,
                indent=4,
            )

    def load_tasks(self) -> List[Any]:
        try:
            with open(self.storage_file, "r", encoding="utf-8") as file:
                return [Task(**task) for task in json.load(file)]
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def add_task(
        self, title: str, description: str, category: str, due_date: str, priority: str
    ) -> None:
        due_date = self.validate_due_date(due_date)
        new_task = Task(
            id=self.generate_task_id(),
            title=title,
            description=description,
            category=category,
            due_date=due_date,
            priority=priority,
            status="Не выполнена",
        )
        self.tasks.append(new_task)
        self.save_tasks()

    def edit_task(
        self,
        task_id: int,
        title: str,
        description: str,
        category: str,
        due_date: str,
        priority: str,
    ) -> None:
        task = self.get_task_by_id(task_id)
        if task:
            task.title = title or task.title
            task.description = description or task.description
            task.category = category or task.category
            task.due_date = self.validate_due_date(due_date) or task.due_date
            task.priority = priority or task.priority
            self.save_tasks()

    def delete_task(self, task_id: int) -> None:
        task = self.get_task_by_id(task_id)
        if task:
            self.tasks.remove(task)
            self.save_tasks()

    def search_tasks(self, **filters) -> List[Any]:
        result = self.tasks
        for key, value in filters.items():
            result = [
                task
                for task in result
                if str(getattr(task, key, "")).lower() == str(value).lower()
            ]
        return result

    def list_tasks(self) -> List[Dict[str, Any]]:
        return [task.to_dict() for task in self.tasks]

    def get_task_by_id(self, task_id: int) -> Any:
        return next((task for task in self.tasks if task.id == task_id), None)

    def generate_task_id(self) -> int:
        return max((task.id for task in self.tasks), default=0) + 1

    def validate_due_date(self, due_date: str) -> str:
        try:
            datetime.strptime(due_date, "%Y-%m-%d")
            return due_date
        except ValueError:
            raise ValueError("Дата должна быть в формате 2020-10-10.")
