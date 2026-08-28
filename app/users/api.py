"""
Fachada Pública del Módulo de Usuarios.

Punto único de contacto interno para otros módulos del sistema.
"""

import uuid
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from app.users import service as user_service
from app.users.models import User
from app.users.schemas import UserProfileCreate


class UsersFacade:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_user_by_id(self, user_id: uuid.UUID) -> Optional[User]:
        """Obtiene un usuario por su identificador único."""
        return await user_service.get_by_id(self.db, user_id)

    async def get_user_by_email(self, email: str) -> Optional[User]:
        """Busca un usuario por su dirección de correo electrónico."""
        return await user_service.get_by_email(self.db, email)

    async def is_user_active(self, user_id: uuid.UUID) -> bool:
        """Verifica si el usuario existe y su cuenta está activa."""
        user = await user_service.get_by_id(self.db, user_id)
        return bool(user and user.is_active)

    async def create_profile(self, profile_in: UserProfileCreate) -> User:
        """Crea el perfil de usuario de forma síncrona dentro de la misma transacción DB."""
        return await user_service.create_profile(self.db, profile_in)