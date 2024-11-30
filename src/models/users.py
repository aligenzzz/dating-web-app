from datetime import datetime


class User:
    def __init__(
        self,
        id: str = "",
        username: str = "",
        password: str = "",
        created_at: datetime = datetime(1999, 1, 1),
        is_banned: bool = False,
        role: str = "",
        profile_id: str = "",
        **kwargs,
    ):
        self.id = id
        self.username = username
        self.password = password
        self.created_at = created_at
        self.is_banned = is_banned
        self.role = role
        self.profile_id = profile_id
