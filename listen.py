import json
from time import sleep

import moe.config as cfg

from moe.writer.echoer import Echoer
from moe.mailer.gmailer import Gmailer
from moe.encoder import Encoder
from moe.mailer.gmailer import TEXT_SUBJECT
from moe.mailer.gmailer import IMG_SUBJECT


def main():
    '''
    check every n seconds if there is new mail.
    '''
    morser = Encoder('examples/MORSE.csv')

    echoer = Echoer()
    mailer = Gmailer(user=cfg.MAILER_USER,
                     destination=cfg.MAILER_DESTINATION)

    while True:
        unread = mailer.fetch_unread()
        if unread:
            for msg in unread:
                subject = msg['subject']
                if subject == TEXT_SUBJECT:
                    echoer.write(msg['txt'])
                elif subject == IMG_SUBJECT:
                    echoer.write_img(msg['img'])

                mailer.mark_as_read(msg)

        print('sleeping')
        sleep(10)


if __name__ == '__main__':
    main()
