""" Censors audio chunks by muting explicit sections """

from pydub import AudioSegment
from speech import Timestamp, Transcribe

class Censor():
    """ Superclass of CensorFile and CensorRealtime """
    def __init__(self):
        super().__init__()

    def censor_audio_chunk(self, file_path):
        """ Common process to censor an audio chunk """
        audio_segment = AudioSegment.from_file(file_path)
        lyrics = self.__get_lyrics(file_path, audio_segment)
        timestamps = self.__get_timestamps(file_path, lyrics)
        print(timestamps)

    @classmethod
    def __get_lyrics(cls, file_path, audio_segment):
        return Transcribe(file_path, audio_segment.frame_rate).lyrics

    @classmethod
    def __get_timestamps(cls, file_path, lyrics):
        return Timestamp(file_path, lyrics).timestamps
