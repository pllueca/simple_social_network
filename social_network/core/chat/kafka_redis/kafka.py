import json
from kafka import KafkaProducer, KafkaConsumer


def create_kafka_producer() -> KafkaProducer:
    return KafkaProducer(bootstrap_servers="localhost:9092")


def create_kafka_consumer(topic: str) -> KafkaConsumer:
    return KafkaConsumer(
        topic,
        bootstrap_servers=["localhost:9092"],
    )
