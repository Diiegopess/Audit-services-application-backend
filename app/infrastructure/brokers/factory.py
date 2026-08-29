"""
Fábrica de Inyección de Brokers de Mensajería.

Permite instanciar dinámicamente el publicador configurado en las
variables de entorno, manteniendo la aplicación 100% agnóstica al broker.
"""

from app.core.config import settings
from app.core.events.interfaces import IEventPublisher
from app.infrastructure.brokers.redis_stream import RedisStreamPublisher
from app.infrastructure.cache.redis import get_redis_client


def get_event_publisher() -> IEventPublisher:
    """
    Retorna la implementación concreta de IEventPublisher configurada.
    Se utiliza como dependencia en FastAPI: `Depends(get_event_publisher)`.
    """
    broker_type = settings.BROKER_TYPE.upper()

    if broker_type == "REDIS":
        redis_client = get_redis_client()
        return RedisStreamPublisher(redis_client=redis_client)

    # Aquí se extenderá a futuro sin tocar el resto del sistema:
    # elif broker_type == "RABBITMQ":
    #     return RabbitMQPublisher(...)
    # elif broker_type == "KAFKA":
    #     return KafkaPublisher(...)

    raise ValueError(f"Tipo de broker no soportado o no configurado: {broker_type}")