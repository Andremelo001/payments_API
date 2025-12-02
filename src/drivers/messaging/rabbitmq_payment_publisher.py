# src/drivers/messaging/rabbitmq_payment_publisher.py
import os
import json
import pika
from typing import Dict, Optional

from src.drivers.messaging.interfaces.payment_event_publisher_interface import PaymentEventPublisherInterface

class RabbitMQPaymentPublisher(PaymentEventPublisherInterface):
    """Singleton para reutilizar conexão RabbitMQ."""
    
    _instance: Optional['RabbitMQPaymentPublisher'] = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if self._initialized:
            return
            
        self.__url = os.getenv("RABBITMQ_URL")
        self.__exchange = "payments"
        self.__connection: Optional[pika.BlockingConnection] = None
        self.__channel: Optional[pika.channel.Channel] = None
        
        self._connect()
        self._initialized = True
    
    def _connect(self) -> None:
        """Conecta ao RabbitMQ."""
        params = pika.URLParameters(self.__url)
        self.__connection = pika.BlockingConnection(params)
        self.__channel = self.__connection.channel()
        
        self.__channel.exchange_declare(
            exchange=self.__exchange,
            exchange_type="fanout",
            durable=True
        )
    
    async def publish_payment_event(self, event: Dict) -> None:
        """Publica evento de pagamento no RabbitMQ."""
        # Verifica se conexão está ativa
        if self.__connection is None or self.__connection.is_closed:
            self._connect()
        
        body = json.dumps(event)
        self.__channel.basic_publish(
            exchange=self.__exchange,
            routing_key="",
            body=body,
            properties=pika.BasicProperties(
                content_type="application/json",
                delivery_mode=2
            )
        )
    
    def close(self) -> None:
        """Fecha conexão (chamado no shutdown)."""
        try:
            if self.__channel and not self.__channel.is_closed:
                self.__channel.close()
            if self.__connection and not self.__connection.is_closed:
                self.__connection.close()
        except Exception:
            pass
