import asyncio
import os

from modules import logging
from modules.bot import Bot
from modules.name_filter import NameFilterHandler


async def main():
    logging.setup_logging()

    token = os.environ.get("BOT_TOKEN")

    bot = Bot(token)

    bot.root_handler().append(NameFilterHandler())

    while True:
        await bot.poll_updates()

if __name__ == "__main__":
    asyncio.run(main())
