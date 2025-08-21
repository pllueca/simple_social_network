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

# Initialize Kafka Consumer and Redis client


def main():
    redis = create_redis_connection()
    kafka_producer = create_kafka_producer()
    msg_broker = KafkaRedisMessageBroker(
        redis_connection=redis, kafka_producer=kafka_producer
    )
    chat_service = ChatService(msg_broker)
    room_id = chat_service.get_room_id("test-room")
    if room_id is None:
        print("room doenst exist")
        return
    for message in chat_service.room_messages(room_id):
        print(message)


if __name__ == "__main__":
    main()
