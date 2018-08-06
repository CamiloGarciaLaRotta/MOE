'''The daemon module contains all the logic required for the encoding/decoding of morse code'''
import csv


class Encoder():
    '''Encodes and decodes text from a given dictionnary passed through CSV.
    Args:
        file: the csv file containing the encoding: LETTER, CODE.
              It can have an entry for default space called SPACE.
              It can have an entry for default non supported values called DEFAULT.
        default_space: if no default space is present in the CSV file, it can be passed here.
        default_value: if no default value is present in the CSV file, it can be passed here.

    Returns:
        The number of lines read.'''

    def __init__(self, file, default_space=' ', default_value='X'):
        self.dictionnary, self.reverse_dictonnary = {}, {}
        with open(file, mode='r') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            line_count = 0
            for row in csv_reader:
                if line_count == 0:
                    line_count += 1
                    continue

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

    def encode(self, text):
        '''Encode a given text in morse code.

            Args:
                text: The text to be encoded.

            Returns:
                The string containing the equivalent morse code.
            '''

        coded_text = []
        for letter in text:
            if letter.isspace():
                coded_text.append(self.dictionnary['SPACE'])
            elif letter in self.dictionnary.keys():
                coded_text.append(self.dictionnary[letter])
            else:
                coded_text.append(self.dictionnary['DEFAULT'])

        return ''.join(coded_text)

    def decode(self, morse):
        '''Decode a given morse code.

            Args:
                morse: The string morse code to be decoded.

            Returns:
                The string containing the equivalent text.
            '''

        decoded_text = []
        for letter in morse:
            if letter.isspace():
                decoded_text.append(self.reverse_dictonnary['SPACE'])
            elif letter in self.reverse_dictonnary.keys():
                decoded_text.append(self.reverse_dictonnary[letter])
            else:
                decoded_text.append(self.reverse_dictonnary['DEFAULT'])

        return ''.join(decoded_text)
