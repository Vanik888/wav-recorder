# from .libs.logger import CustomLogger
import os
from random import randint

from common_libs.logger import CustomLogger
from common_libs.config_reader import ConfigReader

logger = CustomLogger(module=__name__).get_logger()
logger.info('started')


class Sender():
    def __init__(self, **kwargs):
        self._CONF_FILE_NAME = 'base.cfg'
        self._SECTION = 'sender'

        params = self._get_config(**kwargs)
        self._INPUT_FILE_DIR = params['INPUT_FILE_DIR']
        self._OUTPUT_FILE_DIR = params['OUTPUT_FILE_DIR']
        self._YA_KEY = params['YA_KEY']
        self._FILE_NAME = params['FILE_NAME']
        self._UUID = self._generate_uuid()
        self._CMD = 'curl -4 "asr.yandex.net/asr_xml?key=%(YA_KEY)s&' \
                    'uuid=%(UUID)s&topic=queries&lang=ru-RU" ' \
                    '-H "Content-Type: audio/x-wav" --data-binary ' \
                    '"@%(INPUT_FILE_DIR)s/%(FILE_NAME)s" > ' \
                    '%(OUTPUT_FILE_DIR)s/result.xml'

    def _get_config(self, **kwargs):
        module_dir = os.path.dirname(os.path.abspath(__file__))
        local_conf_file = os.path.join(module_dir, self._CONF_FILE_NAME)
        self._config_reader = ConfigReader(local_conf_file, self._SECTION)
        return self._config_reader.get_complete_config(**kwargs)

    def _generate_uuid(self):
        UUID_LEN = 32
        MIN_VAL_LIMIT = 10**(UUID_LEN-1)
        MAX_VAL_LIMIT = 10**UUID_LEN-1
        return randint(MIN_VAL_LIMIT, MAX_VAL_LIMIT)

    def send(self):
        FILLED_CMD = self._CMD % {'YA_KEY': self._YA_KEY, 'UUID': self._UUID,
                                  'INPUT_FILE_DIR': self._INPUT_FILE_DIR,
                                  'FILE_NAME': self._FILE_NAME,
                                  'OUTPUT_FILE_DIR': self._OUTPUT_FILE_DIR}
        logger.info(FILLED_CMD)
        os.system('pwd')
        os.system('ls -ls')
        logger.info('start curl command')
        # os.system('curl yandex.ru > self._OUTPUT_FILE_DIR/result.xml')
        os.system(FILLED_CMD)
        logger.info(os.path)


if __name__ == '__main__':
    sender = Sender()
    sender.send()

