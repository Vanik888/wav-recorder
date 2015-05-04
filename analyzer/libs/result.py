class Result():
    def __init__(self, confidence=0, value=''):
        self._confidence = confidence
        self._value = value

    def get_confidence(self):
        return self._confidence

    def get_value(self):
        return self._value

    def set_confidence(self, confidence=0):
        self._confidence = confidence

    def set_value(self, value=''):
        self._value = value
