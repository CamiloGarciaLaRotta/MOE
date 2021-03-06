'''The gmailer module contains a Mailer implementation based on Gmail.'''
import base64
import re

from typing import Dict, List

import pickle
import os.path

from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError as HttpAPIError
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request


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

DEFAULT_SUBJECT = 'MOE: message'
TEXT_SUBJECT = 'MOE: text'
IMG_SUBJECT = 'MOE: image'

MOE_FILENAME = 'moeimg'

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

    def __init__(self, user: str, destination: str) -> None:
        if not _valid_email(user):
            raise ValueError('Invalid user email.')
        if not _valid_email(destination):
            raise ValueError('Invalid destination email.')

        self.user = user
        self.destination = _label_email(MOE_LABEL_NAME, destination)
        self.service = _new()
        self.label_id = self._create_label(MOE_LABEL_NAME)
        self._create_filter()

    # TODO it would be nice if create_img_msg just delegated to create_message
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

    def create_img_msg(self, img: bytes, subject: str = DEFAULT_SUBJECT) -> object:
        '''compose_text composes an email with an image attachement'''

        # Create a "related" message container that will hold the HTML
        # message and the image. These are "related" (not "alternative")
        # because they are different, unique parts of the HTML message,
        # not alternative (html vs. plain text) views of the same content.
        html_part = MIMEMultipart(_subtype='related')

        # Create the body with HTML. Note that the image, since it is inline, is
        # referenced with the URL cid:myimage... you should take care to make
        # "myimage" unique
        body = MIMEText(f'<p><img src="cid:{MOE_FILENAME}" /></p>', _subtype='html')
        html_part['to'] = self.destination
        html_part['from'] = self.user
        html_part['subject'] = subject
        html_part.attach(body)

        # Now create the MIME container for the image
        img = MIMEImage(img, 'jpeg')
        img.add_header('Content-Id', f'<{MOE_FILENAME}>')  # angle brackets are important
        img.add_header("Content-Disposition", "inline", filename=MOE_FILENAME)
        html_part.attach(img)

        return {'raw': base64.urlsafe_b64encode(html_part.as_bytes()).decode("utf-8")}

    def delete_message(self, message_id: str) -> None:
        '''Deletes a message from the inbox.

        Args:
            message_id (str): The id of the message to delete.'''

        try:
            self.service.users().messages().delete(userId=self.user, id=message_id).execute()
        except HttpAPIError as error:
            if MESSAGE_NOT_FOUND_ERROR not in repr(error):
                raise

    def delete_all(self) -> None:
        '''Deletes all messages from MOE's inbox.'''

        ids = [email['id'] for email in self.fetch_all()]
        # print(ids) # TODO good debugger thing
        res = self.service.users().messages().batchDelete(userId=self.user, body={'ids': ids}).execute()
        if res != '':
            print(res)

    def fetch_all(self) -> List[Dict]:
        '''Fetch all the emails in MOE's inbox.

        Returns:
            List[Dict]: A list with the MOE email dicts in chronological order.'''

        msg_refs = self.service.users().messages().list(userId=self.user, labelIds=[self.label_id]).execute().get('messages', [])
        msg_ids = [msg['id'] for msg in msg_refs]

        full_msgs = [self.service.users().messages().get(userId=self.user, id=id, format='full').execute() for id in msg_ids]

        msg_headers = [msg['payload']['headers'] for msg in full_msgs]
        msg_subjects = [_get_subject(headers) for headers in msg_headers]

        msg_parts = [msg['payload']['parts'] if 'parts' in msg['payload'] else '' for msg in full_msgs]
        msg_attachement_ids = [_get_attachement_id(parts) if isinstance(parts, list) else '' for parts in msg_parts]

        msg_imgs = []
        for i in range(len(msg_ids)):
            aid = msg_attachement_ids[i]
            if aid != '':
                attach = self._get_attachement(aid=aid, msg_id=msg_ids[i])
                msg_imgs.append(attach)
            else:
                msg_imgs.append('')

        msg_txts = [msg['snippet'] for msg in full_msgs]
        msg_labels = [msg['labelIds'] for msg in full_msgs]
        msg_is_unread = [UNREAD_LABEL in msg['labelIds'] for msg in full_msgs]

        return [
            {
                'id': id,
                'subject': msg_subject,
                'txt': msg_txt,
                'img': msg_img,
                'labelIds': msg_label,
                'unread': msg_unread
            }
            for id, msg_subject, msg_txt, msg_img, msg_label, msg_unread in
            zip(msg_ids, msg_subjects, msg_txts, msg_imgs, msg_labels, msg_is_unread)]

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

        return {'id': new_msg['id'], 'txt': msg['txt'], 'img': msg['img'], 'labelIds': new_msg['labelIds'], 'unread': False}

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

    def write_img(self, img: bytes) -> str:
        '''Sends an email with the image attached to the configured receiver.

        Args:
            img (bytes): The image to send.

        Returns:
            str: The id of the sent message.'''

        return self._send(self.create_img_msg(img, subject='MOE: image'))

    def write(self, content: str) -> str:
        '''Sends an email with the content to the configured receiver.

        This method ensures Gmailer is an implementation of the Writer interface.

        Args:
            content (str): The content to send.

        Returns:
            str: The id of the sent message.'''

        return self._send(self.create_message(content, subject='MOE: text'))

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

    def _get_attachement(self, aid: str, msg_id: str) -> str:
        '''Given an attachement id, obtain the image'''

        message = self.service.users().messages().attachments().get(userId=self.user, messageId=msg_id, id=aid).execute()

        if message['data']:
            data = message['data']
            return base64.urlsafe_b64decode(data.encode('UTF-8'))

        return 'no img :('


def _is_unread(msg: str) -> bool:
    '''Check if an email message is unread.

    Args:
        msg (str): The email message to check.'''

    return msg['unread']


def _new() -> object:
    '''Sets up the Gmail API service used.

    If the token.pickle does not exist, it will open a browser so that
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
            # TODO we have created this pickle, so we know what is does
            # look into using JSON instead
            creds = pickle.load(token)  # nosec
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


def _get_subject(headers: Dict) -> str:
    '''Given dictionnary of email headers, find and return the subject'''
    for header in headers:
        if header['name'] == 'subject':
            return header['value']

    return ''

def _get_attachement_id(parts: Dict) -> str:
    '''Given dictionnary of email parts, find and return the moe attached img'''
    for part in parts:
        if part['filename'] == MOE_FILENAME:
            return part['body']['attachmentId']

    return ''
