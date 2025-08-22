from api.repositories.user_repository import UserRepository
from api.models.user import UserInDB, User


class UserService:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

