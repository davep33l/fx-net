'''
Shared utilities for the package
'''

import time
import os

from rich import print as rprint
from InquirerPy import inquirer
from lib.database import GDRIVE_CLIENT


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
    Small script that is used throughout the program to exit the program
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
    '''
    Small utility function to inform user of no data in the database
    '''
    rprint("[red]No data stored in FX Net Database")
    rprint("[red]Please load data or select another option")
    time.sleep(2)


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


def get_file_list(file_name_filter=None):
    '''
    TBD
    '''
    list_of_files = []
    if file_name_filter is None:
        notification = "with no filter"
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
                # list_of_files.append((file['name'], file['id']))
                list_of_files.append((file['id']))

            elif file["name"].startswith(file_name_filter):
                print(f"{file['name']} ({file['id']})")
                # list_of_files.append((file['name'], file['id']))
                list_of_files.append((file['id']))

    return list_of_files

