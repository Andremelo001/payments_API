# src/drivers/messaging/rabbitmq_payment_publisher.py
import os
import json
import pika
from typing import Dict

from src.drivers.messaging.interfaces.payment_event_publisher_interface import PaymentEventPublisherInterface

class RabbitMQPaymentPublisher(PaymentEventPublisherInterface):
    def __init__(self):
        self.__url = os.getenv("RABBITMQ_URL")

        self.__params = pika.URLParameters(self.__url)

        self.__connection = pika.BlockingConnection(self.__params)

        self.__channel = self.__connection.channel()

        self.__exchange = "payments"

        self.__channel.exchange_declare(
            exchange=self.__exchange,
            exchange_type="fanout",
            durable=True
        )

    async def publish_payment_event(self, event: Dict) -> None:
        body = json.dumps(event)
        self.__channel.basic_publish(
            exchange=self.__exchange,
            routing_key="",
            body=body,
            properties=pika.BasicProperties(content_type="application/json")
        )
    
    def close(self):
        if self._connection and not self._connection.is_closed:
            self._connection.close()
