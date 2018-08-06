'''The echoer module contains an implementation of Writer which prints morse code to stdout'''
import sys


class Echoer():
    '''Writer that prints morse code to a given stream'''

    def __init__(self, stream=sys.stdout):
        self.stream = stream

    def write(self, morse):
        '''Write morse code to a given stream'''
        print(morse, file=self.stream)

    def set_stream(self, stream):
        '''define the stream to which to write the morse code'''
        self.stream = stream
