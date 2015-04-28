import logging


class CustomLogger():
    def __init__(self, format='%(asctime)s - %(name)s - %(levelname)s - '
                 '%(message)s',
                 level=logging.DEBUG,
                 module=__name__):
        logging.basicConfig(format=format, level=level)
        self._module = module

    def get_logger(self):
        return logging.getLogger(self._module)
