import configparser

_config = configparser.ConfigParser()
_config.read_file(open('moe.ini'))
MAILER_USER = _config['mailer']['user']
MAILER_DESTINATION = _config['mailer']['destination']
