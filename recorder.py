#!/usr/bin/python3

from sys import byteorder
from array import array
from struct import pack

import pyaudio
import wave

from libs.trimmer import Trimmer
from libs.silent_generator import Silent_Generator
from libs.logger import CustomLogger


class Recorder():
    def __init__(self):
        self._THRESHOLD = 500
        self._CHUNK_SIZE = 1024
        self._FORMAT = pyaudio.paInt16
        self._RATE = 44100
        self._VOLUME_MAXIMUM = 16384
        self._CHANNELS = 1
        self._logger = CustomLogger(module=__name__).get_logger()
        self._logger.info('logging starts')

    def _is_silent(self, snd_data):
        return max(snd_data) < self._THRESHOLD

    def _normalize(self, snd_data):
        times = float(self._VOLUME_MAXIMUM)/max(abs(i) for i in snd_data)

        r = array('h')
        for i in snd_data:
            r.append(int(times*i))
        return r

    def _trim(self, snd_data):
        trimmer = Trimmer(self._THRESHOLD)
        self._logger.info('before trim %s' % snd_data)
        r = trimmer.trim_from_start(snd_data)
        self._logger.info('after trim from start %s' % r)
        r.reverse()
        self._logger.info('after reverse %s' % r)
        r = trimmer.trim_from_start(snd_data)
        self._logger.info('trim from end %s' % r)
        r.reverse()
        self._logger.info('after reverse %s' % r)
        return r

    def _add_silence(self, snd_data, seconds):
        self._logger.info('before add silence %s' % snd_data)
        sg = Silent_Generator(self._RATE)
        r = array('h', sg.get_silent(seconds))
        self._logger.info('start silence = %s' % r)
        r.extend(snd_data)
        self._logger.info('silence + signal = %s' % r)
        r.extend(sg.get_silent(seconds))
        self._logger.info('silence + signal + silence = %s' % r)
        return r

    def _record(self):
        p = pyaudio.PyAudio()
        stream = p.open(format=self._FORMAT, channels=self._CHANNELS,
                        rate=self._RATE, input=True, output=True,
                        frames_per_buffer=self._CHUNK_SIZE)
        num_silent = 0
        snd_started = False

        r = array('h')
        while True:
            snd_data = array('h', stream.read(self._CHUNK_SIZE))
            if byteorder == 'big':
                snd_data.byteswap()
            r.extend(snd_data)

            silent = self._is_silent(snd_data)

            if silent and snd_started:
                num_silent += 1
            if not silent and not snd_started:
                snd_started = True
            if snd_started and num_silent > 30:
                break

        sample_width = p.get_sample_size(self._FORMAT)
        stream.stop_stream()
        stream.close()
        p.terminate()

        self._logger.info('before normalize %s' % r)
        r = self._normalize(r)
        self._logger.info('after normalize %s' % r)
        r = self._trim(r)
        self._logger.info('after trim %s' % r)
        r = self._add_silence(r, 0.5)
        self._logger.info('after silence add %s' % r)

        return sample_width, r

    def record_to_file(self, path):
        sample_width, data = self._record()
        data = pack('<' + ('h'*len(data)), *data)

        wf = wave.open(path, 'wb')
        wf.setnchannels(self._CHANNELS)
        wf.setsampwidth(sample_width)
        wf.setframerate(self._RATE)
        wf.writeframes(data)
        wf.close()


if __name__ == '__main__':
    recorder = Recorder()
    print('say something')
    recorder.record_to_file('custom.wav')
    print('end of record')
