'''The daemon module contains all the logic required for the daemon controlling MOE to work'''
from mailer import Mailer

MAILER = Mailer(user='camilo.garcia.larotta@gmail.com', destination='camilo.garcia.larotta@gmail.com')

for message in MAILER.fetch():
    print(message)

MAILER.send_message('automated')

for message in MAILER.fetch():
    print(message)

MAILER.delete_message(1650544082422387)

for message in MAILER.fetch():
    print(message)
