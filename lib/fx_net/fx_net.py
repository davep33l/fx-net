import os
import time
from rich import print as rprint

from lib import utils

def fx_net():
    print("From FX Net")


# Move to fx_net folder
def fx_net_menu():
    '''
    TBD
    '''

    rprint("[green]Opening the FX Net Application")
    utils.please_wait()
    os.system("clear")
    rprint("[green]FX Net is open") # call the FX Net app here
    time.sleep(1)
    while True:

        fx_net_response = menu(menu_2_question, menu_2_choices)
        if fx_net_response == menu_2_choices[0]:
            print("loading fx data")
            # load_fx_data()
        elif fx_net_response == menu_2_choices[1]:
            reporting_menu()
            break
        elif fx_net_response == menu_2_choices[2]:
            print("Returning previous menu")
            time.sleep(1)
            os.system("clear")
            break


# Move to fx_net folder
def reporting_menu():
    '''
    TBD
    '''

    rprint("[green]Opening Reporting Menu")
    time.sleep(1)
    os.system("clear")
    while True:
        os.system("clear")
        rprint("\nWelcome to the analsyis menu\n")
        rep_response = menu(menu_3_question, menu_3_choices)

        if rep_response == menu_3_choices[0]:
            print("creating table")
            time.sleep(1)
            # create_table()
        elif rep_response == menu_3_choices[1]:
            # create_report_spreadsheet("20240625")
            pass
        elif rep_response == menu_3_choices[2]:
            pass
        elif rep_response == menu_3_choices[3]:
            pass
        elif rep_response == menu_3_choices[4]:
            pass
        elif rep_response == menu_3_choices[5]:
            pass
        elif rep_response == menu_3_choices[6]:
            print("Returning previous menu")
            time.sleep(1)
            os.system("clear")
            return


from InquirerPy import inquirer

menu_1_question = "Do you want to proceed with creating the simulated data?"
menu_1_choices = ["Yes", "Exit program"]

menu_2_question = "Please choose an option?"
menu_2_choices = ["Load Data", "Reporting Menu", "Return to previous menu"]

menu_3_question = "Please select an option"
menu_3_choices = ["Show Netting Summary by Value Date (working)",
                  "Create Netting Report by Value Date (WIP)",
                   "Create payment files (WIP)",
                   "Show trade count by clients (WIP)",
                   "Show trade count by client and client trader (WIP)",
                   "Show trade count by bank trader (WIP)",
                   "Return to main menu (working)"]

def menu(question, choices):

    result = inquirer.select(
    message=question,
    choices=choices,
    ).execute()

    return result


def menu_fuzzy(message, choices):

    result = inquirer.fuzzy(
        message=message, 
        choices=choices).execute()

    return result