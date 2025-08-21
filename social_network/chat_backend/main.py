import sys

sys.path.append("/Users/pllueca/Code/simple_social_network")
import time
from social_network.core.chat.kafka_redis.kafka import (
    create_kafka_producer,
    create_kafka_consumer,
)
from social_network.core.chat.interfaces.message_broker import (
    MessageBroker,
    ChatMessage,
)
from social_network.core.chat.kafka_redis.redis import create_redis_connection
from social_network.core.chat.kafka_redis.message_broker import KafkaRedisMessageBroker
from social_network.core.services.chat import ChatService

from kafka import KafkaConsumer
from redis import Redis
import json
from uuid import uuid4

# Initialize Kafka Consumer and Redis client


def main():
    redis = create_redis_connection()
    kafka_producer = create_kafka_producer()
    msg_broker = KafkaRedisMessageBroker(
        redis_connection=redis, kafka_producer=kafka_producer
    )
    chat_service = ChatService(msg_broker)
    room_id = chat_service.create_chat_room("test-room")
    while True:
        chat_service.send_message(room_id, uuid4(), "hello hello")
        print("sent message")
        time.sleep(3)


if __name__ == "__main__":
    main()
