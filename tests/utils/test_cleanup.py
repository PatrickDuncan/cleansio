#pylint: skip-file

# Standard imports
from uuid import uuid4
from random import randint
import os
import pytest

# Function to test
from utils import cleanup

# Tests the cleanup function
def test_cleanup():
    ## Temporary file ##

    # Temp file shouldn't exist
    if 'CLEANSIO_TEMP_FILE' in os.environ: # Temp file var exists
        # Fetch the name of the temp file
        temp_file = os.environ.get('CLEANSIO_TEMP_FILE')
    else: # Temp file variable doesn't exist
        temp_file_name = str(uuid4().hex) # Fetch a random temporary file name
        # Create a path to the temporary file
        temp_file = "./{0}".format(temp_file_name)
        os.environ['CLEANSIO_TEMP_FILE'] = temp_file # For function

    create_temp_file(temp_file)

    ## Chunks ##
    chunks_list = [] # Holds names of chunk files. Used later on in test.

    if 'CLEANSIO_CHUNKS_LIST' in os.environ: # Chunks exist
        chunks_list_env_var = os.environ['CLEANSIO_CHUNKS_LIST']
        chunks_list = chunks_list_env_var.split[2:-2].split('\', \'')
        for chunk_file in chunks_list:
            create_temp_file(chunk_file)
    else: # Chunks don't exist
        # Generate a random number of chunk files
        for i in range(0,randint(3, 10)+1):
            # Choose a random name for the chunk which we'll generate
            temp_chunk_name = str(uuid4().hex)
            create_temp_file(temp_chunk_name)
            chunks_list.append(temp_chunk_name)
        os.environ['CLEANSIO_CHUNKS_LIST'] = str(chunks_list)

    with pytest.raises(SystemExit) as pytest_e: # Ignore sys.exit()
        cleanup() # Run the function

    ## Checking whether or not the function worked ##
    # The temporary file shouldn't exist after the cleanup function runs
    assert(not exists(temp_file))

    for chunk in chunks_list: # None of the "chunk files" should exist
        assert(not exists(chunk))

def exists(file_name):
    """ Checks whether a file with the given name exists. """
    try:
        f = open(file_name, "r")
        f.close()
        return True
    except FileNotFoundError:
        return False

def create_temp_file(file_name):
    """ Creates a temp file with the given name, if it doesn't already exist """
    if not exists(file_name):
        f = open(file_name, "w")
        fconts = str(uuid4().hex)
        f.write(fconts)
        f.close()
    else:
        errStr = "File {0} already exists, won't overwrite".format(file_name)
        raise FileExistsError(errStr)
