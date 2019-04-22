""" Creates a clean version of a file by removing explicits """

from itertools import repeat
from multiprocessing.dummy import Pool as ThreadPool
from pathlib import Path
from colorama import Fore, Style
from tqdm import tqdm
from pydub import AudioSegment
from audio import AudioFile
from .censor import Censor

class CensorFile(Censor):
    """ Removes explicits from a file """
    def __init__(self, args, explicits):
        super().__init__(explicits)
        self.file_path = args.file_path
        self.encoding = self.__encoding(args.output_encoding)
        self.location = self.__location(args.output_location)

    def censor(self):
        """ Creates a clean/new version of a file by removing explicits """
        audio_file = AudioFile(self.file_path)
        # Define the CLI progress bar
        p_bar, p_bar_step = self.__progress_bar(audio_file.normal_chunks)
        async_iter = zip(
            repeat(p_bar),
            repeat(p_bar_step),
            audio_file.normal_chunks)
        # Censor each audio chunk file asynchronously
        censored_chunks = ThreadPool(6).map(self.__censor_chunk, async_iter)
        clean_file = self.__create_clean_segment(censored_chunks)
        p_bar.close()
        self.__create_clean_file(clean_file)

    def __censor_chunk(self, async_iter):
        """ Censors a chunk and updates the progress bar """
        p_bar, p_bar_step, chunk_file_path = async_iter
        p_bar.update(p_bar_step)
        return self.censor_audio_chunk(chunk_file_path)

    def __create_clean_file(self, clean_file):
        exp = 'explicit' if Censor.explicit_count == 1 else 'explicits'
        print('Cleansio found {1}{2}{0}{3} {4}!'.format(
            Censor.explicit_count, Style.BRIGHT, Fore.GREEN, Fore.RESET, exp))
        clean_file.export(self.location, format=self.encoding)
        print(Fore.CYAN + 'Successfully created clean file, it\'s located at:')
        print(Fore.YELLOW + self.location)

    def __location(self, location):
        if location:
            return location[0]
        current_dir = str(Path(__file__).parents[2])
        return current_dir + '/clean_file.' + self.encoding

    @classmethod
    def __create_clean_segment(cls, censored_chunks):
        clean_file = AudioSegment.empty()
        s_mute = 0
        for wrapper in censored_chunks: # Join the chunks together
            # Mute the start of a chunk based on the previous chunk
            clean_file += \
                AudioSegment.silent(duration=s_mute) + wrapper.segment[s_mute:]
            s_mute = wrapper.mute_next_start
        return clean_file

    @classmethod
    def __progress_bar(cls, normal_chunks):
        progress_bar_total = 100
        progress_bar = tqdm(
            # Remove the detailed percentage stats
            bar_format=Style.BRIGHT + Fore.GREEN + '{l_bar}{bar}' + Fore.RESET,
            desc='Censoring file', # Description
            leave=False,           # Remove bar after completion
            ncols=42,              # Set width
            total=progress_bar_total)
        progress_bar_step = (1 / len(normal_chunks)) * progress_bar_total
        return progress_bar, progress_bar_step

    @classmethod
    def __encoding(cls, encoding):
        return encoding[0] if encoding else 'wav'
