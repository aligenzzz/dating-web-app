import flet as ft


class BaseView:
    def __init__(self, page: ft.Page):
        self.page = page

    def get_base_component(self) -> ft.Container:
        return ft.Container(
            expand=True,
            gradient=ft.LinearGradient(
                begin=ft.alignment.top_left,
                end=ft.alignment.bottom_right,
                colors=["#5783b0", "#6977a7", "#7a6a9d", "#8c5e94", "#9d528a"],
            ),
        )
