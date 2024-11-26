import aiohttp
from modules import logging


class Bot:
    def __init__(self, token):
        self.__token = token
        self.__logger = logging.init_logger(f"{__name__}.bot-{token[0:4]}")

        self.__session = aiohttp.ClientSession()

        self.__last_update = None

    async def pull_updates(self):
        self.__logger.debug("Pulling updates")

        try:
            request_params = dict()
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
