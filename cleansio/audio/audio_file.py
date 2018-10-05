""" Classifies an audio file """

class AudioFile:
    """ Classifies an audio file """
    def __init__(self, file_path):
        self.file_path = file_path
        self.sample_rate = 44100 # TODO
        self.channels = 1        # TODO
