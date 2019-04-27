""" Censors audio chunks in a continuous stream """

import os
import threading
import sounddevice as sd
import soundfile as sf
from pydub import AudioSegment
from audio import improve_accuracy, convert_and_write_chunk, \
    read_and_convert_audio
from utils import create_env_var, create_temp_dir, append_before_ext, \
    time_filename, MacUtil, CHUNK_LEN
from .censor import Censor

class CensorRealtimeMac(Censor):
    """ Removes explicits from audio stream in real-time """

    running = True

    def __init__(self, args, explicits):
        print('Initialzed realtime censor object')
        super().__init__(explicits, args.output_encoding, args.output_location)
        self.__switch_audio_source()
        create_env_var('CLEANSIO_CHUNKS_LIST', '[]')
        self.args = args
        self.directory = create_temp_dir()
        self.chunk_prefix = self.directory + time_filename() + '-'
        self.temp_chunk_filepath = self.directory + 'temp_chunk.wav'
        self.__update_env_chunks_list(self.temp_chunk_filepath)
        self.clean_file = AudioSegment.empty()
        self.processing_queue = []
        self.processing_lock = threading.Lock()
        self.playback_queue = []
        self.playback_lock = threading.Lock()
        self.samplerate = 44100 # Hertz
        self.duration = 5 # seconds

    def censor(self):
        """ Censors audio chunks in a continuous stream """

        # Start thread that will analyze and censor recorded chunks
        processing_thread = threading.Thread(target=self.run)
        processing_thread.daemon = True
        processing_thread.start()

        try:
            # Device indexes in sd.default.device should have already been set
            #   to Soundflower (2ch) for input and Built-in Output for output.
            #   Capture stream from Soundflower (2ch) & play to Built-in Output
            with sd.Stream(samplerate=self.samplerate,
                           blocksize=int(self.samplerate*self.duration),
                           channels=1, callback=self.callback,
                           finished_callback=self.finished_callback):
                print('#' * 80)
                print('Press Return to stop censoring')
                print('#' * 80)
                input()
        except KeyboardInterrupt:
            print('\nInterrupted by user')
            CensorRealtimeMac.running = False
        except Exception as exception:
            print(type(exception).__name__ + ': ' + str(exception))
            CensorRealtimeMac.running = False

    def callback(self, indata, outdata, _, __, status):
        """ Process audio data from Stream  """
        if status:
            print(status)

        # Add to processing_queue
        with self.processing_lock:
            self.processing_queue.append(indata.copy())

        # Consume playback_queue
        with self.playback_lock:
            if self.playback_queue:
                outdata[:] = self.playback_queue.pop(0)
            else:
                outdata.fill(0)

    def finished_callback(self):
        """ Once stream is inactive, output cleaned recordings to audio file """
        if self.args.store_recording:
            trailing_audio_length = len(self.playback_queue) * CHUNK_LEN
            if trailing_audio_length > 0:
                self.clean_file = self.clean_file[:-trailing_audio_length]
            self.create_clean_file(self.clean_file)
        else:
            self.print_explicits_count()

    def run(self):
        """ Process 10 seconds of captured audio data at a time """
        index = 0
        leftover_mute = 0

        while True:
            if not CensorRealtimeMac.running:
                break

            with self.processing_lock:
                processing_queue_length = len(self.processing_queue)

            if processing_queue_length >= 2:
                with self.processing_lock:
                    frames_to_process = self.processing_queue.pop(0)
                    next_frames = self.processing_queue[0]

                # Convert next two recordings into chunks
                recorded_chunk, file_path = \
                    self.__convert_frames_to_chunk(frames_to_process, index)
                next_recorded_chunk, _ = \
                    self.__convert_frames_to_chunk(next_frames, index+1)

                overlapping_chunk, overlapping_path = \
                    self.__create_overlapping_chunk(recorded_chunk,
                                                    next_recorded_chunk,
                                                    file_path)

                # Create accuracy chunk for current chunk and overlapping chunk
                self.__create_accuracy_chunk(recorded_chunk, file_path)
                self.__create_accuracy_chunk(overlapping_chunk, overlapping_path)

                # Censor current chunk and also mute any spillover explicits
                #   from previous chunk
                clean_chunk_wrapper = self.censor_audio_chunk(file_path)
                clean_chunk = AudioSegment.silent(duration=leftover_mute) \
                    + clean_chunk_wrapper.segment[leftover_mute:]

                # Remember to mute any overlapping explicit in the next chunk
                leftover_mute = clean_chunk_wrapper.mute_next_start

                # Convert current chunk into frames and add it to the playback
                #   queue
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
        chunk.export(self.temp_chunk_filepath, format='wav')
        clean_frames, _ = sf.read(self.temp_chunk_filepath,
                                  dtype='float32',
                                  fill_value=0.0,
                                  frames=int(self.samplerate*self.duration),
                                  always_2d=True)
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
        cls.__set_default_device('Soundflower (2ch)', 'Built-in Output')

    @classmethod
    def __set_default_device(cls, input_device_name, output_device_name):
        device_index = 0
        input_device_index = 2 # Soundflower (2ch) is usually no. 2
        output_device_index = 1 # Built-in Output is usually no. 1
        for device in sd.query_devices():
            if device['name'] == input_device_name:
                input_device_index = device_index
            if device['name'] == output_device_name:
                output_device_index = device_index
            device_index += 1
        sd.default.device = (input_device_index, output_device_index)

    @classmethod
    def __update_env_chunks_list(cls, file_path):
        """ Call after every write for later cleanup """
        env_list = os.environ['CLEANSIO_CHUNKS_LIST']
        beginning = '[\'' if env_list[:-1] == '[' else env_list[:-1] + ', \''
        create_env_var(
            'CLEANSIO_CHUNKS_LIST', beginning + file_path + '\']')
