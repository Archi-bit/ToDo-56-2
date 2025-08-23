CREATE_TASKS = """
    CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        task TEXT NOT NULL,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP,
        completed INTEGER DEFAULT 0
    )
"""


INSERT_TASK = "INSERT INTO tasks (task) VALUES (?)"

SELECT_TASK = "SELECT id, task, created_at, completed FROM tasks"

UPDATE_TASK = "UPDATE tasks SET task = ? WHERE id = ?"

UPDATE_COMPLETED = "UPDATE tasks SET completed = ? WHERE id = ?"

DELETE_TASK = "DELETE FROM tasks WHERE id = ?"
