from enum import Enum
from pydantic import BaseModel
from typing import List, Optional

class DisputeStatus(Enum):
    WAITING_FOR_SELLER = "WAITING_FOR_SELLER"
    WAITING_FOR_CLIENT = "WAITING_FOR_CLIENT"
    CLOSED = "CLOSED"

class DisputeReason(Enum):
    RETURN = "RETURN"
    GUARANTEE = "GUARANTEE"
    WARRANTY = "WARRANTY"

class DisputeLineItem (BaseModel):
    id: str

class DisputeOffer (BaseModel):
    id: str

class DisputeOrder (BaseModel):
    id: str

class DisputeAuthor (BaseModel):
    login: str
    role: str

class Dispute (BaseModel):
    id: str
    status: DisputeStatus
    reason: DisputeReason
    createdAt: str
    updatedAt: str
    resolvedAt: Optional[str]
    lineItems: List[DisputeLineItem]
    offer: DisputeOffer
    order: DisputeOrder
    author: DisputeAuthor