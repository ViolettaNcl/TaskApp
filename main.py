from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
from kivymd.uix.screen import MDScreen
from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.core.window import Window
from datetime import datetime
from database import Database

Window.size = (500, 500)
db = Database()

class MainScreen(MDScreen):
    pass

class AddTaskScreen(MDScreen):
    def add_task(self):
        client = self.ids.client.text
        description = self.ids.description.text
        if client and description:
            db.add_task(client, description)
            self.show_notification("Задача добавлена")
            self.clear_fields()  
            self.manager.current = "main"
        else:
            self.show_notification("Пожалуйста, убедитесь, что все поля заполнены корректно!")

    def go_back(self):
        self.clear_fields()
        self.manager.current = "main"

    def show_notification(self, message):
        dialog = MDDialog(
            text=message,
            buttons=[
                MDFlatButton(
                    text="OK",
                    on_release=lambda *args: dialog.dismiss()
                )
            ]
        )
        dialog.open()

    def clear_fields(self):
        self.ids.client.text = ""
        self.ids.description.text = ""

class UpdateTaskScreen(MDScreen):
    def update_task(self):
        task_id = self.ids.task_id.text
        manager = self.ids.manager.text
        executor = self.ids.executor.text
        start_date = self.ids.start_date.text
        deadline = self.ids.deadline.text

        try:
            datetime.strptime(start_date, '%Y-%m-%d')
            datetime.strptime(deadline, '%Y-%m-%d')
        except ValueError:
            self.show_notification("Пожалуйста, убедитесь, что все поля заполнены корректно!")
            return

        if task_id.isdigit() and manager and executor and start_date and deadline:
            db.update_task(int(task_id), manager, executor, start_date, deadline)
            self.show_notification("Задача обновлена")
            self.clear_fields()  
            self.manager.current = "main"
        else:
            self.show_notification("ID задачи должно быть числом")

    def go_back(self):
        self.clear_fields()
        self.manager.current = "main"

    def show_notification(self, message):
        dialog = MDDialog(
            text=message,
            buttons=[
                MDFlatButton(
                    text="OK",
                    on_release=lambda *args: dialog.dismiss()
                )
            ]
        )
        dialog.open()

    def clear_fields(self):
        self.ids.task_id.text = ""
        self.ids.manager.text = ""
        self.ids.executor.text = ""
        self.ids.start_date.text = ""
        self.ids.deadline.text = ""

class CompleteTaskScreen(MDScreen):
    def complete_task(self):
        task_id = self.ids.task_id.text
        if task_id.isdigit():
            completed_at = db.is_task_completed(int(task_id))
            if completed_at:
                self.show_notification(f"Задача уже была завершена {completed_at.strftime('%Y-%m-%d %H:%M:%S')}")
            else:
                self.show_confirmation_dialog(int(task_id))
        else:
            self.show_notification("ID задачи должно быть числом")

    def show_confirmation_dialog(self, task_id):
        dialog = MDDialog(
            text="Задача еще не завершена. Точно ее завершить?",
            buttons=[
                MDFlatButton(
                    text="ДА",
                    on_release=lambda *args: self.confirm_completion(dialog, task_id)
                ),
                MDFlatButton(
                    text="ОТМЕНА",
                    on_release=lambda *args: dialog.dismiss()
                )
            ]
        )
        dialog.open()

    def confirm_completion(self, dialog, task_id):
        db.complete_task(task_id)
        self.show_notification("Задача завершена")
        self.clear_fields()
        self.manager.current = "main"
        dialog.dismiss()

    def go_back(self):
        self.clear_fields()
        self.manager.current = "main"

    def show_notification(self, message):
        dialog = MDDialog(
            text=message,
            buttons=[
                MDFlatButton(
                    text="OK",
                    on_release=lambda *args: dialog.dismiss()
                )
            ]
        )
        dialog.open()

    def clear_fields(self):
        self.ids.task_id.text = ""

class ExecutorTaskScreen(MDScreen):
    def complete_task(self):
        executor = self.ids.executor.text
        task_id = self.ids.task_id.text
        if task_id.isdigit():
            completed_at = db.is_task_completed(int(task_id))
            if completed_at:
                self.show_notification(f"Задача уже была завершена {completed_at.strftime('%Y-%m-%d %H:%M:%S')}")
            else:
                self.show_confirmation_dialog(int(task_id))
        else:
            self.show_notification("Пожалуйста, убедитесь, что все поля заполнены корректно!")

    def show_confirmation_dialog(self, task_id):
        dialog = MDDialog(
            text="Задача еще не завершена. Точно ее завершить?",
            buttons=[
                MDFlatButton(
                    text="ДА",
                    on_release=lambda *args: self.confirm_completion(dialog, task_id)
                ),
                MDFlatButton(
                    text="ОТМЕНА",
                    on_release=lambda *args: dialog.dismiss()
                )
            ]
        )
        dialog.open()

    def confirm_completion(self, dialog, task_id):
        db.complete_task(task_id)
        executor = self.ids.executor.text
        tasks = db.get_tasks_by_executor(executor)
        if tasks:
            self.show_notification(f"У исполнителя {executor} осталось {len(tasks)} задач(и)")
        else:
            self.show_notification("Нет задач для данного исполнителя")
        self.clear_fields()
        dialog.dismiss()

    def go_back(self):
        self.clear_fields()
        self.manager.current = "main"

    def show_notification(self, message):
        dialog = MDDialog(
            text=message,
            buttons=[
                MDFlatButton(
                    text="OK",
                    on_release=lambda *args: dialog.dismiss()
                )
            ]
        )
        dialog.open()

    def clear_fields(self):
        self.ids.executor.text = ""
        self.ids.task_id.text = ""

class AssignTaskScreen(MDScreen):
    def assign_task(self):
        task_id = self.ids.task_id.text
        manager = self.ids.manager.text
        executor = self.ids.executor.text
        start_date = self.ids.start_date.text
        deadline = self.ids.deadline.text

        try:
            datetime.strptime(start_date, '%Y-%m-%d')
            datetime.strptime(deadline, '%Y-%m-%d')
        except ValueError:
            self.show_notification("Пожалуйста, убедитесь, что все поля заполнены корректно!")
            return

        if task_id.isdigit() and manager and executor and start_date and deadline:
            db.update_task(int(task_id), manager, executor, start_date, deadline)
            self.show_notification("Задача назначена")
            self.clear_fields()  
            self.manager.current = "main"
        else:
            self.show_notification("ID задачи должно быть числом")

    def go_back(self):
        self.clear_fields()
        self.manager.current = "main"

    def show_notification(self, message):
        dialog = MDDialog(
            text=message,
            buttons=[
                MDFlatButton(
                    text="OK",
                    on_release=lambda *args: dialog.dismiss()
                )
            ]
        )
        dialog.open()

    def clear_fields(self):
        self.ids.task_id.text = ""
        self.ids.manager.text = ""
        self.ids.executor.text = ""
        self.ids.start_date.text = ""
        self.ids.deadline.text = ""

class TaskManagerApp(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "Purple"
        self.theme_cls.primary_hue = "200"
        return Builder.load_file("task_manager.kv")

if __name__ == '__main__':
    TaskManagerApp().run()
