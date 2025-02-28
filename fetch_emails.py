import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from bs4 import BeautifulSoup
import base64

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

def authenticate():
    """Shows basic usage of the Gmail API.
    Lists the user's Gmail labels.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return creds

def get_email_service():
    creds = authenticate()
    return build('gmail', 'v1', credentials=creds)

def fetch_emails(service, max_results=10):
    results = service.users().messages().list(
        userId='me',
        maxResults=max_results
    ).execute()
    return results.get('messages', [])

def get_email_content(service, msg_id):
    msg = service.users().messages().get(
        userId='me',
        id=msg_id,
        format='full'
    ).execute()
    return msg

def extract_body(email):
    if 'parts' in email['payload']:
        for part in email['payload']['parts']:
            if part['mimeType'] == 'text/html':
                data = part['body']['data']
                return base64.urlsafe_b64decode(data).decode('utf-8')
    return ''

def find_unsubscribe_links(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    patterns = [
        r'unsubscribe',
        r'opt-out',
        r'email preferences',
        r'mailing preferences'
    ]
    links = []
    for a in soup.find_all('a', href=True):
        if any(pattern in a.text.lower() for pattern in patterns):
            links.append(a['href'])
    return links

def main():
    service = get_email_service()
    emails = fetch_emails(service)
    
    for email in emails:
        msg = get_email_content(service, email['id'])
        html_content = extract_body(msg)
        unsubscribe_links = find_unsubscribe_links(html_content)
        
        if unsubscribe_links:
            print(f"Found unsubscribe links in email {email['id']}:")
            for link in unsubscribe_links:
                print(f" - {link}")
        else:
            print(f"No unsubscribe links found in email {email['id']}")

if __name__ == '__main__':
    main()
