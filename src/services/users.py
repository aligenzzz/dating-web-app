import re

from models import Profile, User
from repositories import ProfileRepository, UserRepository


class UserService:
    def __init__(
        self,
        user_repository: UserRepository,
        profile_repository: ProfileRepository,
    ):
        self._user_repository = user_repository
        self._profile_repository = profile_repository

    def login(self, username: str, password: str) -> User:
        user = self._user_repository.get_user_by_credentials(
            username, password
        )

        if not user:
            raise Exception("Invalid credentials")
        else:
            return user

    def registrate(
        self,
        username: str,
        password: str,
        confirm_password: str,
        first_name: str,
        last_name: str,
        age: str,
        photo_url: str,
        hobbies: str,
        occupation: str,
        description: str,
        country: str,
        city: str,
    ) -> None:
        if not username or username.isspace() or len(username) < 8:
            raise Exception("Username must be at least 8 characters")
        if not password or password.isspace() or len(password) < 8:
            raise Exception("Password must be at least 8 characters")
        if password != confirm_password:
            raise Exception("Passwords don't match")

        if not first_name or first_name.isspace():
            raise Exception("First name cannot be empty")
        if not last_name or last_name.isspace():
            raise Exception("Last name cannot be empty")

        try:
            age_number = int(age)
        except ValueError:
            raise Exception("Age must be a valid integer")
        if not age_number or age_number < 14 or age_number > 120:
            raise Exception("Age must be between 14 and 120")

        if not country or country.isspace():
            raise Exception("Country cannot be empty")
        if not city or city.isspace():
            raise Exception("City cannot be empty")

        url_pattern = re.compile(
            r"^(https?://)?" r"([a-zA-Z0-9.-]+\.[a-zA-Z]{2,})" r"(/\S*)?$"
        )
        if not photo_url or not url_pattern.match(photo_url):
            raise Exception("Invalid photo URL format")

        profile = Profile(
            first_name=first_name,
            last_name=last_name,
            age=age_number,
            photo_url=photo_url,
            hobbies=hobbies,
            occupation=occupation,
            description=description,
            country=country,
            city=city,
        )
        profile = self._profile_repository.add_profile(profile)

        user = User(
            username=username,
            password=password,
            is_banned=False,
            role="user",
            profile_id=profile.id,
        )
        self._user_repository.add_user(user)
