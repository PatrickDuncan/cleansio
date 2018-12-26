""" Displays the lyrics of an audio file """

# Standard imports
import sys
from atexit import register
from signal import signal, SIGABRT, SIGILL, SIGINT, SIGSEGV, SIGTERM

# Imports from our modules
from censor import CensorFile, CensorRealtime
from utils import cleanup

def is_file_mode():
    """ Validates if user is running file mode """
    return len(sys.argv) > 1

def setup_cleanup():
    """ Always call cleanup on any type of exit by creating triggers """
    # Set the cleanup handler for each signal which we want to catch
    for sig in (SIGABRT, SIGILL, SIGINT, SIGSEGV, SIGTERM):
        signal(sig, cleanup)
    # Register the cleanup function to be called if the program exits normally
    register(cleanup)

if __name__ == '__main__':
    setup_cleanup()
    if is_file_mode():
        CensorFile(sys.argv[1]).censor()
    else:
        CensorRealtime().censor()
