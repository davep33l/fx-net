import time
import os

from rich import print as rprint
from InquirerPy import inquirer
import gspread
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build


def please_wait(seconds=3):
    '''
    Helper function to print please wait to the console.
    It takes in an integer param which determines how many
    periods to print (and how many seconds to wait)
    '''
    for _ in range(seconds):
        time.sleep(1)
        os.system("clear")
        rprint("[green]Please wait" + "." * (_ + 1))
    os.system("clear")


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

# Specficially used this part of the documentation to work out how
# to validate the input of a fuzzy menu
# https://inquirerpy.readthedocs.io/en/latest/pages/prompts/fuzzy.html#codecell1


def fuzzy_select_menu(message, choices):
    '''
    Menu generation function for a fuzzy search menu.
    You need to pass in a message and a list of choices.
    There is a validation to check if the choice is in the
    initial list you passed in.

    Returns the choice
    '''

    def validate_choice(choice):
        if choice in choices:
            return True

    result = inquirer.fuzzy(
        message=message,
        choices=choices,
        validate=validate_choice,
        invalid_message="Must Enter a valid date").execute()

    return result

def no_data_message():
    rprint("[red]No data stored in FX Net Database")
    rprint("[red]Please load data or select another option")
    time.sleep(2)

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
    GDRIVE_CLIENT = build('drive', 'v3', credentials=SCOPED_CREDS)

    return GSPREAD_CLIENT, GDRIVE_CLIENT
