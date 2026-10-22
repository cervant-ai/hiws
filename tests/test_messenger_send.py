import pytest

from hiws import WhatsappMessenger


@pytest.fixture
def messenger(monkeypatch):
    messenger = WhatsappMessenger(access_token="token", phone_number_id="123")
    messenger.sent_payloads = []

    async def fake_send_message_payload(payload):
        messenger.sent_payloads.append(payload)
        return "wamid.X"

    monkeypatch.setattr(messenger, "_send_message_payload", fake_send_message_payload)
    return messenger


@pytest.mark.asyncio
async def test_send_cta_url_payload(messenger):
    message_id = await messenger.send_cta_url(
        recipient_phone_number="16505551234",
        body_text="Here is your offer",
        display_text="Open offer",
        url="https://crvnt.link/AbCdEfGhIjKlMnOp",
    )

    assert message_id == "wamid.X"
    assert messenger.sent_payloads == [
        {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": "16505551234",
            "type": "interactive",
            "interactive": {
                "type": "cta_url",
                "body": {"text": "Here is your offer"},
                "action": {
                    "name": "cta_url",
                    "parameters": {
                        "display_text": "Open offer",
                        "url": "https://crvnt.link/AbCdEfGhIjKlMnOp",
                    },
                },
            },
        }
    ]


@pytest.mark.asyncio
async def test_send_cta_url_reply_to_adds_context(messenger):
    await messenger.send_cta_url(
        recipient_phone_number="16505551234",
        body_text="Body",
        display_text="Open",
        url="https://example.com",
        reply_to="wamid.PARENT",
    )

    assert messenger.sent_payloads[0]["context"] == {"message_id": "wamid.PARENT"}


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("body_text", "display_text", "url"),
    [
        ("b" * 1024, "Open", "https://example.com"),
        ("b", "d" * 20, "https://example.com"),
        ("b", "d", "http://example.com/path?q=1"),
    ],
)
async def test_send_cta_url_accepts_limits(messenger, body_text, display_text, url):
    await messenger.send_cta_url("16505551234", body_text, display_text, url)

    assert len(messenger.sent_payloads) == 1


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("body_text", "display_text", "url"),
    [
        ("", "Open", "https://example.com"),
        ("b" * 1025, "Open", "https://example.com"),
        ("b", "", "https://example.com"),
        ("b", "d" * 21, "https://example.com"),
        ("b", "Open", "ftp://example.com/file"),
        ("b", "Open", "crvnt.link/abc"),
        ("b", "Open", "https://"),
    ],
)
async def test_send_cta_url_rejects_invalid_input(messenger, body_text, display_text, url):
    with pytest.raises(ValueError):
        await messenger.send_cta_url("16505551234", body_text, display_text, url)

    assert messenger.sent_payloads == []


@pytest.mark.asyncio
async def test_send_text_payload_unchanged(messenger):
    message_id = await messenger.send_text(
        recipient_phone_number="16505551234",
        text="Hello",
        reply_to="wamid.PARENT",
    )

    assert message_id == "wamid.X"
    assert messenger.sent_payloads == [
        {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": "16505551234",
            "type": "text",
            "text": {"preview_url": True, "body": "Hello"},
            "context": {"message_id": "wamid.PARENT"},
        }
    ]
