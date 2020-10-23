'''The daemon module contains all the logic required for the encoding/decoding of any cypher code.'''
import csv


class Encoder():
    '''Encodes and decodes text from a given dictionnary passed through CSV.

    Args:
        file (str): The csv file containing the encoding: LETTER, CODE.
            It can have an entry for default space called SPACE. i.e. the characte to separate encoded words
            It can have an entry for default separator called SEPARATOR. i.e. the character to separate encoded letters
            It can have an entry for default non supported values called DEFAULT.
        default_space (str, optional): Defaults to ' '. If no default space is present in the CSV file, it can be passed here.
        default_separator (str, optional): Defaults to '¶'. If no default space is present in the CSV file, it can be passed here.
        default_value (str, optional): Defaults to '⁜'. If no default value is present in the CSV file, it can be passed here.'''

    def __init__(self, file: str, default_space: str = ' ', default_separator: str = '¶', default_value: str = '⁜') -> None:

        self.dictionnary, self.reverse_dictonnary = {}, {}
        with open(file, mode='r') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            line_count = 0
            for row in csv_reader:
                self.dictionnary[row['LETTER']] = row['CODE']
                self.reverse_dictonnary[row['CODE']] = row['LETTER']
                line_count += 1
            # print(f'Encoder: Processed {line_count} lines.') # TODO good debugging stu

        if 'SEPARATOR' not in self.dictionnary.keys():
            self.dictionnary['SEPARATOR'] = default_separator

        if 'SPACE' not in self.dictionnary.keys():
            self.dictionnary['SPACE'] = default_space

        if 'DEFAULT' not in self.dictionnary.keys():
            self.dictionnary['DEFAULT'] = default_value
            self.reverse_dictonnary['DEFAULT'] = default_value

    def encode(self, text: str) -> str:
        '''Encode a given text with the configured dictionnary.

        Args:
            text (str): The text to be encoded.

        Returns:
            str: The encoded string.'''

        coded_text = []
        for letter in text:
            if letter.isspace():
                coded_text.append(self.dictionnary['SPACE'])
            elif letter in self.dictionnary.keys():
                coded_text.append(self.dictionnary[letter])
            else:
                coded_text.append(self.dictionnary['DEFAULT'])

            coded_text.append(self.dictionnary['SEPARATOR'])

        return ''.join(coded_text).rstrip(self.dictionnary['SEPARATOR'])

    def decode(self, coded_string: str) -> str:
        '''Decode a given coded string.

        Args:
            coded_string (str): The string to be decoded.

        Returns:
            str: The string containing the equivalent text.'''

        decoded_text = []
        for code in coded_string.rstrip().split(self.dictionnary['SEPARATOR']):
            if code == self.dictionnary['SPACE']:
                decoded_text.append(' ')
            elif code in self.reverse_dictonnary.keys():
                decoded_text.append(self.reverse_dictonnary[code])
            else:
                decoded_text.append(self.reverse_dictonnary['DEFAULT'])

        return ''.join(decoded_text).rstrip()
