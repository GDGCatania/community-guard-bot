import aiohttp
from modules import logging
from modules.bot.handling.sequential import SequentialHandler


class Bot:
    def __init__(self, token, polling_update=10):
        self.__token = token
        self.__logger = logging.init_logger(f"{__name__}.bot-{token[0:4]}")

        self.__session = aiohttp.ClientSession()

        self.__polling_update = polling_update
        self.__last_update = None

        self.__root_handler = SequentialHandler()

    def root_handler(self) -> SequentialHandler:
        return self.__root_handler

    async def poll_updates(self):
        self.__logger.debug("Polling updates")

        try:
            request_params = {"timeout": self.__polling_update}

            if self.__last_update is not None:
                request_params["offset"] = self.__last_update + 1

            response = await self.__session.get(
                f"https://api.telegram.org/bot{self.__token}/GetUpdates",
                params=request_params,
            )

            body = await response.json()
            updates = body["result"]

            if len(updates) == 0:
                self.__logger.debug("No updates pulled.")
                return

            for update in updates:
                self.__logger.debug(f"Pulled update: {update}")

            self.__last_update = updates[-1]["update_id"]
        except Exception:
            self.__logger.exception("Unable to pull updates")
