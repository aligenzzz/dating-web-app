from psycopg2.extensions import connection as DbConnection
from psycopg2.extras import RealDictCursor

from models import Action


class ActionRepository:
    def __init__(self, connection: DbConnection):
        self._connection = connection

    def get_actions(self) -> list[Action]:
        with self._connection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute("SELECT * FROM actions ORDER BY completed_at DESC;")
            actions_data = cursor.fetchall()

            actions = []
            for action_data in actions_data:
                actions.append(Action(**action_data))

            return actions

    def add_action(self, action: Action) -> None:
        with self._connection.cursor() as cursor:
            cursor.execute(
                "INSERT INTO actions (name, user_id) " "VALUES (%s, %s);",
                (action.name, action.user_id),
            )
