from psycopg2.extensions import connection as DbConnection
from psycopg2.extras import RealDictCursor

from models import User


class UserRepository:
    def __init__(self, connection: DbConnection):
        self._connection = connection

    def get_users(self) -> list[User]:
        with self._connection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                "SELECT users.*, roles.name AS role "
                "FROM users JOIN roles ON role_id = roles.id "
                "WHERE roles.name = 'user';"
            )
            users_data = cursor.fetchall()

            users = []
            for user_data in users_data:
                users.append(User(**user_data))

            return users

    def get_user_by_profile(self, profile_id: str) -> User | None:
        if not profile_id or profile_id.isspace():
            return None

        with self._connection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                "SELECT users.*, roles.name AS role "
                "FROM users JOIN roles ON role_id = roles.id "
                "WHERE profile_id = %s;",
                (profile_id,),
            )
            user_data = cursor.fetchone()

            if not user_data:
                return None
            else:
                return User(**user_data)

    def get_user_by_credentials(
        self, username: str, password: str
    ) -> User | None:
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

    def get_user(self, id: str) -> User | None:
        if not id or id.isspace():
            return None

        with self._connection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                "SELECT * FROM users WHERE id = %s;",
                (id,),
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

    def ban_user(self, id: str) -> None:
        with self._connection.cursor() as cursor:
            cursor.execute(
                "SELECT is_banned FROM users WHERE id = %s;",
                (id,),
            )
            result = cursor.fetchone()

            is_banned = result[0]
            new_status = not is_banned

            cursor.execute(
                "UPDATE users SET is_banned = %s WHERE id = %s;",
                (new_status, id),
            )
