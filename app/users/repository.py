"""
Módulo de Repositorio para el Dominio de Usuarios.

Maneja el acceso a datos y las consultas SQLAlchemy de la tabla 'users'.
"""

import uuid
from typing import Optional, Sequence
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure.repositories.base import BaseRepository
from app.users.models import User
from app.users.schemas import UserProfileCreate, UserUpdateAdmin


class UserRepository(BaseRepository[User, UserProfileCreate, UserUpdateAdmin]):
    def __init__(self, db: AsyncSession):
        super().__init__(model=User, db=db)

    async def get_by_id(self, user_id: uuid.UUID) -> Optional[User]:
        stmt = select(User).where(User.id == user_id)
        result = await self.db.execute(stmt)
        return result.scalars().first()

    async def get_by_email(self, email: str) -> Optional[User]:
        stmt = select(User).where(User.email == email)
        result = await self.db.execute(stmt)
        return result.scalars().first()

    async def get_multi(self, skip: int = 0, limit: int = 100) -> Sequence[User]:
        stmt = select(User).offset(skip).limit(limit)
        result = await self.db.execute(stmt)
        return result.scalars().all()