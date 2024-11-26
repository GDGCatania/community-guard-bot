from typing import Self
from modules.bot.handling import UpdateHandler


class SequentialHandler(UpdateHandler):
    def __init__(self, consume=True):
        super().__init__()

        self.__consume = consume
        self.__handlers = list()

    def append(self, handler: UpdateHandler) -> Self:
        self.__handlers.append(handler)
        return self

    def handle(self, update):
        for handler in self.__handlers:
            consumed = handler.handle(update)
            if consumed:
                break

        if self.__consume:
            return self.consume()
