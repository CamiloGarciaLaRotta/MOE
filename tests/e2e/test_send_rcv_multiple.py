'''e2e test of a gmailer + echoer UC'''
import moe.config as cfg

from moe.mailer.gmailer import Gmailer
from moe.encoder import Encoder


# TODO rename to test_...
def e2e():
    '''Messages will be sent/read through s'''
    mailer = Gmailer(user=cfg.MAILER_USER,
                     destination=cfg.MAILER_DESTINATION)

    morser = Encoder('examples/MORSE.csv')

    # no unread emails
    assert mailer.read() == {}

    # send 2 new emails
    mailer.write(morser.encode('A1'))
    mailer.write(morser.encode('B2'))

    # fetch all unread MOE emails
    unread_msgs = mailer.fetch_unread()
    assert len(unread_msgs) == 2

    encoded_content = [msg['txt'] for msg in unread_msgs]
    decoded_content = [morser.decode(content) for content in encoded_content]

    assert 'A1' in decoded_content
    assert 'B2' in decoded_content
