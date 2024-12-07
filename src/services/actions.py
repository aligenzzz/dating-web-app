from models import Action
from repositories import ActionRepository, UserRepository


class ActionService:
    def __init__(
        self,
        action_repository: ActionRepository,
        user_repository: UserRepository,
    ):
        self._action_repository = action_repository
        self._user_repository = user_repository

    def get_actions(self) -> list[Action]:
        actions = self._action_repository.get_actions()
        for action in actions:
            action.user = self._user_repository.get_user(action.user_id)
        return actions
