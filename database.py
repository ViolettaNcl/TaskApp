import sqlite3
from datetime import datetime

class Database:
    def __init__(self):
        self.conn = sqlite3.connect('tasks.db')
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY,
                client TEXT NOT NULL,
                description TEXT NOT NULL,
                manager TEXT,
                executor TEXT,
                start_date TEXT,
                deadline TEXT,
                status TEXT NOT NULL,
                completion_date TIMESTAMP,
                timestamp TEXT NOT NULL
            )
        """)
        self.conn.commit()

    def add_task(self, client, description):
        self.cursor.execute("""
            INSERT INTO tasks (client, description, status, timestamp)
            VALUES (?, ?, ?, ?)
        """, (client, description, "new", datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
        self.conn.commit()

    def update_task(self, task_id, manager, executor, start_date, deadline):
        self.cursor.execute("""
            UPDATE tasks
            SET manager = ?, executor = ?, start_date = ?, deadline = ?, status = ?
            WHERE id = ?
        """, (manager, executor, start_date, deadline, "in progress", task_id))
        self.conn.commit()

    def complete_task(self, task_id):
        now = datetime.now()
        self.cursor.execute("""
            UPDATE tasks
            SET status = ?, completion_date = ?
            WHERE id = ?
        """, ("completed", now.strftime('%Y-%m-%d %H:%M:%S'), task_id))
        self.conn.commit()

    def get_tasks_by_executor(self, executor):
        self.cursor.execute("""
            SELECT * FROM tasks WHERE executor = ? AND status != 'completed'
        """, (executor,))
        return self.cursor.fetchall()

    def is_task_completed(self, task_id):
        self.cursor.execute("""
            SELECT completion_date
            FROM tasks
            WHERE id = ? AND status = 'completed'
        """, (task_id,))
        result = self.cursor.fetchone()
        if result and result[0]:
            return datetime.strptime(result[0], '%Y-%m-%d %H:%M:%S')
        return None
