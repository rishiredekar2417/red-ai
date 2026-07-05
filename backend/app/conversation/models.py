from dataclasses import dataclass


@dataclass
class Message:
    role: str
    content: str


@dataclass
class Conversation:
    messages: list[Message]