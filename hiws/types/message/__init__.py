from pydantic import BaseModel, Field
from typing import List, Optional, Union, Literal
from hiws.types.message.contact import Contact


class MessageContext(BaseModel):
    from_phone_number: Optional[str] = Field(default=None, alias="from")
    id: Optional[str] = None


class BaseMessage(BaseModel):
    # Senders with a WhatsApp username (BSUID) may come without a phone number.
    from_phone_number: Optional[str] = Field(default=None, alias="from")
    from_user_id: Optional[str] = None
    id: str
    timestamp: str
    context: Optional[MessageContext] = None

class Text(BaseModel):
    body: str

class TextMessage(BaseMessage):
    text: Text
    type: Literal["text"] = "text"
    
class Reaction(BaseModel):
    message_id: str
    # Omitted when the user removes their reaction.
    emoji: Optional[str] = None
    
class ReactionMessage(BaseMessage):
    reaction: Reaction
    type: Literal["reaction"] = "reaction"
    
class Media(BaseModel):
    id: str
    mime_type: str
    caption: Optional[str] = None
    sha256: str
    
class ImageMessage(BaseMessage):
    image: Media
    type: Literal["image"] = "image"

class Audio(BaseModel):
    id: str
    mime_type: str
    sha256: Optional[str] = None
    voice: Optional[bool] = None

class AudioMessage(BaseMessage):
    audio: Audio
    type: Literal["audio"] = "audio"

class Document(BaseModel):
    id: str
    mime_type: str
    sha256: Optional[str] = None
    filename: Optional[str] = None
    caption: Optional[str] = None

class DocumentMessage(BaseMessage):
    document: Document
    type: Literal["document"] = "document"
    
class VideoMessage(BaseMessage):
    video: Media
    type: Literal["video"] = "video"

class StickerMessage(BaseMessage):
    sticker: Media
    type: Literal["sticker"] = "sticker"

class ErrorData(BaseModel):
    details: str
    
class MessageError(BaseModel):
    code: int
    title: str
    message: Optional[str] = None
    error_data: Optional[ErrorData] = None
    
class Unsupported(BaseModel):
    # Known values: "edit", "poll", "button", "unknown", "album". Meta keeps adding
    # new ones, so accept any string instead of rejecting the webhook.
    type: str
    raw_type: Optional[str] = None

class UnsupportedMessage(BaseMessage):
    errors: List[MessageError] = []
    type: Literal["unsupported"] = "unsupported"
    unsupported: Unsupported
    
class Location(BaseModel):
    latitude: float
    longitude: float
    name: Optional[str] = None
    address: Optional[str] = None
    
class LocationMessage(BaseMessage):
    location: Location
    type: Literal["location"] = "location"
    
class ContactMessage(BaseMessage):
    contacts: List[Contact]
    type: Literal["contacts"] = "contacts"
    
class Button(BaseModel):
    text: str
    payload: Optional[str] = None
    
class QuickReplyButtonMessage(BaseMessage):
    button: Button
    type: Literal["button"] = "button"
    
class SystemUpdate(BaseModel):
    body: str
    # e.g. "user_changed_number", "customer_identity_changed".
    type: str = "system"
    new_wa_id: Optional[str] = None
    wa_id: Optional[str] = None
    user_id: Optional[str] = None
    previous_user_id: Optional[str] = None
    
class SystemMessage(BaseMessage):
    system: SystemUpdate
    type: Literal["system"] = "system"
    
class ListReply(BaseModel):
    id: str
    title: str
    description: Optional[str] = None

class ButtonReply(BaseModel):
    id: str
    title: str


class NFMReply(BaseModel):
    name: Optional[str] = None
    body: Optional[str] = None
    response_json: str


class Interactive(BaseModel):
    type: Literal["list_reply", "button_reply", "nfm_reply"]
    list_reply: Optional[ListReply] = None
    button_reply: Optional[ButtonReply] = None
    nfm_reply: Optional[NFMReply] = None


class InteractiveMessage(BaseMessage):
    interactive: Interactive
    type: Literal["interactive"] = "interactive"


class OrderMessage(BaseMessage):
    order: dict
    type: Literal["order"] = "order"


Message = Union[
    TextMessage,
    ReactionMessage,
    ImageMessage,
    VideoMessage,
    AudioMessage,
    DocumentMessage,
    StickerMessage,
    LocationMessage,
    QuickReplyButtonMessage,
    ContactMessage,
    SystemMessage,
    InteractiveMessage,
    OrderMessage,
    UnsupportedMessage,
]
