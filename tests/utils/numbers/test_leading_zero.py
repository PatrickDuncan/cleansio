# pylint: skip-file

from utils import is_number, gcs_time_to_ms, leading_zero
from google.protobuf.duration_pb2 import Duration

################################################################################
### is_number

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

################################################################################
### gcs_time_to_ms

def test_gcs_time_to_ms_empty():
    assert gcs_time_to_ms('') == 0 and gcs_time_to_ms(None) == 0

def test_gcs_time_to_ms_just_nanos():
    duration = Duration()
    duration.nanos = 900000000
    assert gcs_time_to_ms(duration) == 900

def test_gcs_time_to_ms_just_seconds():
    duration = Duration()
    duration.seconds = 2
    assert gcs_time_to_ms(duration) == 2000

def test_gcs_time_to_ms_nanos_and_seconds():
    duration = Duration()
    duration.nanos = 300000000
    duration.seconds = 5
    assert gcs_time_to_ms(duration) == 5300

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
