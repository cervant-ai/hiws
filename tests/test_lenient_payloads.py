"""Payload shapes seen in production that older models rejected."""

from hiws.types import Update
from hiws.types.message import (
    ReactionMessage,
    SystemMessage,
    TextMessage,
    UnsupportedMessage,
    VideoMessage,
)


def _update(message: dict, contacts: list | None = None) -> Update:
    value = {
        "messaging_product": "whatsapp",
        "metadata": {"display_phone_number": "15550000000", "phone_number_id": "100"},
        "messages": [message],
    }
    if contacts is not None:
        value["contacts"] = contacts
    return Update.model_validate(
        {
            "object": "whatsapp_business_account",
            "entry": [{"id": "1", "changes": [{"field": "messages", "value": value}]}],
        }
    )


CONTACT = [{"profile": {"name": "Ana"}, "wa_id": "15551234567", "user_id": "US.1"}]


def _base(type_: str) -> dict:
    return {
        "from": "15551234567",
        "from_user_id": "US.1",
        "id": f"wamid.{type_}",
        "timestamp": "1793304431",
        "type": type_,
    }


def test_text_from_username_only_sender():
    update = _update(
        {
            "from_user_id": "PE.2876",
            "id": "wamid.text",
            "timestamp": "1793668294",
            "text": {"body": "Hola"},
            "type": "text",
        },
        contacts=[{"profile": {"name": "Ana", "username": "ana"}, "user_id": "PE.2876"}],
    )
    msg = update.message
    assert isinstance(msg, TextMessage)
    assert msg.from_phone_number is None
    assert msg.from_user_id == "PE.2876"
    assert update.contact.wa_id is None
    assert update.contact.user_id == "PE.2876"


def test_video():
    msg = _update(
        {
            **_base("video"),
            "video": {
                "caption": "Interesada en este",
                "mime_type": "video/mp4",
                "sha256": "abc=",
                "id": "1100",
                "url": "https://lookaside.fbsbx.com/whatsapp_business/attachments/?mid=1100",
            },
        },
        CONTACT,
    ).message
    assert isinstance(msg, VideoMessage)
    assert msg.video.id == "1100"
    assert msg.video.caption == "Interesada en este"


def test_unsupported_album():
    msg = _update(
        {
            **_base("unsupported"),
            "errors": [
                {
                    "code": 131051,
                    "title": "Message type unknown",
                    "message": "Message type unknown",
                    "error_data": {"details": "Message type is currently not supported."},
                }
            ],
            "unsupported": {"type": "album", "raw_type": "album"},
        },
        CONTACT,
    ).message
    assert isinstance(msg, UnsupportedMessage)
    assert msg.unsupported.type == "album"


def test_unsupported_without_errors():
    msg = _update({**_base("unsupported"), "unsupported": {"type": "poll"}}, CONTACT).message
    assert isinstance(msg, UnsupportedMessage)
    assert msg.errors == []


def test_unsupported_with_minimal_error():
    msg = _update(
        {
            **_base("unsupported"),
            "errors": [{"code": 131051, "title": "Message type unknown"}],
            "unsupported": {"type": "album"},
        },
        CONTACT,
    ).message
    assert isinstance(msg, UnsupportedMessage)
    assert msg.errors[0].code == 131051


def test_reaction_removal():
    msg = _update({**_base("reaction"), "reaction": {"message_id": "wamid.X"}}, CONTACT).message
    assert isinstance(msg, ReactionMessage)
    assert msg.reaction.message_id == "wamid.X"
    assert msg.reaction.emoji is None


def test_reaction_with_emoji():
    msg = _update(
        {**_base("reaction"), "reaction": {"message_id": "wamid.X", "emoji": "👍"}}, CONTACT
    ).message
    assert isinstance(msg, ReactionMessage)
    assert msg.reaction.emoji == "👍"


def test_system_user_changed_number_without_contacts():
    update = _update(
        {
            **_base("system"),
            "system": {
                "body": "User A changed from 15551234567 to 15557654321",
                "wa_id": "15557654321",
                "user_id": "US.1",
                "previous_user_id": "US.0",
                "type": "user_changed_number",
            },
        }
    )
    msg = update.message
    assert isinstance(msg, SystemMessage)
    assert msg.system.type == "user_changed_number"
    assert msg.system.wa_id == "15557654321"
    assert update.contact is None
