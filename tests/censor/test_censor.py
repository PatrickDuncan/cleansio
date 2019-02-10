#pylint: skip-file

import os
from pydub import AudioSegment, silence
from censor import Censor

timestamps = [
    {'word': 'hi', 'start': 1000.0, 'end': 1500.0},
    {'word': 'bye', 'start': 1700.0, 'end': 1900.0},
    {'word': 'mute', 'start': 6000.0, 'end': 7000.0}
]

explicits = ['mute']

def __get_file(file_path):
    return os.path.dirname(os.path.realpath(__file__)) + file_path

def test_censor():
    try:
        file_path = __get_file('/../data/testing.wav')
        audio_segment = AudioSegment.from_file(file_path)
        # Duplicate the audio file and begin muting the new file
        file_path_duplicate = __get_file('/../data//testing-censored.wav')
        duplicate_file = audio_segment.export(file_path_duplicate, format = 'wav')
        audio_segment_duplicate = AudioSegment.from_file(file_path_duplicate)
        # Test that the explicits were successfully removed
        Censor(explicits)._Censor__mute_explicits(
            file_path_duplicate, audio_segment_duplicate, timestamps)
        # Get the silence segments
        audio_segment_duplicate = AudioSegment.from_file(file_path_duplicate)
        silent_ranges = silence.detect_silence(
            audio_segment_duplicate, min_silence_len=500, silence_thresh=-50)
        # Assert silence is only in the 'mute' timestamp
        assert len(silent_ranges) == 1
        beginning_diff = silent_ranges[0][0] - timestamps[2]['start']
        end_diff = silent_ranges[0][1] - timestamps[2]['end']
        # Less than 5 (milliseconds) to account for small inaccuracies
        assert abs(beginning_diff) < 5
        assert abs(end_diff) < 5
    except:
        assert False
    finally:
        # Cleanup
        os.remove(file_path_duplicate)
