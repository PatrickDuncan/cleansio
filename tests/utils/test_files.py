# pylint: skip-file

from utils import file_name_no_ext, append_before_ext

# file_name_no_ext

def test_file_name_no_ext():
    assert file_name_no_ext('/Users/bob/folder/audio.wav') == 'audio'

def test_file_name_no_ext_empty():
    assert file_name_no_ext('') == ''

def test_file_name_no_ext_with_slash():
    assert file_name_no_ext('/c/user/file.mp3') == 'file'

def test_file_name_no_ext_only_file():
    assert file_name_no_ext('file!!.mp3') == 'file!!'

# append_before_ext

def test_append_before_ext_empty_string_empty_addition():
    assert append_before_ext('', '') == ''

def test_append_before_ext_empty_string():
    assert append_before_ext('', '-acc') == '-acc'

def test_append_before_ext_empty_addition():
    assert append_before_ext('cleansio.wav', '') == 'cleansio.wav'

def test_append_before_ext_no_extension_empty_string():
    assert append_before_ext('cleansio', '') == 'cleansio'

def test_append_before_ext_no_extension():
    assert append_before_ext('cleansio', 'extra') == 'cleansioextra'

def test_append_before_ext_extension_1_dot():
    assert append_before_ext('cleansio.wav', '-acc') == 'cleansio-acc.wav'

def test_append_before_ext_extension_2_dots():
    assert append_before_ext('cleansio.w.av', '-acc') == 'cleansio.w-acc.av'

def test_append_before_ext_extension_3_dots():
    assert append_before_ext('cleansio.w.a.v', '-acc') == 'cleansio.w.a-acc.v'
