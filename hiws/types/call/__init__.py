from pydantic import BaseModel, Field
from typing import Optional, Union, Literal


class CallSession(BaseModel):
    sdp_type: Literal["offer", "answer"]
    sdp: str


class CallError(BaseModel):
    code: int
    message: str
    href: Optional[str] = None
    error_data: Optional[dict] = None


class BaseCall(BaseModel):
    id: str
    to: str
    from_phone_number: str = Field(alias="from")
    from_user_id: Optional[str] = None
    from_parent_user_id: Optional[str] = None
    timestamp: str
    direction: Optional[str] = None
    deeplink_payload: Optional[str] = None
    cta_payload: Optional[str] = None


class ConnectCall(BaseCall):
    session: CallSession
    event: Literal["connect"] = "connect"


class TerminateCall(BaseCall):
    status: Optional[str] = None
    start_time: Optional[str] = None
    end_time: Optional[str] = None
    duration: Optional[int] = None
    biz_opaque_callback_data: Optional[str] = None
    event: Literal["terminate"] = "terminate"


Call = Union[ConnectCall, TerminateCall]
