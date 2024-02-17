import re
import time

from rich import print as rprint

from lib.database import GDRIVE_CLIENT

def validate_email(email):
    '''
    Uses regex to validate the most common email address patterns
    '''
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    if re.match(pattern, email):
        return True
    else:
        return False

def create_shareable_link(file_object, email):
    '''
    Takes in a file object and email address, and shares the link with 
    that email address.
    '''

    # Gives access to the file for the email address passed in
    permissions = {
        'type': 'user',
        'role': 'reader',
        'emailAddress': email,
    }

    GDRIVE_CLIENT.permissions().create(
        fileId=file_object['id'], body=permissions).execute()

    rprint(f"[green]Email has been sent to {email}")
    input("Press Enter to continue")


def create_link_menu(file_id):
    '''
    Helper function to present the user with a menu asking if
    the require a link for the file that has been generated.
    Validates the email address against regex pattern
    '''

    response = input("Do you want a link for the file. Press Y and enter: ")

    if response.lower() == "y":
        email = input("Input email address: ")
        if validate_email(email=email):
            print("Creating link for you")
            create_shareable_link(file_id, email)
        else:
            print("Invalid Email, Returning to Menu")
            time.sleep(2)
    else:
        print("You do not want a link, returning to menu")
        time.sleep(2)