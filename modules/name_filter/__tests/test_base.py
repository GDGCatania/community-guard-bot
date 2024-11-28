from unittest.mock import AsyncMock
import pytest

from modules.bot.session import TelegramHTTPSession
from modules.name_filter import NameFilterHandler

DEFAULT_TOKEN = "TEST:TOKEN"
DEFAULT_CHAT_ID = 1
DEFAULT_USER_ID = 1000

@pytest.mark.asyncio
async def test_no_block():
    block_expressions = [".*drug.*"]
    mock_session = TelegramHTTPSession(DEFAULT_TOKEN)
    mock_session.request = AsyncMock()
    filter = NameFilterHandler(mock_session, block_expressions)

    await filter.handle({
        "message": {
            "chat": {
                "id": DEFAULT_CHAT_ID
            },
            "new_chat_member": {
                "id": DEFAULT_USER_ID,
                "first_name": "Drugo drago",
                "username": "thedrugo",
            }
        }
    })

    mock_session.request.assert_called_with()
