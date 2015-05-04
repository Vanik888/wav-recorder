import xml.etree.ElementTree as ET
import os

from common_libs.logger import CustomLogger
from .result import Result

logger = CustomLogger().get_logger(module=__name__)


class XmlParser():
    def __init__(self, xml_abs_path='result.xml'):
        self._xml_abs_path = xml_abs_path

    def _check_xml_exists(self, xml_abs_path):
        if os.path.isfile(xml_abs_path):
            return True
        elif os.path.exists(xml_abs_path):
            logger.error('Error: %s is not a file' % xml_abs_path)
            return False
        elif not os.path.exists(xml_abs_path):
            logger.error('Error: %s does not exists' % xml_abs_path)

    def get_result_list(self):
        result_list = []
        if self._check_xml_exists(self._xml_abs_path):
            try:
                tree = ET.parse(self._xml_abs_path)
                root = tree.getroot()
                for child in root:
                    result = Result(float(child.attrib['confidence']), child.text)
                    result_list.append(result)
                return result_list
            except ET.ParseError as e:
                logger.error(e)
                return []
        else:
            return []
