from models import Action, Message
from repositories import (
    ActionRepository,
    ChatRepository,
    MessageRepository,
    UserRepository,
)


class MessageService:
    def __init__(
        self,
        message_repository: MessageRepository,
        user_repository: UserRepository,
        chat_repository: ChatRepository,
        action_repository: ActionRepository,
    ):
        self._message_repository = message_repository
        self._user_repository = user_repository
        self._chat_repository = chat_repository
        self._action_repository = action_repository

    def get_messages_by_chat_id(self, chat_id: str) -> list[Message]:
        messages = self._message_repository.get_messages_by_chat_id(chat_id)
        for message in messages:
            message.user = self._user_repository.get_user(message.user_id)
        return messages

    def add_message(
        self,
        content: str,
        chat_id: str,
        user_id: str,
    ) -> None:
        if not content or content.isspace():
            raise Exception("Content cannot be empty")

        chat = self._chat_repository.get_chat(chat_id)
        if not chat:
            raise Exception("Chat not found")

        user = self._user_repository.get_user(user_id)
        if not user:
            raise Exception("User not found")

        message = Message(content=content, chat_id=chat_id, user_id=user_id)
        self._message_repository.add_message(message)
        self._action_repository.add_action(
            Action(name="Sent a message", user_id=user_id)
        )
