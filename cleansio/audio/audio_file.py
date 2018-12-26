""" Classifies an audio file """
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
        self.sample_rate = audio_segment.frame_rate
        slice_length = 5000 # time in milliseconds
        self.slices_file_paths = self.__create_slices(audio_segment, slice_length)

    def __create_slices(self, audio_segment, slice_length):
        temp_dir = create_temp_dir()
        slices_file_paths = []
        # Break up the file into $slice_length ms length WAV audio chunks
        for index, chunk in enumerate(audio_segment[::slice_length]):
            slice_path = self.__create_slice(index, chunk, 'wav', temp_dir)
            slices_file_paths.append(slice_path)
        # Add the list of chunk filepaths to an ENV variable for post cleanup
        create_env_var('CLEANSIO_SLICES_LIST', str(slices_file_paths))
        return slices_file_paths

    def __create_slice(self, index, chunk, extension, temp_dir):
        file_name = file_name_no_ext(self.file_path)
        file_path = temp_dir + file_name + '-' + str(index) + '.' + extension
        with open(file_path, 'wb') as slice_file:
            chunk.export(slice_file, format=extension)
            return slice_file.name

    @classmethod
    def __handle_file_not_found(cls, file_path):
        print('Audio file \'' + str(file_path) + '\' could not be found.')
        print('Make sure the audio file path is correct.')
        sys.exit(0)
