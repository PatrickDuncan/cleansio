""" Convert audio to text using Google Cloud Speech """

from google.cloud.speech import enums, SpeechClient, types

class Transcribe():
    """ Transcribes the lyrics from the vocals """
    def __init__(self, file_path, frame_rate, encoding='LINEAR16'):
        super().__init__()
        self.file_path = file_path
        self.lyrics = self.__transcribe_chunk(encoding, frame_rate)

    def __transcribe_chunk(self, frame_rate, encoding):
        """ Accesses Google Cloud Speech and print the lyrics for each chunk """
        with open(self.file_path, 'rb') as audio_content:
            content = audio_content.read()
        config = self.__get_config(encoding, frame_rate)
        audio = types.RecognitionAudio(content=content)
        return SpeechClient().recognize(config, audio)

    @classmethod
    def __get_config(cls, frame_rate, encoding):
        params = {
            'encoding': enums.RecognitionConfig.AudioEncoding[encoding],
            'sample_rate_hertz': frame_rate,
            'language_code': 'en-US',
            'enable_word_time_offsets': True,
            'profanity_filter': False
        }
        return types.RecognitionConfig(**params)
