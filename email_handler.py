from googleapiclient.errors import HttpError
import base64
import logging
from email.mime.text import MIMEText

# Set up logging
logging.basicConfig(filename='app.log', filemode='a', format='%(name)s - %(levelname)s - %(message)s', level=logging.INFO)

def get_unread_emails(service):
    try:
        result = service.users().messages().list(userId='me', q="is:unread").execute()
        messages = result.get('messages', [])
        return messages
    except HttpError as error:
        logging.error(f'An error occurred: {error}')
        return None

def parse_email_content(service, email):
    try:
        message = service.users().messages().get(userId='me', id=email['id']).execute()
        payload = message['payload']
        headers = payload.get("headers")
        parts = payload.get("parts")

        data = parts[0]
        data_bytes = data['body']['data']
        decoded_data = base64.urlsafe_b64decode(data_bytes)
        str_data = decoded_data.decode('utf-8')

        # Extract the 'To', 'From', and 'Subject' fields from headers
        email_data = {
            'Body': str_data,
            'To': next(header['value'] for header in headers if header['name'] == 'From'),
            'From': next(header['value'] for header in headers if header['name'] == 'To'),
            'Subject': next(header['value'] for header in headers if header['name'] == 'Subject'),
            'ThreadId': message['threadId'],  # Add the ThreadId
            'Id': email['id']  # Add the email Id
        }

        if email_data is None:
            logging.error('Failed to parse email content.')
        
        return email_data
    except HttpError as error:
        logging.error(f'An error occurred: {error}')
        return None

def mark_read(service, user_id, email_id):
    try:
        service.users().messages().modify(userId=user_id, id=email_id, body={'removeLabelIds': ['UNREAD']}).execute()
        logging.info(f'Email id: {email_id} marked as read.')
    except HttpError as error:
        logging.error(f'An error occurred: {error}')
