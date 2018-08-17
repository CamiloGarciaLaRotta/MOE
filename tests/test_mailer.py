'''Unit and Integration tests for the Mailer module'''
from moe.encoder import Encoder


WORDS = (('HELLO', '.... . ._.. ._.. ___'),
         ('NEPE', '_. . .__. .'),
         ('ILOVEYOU', '.. ._.. ___ ..._ . _.__ ___ .._'),
         ('0123THEANSWERIS42', '_____ .____ ..___ ...__ _ .... . ._ _. ... .__ . ._. .. ... ...._ ..___'))


def test_encoder():
    '''verify that the text encodes into the correct Morse code'''
    morser = Encoder('examples/MORSE.csv')

    for text, expected in WORDS:
        assert expected == morser.encode(text)


def test_decoder():
    '''verify that the Morse code decodes into the text'''
    morser = Encoder('examples/MORSE.csv')

    for expected, code in WORDS:
        expected = ' '.join(list(expected))
        assert expected == morser.decode(code)
