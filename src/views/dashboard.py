import flet as ft

from .base import BaseView
from .components import SearchComponent

USERS = [
    {
        "name": "Иван Иванов",
        "age": 30,
        "location": "Москва",
        "avatar": "https://avatars.githubusercontent.com/u/5041459?s=88&v=4",
    },
    {
        "name": "Петр Петров",
        "age": 25,
        "location": "Санкт-Петербург",
        "avatar": "https://avatars.githubusercontent.com/u/5041459?s=88&v=4",
    },
    {
        "name": "Анна Смирнова",
        "age": 28,
        "location": "Екатеринбург",
        "avatar": "https://avatars.githubusercontent.com/u/5041459?s=88&v=4",
    },
    {
        "name": "Ольга Кузнецова",
        "age": 32,
        "location": "Новосибирск",
        "avatar": "https://avatars.githubusercontent.com/u/5041459?s=88&v=4",
    },
]

EXISTING_CHATS = [
    {
        "name": "Иван Иванов",
        "last_message": "Привет, как дела?",
        "time": "14:30",
        "messages": [
            {"sender": "Иван", "text": "Привет!", "time": "14:00"},
            {"sender": "Вы", "text": "Как дела?", "time": "14:05"},
        ],
    },
]
EXISTING_MEETINGS = []


class DashboardView(BaseView):
    def __init__(self, page):
        self.page = page

        self.search_component = SearchComponent(self.on_search_change)
        self.content = ft.Container(ft.Text(""), expand=True)
        self.show_users()

    def on_nav_change(self, index: int) -> None:
        if index == 0:
            self.show_users()
        elif index == 1:
            self.show_chats()
        elif index == 2:
            self.show_meetings()
        self.page.update()

    def show_user_info(self, user):
        user_info = ft.Column(
            [
                ft.CircleAvatar(
                    foreground_image_src=user["avatar"],
                    width=150,
                    height=150,
                    content=ft.Text(user["name"][0], size=50),
                ),
                ft.Text(user["name"], size=24, weight=ft.FontWeight.BOLD),
                ft.Text(f"Возраст: {user['age']}", size=20),
                ft.Text(f"Местоположение: {user['location']}", size=20),
                ft.Row(
                    [
                        ft.ElevatedButton(
                            text="Add chat",
                            style=ft.ButtonStyle(
                                bgcolor="#5783b0",
                                color="#f8f9ff",
                            ),
                            on_click=lambda e: self.show_add_chat_form(user),
                        ),
                        ft.ElevatedButton(
                            text="Add meeting",
                            style=ft.ButtonStyle(
                                bgcolor="#5783b0",
                                color="#f8f9ff",
                            ),
                            on_click=lambda e: self.show_add_meeting_form(
                                user
                            ),
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=20,
                ),
                ft.TextButton(
                    "Close",
                    on_click=self.close_user_info,
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

    def show_add_chat_form(self, user):
        if user["name"] in EXISTING_CHATS:
            self.page.snack_bar = ft.SnackBar(
                ft.Text(f"Чат с {user['name']} уже существует!"), open=True
            )
        else:
            EXISTING_CHATS.append(user["name"])
            self.page.snack_bar = ft.SnackBar(
                ft.Text(f"Чат с {user['name']} создан!"), open=True
            )
        self.page.update()

    def show_add_meeting_form(self, user):
        def submit_meeting(e):
            EXISTING_MEETINGS.append(user["name"])
            self.page.dialog.open = False
            self.page.snack_bar = ft.SnackBar(
                ft.Text(f"Встреча с {user['name']} создана!"), open=True
            )
            self.page.update()

        meeting_form = ft.AlertDialog(
            title=ft.Text(f"Добавление встречи с {user['name']}"),
            content=ft.Column(
                [
                    ft.TextField(label="Дата встречи"),
                    ft.TextField(label="Описание"),
                ],
                spacing=20,
            ),
            actions=[
                ft.TextButton(
                    "Отменить", on_click=lambda e: self.close_dialog()
                ),
                ft.TextButton("Создать", on_click=submit_meeting),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )

        self.page.dialog = meeting_form
        meeting_form.open = True
        self.page.update()

    def close_dialog(self):
        self.page.dialog.open = False
        self.page.update()

    def close_user_info(self, e):
        self.show_users()

    def show_users(self, search_query: str = ""):
        filtered_users = [
            user
            for user in USERS
            if search_query.lower() in str(user["name"]).lower()
            or search_query.lower() in str(user["age"]).lower()
            or search_query.lower() in str(user["location"]).lower()
        ]

        user_list = ft.Row(
            wrap=True,
            scroll=ft.ScrollMode.AUTO,
        )

        for user in filtered_users:
            user_tile = ft.Container(
                content=ft.Column(
                    [
                        ft.CircleAvatar(
                            foreground_image_src=user["avatar"],
                            content=ft.Text("N"),
                            width=75,
                            height=75,
                        ),
                        ft.Text(user["name"]),
                        ft.Text(f"Возраст: {user['age']}"),
                        ft.Text(f"Местоположение: {user['location']}"),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                padding=20,
                on_click=lambda e, user=user: self.show_user_info(user),
                bgcolor="#f8f9ff",
                border_radius=20,
            )
            user_list.controls.append(user_tile)

        self.content.content = ft.Container(
            ft.Column(
                [self.search_component.get_view(search_query), user_list],
                spacing=40,
            ),
            margin=20,
        )
        self.page.update()

    def on_search_change(self, e):
        search_query = e.control.value
        self.show_users(search_query)

    def show_chats(self):
        chat_list = ft.Column(spacing=10)

        for chat in EXISTING_CHATS:
            chat_row = ft.Container(
                content=ft.Row(
                    [
                        ft.CircleAvatar(
                            foreground_image_src="https://avatars.githubusercontent.com/u/5041459?s=88&v=4",  # noqa: E501
                            width=50,
                            height=50,
                        ),
                        ft.Column(
                            [
                                ft.Text(
                                    chat["name"],
                                    size=18,
                                    weight=ft.FontWeight.BOLD,
                                ),
                                ft.Text(
                                    chat["last_message"],
                                    size=14,
                                    color=ft.Colors.GREY,
                                ),
                            ],
                            spacing=5,
                        ),
                        ft.Text(chat["time"], size=12, color=ft.Colors.GREY),
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                padding=10,
                on_click=lambda e, chat=chat: self.open_chat(chat),
                bgcolor="#f8f9ff",
                border_radius=10,
            )
            chat_list.controls.append(chat_row)

        self.content.content = chat_list
        self.page.update()

    def open_chat(self, chat):
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

    def send_message(self, chat, message_input):
        new_message = {
            "sender": "Вы",
            "text": message_input.value,
            "time": "14:45",
        }
        chat["messages"].append(new_message)
        message_input.value = ""
        self.open_chat(chat)

    def show_meetings(self):
        self.content.content = ft.Column(
            [
                ft.Text("Встречи"),
                ft.Text("Встреча 1"),
                ft.Text("Встреча 2"),
            ]
        )

    def get_view(self):
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
                    foreground_image_src="https://avatars.githubusercontent.com/u/5041459?s=88&v=4",  # noqa: E501
                    content=ft.Text("N"),
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
                        on_change=lambda e: self.on_nav_change(
                            e.control.selected_index
                        ),
                        expand=True,
                        bgcolor="#f8f9ff",
                    ),
                    ft.Container(
                        avatar,
                        alignment=ft.alignment.center,
                        padding=20,
                        on_click=lambda e: self.on_nav_change(3),
                    ),
                ],
                expand=True,
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            ),
            bgcolor="#f8f9ff",
        )

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
