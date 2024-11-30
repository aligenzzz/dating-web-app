class Chat:
    def __init__(
        self,
        id: str = "",
        name: str = "",
        image_url: str = "",
        companion_id: str = "",
        **kwargs
    ):
        self.id = id
        self.name = name
        self.image_url = image_url
        self.companion_id = companion_id
