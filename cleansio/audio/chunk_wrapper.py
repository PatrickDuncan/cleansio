""" Wrapper for pydub's AudioSegment, used to add new properties """

class ChunkWrapper():
    """ Wrapper for pydub's AudioSegment """

    def __init__(self, audio_segment, mute_next_chunk=0):
        super().__init__()
        self.segment = audio_segment
        self.mute_next_start = mute_next_chunk
