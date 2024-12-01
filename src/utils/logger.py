import logging
from confluent_kafka import Producer
import json
import time
from threading import Timer
from collections import deque

KAFKA_CONFIG = {
    'bootstrap.servers': 'localhost:9092',
    'client.id': 'fastapi-logger',
    'batch.num.messages': 1000,
    'linger.ms': 5,
    'acks': 'all',
}

KAFKA_TOPIC = 'app-logs'

log_buffer = deque()

MAX_LOGS_BATCH_SIZE = 1000

def send_logs_to_kafka(log_messages: list):
    producer = Producer(KAFKA_CONFIG)
    for log_message in log_messages:
        producer.produce(KAFKA_TOPIC, value=log_message)

    producer.flush()

def flush_logs():
    global log_buffer
    if log_buffer:
        log_messages = list(log_buffer)
        log_buffer.clear()
        send_logs_to_kafka(log_messages)

log_flush_timer = Timer(1, flush_logs)
log_flush_timer.start()


# custom logger
class KafkaLogHandler(logging.Handler):
    def emit(self, record):
        try:
            log_message = self.format(record)
            log_buffer.append(log_message)

            # обработка переполнения буфера
            if len(log_buffer) >= MAX_LOGS_BATCH_SIZE:
                flush_logs()
        except Exception as e:
            print(f"Ошибка при отправке лога в Kafka: {e}")


def setup_logger():
    logger = logging.getLogger("KafkaLogger")
    logger.setLevel(logging.INFO)

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    kafka_handler = KafkaLogHandler()
    kafka_handler.setFormatter(formatter)

    logger.addHandler(kafka_handler)

    return logger


logger = setup_logger()
logger.info("Logger is started.")
