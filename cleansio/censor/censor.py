""" Censors audio chunks by muting explicit sections """

from multiprocessing import Lock
from colorama import Fore
from pathlib import Path
from pydub import AudioSegment
from audio import ChunkWrapper
from speech import Timestamp, Transcribe
from utils import CHUNK_LEN
from audio import convert_and_write_chunk

class Censor():
    """ Superclass of CensorFile and CensorRealtime """
    lock = Lock()
    explicit_count = 0
    muted_timestamps = []
    leftover = 0

    def __init__(self, explicits, output_encoding, output_location):
        super().__init__()
        self.explicits = explicits
        self.encoding = self.__encoding(output_encoding)
        self.location = self.__location(output_location)

    def censor_audio_chunk(self, file_path):
        """ Common process to censor an audio chunk """
        audio_segment = AudioSegment.from_file(file_path)
        if Censor.leftover > 0:
            audio_segment = AudioSegment.silent(duration=Censor.leftover) + audio_segment[Censor.leftover:]
            with open(file_path, 'wb') as chunk_file:
                    convert_and_write_chunk(audio_segment, chunk_file, 'wav')
            print("Censoring " + str(Censor.leftover) + " length at start of this chunk and appending it to the remaing " + str(len(audio_segment[Censor.leftover:]))+ "s of chunk audio")
        lyrics = self.__get_lyrics(file_path, audio_segment)
        print('lyrics = '+str(lyrics))
        timestamps = self.__get_timestamps(lyrics)
        wrapper = ChunkWrapper(audio_segment)
        print('timestamps = '+str(timestamps))
        if timestamps:
            return self.__mute_explicits(file_path, wrapper, timestamps)
        else: # No mute so just return the original file
            return wrapper

    def create_clean_file(self, clean_file):
        print('Cleansio found {1}{0}{2} explicit(s)!'.format(
            Censor.explicit_count, Fore.GREEN, Fore.RESET))
        clean_file.export(self.location, format=self.encoding)
        print(Fore.CYAN + 'Successfully created clean file, it\'s located at:')
        print(Fore.YELLOW + self.location)

    def __mute_explicits(self, file_path, wrapper, timestamps):
        """ Go through each word, if its an explicit, mute the duration """
        muted = False
        for stamp in timestamps:
            if stamp['word'] in self.explicits: # Explicit found, mute
                wrapper = self.__mute_explicit(wrapper, stamp)
                muted = True
                chunk_index = int(file_path.split('-')[-1].split('.')[0])
                print('Found ' + str(stamp) + ' at index ' + str(chunk_index))
                self.__explicit_count(stamp, chunk_index * CHUNK_LEN)
        if muted:
            Censor.lock.acquire()
            # Overwrite the chunk with the mute(s) safely
            wrapper.segment.export(file_path, format='wav')
            Censor.lock.release()
        return wrapper

    def __location(self, location):
        if location:
            return location[0]
        current_dir = str(Path(__file__).parents[2])
        return current_dir + '/clean_file.' + self.encoding

    def __encoding(cls, encoding):
        return encoding[0] if encoding else 'wav'

    @classmethod
    def __mute_explicit(cls, wrapper, timestamp):
        len_as = len(wrapper.segment)
        # Check if the timestamp is outside of this chunk (from overlapping)
        if timestamp['start'] > len_as:
            return wrapper
        start_time = wrapper.segment[:timestamp['start']]
        # The end of the timestamp cannot be longer than the file
        end_time = len_as if len_as < timestamp['end'] else timestamp['end']
        duration = end_time - timestamp['start']
        mute = AudioSegment.silent(duration=duration)
        end = wrapper.segment[end_time:]
        wrapper.segment = (start_time + mute + end)
        wrapper.mute_next_start = \
            cls.__mute_next_chunk(wrapper, timestamp['end'])
        return wrapper

    @classmethod
    def __mute_next_chunk(cls, wrapper, end_time):
        # Store how much the next chunk should mute from its beginning
        extra_time = end_time - CHUNK_LEN
        return max(extra_time, wrapper.mute_next_start)

    @classmethod
    def __get_lyrics(cls, file_path, audio_segment):
        return Transcribe(file_path, audio_segment.frame_rate).lyrics

    @classmethod
    def __get_timestamps(cls, lyrics):
        return Timestamp(lyrics).timestamps

    @classmethod
    def __explicit_count(cls, stamp, chunk_offset):
        """ Count the number of explicits safely """
        stamp['start'] += chunk_offset
        stamp['end'] += chunk_offset
        new_stamp = True
        Censor.lock.acquire()
        for mut in Censor.muted_timestamps:
            if cls.__duplicate_stamp(mut, stamp):
                new_stamp = False
                break
        if new_stamp or not Censor.muted_timestamps:
            Censor.explicit_count += 1
            Censor.muted_timestamps.append(stamp)
        Censor.lock.release()

    @classmethod
    def __duplicate_stamp(cls, stamp1, stamp2):
        """ If 2 timestamps are the same word and start and at relatively the
            same time, then assume they're the same timestamp """
        if stamp1['word'] == stamp2['word'] and            \
          abs(stamp1['start'] - stamp2['start']) < 201 and \
          abs(stamp1['end'] - stamp2['end']) < 201:
            return True
        return False
