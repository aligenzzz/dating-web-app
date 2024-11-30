import flet as ft

from config import settings
from connection import get_connection
from views import AdminView, AuthView, DashboardView


def init_db(init_file_path: str) -> None:
    with get_connection() as connection:
        with connection.cursor() as cursor:
            with open(init_file_path, "r", encoding="utf-8") as file:
                sql_script = file.read()
                cursor.execute(sql_script)


def main(page: ft.Page) -> None:
    page.title = "Dating Agency"
    page.fonts = {
        "B612": "https://raw.githubusercontent.com/google/fonts/master/ofl/b612/B612-Regular.ttf",  # noqa: E501
    }
    page.theme = ft.Theme(font_family="B612")
    page.theme_mode = ft.ThemeMode.LIGHT
    page.bgcolor = ft.Colors.TRANSPARENT
    page.padding = 0
    page.spacing = 0
    page.adaptive = True
    page.theme.page_transitions.windows = "cupertino"

    def route_change(e) -> None:
        page.views.clear()
        page.views.append(AuthView(page).get_view())
        if page.route == "/dashboard":
            page.views.append(DashboardView(page).get_view())
        elif page.route == "/admin":
            page.views.append(AdminView(page).get_view())
        page.update()

    def view_pop(e) -> None:
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)

    page.on_route_change = route_change
    page.on_view_pop = view_pop

    page.go(page.route)


init_db("./src/scripts/init.sql")

ft.app(
    target=main,
    view=ft.AppView.WEB_BROWSER,
    port=settings.PORT,
    host=settings.HOST,
)
