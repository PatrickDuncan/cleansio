import os
from os.path import expanduser

def create_temp_dir():
	os.environ['CLEANSIO_TEMP_DIR'] = f"{expanduser('~')}/.cleansio-temp/"
	os.makedirs(os.environ['CLEANSIO_TEMP_DIR'], exist_ok=True)
	return os.environ['CLEANSIO_TEMP_DIR']

def create_environment_variable(name, value):
	os.environ[name] = value