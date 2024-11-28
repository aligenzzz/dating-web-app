import flet as ft

from .base import BaseView


class AuthView(BaseView):
    show_registration_form = False

    def toggle_form(self, e):
        self.show_registration_form = not self.show_registration_form
        self.page.views[-1] = self.get_view()
        self.page.update()

    def get_view(self):
        title_text = ft.Container(
            content=ft.Text(
                "Register" if self.show_registration_form else "Login",
                theme_style=ft.TextThemeStyle.HEADLINE_MEDIUM,
                color="#9d528a",
                weight="bold",
            ),
            padding=ft.Padding(0, 0, 0, 10),
        )

        enter_button = ft.Container(
            content=ft.ElevatedButton(
                "Enter",
                on_click=(
                    self.handle_register
                    if self.show_registration_form
                    else self.handle_login
                ),
                style=ft.ButtonStyle(
                    color=ft.Colors.BLACK, bgcolor=ft.Colors.WHITE
                ),
            ),
            alignment=ft.alignment.center,
        )

        text_button = ft.TextButton(
            (
                "Already have an account?"
                if self.show_registration_form
                else "Don't have an account?"
            ),
            on_click=self.toggle_form,
            style=ft.ButtonStyle(
                color=ft.Colors.BLACK54,
            ),
        )

        login_form = ft.Column(
            [
                title_text,
                ft.TextField(label="Username"),
                ft.TextField(label="Password", password=True),
                enter_button,
                text_button,
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )

        registration_form = ft.Column(
            [
                title_text,
                ft.TextField(label="Username"),
                ft.TextField(label="Password", password=True),
                ft.TextField(label="Confirm Password", password=True),
                enter_button,
                text_button,
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )

        form_container = ft.Container(
            content=(
                registration_form
                if self.show_registration_form
                else login_form
            ),
            width=400,
            height=400 if self.show_registration_form else 330,
            padding=20,
            margin=20,
            bgcolor=ft.Colors.WHITE,
            border_radius=15,
            alignment=ft.alignment.center,
            shadow=ft.BoxShadow(blur_radius=10, color=ft.Colors.BLACK12),
        )

        centered_container = ft.Container(
            content=form_container, expand=True, alignment=ft.alignment.center
        )

        return ft.View(
            "/",
            [
                ft.Stack(
                    [self.get_base_component(), centered_container],
                    expand=True,
                )
            ],
            padding=0,
            spacing=0,
        )

    def handle_login(self, e):
        self.page.go("/dashboard")

    def handle_register(self, e):
        self.page.go("/admin")
