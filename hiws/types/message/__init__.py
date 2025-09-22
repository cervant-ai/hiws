from pydantic import BaseModel, Field
from typing import List, Optional
from hiws.types.message.contact import Contact


class BaseMessage(BaseModel):
    from_phone_number: str = Field(alias="from")
    id: str
    timestamp: str

class Text(BaseModel):
    body: str

class TextMessage(BaseMessage):
    text: Text
    type: str = "text"
    
class Reaction(BaseModel):
    message_id: str
    emoji: str
    
class ReactionMessage(BaseMessage):
    reaction: Reaction
    type: str = "reaction"
    
class Media(BaseModel):
    id: str
    mime_type: str
    caption: str
    sha256: str
    
class ImageMessage(BaseMessage):
    image: Media
    type: str = "image"
    
class StickerMessage(BaseMessage):
    sticker: Media
    type: str = "sticker"
    
class MessageError(BaseModel):
    code: int
    details: str
    title: str

class UnknownMessage(BaseModel):
    errors: List[MessageError]
    type: str = "unknown"
    
class Location(BaseModel):
    latitude: float
    longitude: float
    name: Optional[str]
    address: Optional[str]
    
class LocationMessage(BaseMessage):
    location: Location
    type: str = "location"
    
class ContactMessage(BaseMessage):
    contacts: List[Contact]
    type: str = "contacts"
    
class Button(BaseModel):
    text: str
    payload: Optional[str]
    
class QuickReplyButtonMessage(BaseMessage):
    button: Button
    type: str = "button"
    
class SystemUpdate(BaseModel):
    body: str
    type: str = "system"
    new_wa_id: Optional[str]
    
class SystemMessage(BaseMessage):
    system: SystemUpdate
    type: str = "system"
    

type Message = TextMessage | ReactionMessage | ImageMessage | StickerMessage | LocationMessage | QuickReplyButtonMessage | SystemMessage | UnknownMessage