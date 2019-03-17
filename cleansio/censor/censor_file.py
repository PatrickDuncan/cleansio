""" Creates a clean version of a file by removing explicits """

from itertools import repeat
from multiprocessing.dummy import Pool as ThreadPool
from tqdm import tqdm
from pydub import AudioSegment
from audio import AudioFile
from .censor import Censor

class CensorFile(Censor):
    """ Removes explicits from a file """
    def __init__(self, args, explicits):
        super().__init__(explicits, args.output_encoding, args.output_location)
        self.file_path = args.file_path

    def censor(self):
        """ Creates a clean/new version of a file by removing explicits """
        clean_file = AudioSegment.empty()
        audio_file = AudioFile(self.file_path)
        # Define the CLI progress bar
        p_bar, p_bar_step = self.__progress_bar(audio_file.normal_chunks)
        async_iter = zip(
            repeat(p_bar),
            repeat(p_bar_step),
            audio_file.normal_chunks)
        # Censor each audio chunk file asynchronously
        censored_chunks = ThreadPool(6).map(self.__censor_chunk, async_iter)
        for chunk in censored_chunks: # Join the chunks together
            clean_file += chunk
        p_bar.close()
        self.create_clean_file(clean_file)

    def __censor_chunk(self, async_iter):
        """ Censors a chunk and updates the progress bar """
        p_bar, p_bar_step, chunk_file_path = async_iter
        p_bar.update(p_bar_step)
        return self.censor_audio_chunk(chunk_file_path)

    @classmethod
    def __progress_bar(cls, normal_chunks):
        progress_bar_total = 100
        progress_bar = tqdm(
            bar_format='{l_bar}{bar}', # Remove the detailed percentage stats
            desc='Censoring file',     # Description
            leave=False,               # Remove bar after completion
            ncols=40,                  # Set width
            total=progress_bar_total)
        progress_bar_step = (1 / len(normal_chunks)) * progress_bar_total
        return progress_bar, progress_bar_step
