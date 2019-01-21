""" Classifies an audio file that will be broken up into chunks """
import sys
from pydub import AudioSegment
from utils import create_temp_dir, create_env_var, file_name_no_ext
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
        self.chunk_length = 5000 # in milliseconds
        self.chunks_file_paths = self.__create_chunks(audio_segment)

    def __create_chunks(self, audio_segment):
        """ Breaks up the file into small chunks """
        temp_dir = create_temp_dir()
        chunks_file_paths = []
        # Break up the file into $chunk_length ms length WAV audio chunks
        for index, chunk in enumerate(audio_segment[::self.chunk_length]):
            chunk_path = self.__create_chunk(index, chunk, 'wav', temp_dir)
            chunks_file_paths.append(chunk_path)
        # Add the list of chunk filepaths to an ENV variable for post cleanup
        create_env_var('CLEANSIO_CHUNKS_LIST', str(chunks_file_paths))
        return chunks_file_paths

    def __create_chunk(self, index, chunk, extension, temp_dir):
        file_name = file_name_no_ext(self.file_path)
        file_path = temp_dir + file_name + '-' + str(index)
        # Chunk that will be modified for accuracy's sake
        with open(file_path + '-accuracy', 'wb') as chunk_file:
            chunk.export(chunk_file, format=extension)
        # Chunk that will be censored and preserve audio quality
        with open(file_path, 'wb') as chunk_file:
            chunk.export(chunk_file, format=extension)
            return chunk_file.name

    @classmethod
    def __handle_file_not_found(cls, file_path):
        print('Audio file \'' + str(file_path) + '\' could not be found.')
        print('Make sure the audio file path is correct.')
        sys.exit(0)
