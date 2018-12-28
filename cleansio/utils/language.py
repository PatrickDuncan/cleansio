""" Utillity functions for language related work """

import re

def num_syllables(word):
    """ Counts the number of syllables in a word """
    # https://codegolf.stackexchange.com/a/47325
    return len(re.findall(r'[aiouy]+e*|e(?!d$|ly).|[td]ed|le$', word))
