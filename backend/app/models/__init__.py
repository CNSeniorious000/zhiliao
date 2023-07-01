from enum import Enum

from pydantic import BaseModel


class Role(str, Enum):
    user = "user"
    assistant = "assistant"
    system = "system"


class Message(BaseModel):
    name: str | None = None
    role: Role
    content: str


class Preset(BaseModel):
    title: str
    messages: list[Message] = []
    examples: list[str] = []
