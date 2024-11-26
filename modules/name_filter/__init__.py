from modules.bot.handling import BLOCK, PASS, UpdateHandler


class NameFilterHandler(UpdateHandler):
    def __init__(self):
        super().__init__()

        self.__block_regexs = list()

    def __get_new_member_data(update):
        try:
            return update["message"]["new_chat_member"]
        except KeyError:
            return None

    def handle(self, update):
        self.__logger().debug(f"Checking if update mentions a new chat member: {update}")

        new_member_data = self.__get_new_member_data(update)
        if new_member_data is None:
            return PASS

        return BLOCK
