from models import Action, Complaint
from repositories import ActionRepository, ComplaintRepository, UserRepository


class ComplaintService:
    def __init__(
        self,
        complaint_repository: ComplaintRepository,
        user_repository: UserRepository,
        action_repository: ActionRepository,
    ):
        self._complaint_repository = complaint_repository
        self._user_repository = user_repository
        self._action_repository = action_repository

    def get_complaints(self) -> list[Complaint]:
        complaints = self._complaint_repository.get_complaints()
        for complaint in complaints:
            complaint.user = self._user_repository.get_user(complaint.user_id)
        return complaints

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
        self._action_repository.add_action(
            Action(name="Filed a complaint", user_id=user_id)
        )

    def delete_complaint(self, id: str) -> None:
        complaint = self._complaint_repository.get_complaint(id)
        if not complaint:
            raise Exception("Complaint not found")
        else:
            self._complaint_repository.delete_complaint(id)
