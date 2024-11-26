import re

from typing import List
from modules import logging
from modules.bot.handling import UpdateHandler
from modules.bot.session import TelegramHTTPSession


class NameFilterHandler(UpdateHandler):
    def __init__(self, session: TelegramHTTPSession, block_expressions: List[str]):
        super().__init__()
        self.__logger = logging.init_logger(__name__)

        self.__session = session

        self.__block_expressions = block_expressions

        self.__logger.info(
            f"Initialized name filter handler with the following block expressions: {self.__block_expressions}"
        )

    def __get_new_member_data(self, update):
        try:
            return update["message"]["new_chat_member"]
        except KeyError:
            return None

    def __contains_block_expression(self, text):
        for expression in self.__block_expressions:
            if re.search(expression, text) is not None:
                return True

        return False

    def __kick_user_by_id(self, chat_id: int, user_id: int):
        self.__logger.info(f"Kicking user {user_id} from chat {chat_id}...")
        self.__session.request(
            "POST", "banChatMember", data={"chat_id": chat_id, "user_id": user_id}
        )

    def handle(self, update):
        self.__logger.debug(f"Checking if update mentions a new chat member: {update}")

        new_member_data = self.__get_new_member_data(update)
        if new_member_data is None:
            return

        self.__logger.debug(f"New member data: {new_member_data}")

        user_id = new_member_data["id"]
        first_name = new_member_data["first_name"]
        username = new_member_data["username"]

        if self.__contains_block_expression(
            first_name
        ) or self.__contains_block_expression(username):
            self.__logger.debug("User has forbidden name or username")

            chat_id = update["chat_id"]
            self.__kick_user_by_id(chat_id, user_id)

        return self.consume()
