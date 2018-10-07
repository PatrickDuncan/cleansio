""" Converts audio properties """

import os
from os.path import expanduser
import time
from pydub import AudioSegment

def __create_converted_file(file_path, encoding):
    AudioSegment.from_file(file_path).export(
        os.environ['CLEANSIO_TEMP_FILE'],
        format=encoding)

def convert(file_path, encoding='wav'):
    """ Converts an audio file's encoding """
    milliseconds = int(round(time.time() * 1000))
    temp_dir = create_temp_dir()
    os.environ['CLEANSIO_TEMP_FILE'] = f"{temp_dir}/{milliseconds}.{encoding}"
    __create_converted_file(file_path, encoding)
    return os.environ['CLEANSIO_TEMP_FILE']
