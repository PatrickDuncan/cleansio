"""
    Loads a list of words from a file.
    It is assumed that the words are separated by the given separator.
"""

class FileLoader():
    """
        Loads a list of words from a file.
        It is assumed that the words are separated by the given separator.
    """
    def __init__(self, filename, sep='\n'):
        # Create the set which stores words
        self.set = {}
        with open(filename, 'r') as uel:
            # Assume that the words are separated by sep and split the file into a set
            self.set = set(uel.read().split(sep))
