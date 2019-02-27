# pylint: skip-file

import os
from pydub import AudioSegment
from audio.accuracy import __maximize_volume
from audio.accuracy import improve_accuracy

def __get_file(file_path):
    return os.path.dirname(os.path.realpath(__file__)) + file_path

def test_loudness_maximization():
    try:
        file_path = __get_file('/../data/testing.wav')
        audio_segment = AudioSegment.from_file(file_path)
        # Duplicate the audio file
        file_path_duplicate = __get_file('/../data/testing-max-volume.wav')
        duplicate_file = audio_segment.export(file_path_duplicate, format='wav')
        audio_segment_duplicate = AudioSegment.from_file(file_path_duplicate)
        init_loudness = audio_segment_duplicate.dBFS
        # Test that the volume was successfully maximized
        max_volume_chunk = __maximize_volume(audio_segment_duplicate)
        max_loundess = max_volume_chunk.dBFS
        assert init_loudness < max_loundess
    except:
        assert False
    finally:
        #Cleanup
        os.remove(file_path_duplicate)
