import flet as ft
from db import main_db

def main(page: ft.Page):
    page.title = 'ToDo list'
    page.theme_mode = ft.ThemeMode.LIGHT
    task_list = ft.Column()

    def load_task():
        task_list.controls.clear()
        for task_id, task_text in main_db.get_task():
            task_list.controls.append(create_task_row(task_id, task_text))
        page.update()

    def create_task_row(task_id, task_text):
        task_field = ft.TextField(value=task_text, expand=True, read_only=True)

        def enable_edit(_):
            if task_field.read_only == False: 
                task_field.read_only = True
            else:
                task_field.read_only = False
            task_field.update()

        def save_task(_):
            main_db.update_task(task_id, task_field.value)
            page.update()
            task_field.read_only = True
            task_field.update()

        edit_button = ft.IconButton(icon=ft.Icons.EDIT, tooltip='Редактировать', on_click=enable_edit)
        save_button = ft.IconButton(icon=ft.Icons.SAVE, on_click=save_task)

        return ft.Row([
            task_field,
            edit_button,
            save_button
        ])

    def add_task(_):
        if task_input.value:
            task_id = main_db.add_task(task_input.value)
            task_list.controls.append(create_task_row(task_id, task_input.value))
            task_input.value = ''
            page.update()


    task_input = ft.TextField(label='Введите задачу', expand=True)
    add_button = ft.ElevatedButton('ADD', on_click=add_task)

    page.add(ft.Column([
        ft.Row([task_input, add_button]),
        task_list
    ]))

    load_task()


if __name__ == '__main__':
    main_db.init_db()
    ft.app(target=main)

