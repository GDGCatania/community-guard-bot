from modules import logging
from modules.bot.handling.sequential import SequentialHandler
from modules.bot.session import TelegramHTTPSession


class Bot:
    def __init__(self, session: TelegramHTTPSession, polling_timeout=10):
        self.__logger = logging.init_logger(f"{__name__}.bot-{session.token()[0:4]}")

        self.__session = session
        self.__polling_timeout = polling_timeout
        self.__last_update = None

        self.__root_handler = SequentialHandler()

    def root_handler(self) -> SequentialHandler:
        return self.__root_handler

    async def poll_updates(self):
        self.__logger.debug("Polling updates")

        try:
            request_params = {"timeout": self.__polling_timeout}

            if self.__last_update is not None:
                request_params["offset"] = self.__last_update + 1

            response = await self.__session.request(
                "GET", "GetUpdates", params=request_params
            )

            body = await response.json()
            updates = body["result"]

            if len(updates) == 0:
                self.__logger.debug("No updates pulled.")
                return

            for update in updates:
                self.__logger.debug(f"Feeding update to the handler's chain: {update}")
                await self.root_handler().handle(update)

            self.__last_update = updates[-1]["update_id"]
        except Exception:
            self.__logger.exception("Unable to pull updates")
