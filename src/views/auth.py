import flet as ft

from connection import get_connection
from state import AppState

from .base import BaseView
from .providers import user_provider as provider


class AuthView(BaseView):
    _show_registration_form = False

    username_ref = ft.Ref[ft.TextField]()
    password_ref = ft.Ref[ft.TextField]()

    reg_username_ref = ft.Ref[ft.TextField]()
    reg_password_ref = ft.Ref[ft.TextField]()
    confirm_password_ref = ft.Ref[ft.TextField]()
    first_name_ref = ft.Ref[ft.TextField]()
    last_name_ref = ft.Ref[ft.TextField]()
    age_ref = ft.Ref[ft.TextField]()
    photo_url_ref = ft.Ref[ft.TextField]()
    hobbies_ref = ft.Ref[ft.TextField]()
    occupation_ref = ft.Ref[ft.TextField]()
    description_ref = ft.Ref[ft.TextField]()
    country_ref = ft.Ref[ft.TextField]()
    city_ref = ft.Ref[ft.TextField]()

    def _toggle_form(self, e: ft.ControlEvent) -> None:
        self._show_registration_form = not self._show_registration_form
        self.page.views[-1] = self.get_view()
        self.page.update()

    def get_view(self) -> ft.View:
        title_text = ft.Container(
            content=ft.Text(
                "Register" if self._show_registration_form else "Login",
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
                    self._handle_register
                    if self._show_registration_form
                    else self._handle_login
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
                if self._show_registration_form
                else "Don't have an account?"
            ),
            on_click=self._toggle_form,
            style=ft.ButtonStyle(
                color=ft.Colors.BLACK54,
            ),
        )

        login_form = ft.Column(
            [
                title_text,
                ft.TextField(ref=self.username_ref, label="Username"),
                ft.TextField(
                    ref=self.password_ref, label="Password", password=True
                ),
                enter_button,
                text_button,
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )

        registration_form = ft.Column(
            [
                title_text,
                ft.Column(
                    [
                        ft.TextField(
                            ref=self.reg_username_ref, label="Username"
                        ),
                        ft.TextField(
                            ref=self.reg_password_ref,
                            label="Password",
                            password=True,
                        ),
                        ft.TextField(
                            ref=self.confirm_password_ref,
                            label="Confirm Password",
                            password=True,
                        ),
                        ft.TextField(
                            ref=self.first_name_ref, label="First Name"
                        ),
                        ft.TextField(
                            ref=self.last_name_ref, label="Last Name"
                        ),
                        ft.TextField(ref=self.age_ref, label="Age"),
                        ft.TextField(
                            ref=self.photo_url_ref, label="Photo URL"
                        ),
                        ft.TextField(
                            ref=self.hobbies_ref,
                            label="Hobbies",
                            multiline=True,
                            min_lines=2,
                        ),
                        ft.TextField(
                            ref=self.occupation_ref,
                            label="Occupation",
                            multiline=True,
                            min_lines=2,
                        ),
                        ft.TextField(
                            ref=self.description_ref,
                            label="Description",
                            multiline=True,
                            min_lines=2,
                        ),
                        ft.TextField(ref=self.country_ref, label="Country"),
                        ft.TextField(ref=self.city_ref, label="City"),
                    ],
                    scroll=ft.ScrollMode.AUTO,
                    expand=True,
                ),
                enter_button,
                text_button,
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )

        form_container = ft.Container(
            content=(
                registration_form
                if self._show_registration_form
                else login_form
            ),
            width=400,
            height=700 if self._show_registration_form else 330,
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

    def _handle_login(self, e: ft.ControlEvent) -> None:
        username = self.username_ref.current.value
        password = self.password_ref.current.value

        try:
            with get_connection() as connection:
                user = provider(connection).login(username, password)

            AppState.set("user", user)

            if user.role == "admin":
                self.page.go("/admin")
            else:
                self.page.go("/dashboard")

        except Exception as exc:
            print(str(exc))

            self.page.snack_bar = ft.SnackBar(
                content=ft.Text(str(exc)), open=True
            )
            self.page.update()

    def _handle_register(self, e: ft.ControlEvent) -> None:
        form_data = {
            field: ref.current.value
            for field, ref in {
                "username": self.reg_username_ref,
                "password": self.reg_password_ref,
                "confirm_password": self.confirm_password_ref,
                "first_name": self.first_name_ref,
                "last_name": self.last_name_ref,
                "age": self.age_ref,
                "photo_url": self.photo_url_ref,
                "hobbies": self.hobbies_ref,
                "occupation": self.occupation_ref,
                "description": self.description_ref,
                "country": self.country_ref,
                "city": self.city_ref,
            }.items()
        }

        try:
            with get_connection() as connection:
                provider(connection).registrate(**form_data)

            self.page.snack_bar = ft.SnackBar(
                content=ft.Text("Registration successful!"), open=True
            )
            self.page.update()
            self._toggle_form(None)

        except Exception as exc:
            print(str(exc))

            self.page.snack_bar = ft.SnackBar(
                content=ft.Text(str(exc)), open=True
            )
            self.page.update()
