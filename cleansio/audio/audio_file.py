""" Classifies an audio file that will be broken up into chunks """

import sys
from textwrap import dedent
from pydub import AudioSegment
from colorama import Fore
from utils import create_temp_dir, create_env_var, file_name_no_ext, \
    append_before_ext
from .accuracy import improve_accuracy
from .convert import convert

class AudioFile:
    """ Classifies an audio file """
    def __init__(self, file_path):
        try:
            self.file_path = convert(file_path)
        except FileNotFoundError:
            self.__handle_file_not_found(file_path)
        self.encoding = 'LINEAR16'
        audio_segment = AudioSegment.from_file(self.file_path)
        self.channels = audio_segment.channels
        self.frame_rate = audio_segment.frame_rate
        self.chunk_length = 5000 # In milliseconds
        self.normal_chunks, self.overlapping_chunks = \
            self.__init_create_chunks(audio_segment)

    def __init_create_chunks(self, audio_segment):
        """ Breaks up the file into small chunks """
        temp_dir = create_temp_dir()
        normal_chunks = []
        overlapping_chunks = []
        # Create normal and overlapping chunks
        self.__create_chunks(audio_segment, temp_dir, normal_chunks, False)
        self.__create_chunks(audio_segment, temp_dir, overlapping_chunks, True)
        # Add the list of chunk filepaths to an ENV variable for post cleanup
        create_env_var(
            'CLEANSIO_CHUNKS_LIST', str(normal_chunks + overlapping_chunks))
        return normal_chunks, overlapping_chunks

    def __create_chunks(self, audio_segment, temp_dir, chunks_arr, overlapping):
        start = 2500 if overlapping else 0
        chunks = audio_segment[start::self.chunk_length]
        for index, chunk in enumerate(chunks):
            chunk_path = self.__create_chunk(
                index, chunk, 'wav', temp_dir, overlapping)
            chunks_arr.append(chunk_path)
        # Fix for when the last chunk isn't long enough to support overlapping
        self.__last_overlapping_chunk(
            audio_segment, temp_dir, chunks_arr, overlapping)

    def __create_chunk(self, index, chunk, extension, temp_dir, overlapping):
        file_name = file_name_no_ext(self.file_path)
        file_path = temp_dir + file_name + '-' + str(index) + '.' + extension
        if overlapping:
            file_path = append_before_ext(file_path, '-overlapping')
        # Chunk that will be modified for accuracy's sake
        accuracy_path = append_before_ext(file_path, '-accuracy')
        with open(accuracy_path, 'wb') as chunk_file:
            accuracy_chunk = improve_accuracy(chunk)
            accuracy_chunk.export(chunk_file, format=extension)
            if overlapping: # The normal overlapping chunk is not needed
                return chunk_file.name
        # Chunk that will be censored and preserve audio quality
        with open(file_path, 'wb') as chunk_file:
            chunk.export(chunk_file, format=extension)
            return chunk_file.name

    def __last_overlapping_chunk(
            self, audio_segment, temp_dir, chunks_arr, overlapping):
        """ Check if the chunk is long enough to support overlapping """
        if overlapping and len(audio_segment) % self.chunk_length < 4000:
            chunk_path = self.__create_chunk(
                len(audio_segment) // self.chunk_length, # Last index
                AudioSegment.silent(frame_rate=44100),   # Silent chunk
                'wav', temp_dir, overlapping)
            chunks_arr.append(chunk_path)

    @classmethod
    def __handle_file_not_found(cls, file_path):
        print(dedent('''\
            {0}Audio file '{1}{2}{0}' could not be found
            Make sure the audio file path is correct.\
        '''.format(Fore.RED, Fore.YELLOW, str(file_path))))
        sys.exit(0)
