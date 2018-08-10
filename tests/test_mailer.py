'''Unit and Integration tests for the Mailer module'''
import unittest
from moe.encoder import Encoder

# TODO add tests for Mailer, also rename to Gmailer <<Mailer>>


class TestMailer(unittest.TestCase):
    '''Unit tests for the Mailer module'''

    words = (('HELLO', '.... . ._.. ._.. ___'),
             ('NEPE', '_. . .__. .'),
             ('ILOVEYOU', '.. ._.. ___ ..._ . _.__ ___ .._'),
             ('0123THEANSWERIS42', '_____ .____ ..___ ...__ _ .... . ._ _. ... .__ . ._. .. ... ...._ ..___'))

    def test_encoder(self):
        '''verify that the text encodes into the correct Morse code'''
        morser = Encoder('examples/MORSE.csv')

        for text, expected in self.words:
            self.assertEqual(expected, morser.encode(text))

    def test_decoder(self):
        '''verify that the Morse code decodes into the text'''
        morser = Encoder('examples/MORSE.csv')

        for expected, code in self.words:
            expected = ' '.join(list(expected))
            self.assertEqual(expected, morser.decode(code))


if __name__ == '__main__':
    unittest.main()
