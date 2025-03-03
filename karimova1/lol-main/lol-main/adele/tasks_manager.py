import tkinter as tk
from tkinter import messagebox
from tkinter import simpledialog
import sqlite3
from datetime import date

class Task:
    def __init__(self, task_id, title, description, due_date, priority, category, status="не выполнено"):
        # Здесь исправлено: добавлены поля task_id, title, description, due_date, priority, category
        self.task_id = task_id
        self.title = title
        self.description = description
        self.due_date = due_date
        self.priority = priority
        self.category = category
        self.status = status

    def update_status(self, new_status):
        self.status = new_status

    def __str__(self):
        return f"{self.task_id}. {self.title} | {self.priority} | {self.due_date} | {self.category} | {self.status}"

class TaskManager:
    def __init__(self):
        self.tasks = {}
        self.load_tasks()

    def add_task(self, task):
        self.tasks[task.task_id] = task
        self.save_tasks()

    def save_tasks(self):
        conn = sqlite3.connect('tasks.db')
        cursor = conn.cursor()
        cursor.execute('DROP TABLE IF EXISTS tasks')
        cursor.execute(''' CREATE TABLE tasks ( id INTEGER PRIMARY KEY, title TEXT, description TEXT, due_date TEXT, priority TEXT, category TEXT, status TEXT ) ''')
        cursor.execute('ALTER TABLE tasks ADD COLUMN due_date TEXT')
        for task in self.tasks.values():
            cursor.execute('''INSERT INTO tasks ( title, description, due_date, priority, category, status ) VALUES (?, ?, ?, ?, ?, ?)''',
                (task.title, task.description, str(task.due_date), task.priority, task.category, task.status)
            )
        conn.commit()
        conn.close()

    def load_tasks(self):
        conn = sqlite3.connect('tasks.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM tasks')
        for row in cursor.fetchall():
            task = Task(
                task_id=row[0],
                title=row[1],
                description=row[2],
                due_date=row[3],
                priority=row[4],
                category=row[5],
                status=row[6]
            )
            self.tasks[task.task_id] = task
        conn.close()

class TaskManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Задачи Адель")
        self.root.configure(bg="#ffccff")
        self.manager = TaskManager()
        self.create_widgets()

    def create_widgets(self):
        self.listbox = tk.Listbox(self.root, width=50, bg="#ffe6f2", fg="#000000")
        self.listbox.pack(pady=10)

        tk.Button(self.root, text="Добавить задачу", command=self.add_task, bg="#ff99cc").pack(pady=5)
        tk.Button(self.root, text="Удалить задачу", command=self.delete_task, bg="#ff99cc").pack(pady=5)
        tk.Button(self.root, text="Изменить статус", command=self.update_status, bg="#ff99cc").pack(pady=5)

        self.refresh_task_list()

    def refresh_task_list(self):
        self.listbox.delete(0, tk.END)
        for task in self.manager.tasks.values():
            self.listbox.insert(tk.END, f"{task.task_id}. {task.title} - {task.status}")

    def add_task(self):
        title = simpledialog.askstring("Название задачи", "Введите название задачи:")
        description = simpledialog.askstring("Описание задачи", "Введите описание задачи:")
        due_date = simpledialog.askstring("Дата выполнения", "Введите дату выполнения (ГГГГ-ММ-ДД):")
        priority = simpledialog.askstring("Приоритет", "Введите приоритет (высокий/средний/низкий):")
        category = simpledialog.askstring("Категория", "Введите категорию:")
        
        if title and description and due_date and priority and category:
            task_id = len(self.manager.tasks) + 1
            self.manager.add_task(Task(
                task_id=task_id,
                title=title,
                description=description,
                due_date=due_date,
                priority=priority,
                category=category
            ))
            self.refresh_task_list()

    def delete_task(self):
        selected = self.listbox.curselection()
        if selected:
            task_id = int(selected[0]) + 1
            del self.manager.tasks[task_id]
            self.manager.save_tasks()
            self.refresh_task_list()

    def update_status(self):
        selected = self.listbox.curselection()
        if selected:
            task_id = int(selected[0]) + 1
            status = simpledialog.askstring("Статус задачи", "Введите новый статус:")
            self.manager.tasks[task_id].update_status(status)
            self.manager.save_tasks()
            self.refresh_task_list()

if __name__ == "__main__":
    root = tk.Tk()
    app = TaskManagerApp(root)
    root.mainloop()