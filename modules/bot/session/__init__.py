import aiohttp
from modules import logging


class TelegramHTTPSession:
    def __init__(self, token):
        self.__logger = logging.init_logger(__name__)
        self.__token = token
        self._http_session = aiohttp.ClientSession()
        self._base_url = f"https://api.telegram.org/bot{self.__token}"

    def token(self):
        return self.__token

    async def request(self, method: str, action: str, **kwargs):
        url = f"{self._base_url}/{action}"
        self.__logger.debug(
            f"Sending {method} request at endpoint {url} with args {kwargs}..."
        )
        return await self._http_session.request(method, url, **kwargs)
