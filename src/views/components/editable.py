from typing import Any, Callable

import flet as ft


class EditableComponent:
    def __init__(
        self,
        label: str,
        max_length: int,
        value: Any,
        submit: Callable,
        ref: ft.Ref[ft.TextField],
        min_lines: int = 1,
    ):
        self.label = label
        self.max_length = max_length
        self.value = value
        self.submit = submit
        self.ref = ref
        self.min_lines = min_lines

    def get_view(self) -> ft.Row:
        return ft.Row(
            [
                ft.TextField(
                    label=self.label,
                    value=str(self.value),
                    max_length=self.max_length,
                    ref=self.ref,
                    min_lines=self.min_lines,
                    multiline=(self.min_lines != 1),
                ),
                ft.IconButton(
                    icon=ft.icons.EDIT,
                    on_click=lambda e: self.submit(e),
                    icon_color="#9d528a",
                ),
            ],
            spacing=10,
            alignment=ft.MainAxisAlignment.CENTER,
        )
