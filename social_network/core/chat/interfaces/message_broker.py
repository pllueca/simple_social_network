from typing import Iterable
from uuid import UUID
from abc import ABC, abstractmethod
from pydantic import BaseModel, Field
from datetime import datetime


class ChatMessage(BaseModel):
    user_id: UUID
    room_id: UUID
    message: str
    timestamp: datetime = Field(default_factory=datetime.now)


class MessageBroker(ABC):
    @abstractmethod
    def create_room(self, room_name: str) -> UUID:
        pass

    @abstractmethod
    def get_room_id(self, room_name: str) -> UUID | None:
        pass

    @abstractmethod
    def send_message(self, room_id: UUID, user_id: UUID, message: str):
        pass

    @abstractmethod
    def message_consumer(self, room_id: UUID) -> Iterable[ChatMessage]:
        pass
