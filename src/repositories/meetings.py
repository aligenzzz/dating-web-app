from psycopg2.extensions import connection as DbConnection
from psycopg2.extras import RealDictCursor

from models import Meeting


class MeetingRepository:
    def __init__(self, connection: DbConnection):
        self._connection = connection

    def get_meeting(self, id: str) -> Meeting | None:
        if not id or id.isspace():
            return None

        with self._connection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                "SELECT * FROM meetings WHERE id = %s;",
                (id,),
            )
            meeting_data = cursor.fetchone()

            if not meeting_data:
                return None
            else:
                return Meeting(**meeting_data)

    def get_meetings_of_user(self, user_id: str) -> list[Meeting]:
        with self._connection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                "SELECT meetings.*, mu2.user_id AS companion_id, "
                "locations.country, locations.city, locations.address "
                "FROM meetings JOIN meeting_users mu1 ON "
                "meetings.id = mu1.meeting_id JOIN meeting_users mu2 "
                "ON meetings.id = mu2.meeting_id "
                "JOIN locations ON location_id = locations.id "
                "WHERE mu1.user_id = %s AND mu2.user_id != mu1.user_id;",
                (user_id,),
            )
            meetings_data = cursor.fetchall()

            meetings = []
            for meeting_data in meetings_data:
                meetings.append(Meeting(**meeting_data))

            return meetings

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

    def delete_meeting(self, id: str) -> None:
        with self._connection.cursor() as cursor:
            cursor.execute("DELETE FROM meetings WHERE id = %s;", (id,))
