from psycopg2.extensions import connection as DbConnection
from psycopg2.extras import RealDictCursor

from models import Message


class MessageRepository:
    def __init__(self, connection: DbConnection):
        self._connection = connection

    def get_messages_by_chat_id(self, chat_id: str) -> list[Message]:
        if not chat_id or chat_id.isspace():
            return []

        with self._connection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                "SELECT * FROM messages WHERE chat_id = %s;",
                (chat_id,),
            )
            messages_data = cursor.fetchall()

            messages = []
            for message_data in messages_data:
                messages.append(Message(**message_data))

            return messages

    def get_message(self, id: str) -> Message | None:
        if not id or id.isspace():
            return None

        with self._connection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                "SELECT * FROM messages WHERE id = %s;",
                (id,),
            )
            message_data = cursor.fetchone()

            if not message_data:
                return None
            else:
                return Message(**message_data)

    def add_message(self, message: Message) -> Message:
        with self._connection.cursor() as cursor:
            cursor.execute(
                "INSERT INTO messages (content, chat_id, user_id) "
                "VALUES (%s, %s, %s) RETURNING id;",
                (message.content, message.chat_id, message.user_id),
            )
            message.id = cursor.fetchone()[0]
            return message
