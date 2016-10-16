
from __future__ import print_function
import httplib2
import os
import json

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/drive-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/drive.metadata.readonly'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Drive API Python Quickstart'


def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'drive-python-quickstart.json')

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials

def main():
    """Shows basic usage of the Google Drive API.

    Creates a Google Drive API service object and outputs the names and IDs
    for up to 10 files.
    """
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('drive', 'v3', http=http)

    page_token = None
    while True:
        response = service.files().list( q="fullText contains 'IMG' or name contains 'IMG' or 'cisco' in parents",
                                         spaces='drive',
                                         fields='nextPageToken, files(id, name, fileExtension, owners,webViewLink)',
                                         pageToken=page_token).execute()
        for file in response.get('files', []):
            text=file.get('owners')
            #print (file.get('owners'))
            for i in text:
                print (i)
            #parsed_json=json.load(text)
            #print ('%s %s %s %s %s' % (file.get('name'), file.get('id')[2],file.get('fileExtension'),file.get('webViewLink'),file.get('ownerNames')))
           # print (parsed_json[displayName])
        page_token = response.get('nextPageToken', None)
        if page_token is None:
            break;

"""
This is querying all the random stuff in the first page

    results = service.files().list(
        pageSize=20,
        fields="nextPageToken, files(id, name, webViewLink, kind)").execute()
    items = results.get('files', [])
    if not items:
        print('No files found.')
    else:
        print('Files:')
        for item in items:
            print('{0} ({1}) {2} {3}'.format(item['name'], item['id'], item['webViewLink'], item['kind']))

"""
if __name__ == '__main__':
    main()