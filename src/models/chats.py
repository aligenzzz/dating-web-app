from typing import Optional


class Chat:
    def __init__(
        self,
        id: str = "",
        name: str = "",
        image_url: str = "",
        companion_id: str = "",
        last_message_id: str = "",
        **kwargs
    ):
        from models import Message, Profile

        self.id = id
        self.name = name
        self.image_url = image_url
        self.companion_id = companion_id
        self.last_message_id = last_message_id

        self.companion: Optional[Profile] = None
        self.last_message: Optional[Message] = None
