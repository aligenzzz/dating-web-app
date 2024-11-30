from psycopg2.extensions import connection as DbConnection

from repositories import (
    ChatRepository,
    MeetingRepository,
    ProfileRepository,
    UserRepository,
)
from services import ChatService, MeetingService, ProfileService, UserService


def user_provider(connection: DbConnection) -> UserService:
    return UserService(
        UserRepository(connection), ProfileRepository(connection)
    )


def profile_provider(connection: DbConnection) -> ProfileService:
    return ProfileService(ProfileRepository(connection))


def chat_provider(connection: DbConnection) -> ChatService:
    return ChatService(ChatRepository(connection), UserRepository(connection))


def meeting_provider(connection: DbConnection) -> MeetingService:
    return MeetingService(
        MeetingRepository(connection), UserRepository(connection)
    )
