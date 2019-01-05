""" Locates where words are located in an audio chunk """

from utils import gcs_time_to_ms

class Timestamp():
    """ Words are located by either assessing silence or by estimatingself.
        Timestamps in the form of {word:, start:, end:} """
    def __init__(self, file_path, lyrics):
        super().__init__()
        self.file_path = file_path
        self.lyrics = lyrics
        self.simple_lyrics = self.__parse_simple_lyrics()
        self.timestamps = self.__compute_timestamps()

    def __parse_simple_lyrics(self):
        """ Returns the lyrics without any timestamps, confidence, etc. """
        results = self.lyrics.results
        return results[0].alternatives[0].transcript if results else None

    def __compute_timestamps(self):
        """ Goes through each word in the chunk and computes the timestamps """
        if not self.lyrics.results:
            return None
        return self.__parse_timestamps()

    def __parse_timestamps(self):
        """ Parses GCS's output and returns [{word:str, start:ms, end:ms},].
            O(n) """
        timestamps = []
        for word_dict in self.lyrics.results[0].alternatives[0].words:
            timestamps.append({
                'word': word_dict.word,
                'start': gcs_time_to_ms(word_dict.start_time),
                'end': gcs_time_to_ms(word_dict.end_time)
            })
        return timestamps
