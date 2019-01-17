""" Displays the lyrics of an audio file """

# Imports from our modules
from censor import CensorFile, CensorRealtime
from utils import setup_cleanup, setup_cli_args
from explicits import Explicits

def is_file_mode():
    """ Validates if user is running file mode """
    return ARGS.file_path

if __name__ == '__main__':
    setup_cleanup()
    ARGS = setup_cli_args()
    EXPLICITS = Explicits(ARGS).set
    if is_file_mode():
        CensorFile(ARGS, EXPLICITS).censor()
    else:
        CensorRealtime(EXPLICITS).censor()
