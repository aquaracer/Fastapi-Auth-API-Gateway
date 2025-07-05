from dataclasses import dataclass

from src.users.repositories.user_repository import UserRepository
from src.users.schemas.user_schema import UserCreateSchema, UserLoginSchema
from src.users.services.auth_service import AuthService


@dataclass
class UserService:
    user_repository: UserRepository
    auth_service: AuthService

    async def create_user(self, body: UserCreateSchema) -> UserLoginSchema:
        user = await self.user_repository.create_user(body)
        access_token = self.auth_service.generate_access_token(user_id=user.id)
        return UserLoginSchema(user_id=user.id, access_token=access_token)
