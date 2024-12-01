from unittest.mock import AsyncMock
import logging
import pytest

from modules.bot.session import TelegramHTTPSession
from modules.logging import setup_logging
from modules.name_filter import NameFilterHandler

DEFAULT_TOKEN = "TEST:TOKEN"
DEFAULT_CHAT_ID = 1
DEFAULT_USER_ID = 1000


class MockSession(TelegramHTTPSession):
    def __init__(self):
        self.request = AsyncMock()

    def expect_ban(self, chat_id=DEFAULT_CHAT_ID, user_id=DEFAULT_USER_ID):
        self.request.assert_called_with(
            "POST",
            "banChatMember",
            data={"chat_id": chat_id, "user_id": user_id},
        )

    def expect_no_bans(self):
        self.request.assert_not_called()


def build_update(first_name, username):
    return {
        "message": {
            "chat": {"id": DEFAULT_CHAT_ID},
            "new_chat_member": {
                "id": DEFAULT_USER_ID,
                "first_name": first_name,
                "username": username,
            },
        }
    }


async def __execute_with(first_name, username, block_expressions, should_ban):
    mock_session = MockSession()
    filter = NameFilterHandler(mock_session, block_expressions)
    await filter.handle(build_update(first_name, username))
    if should_ban:
        mock_session.expect_ban()
    else:
        mock_session.expect_no_bans()


@pytest.mark.parametrize(
    "first_name,username,block_expressions",
    [
        ("Drugo drago", "thedrugo", [".*drug.*"]),
        ("Kitty freesex", "kittypig", [".*sex.*"]),
    ],
)
@pytest.mark.asyncio
async def test_block(first_name, username, block_expressions):
    await __execute_with(first_name, username, block_expressions, True)


@pytest.mark.parametrize(
    "first_name,username,block_expressions",
    [
        ("Mario Buoni", "mariobuoni79", [".*drug.*", ".*sex.*"]),
    ],
)
@pytest.mark.asyncio
async def test_do_not_block(first_name, username, block_expressions):
    await __execute_with(first_name, username, block_expressions, False)


PRODUCTION_BLOCKLIST = [
    "porco dio",
    "porcoddio",
    "dio cane",
    "dio porco",
    "apri le gambe",
    "porca madonna",
    "porcamadonna",
    "weed",
    ".*weed.*",
    ".*🍑.*",
    ".*🔫.*",
    ".*💊.*",
    ".*ketamine.*",
    ".*🍆.*",
    ".*dio.*porco.*",
    ".*dio.*cane.*",
    ".*dio.*maiale.*",
    ".*madonna.*maiala.*",
    "𝗗𝗥𝗢𝗚u𝗘, 𝗩𝗜𝗔𝗚𝗥𝗔",
    ".*𝗔.*",
    ".*𝗥.*",
    ".*𝗜.*",
    ".*𝗘.*",
    ".*𝗗.*",
    ".*𝗚.*",
    ".*🧫.*",
    ".*dealer.*",
    ".*drug.*",
]


@pytest.mark.parametrize(
    "first_name,username",
    [
        ("Drugo drago", "thedrugo"),
        ("Drugo drago", "drugo_the_dealer"),
        ("Drugo The Dealer", "drugo_the_dealer"),
        ("Salvo Fumeri", "Salvo_Dealer"),
        ("𝙒𝙀𝙀𝘿🌳𝘾𝙊𝙆𝙀 🍚𝙑𝙄𝘼𝙂𝙍𝘼💊𝙈𝘿𝙈𝘼🧫𝙎𝙃𝙄𝙏🍁𝙎𝙋𝙀𝙀𝘿💠𝗠𝗘𝗧𝗛❄️𝗛𝗔𝗦𝗛🍫🍄𝗟𝗦𝗗🍭", "Ralf_Dealer12"),
        ("Weed 🍁Stores🍁", "@sam8_3"),
    ],
)
@pytest.mark.asyncio
async def test_block_with_production_blocklist(first_name, username):
    await __execute_with(first_name, username, PRODUCTION_BLOCKLIST, True)
