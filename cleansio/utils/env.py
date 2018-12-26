""" Utillity functions for environment variables """

import os

def create_env_var(name, value):
    """ Instantiate a new environment variable with given value """
    os.environ[name] = value
