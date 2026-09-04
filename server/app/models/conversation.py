from beanie import Document, PydanticObjectId
from pydantic import BaseModel, Field
from typing import Optional, List, Any, Dict
from datetime import datetime


class ChatMessage(BaseModel):
    role: str  # 'user' | 'assistant' | 'system'
    content: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    metadata: Optional[Dict[str, Any]] = None


class Conversation(Document):
    user_id: PydanticObjectId
    title: str = "New Conversation"
    messages: List[ChatMessage] = []
    is_archived: bool = False
    last_message: Optional[str] = None
    message_count: int = 0
    tags: List[str] = []
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        name = "conversations"

    def update_meta(self):
        if self.messages:
            self.last_message = self.messages[-1].content[:100]
            self.message_count = len(self.messages)
            if len(self.messages) >= 1 and self.title == "New Conversation":
                self.title = self.messages[0].content[:50]
        self.updated_at = datetime.utcnow()
