from typing import Self
from modules.bot.handling import BLOCK, UpdateHandler


class SequentialHandler(UpdateHandler):
    def __init__(self, terminal=BLOCK):
        super().__init__()

        self.__terminal = terminal
        self.__handlers = list()

    def append(self, handler: UpdateHandler) -> Self:
        self.__handlers.append(handler)
        return self

    def handle(self, update):
        for handler in self.__handlers:
            keep_handling = handler(update)
            if not keep_handling:
                break

        return self.__terminal
