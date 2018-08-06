'''The daemon module contains all the logic required for the daemon controlling MOE to work'''
from mailer import Mailer
from echoer import Echoer

# TODO periodically delete emails from MOE so that query times remain small

MAILER = Mailer(user='camilo.garcia.larotta@gmail.com', destination='camilo.garcia.larotta@gmail.com')

# print('no unread emails')
# print(MAILER.read())

# print('send new email')
# MAILER.write('tis some lit morse')

# print('read new unread email')
# print(MAILER.read())

# print('Because read() marks email as read, calling read() again will return nothing')
# print(MAILER.read())

# print('send 2 new emails')
# MAILER.write('A')
# MAILER.write('B')

# print('see all unread MOE emails')
# print(MAILER.fetch_unread())

# print('see all MOE emails')
# print(MAILER.fetch())

# print('Showcasing a Writer: Echoer')
# ECHOER = Echoer()
# MAILER.write('testing echoer')
# ECHOER.write(MAILER.read()['content'])
