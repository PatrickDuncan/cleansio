""" Censors audio chunks in a continuous stream """

from .censor import Censor
from utils import create_env_var, create_temp_dir, append_before_ext
from audio import improve_accuracy
from pathlib import Path
from pydub import AudioSegment
from colorama import Fore
from _thread import start_new_thread, allocate_lock
from collections import deque

import sounddevice as sd
import soundfile as sf
import subprocess

class CensorRealtime(Censor):
    """ Filters audio stream in real-time """
    def __init__(self, explicits):
        super().__init__(explicits)
        create_env_var('CLEANSIO_REALTIME','true')
        # self.encoding = self.__encoding(args.output_encoding)
        # self.location = self.__location(args.output_location)
        self.__switch_audio_source()

    def censor(self):
        """ Censors audio chunks in a continuous stream """
        """ Creates a clean/new version of a file by removing explicits """
        clean_file = AudioSegment.empty()

        temp_dir = create_temp_dir()

        normal_chunks = []
        overlapping_chunk_start = self.convert_audio_segment(AudioSegment.silent(duration=2500))

        samplerate = 44100  # Hertz
        duration = 5  # seconds
        filename = 'output'

        i = 0
        end = 60

        total_file = []

        all_data = deque([])

        global lock
        lock = allocate_lock()

        start_new_thread(self.run,(all_data,total_file,temp_dir,filename,normal_chunks,overlapping_chunk_start))

        while i < end:
            print('i={}'.format(i))
            # Record
            mydata = sd.rec(int(samplerate * duration), samplerate=samplerate,
                            channels=1, blocking=True)
            lock.acquire()
            all_data.append(mydata)
            lock.release()
            i += 5

        print('Length of total file is' + str(len(total_file)))
        for audio in total_file:
            print('Length of audio is' + str(len(audio)))
            clean_file += audio

        create_env_var('CLEANSIO_CHUNKS_LIST', str(normal_chunks))

        self.__create_clean_file(clean_file)

    def run(self,all_data,total_file,temp_dir,filename,normal_chunks,overlapping_chunk_start):
        start = 0
        while True:
            if len(all_data) > 0:
                lock.acquire()
                mydata = all_data.popleft()
                lock.release()
                # Write recording to file
                file_path = temp_dir + filename + str(start) +'.wav'
                # print('normal_chunks filepath is {}'.format(file_path))
                sf.write(file_path, mydata, 44100)

                # Create AudioSegment object from recording and append it to list
                recorded_chunk = self.get_converted_audio_file(file_path)
                normal_chunks.append(recorded_chunk)

                # Use first half of recorded chunk as start of overlapping chunk
                overlapping_chunk = overlapping_chunk_start + recorded_chunk[:2500]
                overlapping_path = append_before_ext(file_path, '-overlapping')
                # print('overlapping_chunk filepath is {}'.format(overlapping_path))
                self.__create_converted_file(overlapping_chunk,overlapping_path,'wav')

                # Create next overlapping_start from second half of recorded chunk
                overlapping_chunk_start = recorded_chunk[-2500:]

                accuracy_path = append_before_ext(file_path, '-accuracy')
                # print('accuracy_path filepath is {}'.format(accuracy_path))
                with open(accuracy_path, 'wb') as chunk_file:
                    accuracy_chunk = improve_accuracy(recorded_chunk)
                    self.__create_converted_file(accuracy_chunk,chunk_file,'wav')

                overlapping_accuracy_path = append_before_ext(overlapping_path, '-accuracy')
                # print('overlapping_accuracy_path filepath is {}'.format(overlapping_accuracy_path))
                with open(overlapping_accuracy_path, 'wb') as chunk_file:
                    overlapping_accuracy_chunk = improve_accuracy(overlapping_chunk)
                    self.__create_converted_file(overlapping_accuracy_chunk,chunk_file,'wav')

                total_file.append(self.censor_audio_chunk(file_path))

                start += 5
        

    @classmethod
    def __create_converted_file(cls,chunk, file_path, encoding):
        """ LINEAR16 must be mono and 16 bits (2) """
        chunk.set_channels(1)                             \
            .set_sample_width(2)                          \
            .set_frame_rate(44100)                        \
            .export(file_path, format=encoding)

    def __create_clean_file(self, clean_file):
        location = str(Path(__file__).parents[2]) + '/clean_file.wav'
        clean_file.export(location, format='wav')
        print(Fore.CYAN + 'Successfully created clean file, it\'s located at:')
        print(Fore.YELLOW + location)

    @classmethod
    def __switch_audio_source(cls) :
        create_env_var('CLEANSIO_OLD_SOUND_OUT',subprocess.run(['SwitchAudioSource','-c','-t','output'],stdout=subprocess.PIPE).stdout.decode('utf-8').replace('\n',''))
        create_env_var('CLEANSIO_OLD_SOUND_IN',subprocess.run(['SwitchAudioSource','-c','-t','input'],stdout=subprocess.PIPE).stdout.decode('utf-8').replace('\n',''))
        subprocess.run(['SwitchAudioSource', '-t', 'output', '-s', 'Soundflower (2ch)'])
        subprocess.run(['SwitchAudioSource', '-t', 'input', '-s', 'Soundflower (2ch)'])

    def __location(self, location):
        if location:
            return location[0]
        current_dir = str(Path(__file__).parents[2])
        return current_dir + '/clean_file.' + self.encoding

    @classmethod
    def __encoding(cls, encoding):
        return encoding[0] if encoding else 'wav'

    @classmethod
    def get_converted_audio_file(cls, file_path):
        audio_segment = AudioSegment.from_file(file_path)
        audio_segment                                     \
            .set_channels(1)                              \
            .set_sample_width(2)                          \
            .set_frame_rate(16000 if audio_segment.frame_rate < 16000 else audio_segment.frame_rate)
        return audio_segment

    @classmethod
    def convert_audio_segment(cls, audio_segment):
        audio_segment                                     \
            .set_channels(1)                              \
            .set_sample_width(2)                          \
            .set_frame_rate(16000 if audio_segment.frame_rate < 16000 else audio_segment.frame_rate)
        return audio_segment
