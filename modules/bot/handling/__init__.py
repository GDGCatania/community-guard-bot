from modules import logging


class UpdateHandler:
    def __init__(self):
        pass

    def consume(self):
        return True

    def handle(self, update):
        raise NotImplementedError
