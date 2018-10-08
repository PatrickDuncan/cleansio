""" Classifies an audio file """

import magic
from pydub import AudioSegment
from .convert import convert
from .helper import create_temp_dir, create_env_var

class AudioFile:
    """ Classifies an audio file """
    def __init__(self, file_path):
        self.file_path = self.__converted_file_path(file_path)
        audio_segment = AudioSegment.from_file(self.file_path)
        self.channels = audio_segment.channels
        self.sample_rate = audio_segment.frame_rate
        slice_length = 5000 # time in milliseconds
        self.slices_file_paths = self.__create_slices(audio_segment, slice_length)

    def __converted_file_path(self, file_path):
        """ The input file or converts the input to a GCS compliant encoding """
        self.encoding = 'LINEAR16' # wav
        raw_file_info = magic.from_file(file_path).split(', ')
        encoding_type = raw_file_info[0] + raw_file_info[1]
        if 'WAVE' in encoding_type:
            return file_path
        elif 'FLAC' in encoding_type:
            self.encoding = 'FLAC'
            return file_path
        return convert(file_path, encoding='wav')

    def __create_slices(self, audio_segment, slice_length):
        extension = self.encoding.lower()
        temp_dir = create_temp_dir()
        slices_file_paths = []
        for index, chunk in enumerate(audio_segment[::slice_length]):
            with open(f"{temp_dir}slice-{index}.{extension}", "wb") as slice_file:
                chunk.export(slice_file, format=extension)
                slices_file_paths.append(slice_file.name)
        create_env_var('CLEANSIO_SLICES_LIST', str(slices_file_paths))
        return slices_file_paths
