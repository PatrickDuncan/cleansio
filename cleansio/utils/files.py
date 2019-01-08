""" Utillity functions for File I/O """

from errno import EEXIST
import os
from os.path import basename, expanduser
from .env import create_env_var

def create_temp_dir():
    """ Create directory to store all temporary files """
    create_env_var('CLEANSIO_TEMP_DIR', expanduser('~') + '/.cleansio-temp/')
    try:
        os.makedirs(os.environ['CLEANSIO_TEMP_DIR'])
    except OSError as os_error:
        # Ignore the error if it's just that the directory exists
        if os_error.errno != EEXIST:
            raise # Don't ignore errors other than the directory existing
    return os.environ['CLEANSIO_TEMP_DIR']

def file_name_no_ext(file_path):
    """ Get a file name with no extension from a file path """
    return ''.join(basename(file_path).split('.')[:-1])