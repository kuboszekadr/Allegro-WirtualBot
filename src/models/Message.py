from enum import Enum
from pydantic import BaseModel
from typing import List, Optional

class MessageType(Enum):
    ASK_QUESTION = "ASK_QUESTION"
    MAIL = "MAIL"
    MESSAGE_CENTER = "MESSAGE_CENTER"

class Thread (BaseModel):
    id: str

class Offer (BaseModel):
    id: str

class Order (BaseModel):
    id: str

class Author (BaseModel):
    login: str
    isInterlocutor: bool

class RelatesTo (BaseModel):
    offer: Optional [Offer]
    order: Optional [Order]

class Attachment (BaseModel):
    fileName: str
    mimeType: str
    url: str
    status: str

class Message (BaseModel):
    id: str
    status: str
    type: MessageType
    createdAt: str
    thread: Thread
    author: Author
    text: str
    subject: Optional [str]
    relatesTo: RelatesTo
    hasAdditionalAttachments: bool
    attachments: List [Attachment]
