from psycopg2.extensions import connection as DbConnection

from models import User


class UserRepository:
    def __init__(self, connection: DbConnection):
        self._connection = connection

    def get_user(self, username: str, password: str) -> User | None:
        with self._connection.cursor() as cursor:
            cursor.execute(
                f"SELECT users.*, roles.name FROM users JOIN roles ON "
                f"role_id = roles.id WHERE username = {username} "
                f"AND password = {password};"
            )
            user_data = cursor.fetchone()
            return User(**user_data)

    def add_user(self, user: User) -> None:
        with self._connection.cursor() as cursor:
            cursor.execute(f"SELECT id FROM roles WHERE name = {user.role};")
            role_id = cursor.fetchone()[0]
            cursor.execute(
                f"INSERT INTO users (username, password, is_banned, "
                f"role_id, profile_id) VALUES ({user.username}, "
                f"{user.password}, {int(user.is_banned)}, "
                f"{role_id}, {user.profile_id});"
            )
