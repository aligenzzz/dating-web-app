from datetime import datetime, timedelta

import flet as ft

from connection import get_connection
from models import Profile, User
from state import AppState

from .base import BaseView
from .components import SearchComponent
from .providers import chat_provider, meeting_provider, profile_provider


class DashboardView(BaseView):
    user = User()
    profile = Profile()

    chat_name_ref = ft.Ref[ft.TextField]()
    chat_image_url_ref = ft.Ref[ft.TextField]()

    meeting_name_ref = ft.Ref[ft.TextField]()
    meeting_country_ref = ft.Ref[ft.TextField]()
    meeting_city_ref = ft.Ref[ft.TextField]()
    meeting_address_ref = ft.Ref[ft.TextField]()

    def __init__(self, page):
        self.page = page
        self.search_component = SearchComponent(self._on_search_change)
        self.content = ft.Container(ft.Text(""), expand=True)

    def _on_nav_change(self, index: int) -> None:
        if index == 0:
            self._show_profiles()
        elif index == 1:
            self.show_chats()
        elif index == 2:
            self.show_meetings()
        self.page.update()

    def _show_profile(self, profile: Profile) -> None:
        user_info = ft.Column(
            [
                ft.CircleAvatar(
                    foreground_image_src=profile.photo_url,
                    width=150,
                    height=150,
                    content=ft.Text(profile.full_name[0], size=50),
                ),
                ft.Text(profile.full_name, size=24, weight=ft.FontWeight.BOLD),
                ft.Text(f"Age: {profile.age}", size=20),
                ft.Text(f"Location: {profile.location}", size=20),
                ft.Text(f"Hobbies: {profile.hobbies}", size=20),
                ft.Text(f"Occupation: {profile.occupation}", size=20),
                ft.Text(f"Decription: {profile.description}", size=20),
                ft.Row(
                    [
                        ft.ElevatedButton(
                            text="Create chat",
                            style=ft.ButtonStyle(
                                bgcolor="#5783b0",
                                color="#f8f9ff",
                            ),
                            on_click=lambda e, profile=profile: self._show_chat_form(  # noqa: E501
                                profile
                            ),
                        ),
                        ft.ElevatedButton(
                            text="Create meeting",
                            style=ft.ButtonStyle(
                                bgcolor="#5783b0",
                                color="#f8f9ff",
                            ),
                            on_click=lambda e, profile=profile: self._show_meeting_form(  # noqa: E501
                                profile
                            ),
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=20,
                ),
                ft.TextButton(
                    "Close",
                    on_click=self._close_profile,
                    style=ft.ButtonStyle(
                        color="#9d528a",
                    ),
                ),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=20,
        )

        self.content.content = ft.Container(
            content=user_info,
            alignment=ft.alignment.center,
            padding=20,
        )
        self.page.update()

    def _show_chat_form(self, profile: Profile) -> None:
        def submit(e):
            name = self.chat_name_ref.current.value
            image_url = self.chat_image_url_ref.current.value

            try:
                with get_connection() as connection:
                    chat_provider(connection).add_chat(
                        name, image_url, self.user.id, profile.id
                    )

                self.page.dialog.open = False
                self.page.snack_bar = ft.SnackBar(
                    ft.Text(f"Chat with {profile.full_name} was created!"),
                    open=True,
                )

            except Exception as exc:
                print(str(exc))
                self.page.snack_bar = ft.SnackBar(
                    content=ft.Text(str(exc)), open=True
                )

            self.page.update()

        chat_form = ft.AlertDialog(
            title=ft.Text(f"Chat creation with {profile.full_name}:"),
            content=ft.Column(
                [
                    ft.TextField(ref=self.chat_name_ref, label="Name"),
                    ft.TextField(
                        ref=self.chat_image_url_ref, label="Image URL"
                    ),
                ],
                spacing=20,
                height=200,
            ),
            actions=[
                ft.TextButton(
                    "Cancel", on_click=lambda e: self._close_dialog()
                ),
                ft.TextButton("Create", on_click=submit),
            ],
        )

        self.page.dialog = chat_form
        chat_form.open = True
        self.page.update()

    def _show_meeting_form(self, profile: Profile) -> None:
        def submit(e):
            name = self.meeting_name_ref.current.value
            country = self.meeting_country_ref.current.value
            city = self.meeting_city_ref.current.value
            address = self.meeting_address_ref.current.value

            held_at_date = date_picker.value
            held_at_time = time_picker.value

            try:
                with get_connection() as connection:
                    meeting_provider(connection).add_meeting(
                        name,
                        held_at_date,
                        held_at_time,
                        country,
                        city,
                        address,
                        self.user.id,
                        profile.id,
                    )

                self.page.dialog.open = False
                self.page.snack_bar = ft.SnackBar(
                    ft.Text(f"Meeting with {profile.full_name} was created!"),
                    open=True,
                )

            except Exception as exc:
                print(str(exc))
                self.page.snack_bar = ft.SnackBar(
                    content=ft.Text(str(exc)), open=True
                )

            self.page.update()

        date_picker = ft.DatePicker(
            first_date=datetime.now(),
            last_date=datetime.now() + timedelta(days=365),
        )
        time_picker = ft.TimePicker()

        meeting_form = ft.AlertDialog(
            title=ft.Text(f"Meeting creation with {profile.full_name}:"),
            content=ft.Column(
                [
                    ft.TextField(ref=self.meeting_name_ref, label="Name"),
                    ft.Row(
                        [
                            ft.ElevatedButton(
                                "Pick date",
                                icon=ft.Icons.CALENDAR_MONTH,
                                on_click=lambda e: self.page.open(date_picker),
                            ),
                            ft.ElevatedButton(
                                "Pick time",
                                icon=ft.Icons.TIMER,
                                on_click=lambda e: self.page.open(time_picker),
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                    ),
                    ft.TextField(
                        ref=self.meeting_country_ref, label="Country"
                    ),
                    ft.TextField(ref=self.meeting_city_ref, label="City"),
                    ft.TextField(
                        ref=self.meeting_address_ref, label="Address"
                    ),
                ],
                spacing=20,
                height=400,
            ),
            actions=[
                ft.TextButton(
                    "Cancel", on_click=lambda e: self._close_dialog()
                ),
                ft.TextButton("Create", on_click=submit),
            ],
        )

        self.page.dialog = meeting_form
        meeting_form.open = True
        self.page.update()

    def _close_dialog(self) -> None:
        self.page.dialog.open = False
        self.page.update()

    def _close_profile(self, e) -> None:
        self._show_profiles()

    def _show_profiles(self, search_query: str = "") -> None:
        with get_connection() as connection:
            profiles = profile_provider(connection).get_profiles_exclude_one(
                self.profile.id
            )

        filtered_profiles = [
            profile
            for profile in profiles
            if search_query.lower() in str(profile.full_name).lower()
            or search_query.lower() in str(profile.age).lower()
            or search_query.lower() in str(profile.location).lower()
        ]

        profile_list = ft.Row(
            wrap=True,
            scroll=ft.ScrollMode.AUTO,
        )

        for profile in filtered_profiles:
            profile_tile = ft.Container(
                content=ft.Column(
                    [
                        ft.CircleAvatar(
                            foreground_image_src=profile.photo_url,
                            content=ft.Text(profile.full_name[0]),
                            width=75,
                            height=75,
                        ),
                        ft.Text(profile.full_name),
                        ft.Text(f"Age: {profile.age}"),
                        ft.Text(f"Location: {profile.location}"),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                padding=20,
                on_click=lambda e, profile=profile: self._show_profile(
                    profile
                ),
                bgcolor="#f8f9ff",
                border_radius=20,
            )
            profile_list.controls.append(profile_tile)

        self.content.content = ft.Container(
            ft.Column(
                [self.search_component.get_view(search_query), profile_list],
                spacing=40,
            ),
            margin=20,
        )
        self.page.update()

    def _on_search_change(self, e) -> None:
        search_query = e.control.value
        self._show_profiles(search_query)

    def show_chats(self) -> None:
        pass
        # chat_list = ft.Column(spacing=10)

        # for chat in EXISTING_CHATS:
        #     chat_row = ft.Container(
        #         content=ft.Row(
        #             [
        #                 ft.CircleAvatar(
        #                     foreground_image_src="https://avatars.githubusercontent.com/u/5041459?s=88&v=4",  # noqa: E501
        #                     width=50,
        #                     height=50,
        #                 ),
        #                 ft.Column(
        #                     [
        #                         ft.Text(
        #                             chat["name"],
        #                             size=18,
        #                             weight=ft.FontWeight.BOLD,
        #                         ),
        #                         ft.Text(
        #                             chat["last_message"],
        #                             size=14,
        #                             color=ft.Colors.GREY,
        #                         ),
        #                     ],
        #                     spacing=5,
        #                 ),
        #                 ft.Text(chat["time"], size=12, color=ft.Colors.GREY),
        #             ],
        #             alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        #             vertical_alignment=ft.CrossAxisAlignment.CENTER,
        #         ),
        #         padding=10,
        #         on_click=lambda e, chat=chat: self.open_chat(chat),
        #         bgcolor="#f8f9ff",
        #         border_radius=10,
        #     )
        #     chat_list.controls.append(chat_row)

        # self.content.content = chat_list
        # self.page.update()

    def open_chat(self, chat) -> None:
        messages_list = ft.Column(
            controls=[
                ft.Container(
                    content=ft.Text(
                        f"{message['sender']}: {message['text']} "
                        f"({message['time']})"
                    ),
                    alignment=(
                        ft.alignment.center_right
                        if message["sender"] == "Вы"
                        else ft.alignment.center_left
                    ),
                    padding=10,
                    bgcolor=(
                        "#e8f0fe" if message["sender"] == "Вы" else "#f1f3f4"
                    ),
                    border_radius=10,
                )
                for message in chat["messages"]
            ],
            scroll=ft.ScrollMode.AUTO,
        )

        message_input = ft.TextField(
            hint_text="Введите сообщение...", expand=True
        )

        send_button = ft.IconButton(
            icon=ft.icons.SEND,
            on_click=lambda e: self.send_message(chat, message_input),
        )

        self.content.content = ft.Column(
            [
                ft.Container(messages_list, expand=True),
                ft.Row([message_input, send_button]),
            ],
            expand=True,
        )
        self.page.update()

    def send_message(self, chat, message_input) -> None:
        new_message = {
            "sender": "Вы",
            "text": message_input.value,
            "time": "14:45",
        }
        chat["messages"].append(new_message)
        message_input.value = ""
        self.open_chat(chat)

    def show_meetings(self) -> None:
        self.content.content = ft.Column(
            [
                ft.Text("Встречи"),
                ft.Text("Встреча 1"),
                ft.Text("Встреча 2"),
            ]
        )

    def get_view(self) -> ft.View:
        self.user = AppState.get("user")

        with get_connection() as connection:
            self.profile = profile_provider(connection).get_profile(
                self.user.profile_id
            )

        navigation_items = [
            ft.NavigationRailDestination(icon=ft.icons.PEOPLE, label="Users"),
            ft.NavigationRailDestination(icon=ft.icons.CHAT, label="Chats"),
            ft.NavigationRailDestination(
                icon=ft.icons.EVENT, label="Meetings"
            ),
        ]

        avatar = ft.Stack(
            [
                ft.CircleAvatar(
                    foreground_image_src=self.profile.photo_url,
                    content=ft.Text(self.profile.full_name[0]),
                ),
                ft.Container(
                    content=ft.CircleAvatar(bgcolor=ft.Colors.GREEN, radius=5),
                    alignment=ft.alignment.bottom_left,
                ),
            ],
            width=40,
            height=40,
        )

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
                    ft.Container(
                        avatar,
                        alignment=ft.alignment.center,
                        padding=20,
                        on_click=lambda e: self._on_nav_change(3),
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
            "/dashboard",
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
