# import google_client_manager
# from _trading_simulator import trading_simulator as trading_app
# import pandas as pd


# clients = google_client_manager.get_google_clients()

# DATABASE_WORKBOOK = clients[0].open('fx-net-data')

# # Worksheet connections
# USERS = DATABASE_WORKBOOK.worksheet("USERS").get_all_values()
# print(USERS)

# df = pd.DataFrame(USERS[1:], columns=USERS[0])

# data, file = trading_app.create_simulated_trade_data("20240424",10)

# email = input("please provide email: ")

# if email in df.values:
#     print("yes")
#     trading_app.create_and_save_output_file(data, file, clients, email)
# else:
#     print("Please use a valid user account to store the files")

from InquirerPy import inquirer




def yes_answer():
    print("you selected yes")

def exit_answer():
    print("you selected exit")

def menu(question, choices):
    '''
    This function takes in a question and a dict of choices.
    The choices dict should contain an "answer" to the question
    as the key and a function name as the value.

    Returns the execution of the respective function based
    on the answer given.

    '''

    choices_keys = list(choices.keys())

    result = inquirer.select(
    message=question,
    choices=choices_keys,
    ).execute()

    return choices[f'{result}']()

question = "Do you want to proceed with creating the simulated data?"
choices = {"Yes": yes_answer, "Exit": exit_answer}

# menu(question, choices)

menu_1 = {
    "Do you want to proceed with creating the simulated data?": {
        "Yes": yes_answer,
        "Exit": exit_answer
    }}


def list_select_menu(menu):

    question = list(menu.keys())[0]
    choices_keys = menu[question].keys()
    result = inquirer.select(
    message=question,
    choices=choices_keys,
    ).execute()

    return choices[f'{result}']()

# print(menu_1)
# question = list(menu_1.keys())[0]
# print(question)
# choices = menu_1[question].keys()
# print(choices)

list_select_menu(menu_1)


def fuzzy_search_menu(message, choices):

    result = inquirer.fuzzy(
        message=message, 
        choices=choices).execute()

    return result
