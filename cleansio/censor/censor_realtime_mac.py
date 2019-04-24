""" Censors audio chunks in a continuous stream """

from .censor import Censor
from utils import create_env_var, create_temp_dir, append_before_ext, \
    time_filename, MacUtil
from audio import improve_accuracy, convert_audio_segment, \
    convert_and_write_chunk, read_and_convert_audio
from pathlib import Path
from pydub import AudioSegment
from colorama import Fore
from utils import CHUNK_LEN

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
        self.args = args
        self.directory = create_temp_dir()
        self.chunk_prefix = self.directory + time_filename() + '-'
        self.clean_file = AudioSegment.empty()
        self.processing_queue = []
        self.processing_lock = threading.Lock()
        self.playback_queue = []
        self.playback_lock = threading.Lock()
        self.samplerate = 44100 # Hertz
        self.duration = 5 # seconds

    def censor(self):
        """ Censors audio chunks in a continuous stream """
        """ Creates a clean/new version of a file by removing explicits """

        # Start thread that will analyze and censor recorded chunks
        processing_thread = threading.Thread(target=self.run)
        processing_thread.daemon = True
        processing_thread.start()

        try:
            # listen from Soundflower, play to speakers
            with sd.Stream(device=(2, 1),
                       samplerate=self.samplerate, blocksize=int(self.samplerate*self.duration),
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
        if self.args.store_recording:
            trailing_audio_length = len(self.playback_queue) * CHUNK_LEN
            print("clean audio file len is " + str(len(self.clean_file)))
            print("trimming " + str(trailing_audio_length) + "s of audio from end of clean audio file")
            print("clean audio file len is " + str(len(self.clean_file)))
            if trailing_audio_length > 0:
                self.clean_file = self.clean_file[:-trailing_audio_length]
            self.create_clean_file(self.clean_file)
        else:
            self.print_explicits_count()

    def run(self):
        index = 0
        leftover_mute = 0

        while True:
            if (not CensorRealtimeMac.running):
                break

            with self.processing_lock:
                processing_queue_length = len(self.processing_queue)

            if processing_queue_length >= 2:
                print('processing_queue length='+str(processing_queue_length))
                print('index={}'.format(index))
                with self.processing_lock:
                    print(len(self.processing_queue))
                    frames_to_process = self.processing_queue.pop(0)
                with self.processing_lock:
                    print(len(self.processing_queue))
                    next_frames = self.processing_queue[0]

                # Convert next two recordings into chunks
                recorded_chunk, file_path = self.__convert_frames_to_chunk(frames_to_process, index)
                next_recorded_chunk, _ = self.__convert_frames_to_chunk(next_frames, (index+1)*5)

                overlapping_chunk, overlapping_path = self.__create_overlapping_chunk(recorded_chunk, next_recorded_chunk, file_path)

                # Create accuracy chunk for current chunk and overlapping chunk
                self.__create_accuracy_chunk(recorded_chunk, file_path)
                self.__create_accuracy_chunk(overlapping_chunk, overlapping_path)

                # censor current chunk and also mute any spillover explicits from previous chunk
                clean_chunk_wrapper = self.censor_audio_chunk(file_path)
                clean_chunk = AudioSegment.silent(duration=leftover_mute) + clean_chunk_wrapper.segment[leftover_mute:]

                # remember to mute any overlapping explicit in the next chunk
                leftover_mute = clean_chunk_wrapper.mute_next_start
                if leftover_mute > 0: print("Remember to mute " + str(leftover_mute) + "s at the start of the next chunk")

                # Convert current chunk into frames and add it to the playback queue
                clean_frames = self.__convert_clean_chunk_to_frames(clean_chunk)
                with self.playback_lock:
                    self.playback_queue.append(clean_frames)
                
                if self.args.store_recording:
                    self.clean_file += clean_chunk

                index += 1

    def __convert_frames_to_chunk(self, frames, index):
        file_path = self.chunk_prefix + str(index) +'.wav'
        sf.write(file_path, frames, self.samplerate)
        self.__update_env_chunks_list(file_path)
        recorded_chunk = read_and_convert_audio(file_path)
        return recorded_chunk, file_path

    def __convert_clean_chunk_to_frames(self, chunk):
        clean_chunk_filepath = self.directory + 'clean_chunk.wav'
        chunk.export(clean_chunk_filepath, format='wav')
        clean_frames, _ = sf.read(clean_chunk_filepath, dtype='float32', fill_value=0.0, frames=int(self.samplerate*self.duration), always_2d=True)
        return clean_frames

    def __create_overlapping_chunk(self, chunk1, chunk2, file_path):
        overlapping_chunk = chunk1[2500:] + chunk2[:2500]
        overlapping_path = append_before_ext(file_path, '-overlapping')
        convert_and_write_chunk(overlapping_chunk, overlapping_path, 'wav')
        self.__update_env_chunks_list(overlapping_path)
        return overlapping_chunk, overlapping_path

    def __create_accuracy_chunk(self, chunk, file_path):
        accuracy_chunk_file_path = append_before_ext(file_path, '-accuracy')
        accuracy_chunk = improve_accuracy(chunk)
        convert_and_write_chunk(accuracy_chunk, accuracy_chunk_file_path, 'wav')

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
