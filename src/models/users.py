from datetime import datetime


class User:
    def __init__(
        self,
        id: str = "",
        username: str = "",
        password: str = "",
        created_at: str = "",
        is_banned: str = "",
        role: str = "",
        profile_id: str = "",
    ):
        self.id = id
        self.username = username
        self.password = password
        self.created_at = datetime.strptime(created_at, "%Y-%m-%d %H:%M:%S")
        self.is_banned = bool(is_banned)
        self.role = role
        self.profile_id = profile_id
