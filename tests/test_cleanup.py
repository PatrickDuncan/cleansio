#pylint: skip-file

# Standard imports
from uuid import uuid4
from random import randint
import os
import pytest

# Function to test
from cleansio import cleanup

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

    ## Slices ##
    slices_list = [] # Holds names of slice files. Used later on in test.

    if 'CLEANSIO_SLICES_LIST' in os.environ: # Slices exist
        slices_list_env_var = os.environ['CLEANSIO_SLICES_LIST']
        slices_list = slices_list_env_var.split[2:-2].split('\', \'')
        for slice_file in slices_list:
            create_temp_file(slice_file)
    else: # Slices don't exist
        # Generate a random number of slice files
        for i in range(0,randint(3, 10)+1):
            # Choose a random name for the slice which we'll generate
            temp_slice_name = str(uuid4().hex)
            create_temp_file(temp_slice_name)
            slices_list.append(temp_slice_name)
        os.environ['CLEANSIO_SLICES_LIST'] = str(slices_list)

    with pytest.raises(SystemExit) as pytest_e: # Ignore sys.exit()
        cleanup() # Run the function

    ## Checking whether or not the function worked ##
    # The temporary file shouldn't exist after the cleanup function runs
    assert(not exists(temp_file))

    for slice in slices_list: # None of the "slice files" should exist
        assert(not exists(slice))

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
