from datetime import datetime
from typing import Optional


class Meeting:
    def __init__(
        self,
        id: str = "",
        name: str = "",
        held_at: datetime = datetime(1999, 1, 1),
        country: str = "",
        city: str = "",
        address: str = "",
        companion_id: str = "",
        **kwargs,
    ):
        from models import Profile

        self.id = id
        self.name = name
        self.held_at = held_at
        self.country = country
        self.city = city
        self.address = address
        self.companion_id = companion_id

        self.companion: Optional[Profile] = None

    @property
    def location(self):
        return f"{self.country}, {self.city}, {self.address}"
