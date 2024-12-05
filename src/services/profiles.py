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
