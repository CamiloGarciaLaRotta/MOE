'''The daemon module contains all the logic required for the encoding/decoding of any cypher code.'''
import csv


class Encoder(object):
    '''Encodes and decodes text from a given dictionnary passed through CSV.

    Args:
        file (str): The csv file containing the encoding: LETTER, CODE.
            It can have an entry for default space called SPACE.
            It can have an entry for default non supported values called DEFAULT.
        default_space (str, optional): Defaults to ' '. If no default space is present in the CSV file, it can be passed here.
        default_value (str, optional): Defaults to 'X'. If no default value is present in the CSV file, it can be passed here.'''

    def __init__(self, file: str, default_space: str = ' ', default_value: str = 'X') -> None:

        self.dictionnary, self.reverse_dictonnary = {}, {}
        with open(file, mode='r') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            line_count = 0
            for row in csv_reader:
                print(row)
                self.dictionnary[row['LETTER']] = row['CODE']
                self.reverse_dictonnary[row['CODE']] = row['LETTER']
                line_count += 1
            print(f'Processed {line_count} lines.')

        if 'SPACE' not in self.dictionnary.keys():
            self.dictionnary['SPACE'] = default_space
            self.reverse_dictonnary['SPACE'] = default_space

        if 'DEFAULT' not in self.dictionnary.keys():
            self.dictionnary['DEFAULT'] = default_value
            self.reverse_dictonnary['DEFAULT'] = default_value

    def encode(self, text: str) -> str:
        '''Encode a given text in morse code.

        Args:
            text (str): The text to be encoded.

        Returns:
            str: The string containing the equivalent morse code.'''

        coded_text = []
        for letter in text:
            if letter.isspace():
                coded_text.append(self.dictionnary['SPACE'])
            elif letter in self.dictionnary.keys():
                coded_text.append(self.dictionnary[letter])
            else:
                coded_text.append(self.dictionnary['DEFAULT'])

            coded_text.append(self.dictionnary['SPACE'])

        return ''.join(coded_text).strip()

    def decode(self, morse: str) -> str:
        '''Decode a given morse code.

        Args:
            morse (str): The string morse code to be decoded.

        Returns:
            str: The string containing the equivalent text.'''

        decoded_text = []
        for code in morse.strip().split(self.dictionnary['SPACE']):
            if code.isspace():
                decoded_text.append(self.reverse_dictonnary['SPACE'])
            elif code in self.reverse_dictonnary.keys():
                decoded_text.append(self.reverse_dictonnary[code])
            else:
                decoded_text.append(self.reverse_dictonnary['DEFAULT'])

            decoded_text.append(self.dictionnary['SPACE'])

        return ''.join(decoded_text).strip()
