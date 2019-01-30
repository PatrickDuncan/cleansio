""" Censors audio chunks by muting explicit sections """

from pydub import AudioSegment
from speech import Timestamp, Transcribe

class Censor():
    """ Superclass of CensorFile and CensorRealtime """
    def __init__(self, explicits):
        super().__init__()
        self.explicits = explicits

    def censor_audio_chunk(self, file_path):
        """ Common process to censor an audio chunk """
        audio_segment = AudioSegment.from_file(file_path)
        lyrics = self.__get_lyrics(file_path, audio_segment)
        timestamps = self.__get_timestamps(lyrics)
        if timestamps:
            self.__mute_explicits(file_path, audio_segment, timestamps)
        # Return a new AudioSegment object because the file may have changed
        return AudioSegment.from_file(file_path)

    def __mute_explicits(self, file_path, audio_segment, timestamps):
        """ Go through each word, if its an explicit, mute the duration """
        muted = False
        for stamp in timestamps:
            if stamp['word'].lower() in self.explicits: # Explicit found, mute
                audio_segment = self.__mute_explicit(audio_segment, stamp)
                muted = True
        if muted:
            # Overwrite the chunk with the mute(s)
            audio_segment.export(file_path, format='wav')

    @classmethod
    def __mute_explicit(cls, audio_segment, timestamp):
        len_as = len(audio_segment)
        # Check if the timestamp is outside of this chunk (from overlapping)
        if timestamp['start'] > len_as:
            return audio_segment
        beginning = audio_segment[:timestamp['start']]
        duration = timestamp['end'] - timestamp['start']
        mute = AudioSegment.silent(duration=duration)
        # The end of the timestamp cannot be longer than the file
        end_length = len_as if len_as < timestamp['end'] else timestamp['end']
        end = audio_segment[end_length:]
        return beginning + mute + end

    @classmethod
    def __get_lyrics(cls, file_path, audio_segment):
        return Transcribe(file_path, audio_segment.frame_rate).lyrics

    @classmethod
    def __get_timestamps(cls, lyrics):
        return Timestamp(lyrics).timestamps
