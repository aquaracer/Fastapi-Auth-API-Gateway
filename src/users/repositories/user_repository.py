from dataclasses import dataclass

from sqlalchemy import insert, select
from sqlalchemy.orm import Session

from src.models.user_model import User
from src.users.schemas.user_schema import UserCreateSchema


@dataclass
class UserRepository:
    db_session: Session

    async def get_user_by_email(self, email: str) -> User | None:
        query = select(User).where(User.email == email)
        async with self.db_session as session:
            return (await session.execute(query)).scalar_one_or_none()

    async def create_user(self, user: UserCreateSchema) -> User:
        query = insert(User).values(**user.model_dump()).returning(User.id)
        async with self.db_session as session:
            user_id: int = (await session.execute(query)).scalar()
            await session.commit()
            await session.flush()
            return await self.get_user(user_id)

    async def get_user(self, user_id) -> User | None:
        query = select(User).where(User.id == user_id)
        async with self.db_session as session:
            return (await session.execute(query)).scalar_one_or_none()

    async def get_user_by_username(self, username: str) -> User | None:
        query = select(User).where(User.username == username)
        async with self.db_session as session:
            return (await session.execute(query)).scalar_one_or_none()
