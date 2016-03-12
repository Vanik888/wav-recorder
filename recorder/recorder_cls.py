#!/usr/bin/python3

import os
import time
from sys import byteorder
from array import array
from struct import pack
import wave

import pyaudio

from recorder.libs.trimmer import Trimmer
from recorder.libs.silent_generator import SilentGenerator
from common_libs.logger import CustomLogger
from common_libs.config_reader import ConfigReader

logger = CustomLogger().get_logger(module=__name__)


class Recorder():
    def __init__(self, **kwargs):
        self._CONF_FILE_NAME = 'global.cfg'
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
        conf_file = os.path.join(os.getcwd(), self._CONF_FILE_NAME)
        self._config_reader = ConfigReader(conf_file, self._SECTION)
        return self._config_reader.get_complete_config(**kwargs)
    
    def _is_silent(self, snd_data):
        return max(abs(i) for i in snd_data) < self._THRESHOLD

    def _normalize(self, snd_data):
        times = float(self._VOLUME_MAXIMUM)/max(abs(i) for i in snd_data)
        r = array('h')
        for i in snd_data:
            r.append(int(times*i))
        return r

    def _trim(self, snd_data):
        trimmer = Trimmer(self._THRESHOLD, self._RATE)
        logger.debug('before trim %s' % snd_data)
        r = trimmer.trim_from_left(snd_data)
        logger.debug('after trim from start %s' % r)
        r.reverse()
        logger.debug('after reverse %s' % r)
        r = trimmer.trim_from_left(r)
        logger.debug('trim from end %s' % r)
        r.reverse()
        logger.debug('after reverse %s' % r)
        return r

    def _add_silence(self, snd_data, seconds):
        logger.debug('before add silence %s' % snd_data)
        sg = SilentGenerator(self._RATE)
        r = array('h', sg.get_silent(seconds))
        logger.debug('start silence = %s' % r)
        r.extend(snd_data)
        logger.debug('silence + signal = %s' % r)
        r.extend(sg.get_silent(seconds))
        logger.debug('silence + signal + silence = %s' % r)
        return r

    def _record(self):
        p = pyaudio.PyAudio()
        stream = p.open(format=self._FORMAT, channels=self._CHANNELS,
                        rate=self._RATE, input=True, output=True,
                        frames_per_buffer=self._CHUNK_SIZE)
        num_silent = 0
        snd_started = False

        r = array('h')

        print("Say command")
        while True:
            snd_data = array('h', stream.read(self._CHUNK_SIZE))
            if byteorder == 'big':
                snd_data.byteswap()
            r.extend(snd_data)

            silent = self._is_silent(snd_data)

            if silent and snd_started:
                num_silent += 1
            elif not silent and not snd_started:
                snd_started = True
                logger.info('Starts record to array')
            if snd_started and num_silent > 30:
                logger.info('Ends record to array')
                break

        sample_width = p.get_sample_size(self._FORMAT)
        stream.stop_stream()
        stream.close()
        p.terminate()
        logger.debug('Array is recorded')
        logger.debug('Array len = %s' % len(r))
        r = self._trim(r)
        logger.debug('after trim %s' % r)
        logger.debug('before normalize %s' % r)
        logger.debug('Array len = %s' % len(r))
        r = self._normalize(r)
        logger.debug('after normalize %s' % r)
        logger.debug('Array len = %s' % len(r))
        r = self._add_silence(r, 0.5)
        logger.debug('after silence add %s' % r)
        logger.debug('Array len = %s' % len(r))

        return sample_width, r

    def record_to_file(self):
        sample_width, data = self._record()
        data = pack('<' + ('h'*len(data)), *data)
        RECORD_ABS_PATH = os.path.join(os.getcwd(),
                                       self._OUTPUT_FILE_DIR,
                                       self._FILE_NAME)
        logger.debug('will be saved in %s' % RECORD_ABS_PATH)
        if os.path.isfile(RECORD_ABS_PATH):
            os.remove(RECORD_ABS_PATH)

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
