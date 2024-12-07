from psycopg2.extensions import connection as DbConnection
from psycopg2.extras import RealDictCursor

from models import Complaint


class ComplaintRepository:
    def __init__(self, connection: DbConnection):
        self._connection = connection

    def get_complaints(self) -> list[Complaint]:
        with self._connection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute("SELECT * FROM complaints;")
            complaints_data = cursor.fetchall()

            complaints = []
            for complaint_data in complaints_data:
                complaints.append(Complaint(**complaint_data))

            return complaints

    def get_complaint(self, id: str) -> Complaint | None:
        if not id or id.isspace():
            return None

        with self._connection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                "SELECT * FROM complaints WHERE id = %s;",
                (id,),
            )
            complaint_data = cursor.fetchone()

            if not complaint_data:
                return None
            else:
                return Complaint(**complaint_data)

    def add_complaint(self, complaint: Complaint) -> None:
        with self._connection.cursor() as cursor:
            cursor.execute(
                "INSERT INTO complaints (content, user_id) "
                "VALUES (%s, %s);",
                (complaint.content, complaint.user_id),
            )

    def delete_complaint(self, id: str) -> None:
        with self._connection.cursor() as cursor:
            cursor.execute("DELETE FROM complaints WHERE id = %s;", (id,))
