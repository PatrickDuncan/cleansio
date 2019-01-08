""" Utillity functions for command line interfaces """

import argparse

def setup_cli_args():
    """ Defines the different CLI arguments """
    parser = argparse.ArgumentParser(description='Real-time music censoring.')
    parser = __set_file_path_arg(parser)
    parser = __set_user_list_args(parser)
    parser = __set_combine_list_args(parser)
    return parser.parse_args()

def __set_file_path_arg(parser):
    parser.add_argument(
        'file_path',
        nargs='?',
        help='enables file mode which creates a clean version of the file. \
            Relative or full path')
    return parser

def __set_user_list_args(parser):
    """ Sets the arguments which control the user list of explicit words """
    parser.add_argument(
        '-u',
        '--user-list',
        nargs=1,
        action='store',
        help='takes a path which points to a custom list of words which you\
        would like to mark as explicit.')
    return parser

def __set_combine_list_args(parser):
    """ Allows the user to combine their list with the internal list """
    parser.add_argument(
        '-c',
        '--combine-lists',
        action='store_true',
        help='the list which you provide with the \'-u\' option replaces the\
        program\'s internal list by default. However, you can pass \
        this option in addition to -u to have your list combined with the \
        internal list.')

    # Ensure that the -u option is present if the -c option is given
    map_args = vars(parser.parse_args()) # Convert the arguments to a map
    if map_args['combine_lists'] and not map_args['user_list']:
        parser.error('The -c option requires that the -u option be present')

    return parser
