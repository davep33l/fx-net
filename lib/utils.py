import time
import os

from rich import print as rprint
from InquirerPy import inquirer
import gspread
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build

def please_wait(seconds=3):
    for _ in range(seconds):
        time.sleep(1)
        os.system("clear")
        rprint("[green]Please wait" + "." * (_ + 1))

def exit_message():
    '''
    TBD
    '''
    rprint("[red]The program is now exiting")
    please_wait()
    rprint("Goodbye!")
    time.sleep(1)
    os.system("clear")

    raise SystemExit

def list_select_menu(menu):
    '''
    Menu generation function that takes in a dict containing
    a question as the key then another dict of responses and 
    functions associated with those responses
    
    Returns: The executed function based on the response
    '''
    question = list(menu.keys())[0]
    choices_keys = menu[question].keys()
    result = inquirer.select(
    message=question,
    choices=choices_keys,
    ).execute()

    return menu[question][result]()

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