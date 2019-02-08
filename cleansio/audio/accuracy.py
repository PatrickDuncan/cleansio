""" Functions which preprocess an audio chunk to improve the accuracy of speech
    recognition. """

def __maximize_volume(chunk):
    """ Increase chunk's volume up to the point before clipping """
    return chunk - chunk.max_dBFS

def __isolate_vocals(chunk):
    return chunk

def improve_accuracy(chunk):
    """ Filter chunk through various functions to improve speech recognition """
    return __maximize_volume(chunk)
