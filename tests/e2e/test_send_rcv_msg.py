'''e2e test of a gmailer + echoer UC'''
from moe.mailer.gmailer import Gmailer
from moe.encoder import Encoder


# TODO rename to test_...
def e2e():
    '''Messages will be sent/read through s'''
    mailer = Gmailer(user='camilo.garcia.larotta@gmail.com',
                     destination='camilo.garcia.larotta@gmail.com',
                     secret="path/to/client_secret.json")

    # no unread emails
    assert mailer.read() == {}

    # send new email
    morser = Encoder('examples/MORSE.csv')
    encoded_content = morser.encode('ONCE MORE INTO THE FRAY')
    mailer.write(encoded_content)

    # read new unread email
    encoded_msg = mailer.read()
    decoded_content = morser.decode(encoded_msg['content'])
    assert decoded_content == "ONCE MORE INTO THE FRAY"

    # Because read() marks email as read, calling read() again will return nothing')
    assert mailer.read() == {}
