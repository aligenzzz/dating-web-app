from psycopg2.extensions import connection as DbConnection
from psycopg2.extras import RealDictCursor

from models import Chat


class ChatRepository:
    def __init__(self, connection: DbConnection):
        self._connection = connection

    def get_chats_of_user(self, user_id: str) -> list[Chat]:
        with self._connection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                "SELECT chats.*, cu2.user_id AS companion_id "
                "FROM chats JOIN chat_users cu1 ON "
                "chats.id = cu1.chat_id JOIN chat_users cu2 "
                "ON chats.id = cu2.chat_id "
                "WHERE cu1.user_id = %s AND cu2.user_id != cu1.user_id;",
                (user_id,),
            )
            chats_data = cursor.fetchall()

            chats = []
            for chat_data in chats_data:
                chats.append(Chat(**chat_data))

            return chats

    def add_chat(self, chat: Chat, user_id: str) -> None:
        with self._connection.cursor() as cursor:
            cursor.execute(
                "INSERT INTO chats (name, image_url) "
                "VALUES (%s, %s) RETURNING id;",
                (chat.name, chat.image_url),
            )
            chat_id = cursor.fetchone()[0]

            cursor.execute(
                "INSERT INTO chat_users (chat_id, user_id) "
                "VALUES (%s, %s), (%s, %s);",
                (
                    chat_id,
                    user_id,
                    chat_id,
                    chat.companion_id,
                ),
            )
