# pylint: skip-file

from audio.helper import file_name_no_ext

def test_file_name_no_ext():
    assert file_name_no_ext('/Users/bob/folder/audio.wav') == 'audio'

def test_file_name_no_ext_empty():
    assert file_name_no_ext('') == ''

def test_file_name_no_ext_with_slash():
    assert file_name_no_ext('/c/user/file.mp3') == 'file'

def test_file_name_no_ext_only_file():
    assert file_name_no_ext('file!!.mp3') == 'file!!'
