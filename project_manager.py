import json
import os

class Task:
    """Класс для хранения информации о задаче."""
    def __init__(self, task_id, description, priority, status="в процессе", assignee=None):
        self.task_id = task_id
        self.description = description
        self.priority = priority
        self.status = status
        self.assignee = assignee

    def to_dict(self):
        return self.__dict__

    @staticmethod
    def from_dict(data):
        return Task(**data)

class Project:
    """Класс для управления проектом и его задачами."""
    def __init__(self, name, description):
        self.name = name
        self.description = description
        self.tasks = []

    def add_task(self, task):
        self.tasks.append(task)

    def to_dict(self):
        return {
            "name": self.name,
            "description": self.description,
            "tasks": [t.to_dict() for t in self.tasks]
        }

    @staticmethod
    def from_dict(data):
        project = Project(data['name'], data['description'])
        project.tasks = [Task.from_dict(t) for t in data['tasks']]
        return project

class ProjectManager:
    """Основной класс для управления всей системой."""
    def __init__(self):
        self.projects = []
        self.users = []

    def add_project(self, name, description):
        new_project = Project(name, description)
        self.projects.append(new_project)
        print(f"Успех: Проект '{name}' создан.")

    def remove_project(self, name):
        original_count = len(self.projects)
        self.projects = [p for p in self.projects if p.name != name]
        if len(self.projects) < original_count:
            print(f"Успех: Проект '{name}' удален.")
        else:
            print("Ошибка: Проект не найден.")

    def add_task_to_project(self, project_name, task_id, description, priority):
        for proj in self.projects:
            if proj.name == project_name:
                new_task = Task(task_id, description, priority)
                proj.add_task(new_task)
                print(f"Успех: Задача добавлена в проект '{project_name}'.")
                return
        print("Ошибка: Проект не найден.")

    def assign_task(self, task_id, user_name):
        if user_name not in self.users:
            self.users.append(user_name)
        
        for proj in self.projects:
            for task in proj.tasks:
                if task.task_id == task_id:
                    task.assignee = user_name
                    print(f"Успех: Задача '{task_id}' назначена студенту {user_name}.")
                    return
        print("Ошибка: Задача с таким ID не найдена.")

    def update_task_status(self, task_id, status):
        for proj in self.projects:
            for task in proj.tasks:
                if task.task_id == task_id:
                    task.status = status
                    print(f"Успех: Статус задачи '{task_id}' изменен на '{status}'.")
                    return
        print("Ошибка: Задача не найдена.")

    def generate_report(self):
        print("\n--- ОТЧЕТ ПО ПРОЕКТАМ ---")
        if not self.projects:
            print("Список проектов пуст.")
        for proj in self.projects:
            total = len(proj.tasks)
            completed = len([t for t in proj.tasks if t.status == "завершено"])
            print(f"Проект: {proj.name} | Задач: {total} | Выполнено: {completed}")
            for t in proj.tasks:
                assignee_str = t.assignee if t.assignee else "Не назначен"
                print(f"  [{t.status}] ID: {t.task_id} | Описание: {t.description} | Исполнитель: {assignee_str}")
        print("------------------------\n")

    def save_to_file(self, filename="data.json"):
        data = {
            "projects": [p.to_dict() for p in self.projects],
            "users": self.users
        }
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
            print("Инфо: Данные сохранены в файл.")
        except Exception as e:
            print(f"Ошибка при сохранении: {e}")

def load_from_file(self, filename="data.json"):
        if not os.path.exists(filename):
            print("Инфо: Файл данных не найден. Инициализирована пустая база.")
            return
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.projects = [Project.from_dict(p) for p in data.get('projects', [])]
                self.users = data.get('users', [])
            print("Инфо: Данные успешно загружены.")
        except Exception as e:
            print(f"Ошибка при загрузке: {e}")

def main():
    manager = ProjectManager()
    
    while True:
        print("\nМЕНЮ ТРЕКЕРА ПРОЕКТОВ")
        print("1 - Создать проект")
        print("2 - Удалить проект")
        print("3 - Добавить задачу")
        print("4 - Назначить задачу")
        print("5 - Обновить статус задачи")
        print("6 - Просмотр отчета")
        print("7 - Сохранить данные")
        print("8 - Загрузить данные")
        print("0 - Выход")
        
        choice = input("Выберите пункт меню: ")
        
        if choice == '1':
            name = input("Название проекта: ")
            desc = input("Описание: ")
            manager.add_project(name, desc)
        elif choice == '2':
            name = input("Название проекта для удаления: ")
            manager.remove_project(name)
        elif choice == '3':
            p_name = input("Название проекта: ")
            t_id = input("ID задачи: ")
            t_desc = input("Описание задачи: ")
            t_prior = input("Приоритет: ")
            manager.add_task_to_project(p_name, t_id, t_desc, t_prior)
        elif choice == '4':
            t_id = input("ID задачи: ")
            u_name = input("Имя студента: ")
            manager.assign_task(t_id, u_name)
        elif choice == '5':
            t_id = input("ID задачи: ")
            status = input("Новый статус: ")
            manager.update_task_status(t_id, status)
        elif choice == '6':
            manager.generate_report()
        elif choice == '7':
            manager.save_to_file()
        elif choice == '8':
            manager.load_from_file()
        elif choice == '0':
            print("Программа завершена.")
            break
        else:
            print("Ошибка: Неверный выбор.")

if __name__ == "__main__":
    main()