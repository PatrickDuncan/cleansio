""" Convert audio to text """

def transcribe(audio_file):
    """ Accesses Google Cloud Speech and print the lyrics """
    from google.cloud import speech
    from google.cloud.speech import enums
    from google.cloud.speech import types
    client = speech.SpeechClient()

    with open(audio_file.file_path, 'rb') as audio_content:
        content = audio_content.read()

    audio = types.RecognitionAudio(content=content)
    config = types.RecognitionConfig(
        encoding=enums.RecognitionConfig.AudioEncoding.FLAC,
        sample_rate_hertz=44100,
        language_code='en-US')

    response = client.recognize(config, audio)
    for result in response.results:
        print(result)
