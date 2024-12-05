from datetime import datetime, time

from models import Meeting
from repositories import MeetingRepository, ProfileRepository, UserRepository


class MeetingService:
    def __init__(
        self,
        meeting_repository: MeetingRepository,
        user_repository: UserRepository,
        profile_repository: ProfileRepository,
    ):
        self._meeting_repository = meeting_repository
        self._user_repository = user_repository
        self._profile_repository = profile_repository

    def get_meetings_of_user(self, user_id: str) -> list[Meeting]:
        user = self._user_repository.get_user(user_id)
        if not user:
            raise Exception("User not found")
        else:
            meetings = self._meeting_repository.get_meetings_of_user(user_id)
            for meeting in meetings:
                meeting.companion = (
                    self._profile_repository.get_profile_by_user_id(
                        meeting.companion_id
                    )
                )
            return meetings

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

    def delete_meeting(self, id: str) -> None:
        meeting = self._meeting_repository.get_meeting(id)
        if not meeting:
            raise Exception("Meeting not found")
        else:
            self._meeting_repository.delete_meeting(id)
