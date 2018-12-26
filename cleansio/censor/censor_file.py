""" Creates a clean version of a file by removing explicits """

from audio import AudioFile
from speech import transcribe
from .censor import Censor

class CensorFile(Censor):
    """ Removes explicits from a file """
    def __init__(self, file_path):
        super().__init__()
        self.file_path = file_path

    def censor(self):
        """ Creates a clean/new version of a file by removing explicits """
        transcribe(AudioFile(self.file_path))
        # TODO
