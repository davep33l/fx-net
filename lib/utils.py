import time
import os
from rich import print as rprint
from InquirerPy import inquirer

def please_wait(seconds=3):
    for _ in range(seconds):
        time.sleep(1)
        os.system("clear")
        rprint("[green]Please wait" + "." * (_ + 1))


# Move to utils folder
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
