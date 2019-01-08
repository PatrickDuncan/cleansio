""" Censors audio chunks in a continuous stream """

from .censor import Censor

class CensorRealtime(Censor):
    """ Filters audio stream in real-time """
    def __init__(self, explicits):
        super().__init__(explicits)

    @classmethod
    def censor(cls):
        """ Censors audio chunks in a continuous stream """
        print('Real-time mode has not been implemented yet.')
        # TODO
