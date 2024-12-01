import asyncio
import json
from datetime import datetime

from aiokafka import AIOKafkaProducer


class AsyncKafkaProducer:
    def __init__(self, brokers: str, topic: str):
        """
        Продюсер кафка с автоматическим запуском, который инициирует констркктор
        """
        self.brokers = brokers
        self.topic = topic
        self.producer = AIOKafkaProducer(bootstrap_servers=self.brokers)

        asyncio.create_task(self.start())   # АВТОМАТИЧЕСКИЙ ЗАПУСК

    async def start(self):
        await self.producer.start()

    async def stop(self):
        if self.producer:
            await self.producer.stop()

    async def send_event(self, event: str, category: str):
        event_time = datetime.utcnow().isoformat() + 'Z'  # Пример: '2024-12-01T10:30:00Z'

        event_data = {
            'event': event,
            'timestamp': event_time
        }
        event_json = json.dumps(event_data)

        await self.producer.send_and_wait(category, value=event_json.encode('utf-8'))
