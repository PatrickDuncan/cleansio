""" Utillity functions for File I/O """

import os
from os.path import basename, expanduser
from .env import create_env_var

def create_temp_dir():
    """ Create directory to store all temporary files """
    create_env_var('CLEANSIO_TEMP_DIR', expanduser('~') + '/.cleansio-temp/')
    os.makedirs(os.environ['CLEANSIO_TEMP_DIR'], exist_ok=True)
    return os.environ['CLEANSIO_TEMP_DIR']

def file_name_no_ext(file_path):
    """ Get a file name with no extension from a file path """
    return ''.join(basename(file_path).split('.')[:-1])
