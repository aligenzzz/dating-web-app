from datetime import datetime
from typing import Optional


class Complaint:
    def __init__(
        self,
        id: str = "",
        content: str = "",
        posted_at: datetime = datetime(1999, 1, 1),
        user_id: str = "",
        **kwargs,
    ):
        from models import User

        self.id = id
        self.content = content
        self.posted_at = posted_at
        self.user_id = user_id

        self.user: Optional[User] = None
