""" Censors audio chunks in a continuous stream """

from .censor import Censor
from utils import create_env_var, create_temp_dir, append_before_ext, \
    time_filename, MacUtil
from audio import improve_accuracy, convert_audio_segment, convert_and_write_chunk, read_and_convert_audio
from pathlib import Path
from pydub import AudioSegment
from colorama import Fore
from collections import deque

import os
import sounddevice as sd
import soundfile as sf
import subprocess
import threading

class CensorRealtimeMac(Censor):
    running = True

    """ Filters audio stream in real-time """
    def __init__(self, args, explicits):
        super().__init__(explicits, args.output_encoding, args.output_location)
        self.__switch_audio_source()
        create_env_var('CLEANSIO_CHUNKS_LIST', '[]')
        self.lock = threading.Lock()
        self.chunk_prefix = create_temp_dir() + time_filename() + '-'
        self.all_chunks = []
        self.clean_file_chunks = []
        self.all_data = deque([])
        self.clean_file = AudioSegment.empty()

    def censor(self):
        """ Censors audio chunks in a continuous stream """
        """ Creates a clean/new version of a file by removing explicits """

        samplerate = 44100  # Hertz
        duration = 5  # seconds

        processing_thread = threading.Thread(target=self.run)
        processing_thread.daemon = True
        processing_thread.start()

        for i in range(0,10+1,5):
            # Record
            mydata = sd.rec(int(samplerate * duration), samplerate=samplerate,
                            channels=1, blocking=True)
            with self.lock:
                self.all_data.append(mydata)

        CensorRealtimeMac.running = False
        processing_thread.join()

    def run(self):
        index = 0
        overlapping_chunk_start = convert_audio_segment(AudioSegment.silent(duration=2500))
        while True:
            if (not CensorRealtimeMac.running):
                break

            if len(self.all_data) > 0:
                print('index={}'.format(index))
                with self.lock:
                    mydata = self.all_data.popleft()

                # Write recording to file
                file_path = self.chunk_prefix + str(index) +'.wav'
                # print('normal_chunks filepath is {}'.format(file_path))
                sf.write(file_path, mydata, 44100)
                self.__update_env_chunks_list(file_path)
                # Create AudioSegment object from recording and append it to list
                recorded_chunk = read_and_convert_audio(file_path, 'wav')
                self.all_chunks.append(file_path)

                # Use first half of recorded chunk as start of overlapping chunk
                overlapping_chunk = overlapping_chunk_start + recorded_chunk[:2500]
                overlapping_path = append_before_ext(file_path, '-overlapping')
                convert_and_write_chunk(overlapping_chunk,overlapping_path,'wav')
                self.__update_env_chunks_list(overlapping_path)
                self.all_chunks.append(overlapping_path)

                # Create next overlapping_start from second half of recorded chunk
                overlapping_chunk_start = recorded_chunk[-2500:]

                accuracy_path = append_before_ext(file_path, '-accuracy')
                with open(accuracy_path, 'wb') as chunk_file:
                    accuracy_chunk = improve_accuracy(recorded_chunk)
                    convert_and_write_chunk(accuracy_chunk,chunk_file,'wav')

                overlapping_accuracy_path = append_before_ext(overlapping_path, '-accuracy')
                with open(overlapping_accuracy_path, 'wb') as chunk_file:
                    overlapping_accuracy_chunk = improve_accuracy(overlapping_chunk)
                    convert_and_write_chunk(overlapping_accuracy_chunk,chunk_file,'wav')

                self.clean_file_chunks.append(self.censor_audio_chunk(file_path))

                index += 5

    @classmethod
    def __switch_audio_source(cls) :
        create_env_var('CLEANSIO_OLD_SOUND_OUT', MacUtil.audio_source('output'))
        create_env_var('CLEANSIO_OLD_SOUND_IN', MacUtil.audio_source('input'))
        MacUtil.switch_audio_source('output', 'Soundflower (2ch)')
        MacUtil.switch_audio_source('input', 'Soundflower (2ch)')
        cls.__set_default_device('Soundflower (2ch)')

    @classmethod
    def __set_default_device(cls, device_name):
        device_index = 0
        for device in sd.query_devices():
            if device['name'] == device_name:
                sd.default.device = device_index
                break
            device_index += 1

    @classmethod
    def __update_env_chunks_list(cls, file_path):
        """ Call after every write for later cleanup """
        env_list = os.environ['CLEANSIO_CHUNKS_LIST']
        beginning = "['" if env_list[:-1] == '[' else env_list[:-1] + ", '"
        create_env_var(
            'CLEANSIO_CHUNKS_LIST', beginning + file_path + "']")
