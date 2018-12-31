""" Displays the lyrics of an audio file """

# Standard imports
import sys
# Imports from our modules
from censor import CensorFile, CensorRealtime
from utils import setup_cleanup, setup_cli_args

def is_file_mode():
    """ Validates if user is running file mode """
    return ARGS.file_path

if __name__ == '__main__':
    setup_cleanup()
    ARGS = setup_cli_args()
    if is_file_mode():
        CensorFile(sys.argv[1]).censor()
    else:
        CensorRealtime().censor()
