'''The gmailer module contains a Mailer implementation based on Gmail.'''
import base64
import re

from typing import Dict, List

import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.errors import HttpError as HttpAPIError

from email.mime.text import MIMEText


# contains user's access and refresh tokens
PICKLE_FILE = 'token.pickle'
CREDENTIALS_FILE = 'credentials.json'

# If modifying these scopes, delete the file token.pickle.
_SCOPES = [
        'https://mail.google.com/',
        'https://www.googleapis.com/auth/gmail.compose ',
        'https://www.googleapis.com/auth/gmail.send ',
        'https://www.googleapis.com/auth/gmail.labels ',
        'https://www.googleapis.com/auth/gmail.modify ',
        'https://www.googleapis.com/auth/gmail.settings.basic']

MOE_LABEL_NAME = 'MOE'
UNREAD_LABEL = 'UNREAD'

# error messages from Gmail API when creating a resource that already exists
LABEL_EXISTS_ERROR = 'Label name exists or conflicts'
FILTER_EXISTS_ERROR = 'Filter already exists'
MESSAGE_NOT_FOUND_ERROR = 'Not Found'

DEFAULT_SUBJECT = 'MOE message'


class Gmailer():
    '''Implementation of Mailer that leverages Gmail.

    Capable of configuring existent gmail accounts for MOE to use.
    It does so through Gmail's Label and a Filter capabilities.

    Args:
        user (str): Email address of the user.
        destination (str): Email address of the other MOE user.
        secret (str, optional): Defaults to 'client_secret.json'. File containing the OAuth 2.0 client ID of the MOE application.
        credentials (str, optional): Defaults to 'credentials.json'. File containing the OAuth 2.0 Google user authentification.

    Raises:
        ValueError: Invalid user email.
        ValueError: Invalid destination email.'''

    def __init__(self, user: str, destination: str,
                 secret: str = 'client_secret.json', credentials: str = 'credentials.json') -> None:

        if not _valid_email(user):
            raise ValueError('Invalid user email.')

        if not _valid_email(destination):
            raise ValueError('Invalid destination email.')

        self.user = user
        self.destination = _label_email(MOE_LABEL_NAME, destination)
        self.service = _new(secret, credentials)
        self.label_id = self._create_label(MOE_LABEL_NAME)
        self._create_filter()

    def create_message(self, content: str, subject: str = DEFAULT_SUBJECT) -> object:
        '''Creates a message object for an email.

        It's receiver its the configured receiver of Mailer.
        It's sender is the configured user of Mailer.

        Args:
            content (str): The subject of the email message.
            subject (str, optional): Defaults to DEFAULT_SUBJECT. The text of the email message.

        Returns:
            object: An object containing a base64url encoded email object.'''

        message = MIMEText(content)
        message['to'] = self.destination
        message['from'] = self.user
        message['subject'] = subject
        return {'raw': base64.urlsafe_b64encode(message.as_bytes()).decode("utf-8")}

    # def create_message_image(self, text):
    #     '''compose_text composes an email with an image attachement'''

    def delete_message(self, message_id: str) -> None:
        '''Deletes a message from the inbox.

        Args:
            message_id (str): The id of the message to delete.'''

        try:
            self.service.users().messages().delete(userId=self.user, id=message_id).execute()
        except HttpAPIError as error:
            if MESSAGE_NOT_FOUND_ERROR not in repr(error):
                raise

    def fetch_all(self) -> List[Dict]:
        '''Fetch all the emails in MOE's inbox.

        Returns:
            List[Dict]: A list with the MOE email dicts in chronological order.'''

        msg_refs = self.service.users().messages().list(userId=self.user, labelIds=[self.label_id]).execute().get('messages', [])
        msg_ids = [msg['id'] for msg in msg_refs]

        full_msgs = [self.service.users().messages().get(userId=self.user, id=id, format='minimal').execute() for id in msg_ids]

        msg_contents = [msg['snippet'] for msg in full_msgs]
        msg_labels = [msg['labelIds'] for msg in full_msgs]
        msg_is_unread = [UNREAD_LABEL in msg['labelIds'] for msg in full_msgs]

        return [{'id': id, 'content': msg_content, 'labelIds': msg_label, 'unread': msg_unread}
                for id, msg_content, msg_label, msg_unread in zip(msg_ids, msg_contents, msg_labels, msg_is_unread)]

    def fetch_unread(self) -> List[Dict]:
        '''Fetch all the emails in MOE's inbox that are unread.

        Returns:
            List[Dict]: A list of MOE emails.'''

        return list(filter(_is_unread, self.fetch_all()))

    def mark_as_read(self, msg: Dict) -> Dict:
        '''Marks the email message as read from the MOE inbox in Gmail

        If the message has already been read the function does not do anything.

        Args:
            msg (Dict): The MOE email to mark as read.

        Returns:
            Dict: The updated MOE email.'''

        if UNREAD_LABEL not in msg['labelIds']:
            return msg

        new_labels = {'addLabelIds': [], 'removeLabelIds': [UNREAD_LABEL]}

        new_msg = self.service.users().messages().modify(userId=self.user, id=msg['id'], body=new_labels).execute()

        return {'id': new_msg['id'], 'content': msg['content'], 'labelIds': new_msg['labelIds'], 'unread': False}

    def read(self) -> Dict:
        '''Reads the latest unread message from the MOE inbox in Gmail.

        If there is an unread email, the email is marked as seen, but not deleted.
        If there is no unread email, it returns an empty object.

        Returns:
            Dict: MOE's email object.'''

        unread_msgs = self.fetch_unread()
        if unread_msgs:
            msg = unread_msgs.pop()
            read_msg = self.mark_as_read(msg)
        else:
            return {}

        return read_msg

    def write(self, content: str) -> str:
        '''Sends an email with the content to the configured receiver.

        This method ensures Gmailer is an implementation of the Writer interface.

        Args:
            content (str): The content to send.

        Returns:
            str: The id of the sent message.'''

        return self._send(self.create_message(content))

    def _create_filter(self) -> None:
        '''Creates a filter in the user Gmail account to redirect all MOE emails to the MOE label

        Raises:
            HttpAPIError'''

        filter_object = {
            'criteria': {
                'to': _label_email(MOE_LABEL_NAME, self.user)
            },
            'action': {
                "addLabelIds": [self.label_id],
                "removeLabelIds": ["INBOX"]
            }
        }

        try:
            self.service.users().settings().filters().create(userId=self.user, body=filter_object).execute()
        except HttpAPIError as error:
            if FILTER_EXISTS_ERROR not in repr(error):
                raise

    def _create_label(self, label_name: str = MOE_LABEL_NAME) -> str:
        '''Creates a label in the user Gmail account.

        If the label already exists, it will simply return its id.

        Args:
            label_name (str, optional): Defaults to MOE_LABEL_NAME. Name of the label to create.

        Returns:
            str: The id of the label.

        Raises:
            HttpApiError'''

        label_id = None
        label_object = {'messageListVisibility': 'show',
                        'name': label_name,
                        'labelListVisibility': 'labelShow'}
        try:
            label = self.service.users().labels().create(userId=self.user, body=label_object).execute()
            label_id = label['id']
        except HttpAPIError as error:
            if LABEL_EXISTS_ERROR in repr(error):
                label_id = self._label_id(label_name)
            else:
                raise

        return label_id

    def _label_id(self, label_name: str) -> str:
        '''Gets the label id for the given label name.

        If the label does not exist, it returns None.

        Args:
            label_name (str): The label name to retrieve the id from.

        Returns:
            str: The label id.'''

        labels = self.service.users().labels().list(userId=self.user).execute().get('labels', [])
        for label in labels:
            if label['name'] == label_name:
                return label['id']

        return None

    def _send(self, message: object) -> str:
        '''Send an email with the to/from/subject/content found in message_body.

        Args:
            message (object): The body of the email message, including headers (base64url encoded).

        Returns:
            str: The message id associate with the sent email.'''

        message = self.service.users().messages().send(userId=self.user, body=message).execute()
        return message['id']


def _is_unread(msg: str) -> bool:
    '''Check if an email message is unread.

    Args:
        msg (str): The email message to check.'''

    return msg['unread']


def _new(secret: str, credentials: str) -> object:
    '''Sets up the Gmail API service used.

    If the file credentials does not exist, it will open a browser so that
    the user can authorize MOE to the required scopes in Gmail.

    Args:
        secret (str): File containing the OAuth 2.0 client ID of the MOE application.
        credentials (str): File containing the OAuth 2.0 Google user authentification.

    Returns:
        object: An authorized Gmail API service instance.'''

    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists(PICKLE_FILE):
        with open(PICKLE_FILE, 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                CREDENTIALS_FILE, _SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open(PICKLE_FILE, 'wb') as token:
            pickle.dump(creds, token)

    return build('gmail', 'v1', credentials=creds, cache_discovery=False)


def _label_email(label: str, email: str) -> str:
    '''Labels the email with the format: <EMAIL>+<LABEL>@gmail.com.
        This format is supported by Gmail to automatically redirect an email to a label.

    Args:
        label (str): The label to apply to the email.
        email (str): The email string to modify.

    Returns:
        str: The labeled email string.'''

    at_idx = email.index('@')
    return '{}+{}{}'.format(email[:at_idx], label, email[at_idx:])


def _valid_email(email: str) -> bool:
    '''Verify if an email is valid.

    Args:
        email (str): The email to validate.'''

    return re.match(r'\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b', email, re.I) is not None
