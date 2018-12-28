# pylint: skip-file

# Word lists: https://github.com/nathanmerrill/wordsbysyllables

import os
from utils import num_syllables

def get_words_file(num):
    curr_dir = os.path.dirname(__file__)
    path = os.path.join(curr_dir, '../data/{0}-syllable-words.txt').format(num)
    with open(path, mode='r') as file:
        return file.readlines()

def validate_syllables(syllables):
    correct = 0
    words = get_words_file(syllables)
    for word in words:
        if abs(num_syllables(word) - syllables) < 2: # 1 off is accurate enough
            correct += 1
    assert correct/len(words) > .90 # 90% is good enough

def test_num_syllables_empty():
    assert num_syllables('') == 0

def test_1_syallable():
    validate_syllables(1)

def test_2_syallables():
    validate_syllables(2)

def test_3_syallables():
    validate_syllables(3)

def test_4_syallables():
    validate_syllables(4)

def test_5_syallables():
    validate_syllables(5)

def test_6_syallables():
    validate_syllables(6)

def test_7_syallables():
    validate_syllables(7)
