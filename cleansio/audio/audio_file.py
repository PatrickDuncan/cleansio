""" Classifies an audio file """
import sys
from pydub import AudioSegment
from .convert import convert
from .helper import create_temp_dir, create_env_var, file_name_no_ext

class AudioFile:
    """ Classifies an audio file """
    def __init__(self, file_path):
        try:
            self.file_path = convert(file_path)
        except FileNotFoundError:
            print('Audio file \'' + str(file_path) + '\' could not be found.' \
                '\nMake sure the audio file path is correct.')
            sys.exit(0)
        self.encoding = 'LINEAR16'
        audio_segment = AudioSegment.from_file(self.file_path)
        self.channels = audio_segment.channels
        self.sample_rate = audio_segment.frame_rate
        slice_length = 5000 # time in milliseconds
        self.slices_file_paths = self.__create_slices(audio_segment, slice_length)

    def __create_slices(self, audio_segment, slice_length):
        temp_dir = create_temp_dir()
        slices_file_paths = []
        for index, chunk in enumerate(audio_segment[::slice_length]):
            slice_path = self.__create_slice(index, chunk, 'wav', temp_dir)
            slices_file_paths.append(slice_path)
        create_env_var('CLEANSIO_SLICES_LIST', str(slices_file_paths))
        return slices_file_paths

    def __create_slice(self, index, chunk, extension, temp_dir):
        file_name = file_name_no_ext(self.file_path)
        file_path = temp_dir + file_name + '-' + str(index) + '.' + extension
        with open(file_path, 'wb') as slice_file:
            chunk.export(slice_file, format=extension)
            return slice_file.name
