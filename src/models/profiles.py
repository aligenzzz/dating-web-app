class Profile:
    def __init__(
        self,
        id: str = "",
        first_name: str = "",
        last_name: str = "",
        age: int = 20,
        photo_url: str = "",
        hobbies: str = "",
        occupation: str = "",
        description: str = "",
        country: str = "",
        city: str = "",
        **kwargs,
    ):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.age = age
        self.photo_url = photo_url
        self.hobbies = hobbies
        self.occupation = occupation
        self.description = description
        self.country = country
        self.city = city
