from psycopg2.extensions import connection as DbConnection

from repositories import UserRepository
from services import UserService


def user_provider(connection: DbConnection) -> UserService:
    return UserService(UserRepository(connection))
