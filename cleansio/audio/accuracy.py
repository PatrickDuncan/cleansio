""" Functions which preprocess an audio chunk to improve the accuracy of speech
    recognition. """
# pylint: disable=C0411

import numpy
import librosa
from pydub import AudioSegment

def __maximize_volume(chunk):
    """ Increase chunk's volume up to the point before clipping """
    return chunk - chunk.max_dBFS

def __magnitude_filter(magnitude, sampling_rate):
    width = int(librosa.time_to_frames(2, sr=sampling_rate))
    return librosa.decompose.nn_filter(
        magnitude, aggregate=numpy.median, metric='cosine', width=width)

def __vocal_mask(magnitude, mag_filter):
    margin = 2 # Reduce bleed between the vocals masks
    power = 3  # Soft mask computed in a numerically stable way
    return librosa.util.softmask(
        magnitude - mag_filter, margin * mag_filter, power=power)

def __time_series_foreground(vocal_mask, magnitude, phase):
    mag_foreground = vocal_mask * magnitude
    spectrogram_foreground = mag_foreground * phase
    return librosa.istft(spectrogram_foreground)

def __isolate_vocals(chunk, chunk_path, chunk_length, index, offset):
    """ Strips away the instrumentals while preserving the vocals.
        Inspiried by Brian McFee's vocal separation from librosa-gallery """
    curr_chunk_len = len(chunk) / 1000
    if curr_chunk_len < 2: # Librosa cannot load small durations
        return chunk
    starting_point = offset + (index * chunk_length)
    time_series, rate = librosa.load(chunk_path, sr=None)
    magnitude, phase = librosa.magphase(librosa.stft(time_series))
    mag_filter = __magnitude_filter(magnitude, rate)
    mag_filter = numpy.minimum(magnitude, mag_filter) # Filter must be < input
    vocal_mask = __vocal_mask(magnitude, mag_filter)
    output = __time_series_foreground(vocal_mask, magnitude, phase)
    # Overwrite the chunk with the vocal isolated audio
    librosa.output.write_wav(chunk_path, output, rate)
    return AudioSegment.from_file(chunk_path)

def improve_accuracy(chunk, chunk_path, chunk_length, index, offset):
    """ Filter chunk through various functions to improve speech recognition """
    chunk_length /= 1000
    offset /= 1000
    accuracy = __isolate_vocals(chunk, chunk_path, chunk_length, index, offset)
    # Maximize after isolating the vocals to ensure instruments do not lower the
    # potency of the increase
    accuracy = __maximize_volume(chunk)
    return accuracy
