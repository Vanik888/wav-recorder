from array import array


class Silent_Generator():
    def __init__(self, rate):
        self._RATE = rate

    def get_silent(self, seconds):
        """Возвращает массив нулей длинной соответствующей тишине
        в seconds секунд при частоте RATE
        """
        return [0 for i in range(int(seconds*self._RATE))]
