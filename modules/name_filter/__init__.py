from modules import logging
from modules.bot.handling import UpdateHandler

class NameFilterHandler(UpdateHandler):
    def __init__(self):
        super().__init__()
        self.__logger = logging.init_logger(__name__)

        self.__block_regexs = list()

    def __get_new_member_data(self, update):
        try:
            return update["message"]["new_chat_member"]
        except KeyError:
            return None

    def __is_forbidden(self, text):
        pass

    def __kick_user_by_id(self):
        pass

    def handle(self, update):
        self.__logger.debug(
            f"Checking if update mentions a new chat member: {update}"
        )

        new_member_data = self.__get_new_member_data(update)
        if new_member_data is None:
            return

        self.__logger.debug(f"New member data: {new_member_data}")

        id = new_member_data["id"]
        first_name = new_member_data["first_name"]
        username = new_member_data["username"]

        if self.__is_forbidden(first_name) or self.__is_forbidden(username):
            self.__kick_user_by_id(id)

        return self.consume()
