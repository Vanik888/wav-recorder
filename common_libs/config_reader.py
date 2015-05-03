from configparser import ConfigParser


class ConfigReader():
    def __init__(self, config_file_full_path='base.cfg', section=''):
        self._CONFIG_FILE_FULL_PATH = config_file_full_path
        self._section = section
        self._config_parser = ConfigParser()

    def get_complete_config(self, **kwargs):
        self._config_parser.read(self._CONFIG_FILE_FULL_PATH)
        for item in self._config_parser.items(self._section):
            if item[0].upper() not in kwargs:
                kwargs[item[0].upper()] = item[1]
        return kwargs
