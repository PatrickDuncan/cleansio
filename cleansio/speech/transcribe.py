""" Convert audio to text """

from .helper import leading_zero

def transcribe(audio_file):
    """ Transcribe each slice of the audio file """
    length = len(audio_file.slices_file_paths)
    for index, file_path in enumerate(audio_file.slices_file_paths):
        transcribe_each_slice(
            file_path,
            index + 1, # Humans count starting at 1
            length,
            audio_file.encoding,
            audio_file.sample_rate)

def transcribe_each_slice(file_path, index, length, encoding, sample_rate):
    """ Accesses Google Cloud Speech and print the lyrics for each slice """
    from google.cloud import speech
    from google.cloud.speech import enums
    from google.cloud.speech import types
    client = speech.SpeechClient()

    with open(file_path, 'rb') as audio_content:
        content = audio_content.read()

    audio = types.RecognitionAudio(content=content)
    config = types.RecognitionConfig(
        encoding=enums.RecognitionConfig.AudioEncoding[encoding],
        sample_rate_hertz=sample_rate,
        language_code='en-US')

    response = client.recognize(config, audio)
    print_transcription(response, index, length)

def print_transcription(response, index, length):
    """ Prints the transcription as x/N: -Lyrics- """
    if not response.results:
        return
    result = response.results[0].alternatives[0].transcript
    print(leading_zero(index) + '/' + leading_zero(length) + ': ' + result)
