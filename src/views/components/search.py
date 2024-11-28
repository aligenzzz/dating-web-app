from typing import Callable

import flet as ft


class SearchComponent:
    def __init__(self, on_search_change: Callable):
        self.on_search_change = on_search_change

    def get_view(self, search_query: str) -> ft.Row:
        return ft.Row(
            controls=[
                ft.Icon(ft.icons.SEARCH, color=ft.Colors.GREY),
                ft.TextField(
                    value=search_query,
                    width=300,
                    autofocus=True,
                    on_change=self.on_search_change,
                ),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=10,
        )
