import re

from models import Chat
from repositories import ChatRepository, UserRepository


class ChatService:
    def __init__(
        self,
        chat_repository: ChatRepository,
        user_repository: UserRepository,
    ):
        self._chat_repository = chat_repository
        self._user_repository = user_repository

    def add_chat(
        self,
        name: str,
        image_url: str,
        user_id: str,
        companion_profile_id: str,
    ) -> None:
        if not name or name.isspace() or len(name) < 8:
            raise Exception("Name must be at least 8 characters")

        url_pattern = re.compile(
            r"^(https?://)?" r"([a-zA-Z0-9.-]+\.[a-zA-Z]{2,})" r"(/\S*)?$"
        )
        if not image_url or not url_pattern.match(image_url):
            raise Exception("Invalid image URL format")

        companion = self._user_repository.get_user_by_profile(
            companion_profile_id
        )
        if not companion:
            raise Exception("User not found")

        user_chats = self._chat_repository.get_chats_of_user(user_id)
        companion_ids = [user_chat.companion_id for user_chat in user_chats]
        if companion.id in companion_ids:
            raise Exception("Chat with this user already exists")

        chat = Chat(name=name, image_url=image_url, companion_id=companion.id)
        self._chat_repository.add_chat(chat, user_id)
