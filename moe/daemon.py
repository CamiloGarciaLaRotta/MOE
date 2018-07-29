'''The daemon module contains all the logic required for the daemon controlling MOE to work'''
from mailer import Mailer

MAILER = Mailer(user='camilo.garcia.larotta@gmail.com', destination='toto@toto.com')
for message in MAILER.fetch():
    print(message)

# TODO add editorconfigs
