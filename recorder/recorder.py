#!/usr/bin/python3

import os
from sys import byteorder
from array import array
from struct import pack
import wave

import pyaudio
print(os.getcwd())

from recorder.libs.trimmer import Trimmer
from recorder.libs.silent_generator import Silent_Generator
from common_libs.logger import CustomLogger
from common_libs.config_reader import ConfigReader

logger = CustomLogger(module=__name__).get_logger()


class Recorder():
    def __init__(self, **kwargs):
        self._CONF_FILE_NAME = 'base.cfg'
        self._SECTION = 'recorder'

        params = self._get_config(**kwargs)
        self._OUTPUT_FILE_DIR = params['OUTPUT_FILE_DIR']
        self._FILE_NAME = params['FILE_NAME']
        self._THRESHOLD = int(params['THRESHOLD'])
        self._CHUNK_SIZE = int(params['CHUNK_SIZE'])
        self._FORMAT = pyaudio.paInt16
        self._RATE = int(params['RATE'])
        self._VOLUME_MAXIMUM = int(params['VOLUME_MAXIMUM'])
        self._CHANNELS = int(params['CHANNELS'])
    
    def _get_config(self, **kwargs):
        module_dir = os.path.dirname(os.path.abspath(__file__))
        local_conf_file = os.path.join(module_dir, self._CONF_FILE_NAME)
        self._config_reader = ConfigReader(local_conf_file, self._SECTION)
        return self._config_reader.get_complete_config(**kwargs)
    
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
        logger.info('before trim %s' % snd_data)
        r = trimmer.trim_from_start(snd_data)
        logger.info('after trim from start %s' % r)
        r.reverse()
        logger.info('after reverse %s' % r)
        r = trimmer.trim_from_start(snd_data)
        logger.info('trim from end %s' % r)
        r.reverse()
        logger.info('after reverse %s' % r)
        return r

    def _add_silence(self, snd_data, seconds):
        logger.info('before add silence %s' % snd_data)
        sg = Silent_Generator(self._RATE)
        r = array('h', sg.get_silent(seconds))
        logger.info('start silence = %s' % r)
        r.extend(snd_data)
        logger.info('silence + signal = %s' % r)
        r.extend(sg.get_silent(seconds))
        logger.info('silence + signal + silence = %s' % r)
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
            if snd_started and num_silent > 150:
                break

        sample_width = p.get_sample_size(self._FORMAT)
        stream.stop_stream()
        stream.close()
        p.terminate()

        logger.info('before normalize %s' % r)
        r = self._normalize(r)
        logger.info('after normalize %s' % r)
        r = self._trim(r)
        logger.info('after trim %s' % r)
        r = self._add_silence(r, 0.5)
        logger.info('after silence add %s' % r)

        return sample_width, r

    def record_to_file(self):
        sample_width, data = self._record()
        data = pack('<' + ('h'*len(data)), *data)
        if __name__ == '__main__':
            CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
        else:
            CURRENT_DIR = os.getcwd()

        RECORD_ABS_PATH = os.path.join(CURRENT_DIR,
                                       self._OUTPUT_FILE_DIR,
                                       self._FILE_NAME)
        wf = wave.open(RECORD_ABS_PATH, 'wb')
        wf.setnchannels(self._CHANNELS)
        wf.setsampwidth(sample_width)
        wf.setframerate(self._RATE)
        wf.writeframes(data)
        wf.close()


if __name__ == '__main__':
    recorder = Recorder()
    print('say something')
    recorder.record_to_file()
    print('end of record')
