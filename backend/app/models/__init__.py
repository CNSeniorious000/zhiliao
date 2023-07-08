from enum import Enum

from pydantic import BaseModel, Field


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
    hide_context: bool = Field(False, alias="hideContext")
