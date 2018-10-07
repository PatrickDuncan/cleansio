""" FLAC audio bitstream data, 16 bit, mono, 44.1 kHz, 132300 samples """

class Flac:
    """ Classifies a FLAC audio file """
    def __init__(self, data):
        self.channels = self.__set_channels(data)
        self.encoding = 'FLAC'
        self.sample_rate = self.__set_sample_rate(data)

    @staticmethod
    def __set_channels(data):
        return {
            'mono': 1,
            'stereo': 2
        }.get(data[2])

    @staticmethod
    def __set_sample_rate(data):
        if len(data) < 5:
            return None
        sample_rate = data[3].split(' ')[0]
        return int(float(sample_rate) * 1000)
