import logging


class CustomLogger():
    def __init__(self, **kwargs):
        if 'format' not in kwargs:
            kwargs['format'] = '%(asctime)s - %(name)s - ' \
                               '%(levelname)s - %(message)s'
        if 'level' not in kwargs:
            kwargs['level'] = logging.INFO
        logging.basicConfig(**kwargs)

    def get_logger(self, module):
        return logging.getLogger(module)
