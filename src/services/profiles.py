import re

from models import Profile
from repositories import ProfileRepository


class ProfileService:
    def __init__(
        self,
        profile_repository: ProfileRepository,
    ):
        self._profile_repository = profile_repository

    def get_profiles(self) -> list[Profile]:
        return self._profile_repository.get_profiles()

    def get_profiles_exclude_one(self, id: str) -> list[Profile]:
        return self._profile_repository.get_profiles_exclude_one(id)

    def get_profile(self, id: str) -> Profile:
        profile = self._profile_repository.get_profile(id)

        if not profile:
            raise Exception("Profile not found")
        else:
            return profile

    def get_profile_by_user_id(self, user_id: str) -> Profile:
        profile = self._profile_repository.get_profile_by_user_id(user_id)

        if not profile:
            raise Exception("Profile not found")
        else:
            return profile

    def update_profile(self, new_profile: Profile) -> Profile:
        profile = self._profile_repository.get_profile(new_profile.id)
        if not profile:
            raise Exception("Profile not found")

        if not new_profile.first_name or new_profile.first_name.isspace():
            raise Exception("First name cannot be empty")
        if not new_profile.last_name or new_profile.last_name.isspace():
            raise Exception("Last name cannot be empty")

        try:
            age_number = int(new_profile.age)
        except ValueError:
            raise Exception("Age must be a valid integer")
        if not age_number or age_number < 14 or age_number > 120:
            raise Exception("Age must be between 14 and 120")

        if not new_profile.country or new_profile.country.isspace():
            raise Exception("Country cannot be empty")
        if not new_profile.city or new_profile.city.isspace():
            raise Exception("City cannot be empty")

        url_pattern = re.compile(
            r"^(https?://)?" r"([a-zA-Z0-9.-]+\.[a-zA-Z]{2,})" r"(/\S*)?$"
        )
        if not new_profile.photo_url or not url_pattern.match(
            new_profile.photo_url
        ):
            raise Exception("Invalid photo URL format")

        self._profile_repository.update_profile(new_profile)

        return new_profile
