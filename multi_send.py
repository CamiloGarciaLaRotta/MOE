import moe.config as cfg

from moe.writer.echoer import Echoer
from moe.mailer.gmailer import Gmailer
from moe.encoder import Encoder


def main():
    '''
    1. email and echo encoded msg
    2. delete MOE emails
    3. email and echo picture
    '''
    morser = Encoder('examples/MORSE.csv')

    mailer = Gmailer(user=cfg.MAILER_USER,
                     destination=cfg.MAILER_DESTINATION)

    # encoded_phrase = morser.encode(phrase)
    # decoded_phrase = morser.decode(encoded_phrase)

    for i in ['ONE', 'TWO', 'THREE']:
        print('sending text')
        msg = morser.encode(f'MSG {i}')
        mailer.write(msg)

    img_data = open('examples/picture.jpg', 'rb').read()
    print('sending img')
    mailer.write_img(img_data)


if __name__ == '__main__':
    main()
