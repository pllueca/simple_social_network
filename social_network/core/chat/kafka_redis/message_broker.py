from typing import Iterable
from uuid import UUID, uuid4
from social_network.core.chat.interfaces.message_broker import (
    MessageBroker,
    ChatMessage,
)
from social_network.core.chat.kafka_redis.kafka import create_kafka_consumer
from redis import StrictRedis
from kafka import KafkaProducer

ACTIVE_ROOMS_KEY = "active-rooms"


class KafkaRedisMessageBroker(MessageBroker):
    def __init__(self, redis_connection: StrictRedis, kafka_producer: KafkaProducer):
        self._redis = redis_connection
        self._kafka_producer = kafka_producer

    def room_is_active(self, room_id: UUID) -> bool:
        return bool(self._redis.sismember(ACTIVE_ROOMS_KEY, str(room_id)))

    def get_room_id(self, room_name: str) -> UUID | None:
        id = self._redis.get(f"NAME_ID:{room_name}")
        if not id:
            return None
        print(id)
        return UUID(id.decode())

    def create_room(self, room_name: str) -> UUID:
        # check if a room with this name exists

        if self._redis.get(f"NAME_ID:{room_name}"):
            raise Exception("already exists")

        new_room_id = uuid4()
        self._redis.sadd(ACTIVE_ROOMS_KEY, str(new_room_id))
        self._redis.set(f"NAME_ID:{room_name}", str(new_room_id))
        self._redis.set(f"ID_NAME:{new_room_id}", str(new_room_id))
        return new_room_id

    def delete_room(self, room_id: UUID):
        self._redis.srem(ACTIVE_ROOMS_KEY, str(room_id))
        room_name = self._redis.get(f"ID_NAME:{room_id}")
        self._redis.set(f"NAME_ID:{room_name}", "")
        self._redis.set(f"ID_NAME:{room_id}", "")

    def send_message(self, room_id: UUID, user_id: UUID, message: str):
        if not self.room_is_active(room_id):
            raise Exception("room not active")

        chat_message = ChatMessage(
            user_id=user_id,
            room_id=room_id,
            message=message,
        )
        self._kafka_producer.send(
            topic=str(room_id),
            value=chat_message.model_dump_json().encode(),
        )

    def message_consumer(self, room_id: UUID) -> Iterable[ChatMessage]:
        if not self.room_is_active(room_id):
            raise Exception("room not active")

        consumer = create_kafka_consumer(str(room_id))
        for message in consumer:
            yield ChatMessage.model_validate_json(message.value)
