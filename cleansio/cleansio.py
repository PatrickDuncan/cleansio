""" Displays the lyrics of an audio file """

import sys
from audio import AudioFile
from speech import transcribe

def valid_input():
    """ Validates the user's input """
    return sys.argv[1].lower()[-5:] == '.flac'

if __name__ == '__main__':
    if valid_input():
        transcribe(AudioFile(sys.argv[1]))
    else:
        print("Please see the README.")
