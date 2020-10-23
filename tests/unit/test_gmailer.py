'''Unit tests for the Gmailer Mailer'''
import pytest

from moe.mailer.gmailer import Gmailer


def test_bad_email():
    '''GIVEN a list of bad emails
    WHEN trying to instantiate a Gmailer
    THEN check that the correct Exception is raised'''

    with pytest.raises(ValueError):
        Gmailer(user='@.com', destination='dummy@dummy.com')

    with pytest.raises(ValueError):
        Gmailer(user='dummy@dummy.com', destination='dummy@')
