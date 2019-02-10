""" Functions which preprocess an audio chunk to improve the accuracy of speech
    recognition. """
# pylint: disable=C0411

import numpy
import librosa
from pydub import AudioSegment
from .convert import convert_file

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
    print(magnitude - mag_filter)
    print(margin * mag_filter)
    print("===================================================================")
    return librosa.util.softmask(
        magnitude - mag_filter, margin * mag_filter, power=power)

def __time_series_foreground(vocal_mask, magnitude, phase):
    mag_foreground = vocal_mask * magnitude
    spectrogram_foreground = mag_foreground * phase
    return librosa.istft(spectrogram_foreground)

def __isolate_vocals(chunk, chunk_path):
    """ Strips away the instrumentals while preserving the vocals.
        Inspiried by Brian McFee's vocal separation from librosa-gallery """
    try:
        if (len(chunk) / 1000) < 2: # Librosa cannot load small durations
            return chunk
        time_series, rate = librosa.load(chunk_path, sr=None)
        magnitude, phase = librosa.magphase(librosa.stft(time_series))
        mag_filter = __magnitude_filter(magnitude, rate)
        mag_filter = numpy.minimum(magnitude, mag_filter)
        vocal_mask = __vocal_mask(magnitude, mag_filter)
        output = __time_series_foreground(vocal_mask, magnitude, phase)
        # Overwrite the chunk with the vocal isolated audio
        librosa.output.write_wav(chunk_path, output, rate)
    except Exception as e:
        # librosa is not reliable, ignore any warnings
        # It's fine if a single chunk fails to get its vocals isolated
        print(chunk_path)
        print(e)
        pass
    finally:
        return AudioSegment.from_file(chunk_path) # New file -> new AS object

def improve_accuracy(chunk, chunk_path):
    """ Filter chunk through various functions to improve speech recognition """
    accuracy_chunk = __isolate_vocals(chunk, chunk_path)
    # Maximize after isolating the vocals to ensure instruments do not lower the
    # potency of the increase
    accuracy_chunk = __maximize_volume(accuracy_chunk)
    convert_file(accuracy_chunk, 'wav', chunk_path)
    return accuracy_chunk
