
import gspread
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build

def get_google_clients():
    """
    Function that creates a Google Spreadsheet client and
    creates a Google Drive client that have been authenticated.

    Returns a tuple of clients:
    GSPREAD_CLIENT and GDRIVE_CLIENT
    """

    SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

    CREDS = Credentials.from_service_account_file('creds.json')
    SCOPED_CREDS = CREDS.with_scopes(SCOPE)
    # Google Sheets and Drive client connections
    GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
    GDRIVE_CLIENT = build('drive', 'v3',credentials=SCOPED_CREDS)

    return GSPREAD_CLIENT, GDRIVE_CLIENT
