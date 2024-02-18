import re
import time

from rich import print as rprint

from lib.database import GDRIVE_CLIENT


def validate_email(email):
    '''
    Uses a regex pattern to validate the most common email address patterns

    Params: email as a string.

    Returns: boolean value of True if the email is valid. False if not valid

    Code used for validation from below link:
    https://emaillistvalidation.com/blog/check-email-using-regex-in-python-validate-email-addresses-with-confidence/

    Other patterns are available from the above source.
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

    Params: file_object representing the file which needs to be shared.
    email as a string for who the email is being shared with (after
    being validated with validate_email function)
    '''

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
    Validates the email address with validate_email function and
    calls the create_shareable_link function if successful.

    Params: file_id as a string. This is a google drive file id.

    '''
    rprint("Would you like a link to the file?")
    response = input("(Y) for Yes, any other key for no: ")

    if response.lower() == "y":
        email = input("Please provide mail address: ")
        if validate_email(email=email):
            create_shareable_link(file_id, email)
        else:
            rprint("[red]Incorrect email format, Returning to Menu")
            time.sleep(2)
    else:
        rprint("[red]You do not want a link, returning to menu")
        time.sleep(2)
