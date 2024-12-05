from datetime import datetime
from typing import Optional


class Message:
    def __init__(
        self,
        id: str = "",
        content: str = "",
        sent_at: datetime = datetime(1999, 1, 1),
        chat_id: str = "",
        user_id: str = "",
        **kwargs,
    ):
        from models import User

        self.id = id
        self.content = content
        self.sent_at = sent_at
        self.chat_id = chat_id
        self.user_id = user_id

        self.user: Optional[User] = None
