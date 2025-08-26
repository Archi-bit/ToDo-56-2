import sqlite3
from db import queries
from config import db_path


def init_db():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute(queries.CREATE_TASKS)

    conn.commit()
    conn.close()


def add_task(task):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute(queries.INSERT_TASK, (task,))
    conn.commit()
    task_id = cursor.lastrowid
    conn.close()
    return task_id

def get_task(order_by=None):
    """
    order_by:
      - "date_desc"  -> новые выше
      - "date_asc"   -> старые выше
      - "status_bottom" -> выполненные внизу
      - "status_top"    -> выполненные вверху
      - None -> по умолчанию новые выше
    """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    base = queries.SELECT_TASK
    if order_by == "date_asc":
        base += " ORDER BY datetime(created_at) ASC"
    elif order_by == "status_bottom":
        base += " ORDER BY completed ASC, datetime(created_at) DESC"
    elif order_by == "status_top":
        base += " ORDER BY completed DESC, datetime(created_at) DESC"
    else:
        base += " ORDER BY datetime(created_at) DESC"

    cursor.execute(base)
    tasks = cursor.fetchall()
    conn.close()
    return tasks


def delete_task(task_id):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute(queries.DELETE_TASK, (task_id,))
    conn.commit()
    conn.close()


def update_task(task_id, new_task):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute(queries.UPDATE_TASK, (new_task, task_id))
    conn.commit()
    conn.close()


def update_completed(task_id, completed_value):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute(queries.UPDATE_COMPLETED, (completed_value, task_id))
    conn.commit()
    conn.close()

    
def delete_complete_tasks():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tasks WHERE completed = 1")
    conn.commit()
    conn.close()
