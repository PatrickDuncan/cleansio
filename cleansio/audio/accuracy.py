""" Functions which preprocess an audio chunk to improve the accuracy of speech
    recognition. """

def __maximize_volume(chunk):
    return chunk - chunk.max_dBFS

def improve_accuracy(chunk):
    """ Filter chunk through various functions to improve speech recognition """
    return __maximize_volume(chunk)
