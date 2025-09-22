from typing import List, Optional
from pydantic import BaseModel
from hiws.types.message import Message
from hiws.types.status import Status


class Profile(BaseModel):
    name: str


class RequestContact(BaseModel):
    profile: Profile
    wa_id: str


class Metadata(BaseModel):
    display_phone_number: str
    phone_number_id: str


class Value(BaseModel):
    messaging_product: str
    metadata: Metadata
    contacts: List[RequestContact]
    messages: Optional[List[Message]] = None
    statuses: Optional[List[Status]] = None


class Change(BaseModel):
    value: Value
    field: str


class Entry(BaseModel):
    id: str
    changes: List[Change]


class Update(BaseModel):
    object: str
    entry: List[Entry]
