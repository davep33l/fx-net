# import google_client_manager
# from _trading_simulator import trading_simulator as trading_app
# import pandas as pd


# clients = google_client_manager.get_google_clients()

# FX_NET_DB = clients[0].open('fx-net-data')

# # Worksheet connections
# USERS = FX_NET_DB.worksheet("USERS").get_all_values()
# print(USERS)

# df = pd.DataFrame(USERS[1:], columns=USERS[0])

# data, file = trading_app.create_simulated_trade_data("20240424",10)

# email = input("please provide email: ")

# if email in df.values:
#     print("yes")
#     trading_app.create_and_save_output_file(data, file, clients, email)
# else:
#     print("Please use a valid user account to store the files")

# from InquirerPy import inquirer




# def yes_answer():
#     print("you selected yes")

# def exit_answer():
#     print("you selected exit")

# def menu(question, choices):
#     '''
#     This function takes in a question and a dict of choices.
#     The choices dict should contain an "answer" to the question
#     as the key and a function name as the value.

#     Returns the execution of the respective function based
#     on the answer given.

#     '''

#     choices_keys = list(choices.keys())

#     result = inquirer.select(
#     message=question,
#     choices=choices_keys,
#     ).execute()

#     return choices[f'{result}']()

# question = "Do you want to proceed with creating the simulated data?"
# choices = {"Yes": yes_answer, "Exit": exit_answer}

# # menu(question, choices)

# menu_1 = {
#     "Do you want to proceed with creating the simulated data?": {
#         "Yes": yes_answer,
#         "Exit": exit_answer
#     }}


# def list_select_menu(menu):

#     question = list(menu.keys())[0]
#     choices_keys = menu[question].keys()
#     result = inquirer.select(
#     message=question,
#     choices=choices_keys,
#     ).execute()

#     return choices[f'{result}']()

# # print(menu_1)
# # question = list(menu_1.keys())[0]
# # print(question)
# # choices = menu_1[question].keys()
# # print(choices)

# # list_select_menu(menu_1)


# def fuzzy_search_menu(message, choices):

#     result = inquirer.fuzzy(
#         message=message, 
#         choices=choices).execute()

#     return result


# def error_check_menu():
#     action = inquirer.fuzzy(
#         message="Select actions:",
#         choices=["hello", "weather", "what", "whoa", "hey", "yo"],
#         default="he",
#     ).execute()
#     words = inquirer.fuzzy(
#         message="Select preferred words:",
#         choices=["dave","linds","ted","sasha"],
#         multiselect=True,
#         validate=lambda result: len(result) > 1,
#         invalid_message="minimum 2 selections",
#         max_height="70%",
#     ).execute()


# error_check_menu()
    


import os

from pandas import pandas as pd
from rich import print as rprint
from rich.console import Console
from rich.table import Table

from lib.database import FX_NET_DB_TRADES_TABLE


    
def trade_count_by_client_and_trader(trade_date_filter=None):
    os.system("clear")
    trades_data = FX_NET_DB_TRADES_TABLE.get_all_values()
    df = pd.DataFrame(trades_data[1:],columns=trades_data[0])

    client_trade_counts = dict(df.groupby(["CLIENT_NAME", "CLIENT_TRADER"])["CLIENT_TRADER"].count())
    # print(client_trade_counts)
    # print(client_trade_counts.keys())
    # print(client_trade_counts.values())

    table = Table(title=f"\n\nTrades booked by Client Trader")
    table.add_column("Client Name", justify="center", style="white")
    table.add_column("Client Client Trader", justify="center", style="white")
    table.add_column("Count of Trades Booked", justify="center", style="white")

    for (client, trader), client_trade_counts in client_trade_counts.items():
        table.add_row(client, trader, str(client_trade_counts))

    console = Console()
    console.print(table)

    rprint("[cyan]Scroll to see full table if required")
    input("Press Enter to continue")

trade_count_by_client_and_trader()