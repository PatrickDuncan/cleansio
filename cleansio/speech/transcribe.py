""" Convert audio to text """

def transcribe(audio_file):
    """ Transcribe each slice of the audio file """
    for audio_file_path in audio_file.slices_file_paths:
        transcribe_each_slice(audio_file_path, audio_file.encoding, audio_file.sample_rate)

def transcribe_each_slice(slice_file_path, audio_encoding, audio_sample_rate):
    """ Accesses Google Cloud Speech and print the lyrics for each slice """
    from google.cloud import speech
    from google.cloud.speech import enums
    from google.cloud.speech import types
    client = speech.SpeechClient()

    with open(slice_file_path, 'rb') as audio_content:
        content = audio_content.read()

    audio = types.RecognitionAudio(content=content)
    config = types.RecognitionConfig(
        encoding=enums.RecognitionConfig.AudioEncoding[audio_encoding],
        sample_rate_hertz=audio_sample_rate,
        language_code='en-US')

    response = client.recognize(config, audio)
    for result in response.results:
        print(result)
