from pydantic import BaseModel
from typing import List

class Interlocutor (BaseModel):
    login: str
    avatarUrl: str

class MessageThread (BaseModel):
    id: str
    read: bool
    lastMessageDateTime: str
    interlocutor: Interlocutor
