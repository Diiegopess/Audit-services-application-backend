"""
Fachada Pública del Módulo de Autenticación.

Punto único de contacto interno para otros módulos del backend.
"""

import uuid
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from app.auth.models import AuthCredential
from app.auth.repository import AuthRepository
from app.core.security import hash_password


class AuthFacade:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.repo = AuthRepository(db)

    async def get_credential_by_id(self, credential_id: uuid.UUID) -> Optional[AuthCredential]:
        """Consulta credenciales por ID."""
        return await self.repo.get_by_id(credential_id)

    async def get_credential_by_email(self, email: str) -> Optional[AuthCredential]:
        """Consulta credenciales por correo electrónico."""
        return await self.repo.get_by_email(email)

    async def create_user_credentials(
        self,
        user_id: uuid.UUID,
        email: str,
        plain_password: str,
        is_active: bool = True,
        is_email_verified: bool = True,
    ) -> AuthCredential:
        """
        Crea de forma síncrona las credenciales en 'auth_credentials'
        aplicando el hashing de contraseña correspondiente.
        """
        hashed_pwd = hash_password(plain_password)
        return await self.repo.create_credential(
            credential_id=user_id,
            email=email,
            password_hash=hashed_pwd,
            is_active=is_active,
            is_email_verified=is_email_verified,
        )