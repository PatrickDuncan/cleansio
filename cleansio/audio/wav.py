""" RIFF (little-endian) data, WAVE audio, Microsoft PCM, 16 bit, mono 44100 Hz """

class Wave:
    """ Classifies a WAVE audio file """
    def __init__(self, data):
        self.channels = self.__set_channels(data)
        self.encoding = 'LINEAR16'
        self.sample_rate = self.__set_sample_rate(data)

    @staticmethod
    def __set_channels(data):
        channels = data[-1]
        if 'mono' in channels:
            return 1
        elif 'stereo' in channels:
            return 2
        return None

    @staticmethod
    def __set_sample_rate(data):
        return int(data[-1].split(' ')[1])
