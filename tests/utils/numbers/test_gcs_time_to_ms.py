# pylint: skip-file

from utils import gcs_time_to_ms
from google.protobuf.duration_pb2 import Duration

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
