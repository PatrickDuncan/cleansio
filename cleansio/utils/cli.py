""" Utillity functions for command line interfaces """

import argparse
import sys
from colorama import Fore
from .files import relative_path

def setup_cli_args():
    """ Defines the different CLI arguments """
    parser = argparse.ArgumentParser(description='Real-time music censoring.')
    parser = __set_file_path(parser)
    parser = __set_user_list(parser)
    parser = __set_combine_list(parser)
    parser = __set_output_path(parser)
    parser = __set_output_encoding(parser)
    parser = __set_output_encoding_list(parser)
    parser = __set_store_recording(parser)
    args = parser.parse_args() # NOTE: Cannot add args after calling parse_args
    __exiting_args(args)
    __validate_args(args, parser)
    return args

def __set_file_path(parser):
    parser.add_argument(
        'file_path',
        nargs='?',
        help='enables file mode which creates a clean version of the file. \
            Relative or full path')
    return parser

def __set_user_list(parser):
    """ Sets the arguments which control the user list of explicit words """
    parser.add_argument(
        '-u',
        '--user-list',
        nargs=1,
        action='store',
        help='takes a path which points to a custom list of words which you \
        would like to mark as explicit.')
    return parser

def __set_combine_list(parser):
    """ Allows the user to combine their list with the internal list """
    parser.add_argument(
        '-c',
        '--combine-lists',
        action='store_true',
        help='the list which you provide with the \'-u\' option replaces the \
        program\'s internal list by default. However, you can pass \
        this option in addition to -u to have your list combined with the \
        internal list.')
    return parser

def __set_store_recording(parser):
    """ Allows the user to determine where the clean file is created """
    parser.add_argument(
        '-s',
        '--store-recording',
        action='store_true',
        help='save the clean realtime audio as a file in the output location')
    return parser

def __set_output_path(parser):
    """ Allows the user to determine where the clean file is created """
    parser.add_argument(
        '-o',
        '--output-location',
        nargs=1,
        action='store',
        help='takes a path which will overwrite the default location of where \
        the clean file will be created. If the file already exists it will be \
        overwritten.')
    return parser

def __set_output_encoding(parser):
    """ Allows the user to determine the audio encoding of the clean file """
    parser.add_argument(
        '-e',
        '--output-encoding',
        nargs=1,
        action='store',
        help='specify the audio encoding type of the output file. The file \
        extension of --output-location is not sufficient. Default is wav.')
    return parser

def __set_output_encoding_list(parser):
    """ Allows the user to determine the different audio encoding types """
    parser.add_argument(
        '--output-encoding-list',
        action='store_true',
        help='list the possible audio encoding types for the output file.')
    return parser

def __exiting_args(args):
    """ Handles arguments that simply print and exit """
    if args.output_encoding_list:
        with open(__encoding_types_path()) as types:
            __exit(types.read())

def __validate_args(args, parser):
    """ Validates user input """
    __validate_combine_list(args, parser)
    __validate_output_encoding(args, parser)

def __validate_combine_list(args, parser):
    # Ensure that the -u option is present if the -c option is given
    map_args = vars(args) # Convert the arguments to a map
    if map_args['combine_lists'] and not map_args['user_list']:
        __error(parser, 'The -c option requires -u!')

def __validate_output_encoding(args, parser):
    # Validate if the user's encoding is valid
    output_encoding = args.output_encoding
    if output_encoding:
        encoding_choice = output_encoding[0]
        valid = False
        with open(__encoding_types_path()) as types:
            for encoding_type in types.readlines():
                if encoding_type.strip() == encoding_choice:
                    valid = True
                    break
        if not valid:
            __error(parser, encoding_choice + ' is not supported!')

def __encoding_types_path():
    return relative_path('../data/encoding-types')

def __error(parser, message):
    parser.error(Fore.RED + message)

def __exit(message):
    print(message.strip())
    sys.exit(0)
