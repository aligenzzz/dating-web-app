from contextlib import contextmanager
from typing import Generator

import psycopg2
from psycopg2.extensions import connection as DbConnection

from config import settings

DATABASE_CONFIG = {
    "dbname": settings.DB_NAME,
    "user": settings.DB_USER,
    "password": settings.DB_PASSWORD,
    "host": settings.DB_HOST,
    "port": settings.DB_PORT,
}


@contextmanager
def get_connection() -> Generator[DbConnection, None, None]:
    connection = psycopg2.connect(**DATABASE_CONFIG)
    try:
        yield connection
        connection.commit()
    except Exception as e:
        connection.rollback()
        raise e
    finally:
        connection.close()
