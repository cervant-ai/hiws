from typing import List, Optional
from pydantic import BaseModel
from hiws.types.message import Message
from hiws.types.status import Status
from hiws.types.call import Call


class Profile(BaseModel):
    name: str


class RequestContact(BaseModel):
    profile: Optional[Profile] = None
    wa_id: str
    user_id: Optional[str] = None


class Metadata(BaseModel):
    display_phone_number: str
    phone_number_id: str


class Value(BaseModel):
    messaging_product: str
    metadata: Metadata
    contacts: Optional[List[RequestContact]] = None
    messages: Optional[List[Message]] = None
    statuses: Optional[List[Status]] = None
    calls: Optional[List[Call]] = None


class Change(BaseModel):
    value: Value
    field: str


class Entry(BaseModel):
    id: str
    changes: List[Change]


class Update(BaseModel):
    object: str
    entry: List[Entry]
    
    # helper properties to access nested data easily
    @property
    def messages(self) -> List[Message]:
        return [
            message
            for entry in self.entry
            for change in entry.changes
            for message in (change.value.messages or [])
        ]

    @property
    def message(self) -> Optional[Message]:
        return self.messages[0] if self.messages else None
    @property
    def changed_field(self) -> Optional[str]:
        for entry in self.entry:
            for change in entry.changes:
                return change.field
        return None
    @property
    def statuses(self) -> List[Status]:
        return [
            status
            for entry in self.entry
            for change in entry.changes
            for status in (change.value.statuses or [])
        ]

    @property
    def status(self) -> Optional[Status]:
        return self.statuses[0] if self.statuses else None
    @property
    def contact(self) -> Optional[RequestContact]:
        for entry in self.entry:
            for change in entry.changes:
                if change.value.contacts:
                    return change.value.contacts[0]
        return None
    @property
    def call(self) -> Optional[Call]:
        for entry in self.entry:
            for change in entry.changes:
                if change.value.calls:
                    return change.value.calls[0]
        return None
