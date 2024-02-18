'''
Shared utilities for the package.

Contents: 

Helper functions for reusable user notifications
that print to the console:

- wait_notification
- no_data_message
- exit_message

Helper functions for creating custom menus with InquirerPY.

- list_select_menu
- fuzzy_select_menu

'''

import time
import os

from rich import print as rprint
from InquirerPy import inquirer

from lib.database import GDRIVE_CLIENT


def wait_notification(seconds=3):
    '''
    Helper function to print please wait to the console.
    It takes in an integer param which determines how many
    periods (.) to print (and how many seconds to wait).

    Params: seconds as an integer for the number of seconds.
    Default of 3 seconds.
    '''
    for _ in range(seconds):
        time.sleep(1)
        os.system("clear")
        rprint("[green]Please wait" + "." * (_ + 1))
    os.system("clear")


def exit_message():
    '''
    Small script that is used throughout the program to exit
    the program upon user direction.

    Raises: SystemExit after the exit message is displayed.
    '''
    rprint("[red]The program is now exiting")
    wait_notification()
    rprint("[cyan]Goodbye!")
    time.sleep(1)
    os.system("clear")

    raise SystemExit


def no_data_message():
    '''
    Small utility function to inform user of no data in the database
    '''
    rprint("[red]No data stored in FX Net Database")
    rprint("[red]Please load data or select another option")
    time.sleep(2)


def list_select_menu(menu):
    '''
    Menu generation function that takes in a dict containing
    a question as the key then another dict as the value
    containing responses as keys and functions associated
    with those responses as values.

    Params: menu dictionary

    Example:
    question = {
    "Please select an option?": {
        "option 1": option_1_function,
        "option 2": option_2_function,
    }}

    list_select_menu(question)

    If user selects option 2 then option_2_function
    is called.

    Returns: The executed function based on the response
    '''
    question = list(menu.keys())[0]
    choices_keys = menu[question].keys()
    result = inquirer.select(
        message=question,
        choices=choices_keys,
    ).execute()

    return menu[question][result]()


def fuzzy_select_menu(message, choices):
    '''
    Menu generation function for a fuzzy search menu.

    Params: message as a string represents the question
    being asked.
    choices as a list represents the choices the user
    can select.

    There is a validation to check if the choice is in the
    initial list you passed in.

    Example:
    dates = ["20240301","20240521"]
    date = fuzzy_select_menu("Type or select a date: ", dates)

    Returns the choice
    '''

    def validate_choice(choice):
        '''
        Validates if the choice is in the list of choices
        provided
        '''
        if choice in choices:
            return True

    result = inquirer.fuzzy(
        message=message,
        choices=choices,
        validate=validate_choice,
        invalid_message="Must Enter a valid date").execute()

    return result


def get_file_list(file_name_filter=None):
    '''
    Helper function to list all file ids in google drive.
    Prints the file name and id to the console whilst running.

    Optional Params:
    file_name_filter is the filter of file name you wish to
    look for

    Returns:
    list_of_file_ids which is a list of file ids in google drive

    '''
    list_of_file_ids = []
    if file_name_filter is None:
        notification = "NO FILTER"
    else:
        notification = f'with filter of "{file_name_filter}"'
    print(f'Files in Google Drive {notification}:')
    results = GDRIVE_CLIENT.files().list().execute()
    files = results.get('files', [])
    if not files:
        print('No files found in Google Drive.')
    else:
        for file in files:
            if file_name_filter is None:
                print(f"{file['name']} ({file['id']})")
                list_of_file_ids.append((file['id']))
            elif file["name"].startswith(file_name_filter):
                print(f"{file['name']} ({file['id']})")
                list_of_file_ids.append((file['id']))

    return list_of_file_ids


def delete_file(file_id):
    '''
    Helper function the developer can use to clean up the
    google drive environment
    '''
    try:
        GDRIVE_CLIENT.files().delete(fileId=file_id).execute()
        print(f'File with ID {file_id} successfully deleted.')

    except Exception as e:
        print(f'Error deleting file: {e}')

