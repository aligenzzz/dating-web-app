from psycopg2.extensions import connection as DbConnection

from repositories import (
    ChatRepository,
    ComplaintRepository,
    MeetingRepository,
    MessageRepository,
    ProfileRepository,
    UserRepository,
)
from services import (
    ChatService,
    ComplaintService,
    MeetingService,
    MessageService,
    ProfileService,
    UserService,
)


def user_provider(connection: DbConnection) -> UserService:
    return UserService(
        UserRepository(connection), ProfileRepository(connection)
    )


def profile_provider(connection: DbConnection) -> ProfileService:
    return ProfileService(ProfileRepository(connection))


def chat_provider(connection: DbConnection) -> ChatService:
    return ChatService(
        ChatRepository(connection),
        UserRepository(connection),
        ProfileRepository(connection),
        MessageRepository(connection),
    )


def meeting_provider(connection: DbConnection) -> MeetingService:
    return MeetingService(
        MeetingRepository(connection),
        UserRepository(connection),
        ProfileRepository(connection),
    )


def message_provider(connection: DbConnection) -> MessageService:
    return MessageService(
        MessageRepository(connection),
        UserRepository(connection),
        ChatRepository(connection),
    )


def complaint_provider(connection: DbConnection) -> ComplaintService:
    return ComplaintService(
        ComplaintRepository(connection),
        UserRepository(connection),
    )
