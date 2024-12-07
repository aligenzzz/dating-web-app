from models import Complaint
from repositories import ComplaintRepository, UserRepository


class ComplaintService:
    def __init__(
        self,
        complaint_repository: ComplaintRepository,
        user_repository: UserRepository,
    ):
        self._complaint_repository = complaint_repository
        self._user_repository = user_repository

    def add_complaint(self, content: str, user_id: str) -> None:
        if not content or content.isspace():
            raise Exception("Content cannot be empty")

        user = self._user_repository.get_user(user_id)
        if not user:
            raise Exception("User not found")

        complaint = Complaint(
            content=content,
            user_id=user_id,
        )
        self._complaint_repository.add_complaint(complaint)
