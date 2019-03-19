""" Censors audio chunks in a continuous stream """

from .censor import Censor
from utils import create_env_var, create_temp_dir, append_before_ext
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
    """ Filters audio stream in real-time """
    def __init__(self, args, explicits):
        super().__init__(explicits, args.output_encoding, args.output_location)
        self.__switch_audio_source()
        self.lock = threading.Lock()
        self.chunk_prefix = create_temp_dir() + 'output'
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

        for i in range(0,60+1,5):
            print('i={}'.format(i))
            # Record
            mydata = sd.rec(int(samplerate * duration), samplerate=samplerate,
                            channels=1, blocking=True)
            with self.lock:
                self.all_data.append(mydata)

    def run(self):
        index = 0
        overlapping_chunk_start = convert_audio_segment(AudioSegment.silent(duration=2500))
        while True:
            if len(self.all_data) > 0:

                with self.lock:
                    mydata = self.all_data.popleft()

                # Write recording to file
                file_path = self.chunk_prefix + str(index) +'.wav'
                # print('normal_chunks filepath is {}'.format(file_path))
                sf.write(file_path, mydata, 44100)

                # Create AudioSegment object from recording and append it to list
                recorded_chunk = read_and_convert_audio(file_path, 'wav')
                self.all_chunks.append(file_path)

                # Use first half of recorded chunk as start of overlapping chunk
                overlapping_chunk = overlapping_chunk_start + recorded_chunk[:2500]
                overlapping_path = append_before_ext(file_path, '-overlapping')
                convert_and_write_chunk(overlapping_chunk,overlapping_path,'wav')
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
        create_env_var('CLEANSIO_OLD_SOUND_OUT',subprocess.run(['SwitchAudioSource','-c','-t','output'],stdout=subprocess.PIPE).stdout.decode('utf-8').replace('\n',''))
        create_env_var('CLEANSIO_OLD_SOUND_IN',subprocess.run(['SwitchAudioSource','-c','-t','input'],stdout=subprocess.PIPE).stdout.decode('utf-8').replace('\n',''))
        os.system('SwitchAudioSource -t output -s "Soundflower (2ch)"')
        os.system('SwitchAudioSource -t input -s "Soundflower (2ch)"')
        sd.default.device = 2
