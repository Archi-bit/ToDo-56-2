import flet as ft
from db import main_db

def main(page: ft.Page):
    page.title = "ToDo list"
    page.theme_mode = ft.ThemeMode.LIGHT

    task_list = ft.Column()
    current_order = "date_desc"

    def load_task(order_by=None):
        nonlocal current_order
        order = order_by if order_by is not None else current_order
        task_list.controls.clear()
        for task_id, task_text, created_at, completed in main_db.get_task(order):
            task_list.controls.append(create_task_row(task_id, task_text, created_at, completed))
        page.update()

    def create_task_row(task_id, task_text, created_at, completed):
        task_field = ft.TextField(value=task_text, expand=True, read_only=True)

        def enable_edit(_):
            task_field.read_only = not task_field.read_only
            task_field.update()

        def save_task(_):
            main_db.update_task(task_id, task_field.value)
            task_field.read_only = True
            task_field.update()
            load_task()

        def toggle_completed(e):
            main_db.update_completed(task_id, 1 if e.control.value else 0)
            load_task()

        completed_checkbox = ft.Checkbox(value=bool(completed), on_change=toggle_completed)

        date_label = ft.Text(created_at, size=12, color=ft.Colors.GREY)

        edit_button = ft.IconButton(icon=ft.Icons.EDIT, tooltip="Редактировать", on_click=enable_edit)
        save_button = ft.IconButton(icon=ft.Icons.SAVE, tooltip="Сохранить", on_click=save_task)

        return ft.Row(
            controls=[
                completed_checkbox,
                ft.Column(
                    controls=[
                        task_field,
                        date_label,
                    ],
                    expand=True,
                ),
                edit_button,
                save_button,
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        )

    def add_task(_):
        text = task_input.value or ""
        if not text:
            return
        if len(text) > 100:
            return
        main_db.add_task(text)
        task_input.value = ""
        task_input.update()
        load_task()

    def clear_completed(f):
        main_db.delete_complete_tasks()
        load_task()


    task_input = ft.TextField(label="Введите задачу", expand=True, max_length=100)
    add_button = ft.ElevatedButton("ADD", on_click=add_task)


    sort_new_first = ft.ElevatedButton("📅 Новые выше", on_click=lambda _: load_task("date_desc"))
    sort_old_first = ft.ElevatedButton("📅 Старые выше", on_click=lambda _: load_task("date_asc"))
    sort_done_bottom = ft.ElevatedButton("✅ Выполненные внизу", on_click=lambda _: load_task("status_bottom"))
    sort_done_top = ft.ElevatedButton("✅ Выполненные вверху", on_click=lambda _: load_task("status_top"))
    clear_button = ft.ElevatedButton("🗑️ Очистить выполненные", on_click=clear_completed)


    page.add(
        ft.Column(
            [
                ft.Row([task_input, add_button]),
                ft.Row([sort_new_first, sort_old_first, sort_done_bottom, sort_done_top, clear_button]),
                task_list,
            ]
        )
    )

    load_task()

if __name__ == "__main__":
    main_db.init_db()
    ft.app(target=main)

