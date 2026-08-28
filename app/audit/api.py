"""
Fachada Pública del Módulo de Auditoría.

Punto único de contacto interno para otros módulos del backend.
"""

from datetime import datetime
from typing import Optional, Sequence
import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from app.audit import service as audit_service
from app.audit.models import AuditLog
from app.audit.schemas import AuditLogCreate


class AuditFacade:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def log_event(self, log_data: AuditLogCreate) -> AuditLog:
        """Registra directamente un evento en la bitácora de auditoría."""
        return await audit_service.record_audit_log(self.db, log_data)

    async def query_logs(
        self,
        skip: int = 0,
        limit: int = 50,
        event_type: Optional[str] = None,
        user_id: Optional[uuid.UUID] = None,
        from_date: Optional[datetime] = None,
        to_date: Optional[datetime] = None,
    ) -> Sequence[AuditLog]:
        """Consulta registros de auditoría aplicando filtros."""
        return await audit_service.get_audit_logs(
            db=self.db,
            skip=skip,
            limit=limit,
            event_type=event_type,
            user_id=user_id,
            from_date=from_date,
            to_date=to_date,
        )