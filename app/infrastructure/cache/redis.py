"""
Adaptador de Redis para Almacenamiento en Memoria y Caché.

Gestiona el pool de conexiones optimizado para:
- Caché y Rate Limiting
- Revocación de sesiones / Tokens en lista negra
- Soporte de conexión para adaptadores de brokers
"""

from typing import AsyncGenerator
import redis.asyncio as redis
from app.core.config import settings

# Pool de conexiones único y compartido
redis_pool = redis.ConnectionPool.from_url(
    settings.REDIS_URL,
    decode_responses=True,
    max_connections=20,
)


def get_redis_client() -> redis.Redis:
    """Retorna una instancia reutilizable del cliente conectada al pool."""
    return redis.Redis(connection_pool=redis_pool)


async def get_redis() -> AsyncGenerator[redis.Redis, None]:
    """
    Inyector de dependencia para FastAPI (Depends).
    Garantiza el ciclo de vida de la conexión en cada petición HTTP.
    """
    client = get_redis_client()
    try:
        yield client
    finally:
        await client.aclose()