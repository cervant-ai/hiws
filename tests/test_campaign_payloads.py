import json
from pathlib import Path

from hiws import Update
from hiws.types.message import (
    InteractiveMessage,
    OrderMessage,
    QuickReplyButtonMessage,
    TextMessage,
)
from hiws.types.status import FailedStatus, ReadStatus


FIXTURES = Path(__file__).parent / "fixtures"


def load_fixture(name: str) -> dict:
    return json.loads((FIXTURES / name).read_text())


def message_payload(message: dict) -> dict:
    return {
        "object": "whatsapp_business_account",
        "entry": [
            {
                "id": "waba-1",
                "changes": [
                    {
                        "field": "messages",
                        "value": {
                            "messaging_product": "whatsapp",
                            "metadata": {
                                "display_phone_number": "15550000001",
                                "phone_number_id": "phone-1",
                            },
                            "contacts": [
                                {
                                    "profile": {"name": "Tomas"},
                                    "wa_id": "584121234567",
                                }
                            ],
                            "messages": [message],
                        },
                    }
                ],
            }
        ],
    }


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


def test_flow_reply_is_parsed_for_safe_rejection():
    update = Update.model_validate(
        message_payload(
            {
                "from": "584121234567",
                "id": "wamid.flow-1",
                "timestamp": "1788350400",
                "type": "interactive",
                "interactive": {
                    "type": "nfm_reply",
                    "nfm_reply": {
                        "name": "flow",
                        "body": "Sent",
                        "response_json": '{"choice":"one"}',
                    },
                },
            }
        )
    )

    assert isinstance(update.message, InteractiveMessage)
    assert update.message.interactive.nfm_reply is not None
    assert update.message.interactive.nfm_reply.response_json == '{"choice":"one"}'


def test_order_is_parsed_for_safe_rejection():
    update = Update.model_validate(
        message_payload(
            {
                "from": "584121234567",
                "id": "wamid.order-1",
                "timestamp": "1788350400",
                "type": "order",
                "order": {
                    "catalog_id": "catalog-1",
                    "product_items": [
                        {"product_retailer_id": "product-1", "quantity": 1}
                    ],
                },
            }
        )
    )

    assert isinstance(update.message, OrderMessage)
    assert update.message.order["catalog_id"] == "catalog-1"
