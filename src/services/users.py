from models import User
from repositories import UserRepository


class UserService:
    def __init__(self, user_repository: UserRepository):
        self._user_repository = user_repository

    def login(self, username: str, password: str) -> User:
        user = self._user_repository.get_user(username, password)

        if not user:
            raise Exception("Invalid credentials")
        else:
            return user

    def registrate(
        self, username: str, password: str, confirm_password: str
    ) -> None:
        if not username and not username.isspace() and len(username) < 8:
            raise Exception("Username must be at least 8 characters")
        if not password and not password.isspace() and len(password) < 8:
            raise Exception("Password must be at least 8 characters")
        if password != confirm_password:
            raise Exception("Passwords don't match")

        user = User(
            username=username, password=password, is_banned="1", role="user"
        )
        self._user_repository.add_user(user)
