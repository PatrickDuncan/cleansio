""" Classifies an audio file """

import magic
from pydub import AudioSegment
from .convert import convert

class AudioFile:
    """ Classifies an audio file """
    def __init__(self, file_path):
        self.file_path = self.__converted_file_path(file_path)
        audio_segment = AudioSegment.from_file(self.file_path)
        self.channels = audio_segment.channels
        self.sample_rate = audio_segment.frame_rate

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
