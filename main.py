import asyncio
import os

from modules import logging
from modules.bot import Bot
from modules.bot.session import TelegramHTTPSession
from modules.name_filter import NameFilterHandler


async def main():
    logging.setup_logging()

    session = TelegramHTTPSession(os.environ.get("BOT_TOKEN"))

    bot = Bot(session)

    bot.root_handler().append(NameFilterHandler())

    while True:
        await bot.poll_updates()


if __name__ == "__main__":
    asyncio.run(main())
