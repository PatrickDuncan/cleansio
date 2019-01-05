""" Utillity functions for dealing with numbers """

import re
from google.protobuf.duration_pb2 import Duration

def is_number(num):
    """ Validates if a string is a number. Can be negative or a float """
    return re.match(r'^-?\d+(\.\d+|\d*)$', str(num))

def leading_zero(num):
    """ Adds a leading 0 to single digit numbers. Converts numbers to string """
    str_num = str(num)
    if not str_num.isdigit(): # Check if it's a number
        return str_num
    if len(str_num) < 2:
        return '0' + str_num
    return str_num

def gcs_time_to_ms(time):
    """ Converts seconds and nano to milliseconds """
    if not isinstance(time, Duration)                 \
        or (time.nanos and not is_number(time.nanos)) \
        or (time.seconds and not is_number(time.seconds)):
        return 0
    milliseconds = time.seconds * 1000 if time.seconds else 0
    milliseconds += time.nanos // 1e6
    return milliseconds
