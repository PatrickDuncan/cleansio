""" Displays the lyrics of an audio file """

# Standard imports
import sys
from atexit import register
from signal import signal, SIGABRT, SIGILL, SIGINT, SIGSEGV, SIGTERM

# Imports from our modules
from audio import AudioFile
from speech import transcribe
from utils import cleanup

def valid_input():
    """ Validates the user's input """
    return len(sys.argv) > 1

if __name__ == '__main__':
    # Set the cleanup handler for each signal which we want to catch
    for sig in (SIGABRT, SIGILL, SIGINT, SIGSEGV, SIGTERM):
        signal(sig, cleanup)
    # Register the cleanup function to be called if the program exits normally
    register(cleanup)
    if valid_input():
        transcribe(AudioFile(sys.argv[1]))
    else:
        print('Please see the README.')
