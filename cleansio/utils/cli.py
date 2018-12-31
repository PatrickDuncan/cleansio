""" Utillity functions for command line interfaces """

import argparse

def setup_cli_args():
    """ Defines the different CLI arguments """
    parser = argparse.ArgumentParser(description='Real-time music censoring.')
    parser = __set_file_path_arg(parser)
    return parser.parse_args()

def __set_file_path_arg(parser):
    parser.add_argument(
        'file_path',
        nargs='?',
        help='enables file mode which creates a clean version of the file. \
            Relative or full path')
    return parser
