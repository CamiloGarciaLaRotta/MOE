'''The daemon module contains all the logic required for the daemon controlling MOE to work'''

from time import sleep
import signal
import os
import sys

import config as cfg

from encoder import Encoder
from writer.echoer import Echoer
from mailer.gmailer import Gmailer
from mailer.gmailer import TEXT_SUBJECT
from mailer.gmailer import IMG_SUBJECT

import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(16, GPIO.OUT)

def terminateProcess(signalNumber, frame):
    print(f'(SIGNAL {signalNumber}) terminating the process')
    sys.exit()


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
                    txt = msg['txt']
                    decoded_txt = morser.decode(txt)
                    echoer.write(txt)
                    echoer.write(decoded_txt)
                    os.system(f'echo -e "original:\\n{txt}\\ndecoded:\\n{decoded_txt}" | lp')
                elif subject == IMG_SUBJECT:
                    img = msg['img']
                    echoer.write_img(img)

                    os.system(f'echo {img} | lp')

                mailer.mark_as_read(msg)

        print('sleeping')
        GPIO.output(16, GPIO.HIGH)
        sleep(cfg.DAEMON_SLEEP)
        GPIO.output(16, GPIO.LOW)
        sleep(cfg.DAEMON_SLEEP)


if __name__ == '__main__':
    print('PID:', os.getpid())

    # register the signals to be caught
    signal.signal(signal.SIGTERM, terminateProcess)
    signal.signal(signal.SIGINT, terminateProcess)
    signal.signal(signal.SIGQUIT, terminateProcess)

    main()
