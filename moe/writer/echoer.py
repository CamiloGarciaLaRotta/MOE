'''The echoer module contains an implementation of Writer which prints strings to stdout.'''
import sys

from imgcat import imgcat


class Echoer():
    '''Writer that prints strings to a given stream.

    Args:
        stream (object, optional): Defaults to sys.stdout. Stream to which to write.'''

    def __init__(self, stream: object = sys.stdout) -> None:
        self.stream = stream

    def set_stream(self, stream: object) -> object:
        '''Define the stream to which to write the strings.

        Args:
            stream (object): Stream to which to write to.

        Returns:
            object: The Echoer instance'''

        self.stream = stream

        return self

    def write(self, string: str) -> None:
        '''Write the string to a given stream

        Args:
            string (str): string to write.'''

        self.stream.write(f'{string}\n')
        self.stream.flush()

    def write_img(self, img: bytes) -> None:
        '''Write the image to a given stream

        Args:
            img (bytes): the image to write.'''

        imgcat(img)
