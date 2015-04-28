
from array import array


class Trimmer():
    def __init__(self, threshold):
        self._THRESHOLD = threshold

    def trim_from_start(self, snd_data):
        """Обрезает тишину в начале"""
        STARTED = False
        r = array('h')
        for i in snd_data:
            if not STARTED and abs(i) > self._THRESHOLD:
                STARTED = True
            if STARTED:
                r.append(i)
        return r
