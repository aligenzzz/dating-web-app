from datetime import datetime, time

from models import Meeting
from repositories import MeetingRepository, UserRepository


class MeetingService:
    def __init__(
        self,
        meeting_repository: MeetingRepository,
        user_repository: UserRepository,
    ):
        self._meeting_repository = meeting_repository
        self._user_repository = user_repository

    def add_meeting(
        self,
        name: str,
        held_at_date: datetime,
        held_at_time: time,
        country: str,
        city: str,
        address: str,
        user_id: str,
        companion_profile_id: str,
    ) -> None:
        if not name or name.isspace() or len(name) < 8:
            raise Exception("Name must be at least 8 characters")
        if not held_at_date or not held_at_time:
            raise Exception("Held at datetime cannot be empty")

        held_at = datetime.combine(held_at_date, held_at_time)
        if held_at < datetime.now():
            raise Exception("The date and time cannot be in the past")

        if not country or country.isspace():
            raise Exception("Country cannot be empty")
        if not city or city.isspace():
            raise Exception("City cannot be empty")
        if not address or address.isspace():
            raise Exception("Address cannot be empty")

        companion = self._user_repository.get_user_by_profile(
            companion_profile_id
        )
        if not companion:
            raise Exception("User not found")

        meeting = Meeting(
            name=name,
            held_at=held_at,
            country=country,
            city=city,
            address=address,
            companion_id=companion.id,
        )
        self._meeting_repository.add_meeting(meeting, user_id)
