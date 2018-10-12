""" Displays the lyrics of an audio file """

import os
import sys
from audio import AudioFile
from speech import transcribe

def valid_input():
    """ Validates the user's input """
    return len(sys.argv) > 1

def cleanup():
    """ Removes temporary files """
    if 'CLEANSIO_TEMP_FILE' in os.environ:
        os.remove(os.environ.get('CLEANSIO_TEMP_FILE'))
    if 'CLEANSIO_SLICES_LIST' in os.environ:
        slices_list_env_var = os.environ['CLEANSIO_SLICES_LIST']
        slices_list = slices_list_env_var[2:-2].split("', '")
        for slice_file in slices_list:
            os.remove(slice_file)

if __name__ == '__main__':
    if valid_input():
        transcribe(AudioFile(sys.argv[1]))
        cleanup()
    else:
        print("Please see the README.")
