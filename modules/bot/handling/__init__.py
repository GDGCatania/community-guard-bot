from modules import logging

PASS = True
BLOCK = False


class UpdateHandler:
    def __init__(self):
        self.__logger = logging.init_logger(__name__)

    def _logger(self):
        return self.__logger

    def handle(self, update):
        raise NotImplementedError
