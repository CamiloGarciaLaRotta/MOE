'''The daemon module contains all the logic required for the daemon controlling MOE to work'''

import json
from time import sleep

import config as cfg

from writer.echoer import Echoer
from mailer.gmailer import Gmailer
from encoder import Encoder
from mailer.gmailer import TEXT_SUBJECT
from mailer.gmailer import IMG_SUBJECT

SLEEP = 10


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
        sleep(SLEEP)


if __name__ == '__main__':
    main()
