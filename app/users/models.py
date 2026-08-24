"""
Módulo de Modelos SQLAlchemy para el Dominio de Usuarios.

Define la estructura física de la tabla 'users' (perfiles de negocio),
desacoplada de las credenciales y mecanismos de autenticación técnica.
"""

import uuid
from datetime import datetime, timezone
from sqlalchemy import Boolean, DateTime, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.infrastructure.db.database import Base


class User(Base):
    __tablename__ = "users"

    # El ID coincide directamente con el UUID de 'auth_credentials'
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    # Identidad y contacto
    email: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        index=True,
        nullable=False,
    )

    # Datos de perfil de negocio
    full_name: Mapped[str | None] = mapped_column(String(255), nullable=True)

    # Roles y permisos de la aplicación
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    is_superuser: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    # Auditoría
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False,
    )