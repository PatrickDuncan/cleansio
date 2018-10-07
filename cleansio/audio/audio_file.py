""" Classifies an audio file """

import magic
from .flac import Flac
from .wav import Wave

class AudioFile:
    """ Classifies an audio file """
    def __init__(self, file_path):
        self.file_path = file_path
        file_object = self.__set_file_object()
        self.channels = file_object.channels
        self.encoding = file_object.encoding
        self.sample_rate = file_object.sample_rate

    def __set_file_object(self):
        raw_file_info = magic.from_file(self.file_path).split(', ')
        encoding_type = raw_file_info[0] + raw_file_info[1]
        if 'WAVE' in encoding_type:
            return Wave(raw_file_info)
        elif 'FLAC' in encoding_type:
            return Flac(raw_file_info)
        return None
