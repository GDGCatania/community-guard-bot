import asyncio
import os

from modules import logging
from modules.bot import Bot


async def main():
    logging.setup_logging()

    token = os.environ.get("BOT_TOKEN")

    bot = Bot(token)
    while True:
        await bot.pull_updates()
        await asyncio.sleep(1.0)


if __name__ == "__main__":
    asyncio.run(main())
