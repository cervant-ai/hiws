import json
from pathlib import Path

from hiws import Update
from hiws.types.message import QuickReplyButtonMessage, TextMessage
from hiws.types.status import FailedStatus, ReadStatus


FIXTURES = Path(__file__).parent / "fixtures"


def load_fixture(name: str) -> dict:
    return json.loads((FIXTURES / name).read_text())


def test_campaign_webhook_fixture_preserves_all_messages_and_statuses():
    update = Update.model_validate(load_fixture("campaign_webhook.json"))

    assert [message.id for message in update.messages] == [
        "wamid.reply-1",
        "wamid.text-1",
    ]
    assert isinstance(update.message, QuickReplyButtonMessage)
    assert update.message.context is not None
    assert update.message.context.id == "wamid.outbound-1"
    assert update.message.context.from_phone_number == "15550000001"
    assert update.message.button.payload == "YES"

    assert [status.status for status in update.statuses] == [
        "read",
        "delivered",
        "delivered",
        "sent",
        "failed",
    ]
    assert isinstance(update.status, ReadStatus)
    assert update.statuses[1].pricing is not None
    assert update.statuses[1].pricing.type == "free_customer_service"
    assert isinstance(update.statuses[-1], FailedStatus)
    assert update.statuses[-1].errors[0].code == 131014
    assert update.statuses[-1].errors[0].error_data.details == "Not Found"


def test_message_without_context_fixture_allows_missing_user_id():
    update = Update.model_validate(load_fixture("message_without_context.json"))

    assert isinstance(update.message, TextMessage)
    assert update.message.from_user_id is None
    assert update.message.context is None
