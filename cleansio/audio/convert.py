""" Converts audio properties """

import os
from pydub import AudioSegment
from utils import create_temp_dir, time_filename

def __sample_rate(audio_segment):
    """ GCS requires at least 16 kHz. Either upscale or keep the same. """
    frame_rate = audio_segment.frame_rate
    return 16000 if frame_rate < 16000 else frame_rate

def __create_converted_file(file_path, encoding):
    """ LINEAR16 must be mono and 16 bits (2) """
    audio_segment = AudioSegment.from_file(file_path)
    audio_segment                                     \
        .set_channels(1)                              \
        .set_sample_width(2)                          \
        .set_frame_rate(__sample_rate(audio_segment)) \
        .export(os.environ['CLEANSIO_TEMP_FILE'], format=encoding)

def convert(file_path, encoding='wav'):
    """ Converts an audio file's encoding, returns the file path """
    temp_dir = create_temp_dir()
    os.environ['CLEANSIO_TEMP_FILE'] = temp_dir + \
        str(time_filename()) + '.' + encoding
    __create_converted_file(file_path, encoding)
    return os.environ['CLEANSIO_TEMP_FILE']

def read_and_convert_audio(file_path):
    """ Create a GCS AudioSegment from the file_path """
    audio_segment = AudioSegment.from_file(file_path)
    audio_segment            \
        .set_channels(1)     \
        .set_sample_width(2) \
        .set_frame_rate(__sample_rate(audio_segment))
    return audio_segment

def convert_audio_segment(audio_segment):
    """ Create a GCS AudioSegment """
    audio_segment            \
        .set_channels(1)     \
        .set_sample_width(2) \
        .set_frame_rate(__sample_rate(audio_segment))
    return audio_segment

def convert_and_write_chunk(chunk, file_path, encoding):
    """ Create a GCS AudioSegment and write to the file path """
    chunk.set_channels(1)      \
        .set_sample_width(2)   \
        .set_frame_rate(44100) \
        .export(file_path, format=encoding)
