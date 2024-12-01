import re

from typing import List
from modules import logging
from modules.bot.handling import UpdateHandler
from modules.bot.session import TelegramHTTPSession


class NameFilterHandler(UpdateHandler):
    def __init__(
        self,
        session: TelegramHTTPSession,
        block_expressions: List[str],
        notifications_chat_id=None,
    ):
        super().__init__()
        self.__logger = logging.init_logger(__name__)

        self.__session = session

        self.__block_expressions = block_expressions
        self.__notifications_chat_id = notifications_chat_id

        self.__logger.info(
            f"Initialized name filter handler with the following block expressions: {self.__block_expressions}"
        )

    def __get_new_member_data(self, update):
        try:
            return update["message"]["new_chat_member"]
        except KeyError:
            return None

    def __search_block_expression(self, text):
        self.__logger.debug(f"Checking text {text}...")
        lowercase = text.lower()
        for expression in self.__block_expressions:
            self.__logger.debug(f"Comparing with expression {expression}...")
            if re.search(expression, lowercase) is not None:
                self.__logger.debug(f"Match with block expression {expression}")
                return expression

        return None

    async def __send_ban_notification(
        self, chat_id: int, user_id: int, block_expression: str
    ):
        if self.__notifications_chat_id is None:
            return

        self.__logger.info(
            f"Sending ban notification for user {user_id} trying to join chat {chat_id}..."
        )

        await self.__session.request(
            "POST",
            "sendMessage",
            data={
                "chat_id": self.__notifications_chat_id,
                "text": f"Banning user {user_id} from chat {chat_id} due to block expression: {block_expression}",
            },
        )

    async def __ban_user_by_id(self, chat_id: int, user_id: int):
        self.__logger.info(f"Kicking user {user_id} from chat {chat_id}...")

        await self.__session.request(
            "POST", "banChatMember", data={"chat_id": chat_id, "user_id": user_id}
        )

    async def handle(self, update):
        self.__logger.debug(f"Checking if update mentions a new chat member: {update}")

        new_member_data = self.__get_new_member_data(update)
        if new_member_data is None:
            return

        self.__logger.debug(f"New member data: {new_member_data}")

        user_id = new_member_data["id"]
        first_name = new_member_data["first_name"]
        username = new_member_data["username"]

        block_expression = self.__search_block_expression(
            first_name
        ) or self.__search_block_expression(username)
        if block_expression is not None:
            self.__logger.debug("User has forbidden name or username")

            chat_id = update["message"]["chat"]["id"]
            await self.__send_ban_notification(chat_id, user_id, block_expression)
            await self.__ban_user_by_id(chat_id, user_id)

        return self.consume()
