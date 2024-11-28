import flet as ft


class AdminView:
    def __init__(self, page):
        self.page = page
        self.content = ft.Text("Добро пожаловать в панель администратора!")

    def update_content(self, text):
        self.content.value = text
        self.page.update()

    def get_view(self):
        return ft.View(
            "/admin",
            controls=[
                ft.Row(
                    [
                        ft.Column(
                            [
                                ft.TextButton(
                                    "Управление пользователями",
                                    on_click=lambda _: self.update_content(
                                        "Управление пользователями"
                                    ),
                                ),
                                ft.TextButton(
                                    "Настройки",
                                    on_click=lambda _: self.update_content(
                                        "Настройки панели администратора"
                                    ),
                                ),
                            ]
                        ),
                        ft.Container(
                            content=self.content,
                            expand=True,
                            alignment=ft.alignment.center,
                        ),
                    ]
                )
            ],
        )
