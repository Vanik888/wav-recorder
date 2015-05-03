# from .libs.logger import CustomLogger
import os
import sys
from random import randint

from libs.logger import CustomLogger

logger = CustomLogger(module=__name__).get_logger()
logger.info('started')


class Sender():
    def __init__(self):
        logger.info('sender is created')
        self._YA_KEY = '728aa4bd-e35d-4cd8-833c-00a4cf790b4a'
        self._UUID = self._generate_uuid()
        self._FILE_NAME = 'custom'
        self._CMD = 'curl -4 "asr.yandex.net/asr_xml?key=%(YA_KEY)s&' \
                    'uuid=%(UUID)s&topic=queries&lang=ru-RU" ' \
                    '-H "Content-Type: audio/x-wav" --data-binary ' \
                    '"@../%(FILE_NAME)s.wav" > result.xml'

    def _generate_uuid(self):
        UUID_LEN = 32
        MIN_VAL_LIMIT = 10**(UUID_LEN-1)
        MAX_VAL_LIMIT = 10**UUID_LEN-1
        return randint(MIN_VAL_LIMIT, MAX_VAL_LIMIT)

    def send(self):
        FILLED_CMD = self._CMD % {'YA_KEY': self._YA_KEY, 'UUID': self._UUID,
                                  'FILE_NAME': self._FILE_NAME}
        logger.info(FILLED_CMD)
        os.system('ls -ls')
        logger.info('start curl command')
        # a = os.system('curl yandex.ru > result.xml')
        # logger.info("a = %s" % a)
        os.system(FILLED_CMD)


if __name__ == '__main__':
    sender = Sender()
    sender.send()

