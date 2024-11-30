from psycopg2.extensions import connection as DbConnection

from models import Meeting


class MeetingRepository:
    def __init__(self, connection: DbConnection):
        self._connection = connection

    def add_meeting(self, meeting: Meeting, user_id: str) -> None:
        with self._connection.cursor() as cursor:
            cursor.execute(
                "INSERT INTO locations (country, city, address) "
                "VALUES (%s, %s, %s) RETURNING id;",
                (meeting.country, meeting.city, meeting.address),
            )
            location_id = cursor.fetchone()[0]

            cursor.execute(
                "INSERT INTO meetings (name, held_at, location_id) "
                "VALUES (%s, %s, %s) RETURNING id;",
                (meeting.name, meeting.held_at, location_id),
            )
            meeting_id = cursor.fetchone()[0]

            cursor.execute(
                "INSERT INTO meeting_users (meeting_id, user_id) "
                "VALUES (%s, %s), (%s, %s);",
                (
                    meeting_id,
                    user_id,
                    meeting_id,
                    meeting.companion_id,
                ),
            )
