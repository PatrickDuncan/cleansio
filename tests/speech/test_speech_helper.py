# pylint: skip-file

from speech.helper import leading_zero

def test_leading_zero_empty():
    assert leading_zero('') == ''

def test_leading_zero_int_single_digit():
    assert leading_zero(4) == '04'

def test_leading_zero_int_double_digit():
    assert leading_zero(23) == '23'

def test_leading_zero_string_single_digit():
    assert leading_zero('9') == '09'

def test_leading_zero_string_triple_digit():
    assert leading_zero('504') == '504'
