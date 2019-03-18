""" Locates where words are located in an audio chunk """

from utils import gcs_time_to_ms

class Timestamp():
    """ Words are located by either assessing silence or by estimatingself.
        Timestamps in the form of {word:, start:, end:} """
    def __init__(self, lyrics):
        super().__init__()
        self.lyrics = lyrics
        self.timestamps = self.__compute_timestamps()

    def __compute_timestamps(self):
        """ Goes through each word in the chunk and computes the timestamps """
        if not self.lyrics:
            return None
        return self.__parse_timestamps()

    def __parse_timestamps(self):
        """ Parses GCS's output and returns [{word:str, start:ms, end:ms},].
            O(n) """
        timestamps = []
        for word in self.lyrics:
            timestamps.append({
                'word': word.word.lower(),
                'start': gcs_time_to_ms(word.start_time),
                'end': gcs_time_to_ms(word.end_time)
            })
        return timestamps
