'''The echoer module contains an implementation of Writer which prints morse code to stdout.'''
import sys


class Echoer():
    '''Writer that prints morse code to a given stream.

    Args:
        stream (object, optional): Defaults to sys.stdout. Stream to which to write.'''

    def __init__(self, stream: object = sys.stdout) -> None:
        self.stream = stream

    def set_stream(self, stream: object) -> None:
        '''Define the stream to which to write the morse code.

        Args:
            stream (object): Stream to which to write to.'''

        self.stream = stream

    def write(self, morse: str) -> None:
        '''Write morse code to a given stream

        Args:
            morse (str): morse code to write.'''

        print(morse, file=self.stream)
