""" Helper Functions """

import os
from os.path import expanduser

def create_temp_dir():
    """ Create directory to store all temporary files"""
    create_env_var('CLEANSIO_TEMP_DIR', f"{expanduser('~')}/.cleansio-temp/")
    os.makedirs(os.environ['CLEANSIO_TEMP_DIR'], exist_ok=True)
    return os.environ['CLEANSIO_TEMP_DIR']

def create_env_var(name, value):
    """ Instantiate a new environment variable with given value"""
    os.environ[name] = value
