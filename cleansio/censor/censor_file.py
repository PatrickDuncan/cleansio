""" Creates a clean version of a file by removing explicits """

from itertools import repeat
from multiprocessing.dummy import Pool as ThreadPool
from pathlib import Path
from colorama import Fore
from tqdm import tqdm
from pydub import AudioSegment
from audio import AudioFile
from .censor import Censor

class CensorFile(Censor):
    """ Removes explicits from a file """
    def __init__(self, file_path, explicits):
        super().__init__(explicits)
        self.file_path = file_path

    def censor(self):
        """ Creates a clean/new version of a file by removing explicits """
        clean_file = AudioSegment.empty()
        audio_file = AudioFile(self.file_path)
        # Define the CLI progress bar
        p_bar, p_bar_step = self.__progress_bar(audio_file.chunks_file_paths)
        async_iter = zip(
            repeat(p_bar),
            repeat(p_bar_step),
            audio_file.chunks_file_paths)
        # Censor each audio chunk file asynchronously
        censored_chunks = ThreadPool(8).map(self.__censor_chunk, async_iter)
        for chunk in censored_chunks: # Join the chunks together
            clean_file += chunk
        p_bar.close()
        self.__create_clean_file(clean_file)

    def __censor_chunk(self, async_iter):
        """ Censors a chunk and updates the progress bar """
        p_bar, p_bar_step, chunk_file_paths = async_iter
        p_bar.update(p_bar_step)
        return self.censor_audio_chunk(chunk_file_paths)

    @classmethod
    def __create_clean_file(cls, clean_file, encoding='wav'):
        current_dir = str(Path(__file__).parents[2])
        clean_file_path = current_dir + '/clean_file.' + encoding
        clean_file.export(clean_file_path, format=encoding)
        print(Fore.CYAN + 'Successfully created clean file, it\'s located at:')
        print(Fore.YELLOW + clean_file_path)

    @classmethod
    def __progress_bar(cls, chunks_file_paths):
        progress_bar_total = 100
        progress_bar = tqdm(
            bar_format='{l_bar}{bar}', # Remove the detailed percentage stats
            desc='Censoring file',     # Description
            leave=False,               # Remove bar after completion
            ncols=40,                  # Set width
            total=progress_bar_total)
        progress_bar_step = (1 / len(chunks_file_paths)) * progress_bar_total
        return progress_bar, progress_bar_step
