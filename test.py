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
import time

from pandas import pandas as pd
from rich import print as rprint
from rich.console import Console
from rich.table import Table

from lib.database import FX_NET_DB_TRADES_TABLE, GDRIVE_CLIENT, GSPREAD_CLIENT
from lib import utils


    
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

# trade_count_by_client_and_trader()

def trade_count_by_client(trade_date_filter=False):
    os.system("clear")
    trades_data = FX_NET_DB_TRADES_TABLE.get_all_values()
    df = pd.DataFrame(trades_data[1:],columns=trades_data[0])

    dates = get_available_report_dates_by_type("trade")
    date = "All Trade Dates"
    if len(dates) == 0:
        rprint("[red]No data stored in FX Net Database")
        rprint("[red]Please load data or select another option")
        time.sleep(2)
    else:
        if trade_date_filter:
            date = utils.fuzzy_select_menu("Please select a date", dates)
            print(date)
            df = df[df['TRADE_DATE'] == date]

        client_trade_counts = list(df['CLIENT_NAME'].value_counts().items())

        trade_count_table = Table(title=f"\n\nTrade Count by Client - {date}")
        trade_count_table.add_column("Client Name", justify="center", style="white")
        trade_count_table.add_column("Count of Trades Booked", justify="center", style="white")

        for client, count_of_trades in client_trade_counts:
            trade_count_table.add_row(client,
                                    str(count_of_trades))
        console = Console()
        console.print(trade_count_table)

        rprint("[cyan]Scroll to see full table if required")
        input("Press Enter to continue")

def get_available_report_dates_by_type(value_or_trade):
    '''
    Helper function to pull out all available dates by type 
    from the TRADES table.

    Parameters: Either trade or value passed in as a string

    Returns: List of value dates or an empty list
    '''
    if value_or_trade == "value":
        date_type = "VALUE_DATE"
    else:
        date_type = "TRADE_DATE"

    all_data = FX_NET_DB_TRADES_TABLE.get_all_values()
    df = pd.DataFrame(all_data[1:],columns=all_data[0])

    value_dates = df[date_type].unique()
    if len(value_dates) > 0:
        return value_dates
    else:
        return []


def create_netting_report_by_value_date():
    """
    Creates the new file, saves it in google drive and returns
    the file id
    """
    os.system("clear")
    trades_data = FX_NET_DB_TRADES_TABLE.get_all_values()
    df = pd.DataFrame(trades_data[1:], columns=trades_data[0])
    

    dates = get_available_report_dates_by_type("value")

    if len(dates) == 0:
        rprint("[red]No data stored in FX Net Database")
        rprint("[red]Please load data or select another option")
        time.sleep(2)
    else:
        date = utils.fuzzy_select_menu("Please select a date", dates)
        df = df[df['VALUE_DATE'] == date]
        print("Creating Report for value", date)

        try:
            # Create a new file
            new_file_metadata = {
                'name': f'netting_report_vd_{date}',
                'mimeType': 'application/vnd.google-apps.spreadsheet',
            }

            permissions = {
                'type': 'user',
                'role': 'writer',
                'emailAddress': 'davidpeel.test1@gmail.com',
            }

            new_file = GDRIVE_CLIENT.files().create(body=new_file_metadata).execute()
            GDRIVE_CLIENT.permissions().create(
                fileId=new_file['id'], body=permissions).execute()
            print(f'File created with ID: {new_file["id"]}')

            headings = df.columns.tolist()
            list_of_data = df.values.tolist()


            workbook = GSPREAD_CLIENT.open_by_key(new_file["id"])
            data_sheet = workbook.add_worksheet(title="Data", rows=100, cols=20)

            rprint("[green]Adding supporting trade data")

            data_sheet.update_cell(
                1, 1, f'Netting Report for Value Date {date}')
            workbook.del_worksheet(workbook.sheet1)
            data_sheet.append_row(headings)
            data_sheet.append_rows(list_of_data)


            rprint("[green]Adding breakdown data")


            breakdown_sheet = workbook.add_worksheet(
                title="Netting Breakdown", rows=100, cols=20)

            breakdown_sheet.update_cell(
                1, 1, f'Netting Report for Value Date {date}')
            
            breakdown_sheet.append_row(["Client", "CCY", "Overall Net", "Actions"])
            netting_data = []

            df['BUY_AMT'] = pd.to_numeric(df['BUY_AMT'], errors='coerce')
            df['SELL_AMT'] = pd.to_numeric(df['SELL_AMT'], errors='coerce')

            unique_clients = df['CLIENT_NAME'].unique()
            unique_buy_ccys = list(df["BUY_CCY"].unique())
            unique_sell_ccys = list(df['SELL_CCY'].unique())
            unique_all_ccys = sorted(set(unique_buy_ccys + unique_sell_ccys))

            for client in unique_clients:
                for ccy in unique_all_ccys:
                    buy_col = df.query(
                        'CLIENT_NAME == @client and BUY_CCY == @ccy')
                    sell_col = df.query(
                        'CLIENT_NAME == @client and SELL_CCY == @ccy')
                    buy_sum = round(buy_col['BUY_AMT'].sum(), 2)
                    sell_sum = round(sell_col['SELL_AMT'].sum(), 2)
                    net = round(buy_sum + sell_sum, 2)

                    if net < 0:
                        action = f"Pay {ccy}"
                    else:
                        action = f"Receive {ccy}"

                    netting_data.append([client,
                                            ccy,
                                            "{:,.2f}".format(net),
                                            action])
            
            breakdown_sheet.append_rows(netting_data)
            rprint("[green]Data populated to file")
            time.sleep(2)

        except Exception as e:
            print(f'Error creating new file: {e}')

create_netting_report_by_value_date()