
from array import array


class Trimmer():
    def __init__(self, threshold, rate):
        self._THRESHOLD = threshold
        self._RATE = rate
        #len of margin in seconds
        self._MARGIN_LEN = 1

    def trim_from_left(self, snd_data):
        """Обрезает тишину в начале"""
        start_index = 0
        for i, val in enumerate(snd_data):
            if abs(val) > self._THRESHOLD:
                start_index = i
                break
        margin_len = self._MARGIN_LEN * self._RATE
        start_index = 0 if start_index < margin_len else \
            start_index - margin_len
        #
        # STARTED = False
        # r = array('h')
        # for i in snd_data:
        #     if not STARTED and abs(i) > self._THRESHOLD:
        #         STARTED = True
        #         r.append(i)
        #     elif STARTED:
        #         r.append(i)
        return snd_data[start_index:]
