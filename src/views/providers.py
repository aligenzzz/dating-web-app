from psycopg2.extensions import connection as DbConnection

from repositories import ProfileRepository, UserRepository
from services import UserService


def user_provider(connection: DbConnection) -> UserService:
    return UserService(
        UserRepository(connection), ProfileRepository(connection)
    )
