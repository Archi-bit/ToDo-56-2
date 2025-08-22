import sqlite3 
from db import queries
from config import db_path


def init_db():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute(queries.CREATE_TASKS)
    print('База данных подключена!!!')
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


def get_task():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute(queries.SELECT_TASK)
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

