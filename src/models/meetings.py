from datetime import datetime


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
        self.id = id
        self.name = name
        self.held_at = held_at
        self.country = country
        self.city = city
        self.address = address
        self.companion_id = companion_id
