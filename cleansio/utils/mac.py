""" Utility functions for macOS """

from os import environ
from subprocess import run

class MacUtil():
    """ Utility functions for macOS """
    def __init__(self):
        super().__init__()

    @classmethod
    def switch_audio_source(cls, interface, device_name):
        """ Switch the system's audio source
            interface : [input|output] """
        run(['SwitchAudioSource', '-t', interface, '-s', device_name],
            capture_output=True, # Ignore output by capturing it
            check=True)          # Throw an error if command fails

    @classmethod
    def audio_source(cls, interface):
        """ Returns the system's audio source
            interface : [input|output] """
        raw_device_name = run(
            ['SwitchAudioSource', '-c', '-t', interface],
            capture_output=True, # Return output
            check=True)          # Throw an error if command fails
        return raw_device_name.stdout.decode('utf-8').replace('\n', '')

    @classmethod
    def clean(cls):
        """ Resets the system's state """
        if 'CLEANSIO_REALTIME' in environ and       \
            'CLEANSIO_OLD_SOUND_OUT' in environ and \
            'CLEANSIO_OLD_SOUND_IN' in environ:
            cls.switch_audio_source('output', environ['CLEANSIO_OLD_SOUND_OUT'])
            cls.switch_audio_source('input', environ['CLEANSIO_OLD_SOUND_IN'])
