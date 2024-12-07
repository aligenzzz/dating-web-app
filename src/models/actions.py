from datetime import datetime
from typing import Optional


class Action:
    def __init__(
        self,
        id: str = "",
        name: str = "",
        completed_at: datetime = datetime(1999, 1, 1),
        user_id: str = "",
        **kwargs,
    ):
        from models import User

        self.id = id
        self.name = name
        self.completed_at = completed_at
        self.user_id = user_id

        self.user: Optional[User] = None
