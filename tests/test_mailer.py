'''Unit and Integration tests for the Mailer module'''
import unittest
from moe import mailer

# TODO: don't test private methods. Learn how to Mock API tests


class TestMailer(unittest.TestCase):
    '''Unit tests for the Mailer module'''

    emails = (('', False),
              ('@', False),
              ('foo@.com', False),
              ('@foo.com', False),
              ('foo@bar.co', True))

    def test_valid_email(self):
        '''verify that the input emails are correctly identified as valid/invalid'''
        for email, expected in self.emails:
            self.assertEqual(expected, mailer._valid_email(email))


if __name__ == '__main__':
    unittest.main()
