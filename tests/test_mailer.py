'''Unit and Integration tests for the Mailer module'''
from moe.encoder import Encoder


WORDS = (('HELLO', '.... . ._.. ._.. ___'),
         ('NEPE', '_. . .__. .'),
         ('ILOVEYOU', '.. ._.. ___ ..._ . _.__ ___ .._'),
         ('0123THEANSWERIS42', '_____ .____ ..___ ...__ _ .... . ._ _. ... .__ . ._. .. ... ...._ ..___'))


def test_encoder():
    '''GIVEN a list of plain text words
    WHEN the words are encoded with a Morse encoder
    THEN check that the encoded string is correct'''

    morser = Encoder('examples/MORSE.csv')

    for text, expected in WORDS:
        assert expected == morser.encode(text)


def test_decoder():
    '''GIVEN a list of Morse encoded strings
    WHEN the words are decoded with a Morse encoder
    THEN check that the decoded string is correct'''

    morser = Encoder('examples/MORSE.csv')

    for expected, code in WORDS:
        expected = ' '.join(list(expected))
        assert expected == morser.decode(code)
