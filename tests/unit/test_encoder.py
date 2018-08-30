'''Unit tests for the Encoder'''
import pytest

from moe.encoder import Encoder


WORDS = (('HELLO', '....¶.¶._..¶._..¶___'),
         ('S P A C E', '...¶ ¶.__.¶ ¶._¶ ¶_._.¶ ¶.'),
         ('NEPE', '_.¶.¶.__.¶.'),
         ('0123THEANSWERIS42', '_____¶.____¶..___¶...__¶_¶....¶.¶._¶_.¶...¶.__¶.¶._.¶..¶...¶...._¶..___'))


@pytest.fixture()
def morser():
    '''returns an Encoder with the Morse dictionnary'''

    return Encoder('examples/MORSE.csv')


def test_encoder(morser):
    '''GIVEN a list of plain text words
    WHEN the words are encoded with a Morse encoder
    THEN check that the encoded string is correct'''

    for text, expected in WORDS:
        assert expected == morser.encode(text)


def test_decoder(morser):
    '''GIVEN a list of Morse encoded strings
    WHEN the words are decoded with a Morse encoder
    THEN check that the decoded string is correct'''

    for expected, code in WORDS:
        assert expected == morser.decode(code)


def test_default_character(morser):
    '''GIVEN a word containing unsupported characters
    WHEN the word is encoded/decoded
    THEN it will be filled with the default character ⁜'''

    original, encoded, decoded = 'I ℇ⇋⊙⛄ YOU', '..¶ ¶⁜¶⁜¶⁜¶⁜¶ ¶_.__¶___¶.._', 'I ⁜⁜⁜⁜ YOU'

    actual_encoded = morser.encode(original)
    assert encoded == actual_encoded
    assert decoded == morser.decode(actual_encoded)
