from moe.writer.echoer import Echoer
from moe.mailer.gmailer import Gmailer
from moe.encoder import Encoder


def main():
    '''
    1. email and echo encoded msg
    2. email (end echo?) picture
    '''
    morser = Encoder('examples/MORSE.csv')

    echoer = Echoer()
    mailer = Gmailer(user='camilo.garcia.larotta@gmail.com',
                     destination='camilo.garcia.larotta@gmail.com')

    phrase = 'NEPE'
    encoded_phrase = morser.encode(phrase)
    decoded_phrase = morser.decode(encoded_phrase)
    msg = f'message: {phrase}\nencoded: {encoded_phrase}\ndecoded: {decoded_phrase}'

    mailer.write(msg)
    echoer.write(msg)

    mailer.delete_all()

    img_data = open('examples/picture.jpg', 'rb').read()
    mailer.write_img(img_data)
    echoer.write_img(img_data)


if __name__ == '__main__':
    main()
