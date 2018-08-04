'''The mailer module contains all the logic required for mailer class to work'''
import base64
import re

from email.mime.text import MIMEText
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError as HttpAPIError
from httplib2 import Http
from oauth2client import file, client, tools

_API = 'gmail'
_VERSION = 'v1'
_SCOPES = 'https://mail.google.com/' + \
        'https://www.googleapis.com/auth/gmail.compose ' + \
        'https://www.googleapis.com/auth/gmail.send ' + \
        'https://www.googleapis.com/auth/gmail.labels ' + \
        'https://www.googleapis.com/auth/gmail.modify ' + \
        'https://www.googleapis.com/auth/gmail.settings.basic'
CLIENT_SECRET = 'client_secret.json'
CREDENTIALS_FILE = 'credentials.json'
LABEL_NAME = 'MOE'

# error messages from Gmail API when creating a resource that already exists
LABEL_EXISTS_ERROR = 'Label name exists or conflicts'
FILTER_EXISTS_ERROR = 'Filter already exists'
MESSAGE_NOT_FOUND_ERROR = 'Not Found'

DEFAULT_SUBJECT = 'MOE message'


class Mailer():
    '''A Mailer is incharged of:
        - Setting up gmail accounts for MOE usage
        - Fetching/Sending MOE emails

    Args:
        user: Email address of the user.
        destination: Email address of the other MOE user.
        secret: file containing the OAuth 2.0 client ID of the MOE application
        credentials: <optional> file containing the OAuth 2.0 Google user authentification

    Effects:
        It will add a MOE label and filter to the Gmail account,

    Returns:
        A configured Mailer object.
    '''

    def __init__(self, user, destination, secret='client_secret.json', credentials='credentials.json'):
        if not _valid_email(user):
            raise ValueError('Invalid user email.')

        if not _valid_email(destination):
            raise ValueError('Invalid destination email.')

        self.user = user
        self.destination = _label_email(LABEL_NAME, destination)
        self.service = self._new(secret, credentials)
        self.label_id = self._create_label(LABEL_NAME)
        self._create_filter()

    def _new(self, secret, credentials):
        '''Sets up the Gmail API service to use for all Mailer's actions.

        Args:
            secret: file containing the OAuth 2.0 client ID of the MOE application.
            credentials: file containing the OAuth 2.0 Google user authentification.

        Effects:
            If the file credentials does not exist, it will open a browser so that
            the user can authorize MOE to the required scopes in Gmail.

        Returns:
            An authorized Gmail API service instance.
        '''

        Http.force_exception_to_status_code = True

        store = file.Storage(credentials)
        creds = store.get()
        if not creds or creds.invalid:
            flow = client.flow_from_clientsecrets(secret, _SCOPES)
            creds = tools.run_flow(flow, store)
        return build(_API, _VERSION, http=creds.authorize(Http())).users()

    def _create_filter(self):
        '''Creates a filter in the user Gmail account to redirect all MOE emails to the MOE label'''

        filter_object = {
            'criteria': {
                'to': _label_email(LABEL_NAME, self.user)
            },
            'action': {
                "addLabelIds": [self.label_id],
                "removeLabelIds": ["INBOX"]
            }
        }

        try:
            self.service.settings().filters().create(userId=self.user, body=filter_object).execute()
        except HttpAPIError as error:
            if FILTER_EXISTS_ERROR not in repr(error):
                raise

    def _create_label(self, label_name):
        '''Creates a label in the user Gmail account.

        Returns:
            The id of the label.
            If the label already exists, it will simply return its id.
        '''

        label_id = None
        label_object = {'messageListVisibility': 'show',
                        'name': label_name,
                        'labelListVisibility': 'labelShow'}
        try:
            label = self.service.labels().create(userId=self.user, body=label_object).execute()
            label_id = label['id']
        except HttpAPIError as error:
            if LABEL_EXISTS_ERROR in repr(error):
                label_id = self._label_id(LABEL_NAME)
            else:
                raise

        return label_id

    def _label_id(self, label_name):
        '''Returns:
            The label id for the given label name.
            If the label does not exist, it returns None.
        '''

        labels = self.service.labels().list(userId=self.user).execute().get('labels', [])
        for label in labels:
            if label['name'] == label_name:
                return label['id']

        return None

    def create_message(self, content, subject=DEFAULT_SUBJECT):
        '''Creates a message object for an email.
        It's receiver its the configured receiver of Mailer.
        It's sender is the configured user of Mailer.

        Args:
            subject: The subject of the email message.
            message_text: The text of the email message.

        Returns:
            An object containing a base64url encoded email object.
        '''

        message = MIMEText(content)
        message['to'] = self.destination
        message['from'] = self.user
        message['subject'] = subject
        return {'raw': base64.urlsafe_b64encode(message.as_bytes()).decode("utf-8")}

    # def create_message_image(self, text):
    #     '''compose_text composes an email with an image attachement'''
    #       TODO

    def send(self, message):
        '''Send an email with the to/from/subject/content found in message_body.

        Args:
            message_body: The body of the email message, including headers.
        '''

        message = self.service.messages().send(userId=self.user, body=message).execute()
        return message

    def send_message(self, text):
        '''Convenience method combining create_message() and send().

        Args:
            text: The text to be sent in an email.
        '''

        self.send(self.create_message(text))

    def fetch(self):
        '''Returns:
            A list with the content of all unread emails in chronological order
        '''

        msg_refs = self.service.messages().list(userId=self.user, labelIds=[self.label_id]).execute().get('messages', [])
        msg_ids = [m['id'] for m in msg_refs]
        full_msgs = [self.service.messages().get(userId=self.user, id=id, format='minimal').execute() for id in msg_ids]
        return [{msg['id']: msg['snippet']} for msg in full_msgs]

    def delete_message(self, message_id):
        '''Deletes a message from the inbox.

        Args:
            message_id: The id of the message to delete.
        '''

        try:
            self.service.messages().delete(userId=self.user, id=message_id).execute()
        except HttpAPIError as error:
            if MESSAGE_NOT_FOUND_ERROR not in repr(error):
                raise


def _label_email(label, email):
    '''Returns:
        The email with the format: <EMAIL>+<LABEL>@gmail.com.
        This format is supported by Gmail to automatically redirect an email to a label
    '''

    at_idx = email.index('@')
    return '{}+{}{}'.format(email[:at_idx], label, email[at_idx:])


def _valid_email(email):
    '''Returns:
        If the string is a valid email
    '''

    return re.match(r'\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b', email, re.I) is not None
