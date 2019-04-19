""" Censors audio chunks in a continuous stream """

from .censor import Censor
from utils import create_env_var, create_temp_dir, append_before_ext, \
    time_filename, MacUtil
from audio import improve_accuracy, convert_audio_segment, \
    convert_and_write_chunk, read_and_convert_audio
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
        print('Initialzed realtime censor object')
        super().__init__(explicits, args.output_encoding, args.output_location)
        self.__switch_audio_source()
        create_env_var('CLEANSIO_CHUNKS_LIST', '[]')
        self.chunk_prefix = create_temp_dir() + time_filename() + '-'
        self.audio_file = AudioSegment.empty()
        self.processing_queue = []
        self.processing_lock = threading.Lock()
        self.playback_queue = []
        self.playback_lock = threading.Lock()

    def censor(self):
        """ Censors audio chunks in a continuous stream """
        """ Creates a clean/new version of a file by removing explicits """
        samplerate = 44100  # Hertz
        duration = 5  # seconds

        # Start thread that will analyze and censor recorded chunks
        processing_thread = threading.Thread(target=self.run)
        processing_thread.daemon = True
        processing_thread.start()

        try:
            # listen from Soundflower, play to speakers
            with sd.Stream(device=(2, 1),
                       samplerate=samplerate, blocksize=int(samplerate*duration),
                       channels=1, callback=self.callback, finished_callback=self.finished_callback):
                print('#' * 80)
                print('press Return to stop censoring')
                print('#' * 80)
                input()
        except KeyboardInterrupt:
            print('\nInterrupted by user')
            CensorRealtimeMac.running = False
        except Exception as e:
            print(type(e).__name__ + ': ' + str(e))
            CensorRealtimeMac.running = False

        # processing_thread.join()

    def callback(self, indata, outdata, frames, time, status):
        if status:
            print(status)

        # add to processing_queue
        with self.processing_lock:
            self.processing_queue.append(indata)
        
        # consume playback_queue
        with self.playback_lock:
            if len(self.playback_queue) > 0:
                outdata[:] = self.playback_queue.pop(0)
            else:
                outdata.fill(0)

    def finished_callback(self):
        self.create_clean_file(self.audio_file)

    def run(self):
        index = 0
        overlapping_chunk_start = convert_audio_segment(AudioSegment.silent(duration=2500))
        while True:
            if (not CensorRealtimeMac.running):
                break

            processing_queue_length = 0;
            with self.processing_lock:
                processing_queue_length = len(self.processing_queue)

            if processing_queue_length > 0:
                print('processing_queue length='+str(processing_queue_length))
                print('index={}'.format(index))
                with self.processing_lock:
                    frames_to_process = self.processing_queue.pop(0)

                # Write recording to file
                file_path = self.chunk_prefix + str(index) +'.wav'
                sf.write(file_path, frames_to_process, 44100)
                self.__update_env_chunks_list(file_path)
                # Create AudioSegment object from recording and append it to list
                recorded_chunk = read_and_convert_audio(file_path)

                # Use first half of recorded chunk to complete overlapping chunk
                overlapping_chunk = overlapping_chunk_start + recorded_chunk[:2500]
                overlapping_path = append_before_ext(file_path, '-overlapping')
                convert_and_write_chunk(overlapping_chunk, overlapping_path, 'wav')
                self.__update_env_chunks_list(overlapping_path)

                # Create next overlapping_start from second half of recorded chunk
                overlapping_chunk_start = recorded_chunk[-2500:]

                accuracy_path = append_before_ext(file_path, '-accuracy')
                with open(accuracy_path, 'wb') as chunk_file:
                    accuracy_chunk = improve_accuracy(recorded_chunk)
                    convert_and_write_chunk(accuracy_chunk, chunk_file, 'wav')

                overlapping_accuracy_path = append_before_ext(overlapping_path, '-accuracy')
                with open(overlapping_accuracy_path, 'wb') as chunk_file:
                    overlapping_accuracy_chunk = improve_accuracy(overlapping_chunk)
                    convert_and_write_chunk(overlapping_accuracy_chunk, chunk_file, 'wav')

                clean_chunk = self.censor_audio_chunk(file_path)
                clean_chunk_filepath = create_temp_dir() + 'clean_chunk.wav'
                clean_chunk.export(clean_chunk_filepath, format='wav')

                # Read and convert it to frames
                clean_frames, sample_rate = sf.read(clean_chunk_filepath, dtype='float32', fill_value=0.0, frames=int(44100*5), always_2d=True)
                with self.playback_lock:
                    self.playback_queue.append(clean_frames)
                index += 1
                self.audio_file += clean_chunk

    @classmethod
    def __switch_audio_source(cls):
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
