from pydantic import BaseModel
from typing import List, Optional

class Thread (BaseModel):
    id: str

class Author (BaseModel):
    login: str
    isInterlocutor: bool

class RelatesTo (BaseModel):
    offer: Optional [str]
    order: Optional [str]

class Message (BaseModel):
    id: str
    status: str
    type: str
    createdAt: str
    thread: Thread
    author: Author
    text: str
    subject: Optional [str]
    relatesTo: RelatesTo
    hasAdditionalAttachments: bool
    attachments: List [str]
