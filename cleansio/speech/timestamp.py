""" Locates where words are located in an audio chunk """

from utils import gcs_time_to_ms, num_syllables

class Timestamp():
    """ Words are located by either assessing silence or by estimatingself.
        Timestamps in the form of {word:, start:, end:} """
    def __init__(self, lyrics):
        super().__init__()
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
        timestamps = self.__parse_timestamps()
        return self.__improve_timestamps(timestamps)

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

    def __improve_timestamps(self, timestamps):
        """ Adjusts the GCS's timestamps to be more accurate. O(n) """
        num_stamps = len(timestamps)
        for i in range(num_stamps):
            accuracy = self.__timestamp_accuracy(timestamps[i])
            # Too long, shorten one end
            if accuracy == 1 and i > 1:
                timestamps[i] = self.__shorten_timestamp(
                    timestamps[i], timestamps[i - 1])
            # Too short, lengthen one end
            elif accuracy == -1 and i < num_stamps - 1:
                timestamps[i] = self.__lengthen_timestamp(
                    timestamps[i], timestamps[i + 1])
        return timestamps

    def __shorten_timestamp(self, timestamp, past):
        """ Shorten the length of a timestamp """
        past_accuracy = self.__timestamp_accuracy(past)
        # Trim more from the beginning if past is short
        timestamp['start'] += 200 if past_accuracy == -1 else 100
        return timestamp

    def __lengthen_timestamp(self, timestamp, future):
        """ Lengthen the length of a timestamp """
        future_accuracy = self.__timestamp_accuracy(future)
        # Add more to the end if future is long
        timestamp['end'] += 200 if future_accuracy == 1 else 100
        return timestamp

    @classmethod
    def __timestamp_accuracy(cls, timestamp):
        """ -1: Too short, 0: Accurate, 1: Too long """
        syllables = num_syllables(timestamp['word'])
        # On average a human says 1 syllable every 200 ms
        expected_syll = (timestamp['end'] - timestamp['start']) / 200
        if expected_syll - 2 > syllables:   # Too long
            return 1
        elif expected_syll + 2 < syllables: # Too short
            return -1
        return 0
