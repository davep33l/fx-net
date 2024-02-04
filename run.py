# Build in imports
import os
import platform
import random
from datetime import timedelta, datetime

# Third party library imports

from rich.console import Console
from rich.table import Table
import pandas as pd
from rich import print as rprint

# Project built imports
from trade_file_generation import create_trade_data
from google_client_manager import get_google_clients
import menus

GSPREAD_CLIENT, GDRIVE_CLIENT = get_google_clients()
DATABASE_WORKBOOK = GSPREAD_CLIENT.open('fx-net-data')

# Worksheet connections
TRADES_DATA_WS = DATABASE_WORKBOOK.worksheet("TRADES")
SYSTEM_INFO_WS = DATABASE_WORKBOOK.worksheet("SYSTEM_INFO")

# Variable connections from worksheets
trading_app_sys_date = SYSTEM_INFO_WS.range("A2")[0].value

def main():  

    while True:

        rprint("[cyan]Welcome to FX NET\n")
        rprint("[cyan]To simulate the output of end of day trading data")
        rprint("[cyan]from the upstream application, please run the following")
        rprint("[cyan]trade simulation program to generate the trade data.\n")

        rprint(f"[cyan]Current System Date is[/cyan] [green]{trading_app_sys_date}\n")

        response = menus.menu(menus.menu_1_question, menus.menu_1_choices)
    
        if response == "Yes":

            rprint("[red]Generating trade file...please wait")

            data, file_name = create_trade_data(trading_app_sys_date, int(random.uniform(50,150)))
            file_id = create_output_file(data, file_name)

            print("Data has been successfully generated and saved")

            update_system_date()

            print("System Date of the trading application has now been rolled")

            break

        elif response == "No":

            rprint("[red]The program is now exiting")

            raise SystemExit

    while True:
        print("Do you want to load the data into FX Net program\n")
        print("1. Yes, load data")
        print("2. Exit the program")

        response = input("Press a number and enter to continue: ")
        if response.lower() == "1":
            print("You selected option 1")
            output_file = GSPREAD_CLIENT.open_by_key(file_id)
            data_to_move = output_file.sheet1.get_all_values()
            TRADES_DATA_WS.append_rows(data_to_move[1:])
            print("Data has been successfully loaded into FX Net database")
            break
        elif response.lower() == "2":
            print("You selected option 2")
            print("The program is now exiting")
            raise SystemExit
        else:
            print("Incorrect input, please select valid option")
            if platform.system() == "Windows":
                os.system("cls")
            else:
                os.system("clear")

    while True:

        print("welcome to the analsyis menu")
        print("1. Create Netting report")
        print("2. Create payment files")
        print("3. Show trade count by clients")
        print("4. Show trade count by client and client trader")
        print("5. Show trade count by bank trader")
        print("6. Exit program")

        response = input("Please select an option and press enter: ")

        if response == "1":
            create_table()
        elif response == "2":
            pass
        elif response == "3":
            pass
        elif response == "4":
            pass
        elif response == "5":
            pass
        elif response == "6":
            print("Exiting program")
            raise SystemExit

def create_output_file(data, file_name):
    """
    Creates the new file, saves it in google drive and returns 
    the file id
    """

    try:
        # Create a new file
        new_file_metadata = {
            'name': file_name,
            'mimeType': 'application/vnd.google-apps.spreadsheet',
        }

        permissions = {
            'type': 'user',
            'role': 'writer',
            'emailAddress': 'davidpeel.test1@gmail.com',
        }

        new_file = GDRIVE_CLIENT.files().create(body=new_file_metadata).execute()
        GDRIVE_CLIENT.permissions().create(fileId=new_file['id'],body=permissions).execute()
        print(f'File created with ID: {new_file["id"]}')

        workbook = GSPREAD_CLIENT.open_by_key(new_file["id"])
        sheet = workbook.sheet1
        sheet.append_rows(data)

    except Exception as e:
        print(f'Error creating new file: {e}')
    
    return new_file["id"]

def delete_file(file_id):

    try:
        GDRIVE_CLIENT.files().delete(fileId=file_id).execute()
        print(f'File with ID {file_id} successfully deleted.')

    except Exception as e:
        print(f'Error deleting folder: {e}')

def show_file_list():

    print('Files in Google Drive:')
    results = GDRIVE_CLIENT.files().list().execute()
    files = results.get('files', [])
    if not files:
        print('No files found in Google Drive.')
    else:
        for file in files:
            print(f"{file['name']} ({file['id']})")

def update_system_date():
    trading_app_sys_date_ISO_format = datetime.strptime(trading_app_sys_date, "%Y%m%d")

    new_trading_app_sys_date = trading_app_sys_date_ISO_format + timedelta(1)

    while new_trading_app_sys_date.weekday() >= 5:
        new_trading_app_sys_date += timedelta(days=1)

    sys_date_string = new_trading_app_sys_date.strftime("%Y%m%d")
    SYSTEM_INFO_WS.update_acell('A2', sys_date_string)

def create_table():
    trades_data = TRADES_DATA_WS.get_all_values()
    df = pd.DataFrame(trades_data[1:],columns=trades_data[0])

    trade_table = Table(title="\n\nFX Netting Data")

    trade_table.add_column("Client", justify="center", style="green", no_wrap=True)
    trade_table.add_column("CCY", justify="center", style="cyan")
    # trade_table.add_column("Net Buy", justify="center", style="green")
    # trade_table.add_column("Net Sell", justify="center", style="red")
    trade_table.add_column("Overall Net", justify="center", style="white")
    trade_table.add_column("Actions", justify="center", style="white")

    df['BUY_AMT'] = pd.to_numeric(df['BUY_AMT'], errors='coerce')
    df['SELL_AMT'] = pd.to_numeric(df['SELL_AMT'], errors='coerce')

    unique_clients = df['CLIENT_NAME'].unique()
    unique_buy_ccys = list(df["BUY_CCY"].unique())
    unique_sell_ccys = list(df['SELL_CCY'].unique())
    unique_all_ccys = sorted(set(unique_buy_ccys + unique_sell_ccys))

    for client in unique_clients:
        for ccy in unique_all_ccys:
            buy_col = df.query('CLIENT_NAME == @client and BUY_CCY == @ccy')
            sell_col = df.query('CLIENT_NAME == @client and SELL_CCY == @ccy')
            buy_sum = round(buy_col['BUY_AMT'].sum(),2)
            sell_sum = round(sell_col['SELL_AMT'].sum(),2)
            net = round(buy_sum + sell_sum,2)

            if net < 0:
                action = f"pay {ccy}"
            else:
                action = f"receive {ccy}"

            # trade_table.add_row(client, ccy, "{:,.2f}".format(buy_sum), "{:,.2f}".format(sell_sum), "{:,.2f}".format(net), action)
            trade_table.add_row(client, ccy, "{:,.2f}".format(net), action)

        
    console = Console()
    console.print(trade_table)


if __name__ == "__main__":
    main()
    # create_table()



