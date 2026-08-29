"""
Módulo de Repositorio para el Dominio de Autenticación.

Maneja el acceso a datos y consultas sobre la tabla 'auth_credentials'.
"""

import uuid
from typing import Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.models import AuthCredential
from app.auth.schemas import RegisterRequest
from app.infrastructure.repositories.base import BaseRepository
from pydantic import BaseModel


class AuthCredentialUpdateSchema(BaseModel):
    password_hash: Optional[str] = None
    google_id: Optional[str] = None
    is_active: Optional[bool] = None
    is_email_verified: Optional[bool] = None
    failed_attempts: Optional[int] = None


class AuthRepository(BaseRepository[AuthCredential, RegisterRequest, AuthCredentialUpdateSchema]):
    def __init__(self, db: AsyncSession):
        super().__init__(model=AuthCredential, db=db)

    async def get_by_id(self, credential_id: uuid.UUID) -> Optional[AuthCredential]:
        stmt = select(AuthCredential).where(AuthCredential.id == credential_id)
        result = await self.db.execute(stmt)
        return result.scalars().first()

    async def get_by_email(self, email: str) -> Optional[AuthCredential]:
        stmt = select(AuthCredential).where(AuthCredential.email == email)
        result = await self.db.execute(stmt)
        return result.scalars().first()

    async def get_by_google_id(self, google_id: str) -> Optional[AuthCredential]:
        stmt = select(AuthCredential).where(AuthCredential.google_id == google_id)
        result = await self.db.execute(stmt)
        return result.scalars().first()

    async def create_credential(
        self,
        email: str,
        password_hash: Optional[str] = None,
        google_id: Optional[str] = None,
        is_active: bool = True,
        is_email_verified: bool = False,
        credential_id: Optional[uuid.UUID] = None,
    ) -> AuthCredential:
        credential = AuthCredential(
            id=credential_id or uuid.uuid4(),
            email=email,
            password_hash=password_hash,
            google_id=google_id,
            is_active=is_active,
            is_email_verified=is_email_verified,
        )
        self.db.add(credential)
        await self.db.commit()
        await self.db.refresh(credential)
        return credential