from pydantic import BaseModel
from typing import List, Literal, Optional

class StatusPricing(BaseModel):
    pricing_model: str
    billable: bool
    category: Optional[str] = None
    type: Optional[str] = None

class StatusConversationOrigin(BaseModel):
    type: str
    
class StatusConversation(BaseModel):
    id: str
    expiration_timestamp: Optional[str] = None
    origin: Optional[StatusConversationOrigin] = None
    
class StatusErrorData(BaseModel):
    details: str
    
class StatusError(BaseModel):
    code: int
    title: str
    message: Optional[str] = None
    error_data: Optional[StatusErrorData] = None
    href: Optional[str] = None
    

class BaseStatus(BaseModel):
    id: str
    status: Literal["delivered", "read", "failed", "sent"]
    timestamp: str
    recipient_id: str
    recipient_user_id: Optional[str] = None
    conversation: Optional[StatusConversation] = None
    pricing: Optional[StatusPricing] = None
    
class SentStatus(BaseStatus):
    status: Literal["sent"]

class DeliveredStatus(BaseStatus):
    status: Literal["delivered"]
    
class ReadStatus(BaseStatus):
    status: Literal["read"]

class FailedStatus(BaseStatus):
    status: Literal["failed"]
    errors: List[StatusError]

type Status = SentStatus | DeliveredStatus | ReadStatus | FailedStatus

