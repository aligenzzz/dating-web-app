from psycopg2.extensions import connection as DbConnection

from models import Complaint


class ComplaintRepository:
    def __init__(self, connection: DbConnection):
        self._connection = connection

    def add_complaint(self, complaint: Complaint) -> None:
        with self._connection.cursor() as cursor:
            cursor.execute(
                "INSERT INTO complaints (content, user_id) "
                "VALUES (%s, %s);",
                (complaint.content, complaint.user_id),
            )
