from __future__ import print_function
import pickle as pickle

from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request


# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']
DEPENDENCIES_INSTALL = 'pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib'

def setup_env():
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    from os import path
    if path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not path.exists('credentials.json'):
                print("The credentials file credentials.json cannot be found in the current directory")
                return
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server()
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('sheets', 'v4', credentials=creds)
    # Call the Sheets API
    sheet = service.spreadsheets()
    return service, sheet


class Reader:
    def __init__(self):
        '''
        Constructor for the transformer:
        Goal is to read in Google Sheet's data entries,
        Convert them into CSV format
        And re-converting the result back into pandas dataframe / or nested list
        '''
        try:
            self.service, self.sheets = setup_env()
        except ModuleNotFoundError as e:
            print("Please try installing all the necessary dependencies with the command: ")
            print(DEPENDENCIES_INSTALL)
            return
        self.values = None

    def read_from_sheet(self, spreadsheetId, range):
        result = self.sheets.values().get(
            spreadsheetId=spreadsheetId,
            range=range
        ).execute()
        values = result.get('values', [])

        if not values:
            print('No data has been found.')
            return
        else:
            self.values = values
            return self