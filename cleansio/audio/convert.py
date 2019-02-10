""" Converts audio properties """

import os
import time
from pydub import AudioSegment
from utils import create_temp_dir

def __sample_rate(audio_segment):
    """ GCS requires at least 16 kHz. Either upscale or keep the same. """
    frame_rate = audio_segment.frame_rate
    return 16000 if frame_rate < 16000 else frame_rate

def convert_file(audio_segment, encoding, export_path):
    """ LINEAR16 must be mono and 16 bits (2) """
    audio_segment                                     \
        .set_channels(1)                              \
        .set_sample_width(2)                          \
        .set_frame_rate(__sample_rate(audio_segment)) \
        .export(export_path, format=encoding)

def __create_converted_file(file_path, encoding, export_path):
    audio_segment = AudioSegment.from_file(file_path)
    convert_file(audio_segment, encoding, export_path)

def convert(file_path, encoding='wav'):
    """ Converts an audio file's encoding, returns the file path """
    milliseconds = int(round(time.time() * 1000))
    temp_dir = create_temp_dir()
    os.environ['CLEANSIO_TEMP_FILE'] = temp_dir + \
        str(milliseconds) + '.' + encoding
    __create_converted_file(
        file_path, encoding, os.environ['CLEANSIO_TEMP_FILE'])
    return os.environ['CLEANSIO_TEMP_FILE']
