""" Cleans up temporary files after the program runs """

# environ - To read the environment variables which we use for communication
# remove  - To remove the temporary files
from atexit import register
from os import environ, remove
from signal import signal, SIGABRT, SIGILL, SIGINT, SIGSEGV, SIGTERM
import sys

# Cleans up files on normal or abnormal exit
# The arguments are unused - they are only here to satisfy atexit.
def cleanup(_sig_num=None, _cur_stack_frame=None):
    """ Removes temporary files """
    __remove_temp_file()
    __remove_slices()
    sys.exit(0)

def setup_cleanup():
    """ Always call cleanup on any type of exit by creating triggers """
    # Set the cleanup handler for each signal which we want to catch
    for sig in (SIGABRT, SIGILL, SIGINT, SIGSEGV, SIGTERM):
        signal(sig, cleanup)
    # Register the cleanup function to be called if the program exits normally
    register(cleanup)

def __remove_temp_file():
    """ Removes converted WAV file """

    if 'CLEANSIO_TEMP_FILE' in environ:
        temp_file = environ.get('CLEANSIO_TEMP_FILE')
        try:
            remove(temp_file)
        except FileNotFoundError:
            pass

def __remove_slices():
    """ Removes each slice of the converted WAV file """

    if 'CLEANSIO_SLICES_LIST' in environ:
        slices_list_env_var = environ['CLEANSIO_SLICES_LIST']
        slices_list = slices_list_env_var[2:-2].split('\', \'')
        for slice_file in slices_list:
            try:
                remove(slice_file)
            except FileNotFoundError:
                pass
