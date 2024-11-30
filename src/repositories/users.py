from psycopg2.extensions import connection as DbConnection
from psycopg2.extras import RealDictCursor

from models import User


class UserRepository:
    def __init__(self, connection: DbConnection):
        self._connection = connection

    def get_user(self, username: str, password: str) -> User | None:
        if not username or username.isspace():
            return None
        if not password or password.isspace():
            return None

        with self._connection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                "SELECT users.*, roles.name AS role "
                "FROM users JOIN roles ON role_id = roles.id "
                "WHERE username = %s AND password = %s;",
                (username, password),
            )
            user_data = cursor.fetchone()

            if not user_data:
                return None
            else:
                return User(**user_data)

    def add_user(self, user: User) -> None:
        with self._connection.cursor() as cursor:
            cursor.execute(
                "SELECT id FROM roles WHERE name = %s;", (user.role,)
            )
            role_id = cursor.fetchone()[0]

            cursor.execute(
                "INSERT INTO users (username, password, is_banned, "
                "role_id, profile_id) VALUES (%s, %s, %s, %s, %s);",
                (
                    user.username,
                    user.password,
                    user.is_banned,
                    role_id,
                    user.profile_id,
                ),
            )
