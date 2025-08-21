from typing import Iterable
from uuid import UUID
from social_network.core.chat.interfaces.message_broker import (
    MessageBroker,
    ChatMessage,
)
from social_network.core.repositories.interfaces.models import User


class ChatService:
    def __init__(self, message_broker: MessageBroker):
        self.message_broker = message_broker

    def create_chat_room(self, room_name: str) -> UUID:
        return self.message_broker.create_room(room_name)

    def get_room_id(self, room_name: str) -> UUID | None:
        return self.message_broker.get_room_id(room_name)

    def send_message(self, room_id: UUID, author_id: UUID, message: str):
        self.message_broker.send_message(room_id, author_id, message)

    def room_messages(self, room_id: UUID) -> Iterable[ChatMessage]:
        for message in self.message_broker.message_consumer(room_id):
            yield message
