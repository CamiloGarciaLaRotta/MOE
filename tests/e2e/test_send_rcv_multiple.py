'''e2e test of a gmailer + echoer UC'''
from moe.mailer.gmailer import Gmailer
from moe.encoder import Encoder


# TODO rename to test_...
def e2e():
    '''Messages will be sent/read through s'''
    mailer = Gmailer(user='camilo.garcia.larotta@gmail.com',
                     destination='camilo.garcia.larotta@gmail.com',
                     secret="path/to/client_secret.json")

    morser = Encoder('examples/MORSE.csv')

    # no unread emails
    assert mailer.read() == {}

    # send 2 new emails
    mailer.write(morser.encode('A1'))
    mailer.write(morser.encode('B2'))

    # fetch all unread MOE emails
    unread_msgs = mailer.fetch_unread()
    assert len(unread_msgs) == 2

    encoded_content = [msg['content'] for msg in unread_msgs]
    decoded_content = [morser.decode(content) for content in encoded_content]

    assert 'A 1' in decoded_content
    assert 'B 2' in decoded_content
