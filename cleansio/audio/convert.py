""" Converts audio properties """

import os
import time
from pydub import AudioSegment
from .helper import create_temp_dir

def __sample_rate(audio_segment):
    """ GCS requires at least 16 kHz. Either upscale or keep the same. """
    if audio_segment.frame_rate < 16000:
        return 16000
    return audio_segment.frame_rate

def __create_converted_file(file_path, encoding, channels):
    audio_segment = AudioSegment.from_file(file_path)
    audio_segment = audio_segment.set_channels(channels) # must be mono
    audio_segment = audio_segment.set_frame_rate(__sample_rate(audio_segment))
    audio_segment.export(os.environ['CLEANSIO_TEMP_FILE'], format=encoding)

def convert(file_path, encoding='wav', channels=1):
    """ Converts an audio file's encoding, returns the file path """
    milliseconds = int(round(time.time() * 1000))
    temp_dir = create_temp_dir()
    os.environ['CLEANSIO_TEMP_FILE'] = temp_dir + str(milliseconds) + "." + encoding
    __create_converted_file(file_path, encoding, channels)
    return os.environ['CLEANSIO_TEMP_FILE']
