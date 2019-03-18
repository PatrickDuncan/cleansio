""" Cleanup macOS """

from os import environ
import subprocess

class CleanupMac():
    """ Cleanup for systems using macOS """

    def __init__(self):
        super(CleanupMac, self).__init__()

    @classmethod
    def clean(self):
        if 'CLEANSIO_REALTIME' in environ and       \
            'CLEANSIO_OLD_SOUND_OUT' in environ and \
            'CLEANSIO_OLD_SOUND_IN' in environ:
            subprocess.run(['SwitchAudioSource', '-t', 'output', '-s', environ['CLEANSIO_OLD_SOUND_OUT']])
            subprocess.run(['SwitchAudioSource', '-t', 'input', '-s', environ['CLEANSIO_OLD_SOUND_IN']])
