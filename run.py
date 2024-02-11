# Build in imports
import os
import time
# import platform
import random
from datetime import timedelta, datetime

# Third party library imports

from rich.console import Console
from rich.table import Table
import pandas as pd
from rich import print as rprint

# Project built imports
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
    '''
    This function controls the menu system
    '''
    # First Menu
    while True:

        rprint("[cyan]Welcome to FX NET\n")
        rprint("[cyan]To simulate the output of end of day trading data")
        rprint("[cyan]from the upstream application, please run the following")
        rprint("[cyan]trade simulation program to generate the trade data.")
        rprint("[red]System Date of the Trading App will automatically be")
        rprint("[red]rolled to the next day\n")    
        rprint(f"[cyan]Current System Date is[/cyan] [green]{trading_app_sys_date}\n")

        response = menus.menu(menus.menu_1_question, menus.menu_1_choices)
    
        if response == menus.menu_1_choices[0]:
            rprint("[green]Generating trade file...please wait")
            # data, file_name = create_trade_data(trading_app_sys_date, int(random.uniform(50,150)))
            # file_id = create_output_file(data, file_name)
            data, file = trading_simulator.create_simulated_trade_data(trading_app_sys_date, int(random.uniform(50,150)))
            file_id = trading_simulator.create_and_save_output_file(data, file, get_google_clients())

            rprint("[green]Data has been successfully generated and saved")
            trading_simulator.update_system_date()
            rprint("[green]System Date of the trading application has now been rolled")
            break
        elif response == menus.menu_1_choices[1]:
            rprint("[red]The program is now exiting")
            raise SystemExit

    # Second Menus
    while True:
        # TODO: Remove the option to exit as naturally you will want to load the data in
        #       or change this so the user can select a file to upload or to exit, which will
        #       help with the data that gets loaded and allow to load data you know is missing 
        #       by selecting another file
        response = menus.menu(menus.menu_2_question, menus.menu_2_choices)
    
        if response == menus.menu_2_choices[0]:
            rprint("[green]Loading data to FX Net database...please wait")
            output_file = GSPREAD_CLIENT.open_by_key(file_id)
            data_to_move = output_file.sheet1.get_all_values()
            TRADES_DATA_WS.append_rows(data_to_move[1:])
            rprint("[green]Data has been successfully loaded into FX Net database")
            break
        elif response == menus.menu_2_choices[1]:
            rprint("[red]The program is now exiting")
            raise SystemExit

    # Third Menu
    while True:

        rprint("\nWelcome to the analsyis menu\n")
        response = menus.menu(menus.menu_3_question, menus.menu_3_choices)

        if response == menus.menu_3_choices[0]:
            date = get_most_recent_file()
            create_table(date)
        elif response == menus.menu_3_choices[1]:
            # create_report_spreadsheet("20240625")
            pass
        elif response == menus.menu_3_choices[2]:
            pass
        elif response == menus.menu_3_choices[3]:
            pass
        elif response == menus.menu_3_choices[4]:
            pass
        elif response == menus.menu_3_choices[5]:
            pass
        elif response == menus.menu_3_choices[6]:
            rprint("[red]Exiting program")
            raise SystemExit

# move to either utils or to fx_net folder
def delete_file(file_id):

    try:
        GDRIVE_CLIENT.files().delete(fileId=file_id).execute()
        print(f'File with ID {file_id} successfully deleted.')

    except Exception as e:
        print(f'Error deleting file: {e}')

# move to either utils or to fx_net folder
def get_file_list(file_name_filter=None):

    list_of_files = []
    if file_name_filter == None:
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
            if file_name_filter == None:
                print(f"{file['name']} ({file['id']})")
                # list_of_files.append((file['name'], file['id']))
                list_of_files.append((file['id']))

            elif file["name"].startswith(file_name_filter):
                print(f"{file['name']} ({file['id']})")
                # list_of_files.append((file['name'], file['id']))
                list_of_files.append((file['id']))

    return list_of_files


# move to fx_net folder
def create_table(date):
    trades_data = TRADES_DATA_WS.get_all_values()
    df = pd.DataFrame(trades_data[1:],columns=trades_data[0])
    df = df[df["VALUE_DATE"] == date]

    trade_table = Table(title=f"\n\nFX Netting Data for {date}")

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

# move to fx_net folder
def get_most_recent_file():
    trades_data = TRADES_DATA_WS.get_all_values()
    df = pd.DataFrame(trades_data[1:],columns=trades_data[0])
    unique_value_dates = df['VALUE_DATE'].unique()
    return unique_value_dates[-1]

# move to fx_net folder
def create_report_spreadsheet(value_date):
    """
    Creates the new file, saves it in google drive and returns 
    the file id
    """

    try:
        # Create a new file
        new_file_metadata = {
            'name': f'netting_report_vd_{value_date}',
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

        trades_data = TRADES_DATA_WS.get_all_values()
        df = pd.DataFrame(trades_data[1:],columns=trades_data[0])
        data = df[df['VALUE_DATE'] == value_date]
        # print(data)
        # print(type(data))
        headings = df.columns.tolist()
        list_of_data = df.values.tolist()

        workbook = GSPREAD_CLIENT.open_by_key(new_file["id"])
        data_sheet = workbook.add_worksheet(title="Data", rows=100, cols=20)
        data_sheet.update_cell(1,1, f'Netting Report for Value Date {value_date}')
        workbook.del_worksheet(workbook.sheet1)
        data_sheet.append_row(headings)
        data_sheet.append_rows(list_of_data)

        breakdown_sheet = workbook.add_worksheet(title="Netting Breakdown", rows=100, cols=20)

        breakdown_sheet.update_cell(1,1, f'Netting Report for Value Date {value_date}')

        # Add code for the format of the netting report here
        

    except Exception as e:
        print(f'Error creating new file: {e}')
    
    return new_file["id"]

from _app_selector import app_selector
from _trading_simulator import trading_simulator_menu, trading_simulator
from _utils import utils

def run():

    response = app_selector.run()

    if response == app_selector.choices[0]:
        os.system("clear")
        rprint("[green]Opening the Trading Simulator")
        utils.please_wait()
        rprint("[green]Trading App is open")
        time.sleep(2)
        os.system("clear")
        ts_response = trading_simulator_menu.run()
        if ts_response == trading_simulator_menu.choices[0]:
            rprint("[green]Generating trade file...please wait")
            data, file = trading_simulator.create_simulated_trade_data(trading_app_sys_date, int(random.uniform(50,150)))
            trading_simulator.create_and_save_output_file(data, file)
            rprint("[green]Data has been successfully generated and saved")
            trading_simulator.update_system_date()
            rprint("[green]System Date of the trading application has now been rolled")
        elif ts_response == trading_simulator_menu.choices[1]:
            rprint("[red]The program is now exiting")
            utils.please_wait()
            rprint("Goodbye!")
            time.sleep(1)
            os.system("clear")
            raise SystemExit
    elif response == app_selector.choices[1]:
        rprint("[green]Opening the FX Net Application")
        utils.please_wait()
        rprint("[green]FX Net is open") # call the FX Net app here
    elif response == app_selector.choices[2]:
        rprint("[red]The program is now exiting")
        utils.please_wait()
        rprint("Goodbye!")
        time.sleep(1)
        os.system("clear")
        raise SystemExit

    input("Press any key to exit: ")


if __name__ == "__main__":
    run()
    # main()
    # # files = get_file_list("netting_report")
    # files = get_file_list("trade_data")

    # for file in files:
    #     delete_file(file)
    # files = get_file_list()
    # print(get_most_recent_file())
    # create_report_spreadsheet(get_most_recent_file())
    # pass
