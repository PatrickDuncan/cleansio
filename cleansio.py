"""Displays the lyrics of an audio file"""

import sys

def transcribe_file(speech_file):
    """Accesses Google Cloud Speech and print the lyrics"""
    from google.cloud import speech
    from google.cloud.speech import enums
    from google.cloud.speech import types
    client = speech.SpeechClient()

    with open(speech_file, 'rb') as audio_file:
        content = audio_file.read()

    audio = types.RecognitionAudio(content=content)
    config = types.RecognitionConfig(
        encoding=enums.RecognitionConfig.AudioEncoding.FLAC,
        sample_rate_hertz=44100,
        language_code='en-US')

    response = client.recognize(config, audio)
    for result in response.results:
        print(result)

def valid_input():
    """Validates the user's input"""
    return sys.argv[1].lower()[-5:] == '.flac'

if __name__ == '__main__':
    if valid_input():
        transcribe_file(sys.argv[1])
    else:
        print("Please see the README.")
