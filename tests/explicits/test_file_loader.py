#pylint: skip-file

# Setup import path to include the wordlist files
import sys
# Import modules to test
from explicits import FileLoader
# Testing
import pytest

# Simplest case - newline-separated word list
# tmpdir - A temporary directory path, supplied by pytest
def test_newline(tmpdir):
    # A list which we will write to the file
    correct_arr = {"a", "b", "c"}
    # Create a temporary file
    tmp_path = tmpdir.join("newlinefile")
    # Write a test array to a temporary file, separated by newlines
    tmp_path.write("\n".join(correct_arr))
    # Test - create a FileLoader and see whether or not it loads the data
    fl = FileLoader(str(tmp_path))
    # The array which we read from the file should be the same as the array which we wrote
    assert fl.set == correct_arr
    assert '' not in fl.set

# Nonexistent file given - exception expected
# tmp_path - A temporary directory path, supplied by pytest
def test_nonexistent_file(tmpdir):
    tmp_path = tmpdir.join("nonexistent")
    with pytest.raises(FileNotFoundError, message="Expecting FileNotFoundError"):
        # Try to read a nonexistent file
        fl = FileLoader(str(tmp_path))

# Non-newline separator (CSV)
# tmp_path - A temporary directory path, supplied by pytest
def test_csv_file(tmpdir):
    # The separator which we want to use in the file
    separator = ","
    # A list which we will write to the file
    correct_arr = {"a", "b", "c"}
    # Create a temp file
    tmp_path = tmpdir.join("test.csv")
    # Write a test array to a temporary file, separated by commas
    tmp_path.write(separator.join(correct_arr))
    # Test - create a FileLoader and see whether or not it loads the data
    fl = FileLoader(str(tmp_path), separator)
    # The array which we read from the file should be the same as the array which we wrote
    assert fl.set == correct_arr
