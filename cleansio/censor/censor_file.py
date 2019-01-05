""" Creates a clean version of a file by removing explicits """

from audio import AudioFile
from .censor import Censor

class CensorFile(Censor):
    """ Removes explicits from a file """
    def __init__(self, file_path):
        super().__init__()
        self.file_path = file_path

    def censor(self):
        """ Creates a clean/new version of a file by removing explicits """
        audio_file = AudioFile(self.file_path)
        # Censor each audio chunk
        for file_path in audio_file.chunks_file_paths:
            self.censor_audio_chunk(file_path)
