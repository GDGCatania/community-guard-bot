import asyncio
import os

from modules import logging
from modules.bot import Bot
from modules.bot.session import TelegramHTTPSession
from modules.name_filter import NameFilterHandler
from modules.name_filter.utils import parse_block_expressions_from_string


def name_filter_chain(session: TelegramHTTPSession):
    block_expressions = parse_block_expressions_from_string(
        os.environ.get("NAME_BLOCK_EXPRESSIONS")
    )
    return NameFilterHandler(session, block_expressions)


async def main():
    logging.setup_logging()

    session = TelegramHTTPSession(os.environ.get("BOT_TOKEN"))

    bot = Bot(session)

    bot.root_handler().append(name_filter_chain(session))

    while True:
        await bot.poll_updates()


if __name__ == "__main__":
    asyncio.run(main())
