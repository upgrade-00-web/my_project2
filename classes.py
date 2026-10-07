import json
from datetime import datetime
from pathlib import Path

class Task:
    def __init__(self, title: str, description: str, due_date: str):
        self.title = title.strip()
        self.description = description.strip()
        self.due_date = due_date.strip()
        self.validate_date()

    def validate_date(self):
        """Проверяет, соответствует ли дата формату YYYY-MM-DD."""
        try:
            datetime.strptime(self.due_date, "%Y-%m-%d")
        except ValueError:
            raise ValueError("Дата должна быть в формате ГГГГ-ММ-ДД (например, 2026-10-25)")

    def to_dict(self) -> dict:
        return {
            "title": self.title,
            "description": self.description,
            "due_date": self.due_date,
        }

    @classmethod
    def from_dict(cls, data: dict):
        return cls(data["title"], data["description"], data["due_date"])


class TaskManager:
    def __init__(self, filename: str = "tasks.json"):
        self.filepath = Path(filename)
        self.tasks: list[Task] = []
        self.load_from_file()

    def add_task(self, task: Task):
        self.tasks.append(task)
        self.save_to_file()

    def delete_task(self, index: int):
        if 0 <= index < len(self.tasks):
            del self.tasks[index]
            self.save_to_file()

    def save_to_file(self):
        data = [task.to_dict() for task in self.tasks]
        with open(self.filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    def load_from_file(self):
        if not self.filepath.exists():
            self.tasks = []
            return

        try:
            with open(self.filepath, "r", encoding="utf-8") as f:
                data = json.load(f)
                self.tasks = [Task.from_dict(item) for item in data]
        except (json.JSONDecodeError, KeyError, ValueError):
            self.tasks = []