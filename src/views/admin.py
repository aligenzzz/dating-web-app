import flet as ft

from connection import get_connection
from models import User
from state import AppState
from utils import format_datetime

from .base import BaseView
from .components import SearchComponent
from .providers import action_provider, complaint_provider, user_provider


class AdminView(BaseView):
    user = User()

    def __init__(self, page):
        self.page = page
        self.search_component = SearchComponent(self._on_search_change)
        self.content = ft.Container(ft.Text(""), expand=True)

    def _on_nav_change(self, index: int) -> None:
        if index == 0:
            self._show_users()
        elif index == 1:
            self._show_complaints()
        elif index == 2:
            self._show_actions()
        self.page.update()

    def _show_users(self, search_query: str = "") -> None:
        def submit(e, user_id: str) -> None:
            try:
                with get_connection() as connection:
                    user_provider(connection).ban_user(user_id)
            except Exception as exc:
                print(str(exc))
            self._show_users(search_query)

        with get_connection() as connection:
            users = user_provider(connection).get_users()

        filtered_users = [
            user
            for user in users
            if search_query.lower() in str(user.username).lower()
        ]

        user_list = ft.Column(
            spacing=10, expand=True, scroll=ft.ScrollMode.AUTO
        )

        for user in filtered_users:
            user_row = ft.Container(
                content=ft.Row(
                    [
                        ft.Column(
                            [
                                ft.Text(
                                    user.username,
                                    size=16,
                                    weight=ft.FontWeight.BOLD,
                                ),
                                ft.Text(
                                    (
                                        "Created at: "
                                        f"{format_datetime(user.created_at)}"
                                    ),
                                    size=14,
                                    color=ft.Colors.GREY,
                                ),
                                ft.Text(
                                    (
                                        "Banned"
                                        if user.is_banned
                                        else "Not banned"
                                    ),
                                    size=14,
                                    color=ft.Colors.GREY,
                                ),
                            ],
                            spacing=5,
                            expand=True,
                        ),
                        ft.IconButton(
                            icon=ft.icons.BLOCK,
                            icon_color=ft.colors.GREY,
                            on_click=lambda e, user_id=user.id: submit(
                                e, user_id
                            ),
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                ),
                padding=25,
                bgcolor="#f8f9ff",
                border_radius=20,
            )
            user_list.controls.append(user_row)

        self.content.content = ft.Container(
            ft.Column(
                [self.search_component.get_view(search_query), user_list],
                spacing=40,
            ),
            margin=20,
        )
        self.page.update()

    def _on_search_change(self, e) -> None:
        search_query = e.control.value
        self._show_users(search_query)

    def _show_complaints(self) -> None:
        def submit(e, complaint_id: str) -> None:
            try:
                with get_connection() as connection:
                    complaint_provider(connection).delete_complaint(
                        complaint_id
                    )
            except Exception as exc:
                print(str(exc))
            self._show_complaints()

        with get_connection() as connection:
            complaints = complaint_provider(connection).get_complaints()

        complaint_list = ft.Column(
            spacing=10, expand=True, scroll=ft.ScrollMode.AUTO
        )

        for complaint in complaints:
            complaint_row = ft.Container(
                content=ft.Row(
                    [
                        ft.Column(
                            [
                                ft.Text(
                                    complaint.content,
                                    size=16,
                                    weight=ft.FontWeight.BOLD,
                                ),
                                ft.Text(
                                    (
                                        "Posted at: "
                                        f"{format_datetime(complaint.posted_at)}"  # noqa: E501
                                    ),
                                    size=14,
                                    color=ft.Colors.GREY,
                                ),
                                ft.Text(
                                    f"User: {complaint.user.username}",
                                    size=14,
                                    color=ft.Colors.GREY,
                                ),
                            ],
                            spacing=5,
                            expand=True,
                        ),
                        ft.IconButton(
                            icon=ft.icons.DELETE,
                            icon_color=ft.colors.GREY,
                            on_click=lambda e, complaint_id=complaint.id: submit(  # noqa: E501
                                e, complaint_id
                            ),
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                ),
                padding=25,
                bgcolor="#f8f9ff",
                border_radius=20,
            )
            complaint_list.controls.append(complaint_row)

        self.content.content = ft.Container(
            content=complaint_list,
            margin=20,
            alignment=ft.alignment.top_left,
        )
        self.page.update()

    def _show_actions(self) -> None:
        with get_connection() as connection:
            actions = action_provider(connection).get_actions()

        action_list = ft.Column(
            spacing=10, expand=True, scroll=ft.ScrollMode.AUTO
        )

        for action in actions:
            action_row = ft.Container(
                content=ft.Row(
                    [
                        ft.Column(
                            [
                                ft.Text(
                                    action.name,
                                    size=16,
                                    weight=ft.FontWeight.BOLD,
                                ),
                                ft.Text(
                                    (
                                        "Completed at: "
                                        f"{format_datetime(action.completed_at)}"  # noqa: E501
                                    ),
                                    size=14,
                                    color=ft.Colors.GREY,
                                ),
                                ft.Text(
                                    f"User: {action.user.username}",
                                    size=14,
                                    color=ft.Colors.GREY,
                                ),
                            ],
                            spacing=5,
                            expand=True,
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                ),
                padding=25,
                bgcolor="#f8f9ff",
                border_radius=20,
            )
            action_list.controls.append(action_row)

        self.content.content = ft.Container(
            content=action_list,
            margin=20,
            alignment=ft.alignment.top_left,
        )
        self.page.update()

    def get_view(self) -> ft.View:
        self.user = AppState.get("user")

        navigation_items = [
            ft.NavigationRailDestination(icon=ft.icons.PEOPLE, label="Users"),
            ft.NavigationRailDestination(
                icon=ft.icons.ANNOUNCEMENT, label="Complaints"
            ),
            ft.NavigationRailDestination(
                icon=ft.icons.CHECKLIST, label="Actions"
            ),
        ]

        navigation = ft.Container(
            content=ft.Column(
                [
                    ft.NavigationRail(
                        selected_index=0,
                        label_type=ft.NavigationRailLabelType.ALL,
                        destinations=navigation_items,
                        on_change=lambda e: self._on_nav_change(
                            e.control.selected_index
                        ),
                        expand=True,
                        bgcolor="#f8f9ff",
                    ),
                ],
                expand=True,
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            ),
            bgcolor="#f8f9ff",
        )

        self._on_nav_change(0)

        rounded_container = ft.Container(
            content=ft.Row([navigation, self.content], expand=True),
            margin=10,
            border_radius=20,
            bgcolor=ft.Colors.WHITE,
            shadow=ft.BoxShadow(
                blur_radius=10,
                spread_radius=2,
                color=ft.Colors.with_opacity(0.2, ft.Colors.BLACK),
            ),
        )

        return ft.View(
            "/admin",
            [
                ft.Stack(
                    [
                        self.get_base_component(),
                        rounded_container,
                    ],
                    expand=True,
                )
            ],
            padding=0,
            spacing=0,
        )
