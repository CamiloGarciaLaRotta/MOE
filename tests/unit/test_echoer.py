'''Unit tests for the Echoer Writer'''
import sys

from moe.writer.echoer import Echoer

# Note we unfortunately can't use Pytest's fixtures
# because Echoer sets up its reference to stdout before
# pytest can change it by the capturng file descriptor
# https://github.com/pytest-dev/pytest/issues/1132#issuecomment-147524722


def test_sdtout(capsys):
    '''GIVEN a list of strings
    WHEN the strings are written through Echoer to stdout
    THEN check that stdout emits the same strings'''

    echoer = Echoer()
    # must explicitly set the stream so that Pytest captures output
    echoer.set_stream(stream=sys.stdout)

    echoer.write("hello\n")
    out, err = capsys.readouterr()
    assert out == "hello\n"
    assert err == ""


def test_sderr(capsys):
    '''GIVEN a list of strings
    WHEN the strings are written through Echoer to stderr
    THEN check that stderr emits the same strings'''

    echoer = Echoer()
    # must explicitly set the stream so that Pytest captures output
    echoer.set_stream(stream=sys.stderr)

    echoer.write("hello\n")
    out, err = capsys.readouterr()
    assert out == ""
    assert err == "hello\n"
