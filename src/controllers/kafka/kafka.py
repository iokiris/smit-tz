from .config import KAFKA_IP, KAFKA_LOGS_TOPIC
from .logger import AsyncKafkaProducer


producer = AsyncKafkaProducer(brokers=KAFKA_IP, topic=KAFKA_LOGS_TOPIC)


async def send_log(event: str, category: str = "system_logs"):
    attemp = await producer.send_event(category, event)