from psycopg2.extensions import connection as DbConnection

from repositories import (
    ActionRepository,
    ChatRepository,
    ComplaintRepository,
    MeetingRepository,
    MessageRepository,
    ProfileRepository,
    UserRepository,
)
from services import (
    ActionService,
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
    return ProfileService(
        ProfileRepository(connection), ActionRepository(connection)
    )


def chat_provider(connection: DbConnection) -> ChatService:
    return ChatService(
        ChatRepository(connection),
        UserRepository(connection),
        ProfileRepository(connection),
        MessageRepository(connection),
        ActionRepository(connection),
    )


def meeting_provider(connection: DbConnection) -> MeetingService:
    return MeetingService(
        MeetingRepository(connection),
        UserRepository(connection),
        ProfileRepository(connection),
        ActionRepository(connection),
    )


def message_provider(connection: DbConnection) -> MessageService:
    return MessageService(
        MessageRepository(connection),
        UserRepository(connection),
        ChatRepository(connection),
        ActionRepository(connection),
    )


def complaint_provider(connection: DbConnection) -> ComplaintService:
    return ComplaintService(
        ComplaintRepository(connection),
        UserRepository(connection),
        ActionRepository(connection),
    )


def action_provider(connection: DbConnection) -> ActionService:
    return ActionService(
        ActionRepository(connection),
        UserRepository(connection),
    )
