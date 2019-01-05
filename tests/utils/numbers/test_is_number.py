# pylint: skip-file

from utils import is_number

def test_is_number_empty():
    assert not is_number('')

def test_is_number_string():
    assert not is_number('cleansio')

def test_is_number_string_and_num():
    assert not is_number('hello123')

def test_is_number_different_type():
    assert is_number(91327)

def test_is_number_integer():
    assert is_number(str(91327))

def test_is_number_negative():
    assert is_number(str(-91327))

def test_is_number_float():
    assert is_number(str(91.327))

def test_is_number_negative_float():
    assert is_number('-91327.23')
    assert is_number(str(-91327.23))
