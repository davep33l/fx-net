''''
TBD
'''
# Build in imports
import os
import time
import random
# from datetime import timedelta, datetime

# Third party library imports
from rich.console import Console
from rich.table import Table
import pandas as pd
from rich import print as rprint

# Project built imports
from google_client_manager import get_google_clients
import menus
from _app_selector import app_selector
from _trading_simulator import trading_simulator_menu, trading_simulator
from _utils import utils

from lib import app_selector, trading_simulator, fx_net, utils


GSPREAD_CLIENT, GDRIVE_CLIENT = get_google_clients()
DATABASE_WORKBOOK = GSPREAD_CLIENT.open('fx_net_db')
DATABASE_WORKBOOK_TA = GSPREAD_CLIENT.open('trading_simulator_db')

# Worksheet connections
TRADES_DATA_WS = DATABASE_WORKBOOK.worksheet("TRADES")
FILES_LOADED_WS = DATABASE_WORKBOOK.worksheet("FILES_LOADED")
SYSTEM_INFO_WS = DATABASE_WORKBOOK_TA.worksheet("SYSTEM_INFO")

# Variable connections from worksheets
trading_app_sys_date = SYSTEM_INFO_WS.range("A2")[0].value

def run():
    '''
    TBD
    '''
    # os.system("clear")


    # while True:
    #     response = app_selector.run()
    #     if response == app_selector.choices[0]:
    #         trading_sim_menu()
    #     elif response == app_selector.choices[1]:
    #         fx_net_menu()
    #     elif response == app_selector.choices[2]:
    #         exit_message()

    app_selector.app_selector()

    # input("Press enter key to exit: ")

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
        rep_response = menus.menu(menus.menu_3_question, menus.menu_3_choices)

        if rep_response == menus.menu_3_choices[0]:
            create_table()
        elif rep_response == menus.menu_3_choices[1]:
            # create_report_spreadsheet("20240625")
            pass
        elif rep_response == menus.menu_3_choices[2]:
            pass
        elif rep_response == menus.menu_3_choices[3]:
            pass
        elif rep_response == menus.menu_3_choices[4]:
            pass
        elif rep_response == menus.menu_3_choices[5]:
            pass
        elif rep_response == menus.menu_3_choices[6]:
            print("Returning previous menu")
            time.sleep(1)
            os.system("clear")
            return

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

        fx_net_response = menus.menu(menus.menu_2_question, menus.menu_2_choices)
        if fx_net_response == menus.menu_2_choices[0]:
            load_fx_data()
        elif fx_net_response == menus.menu_2_choices[1]:
            reporting_menu()
            break
        elif fx_net_response == menus.menu_2_choices[2]:
            print("Returning previous menu")
            time.sleep(1)
            os.system("clear")
            break

# Move to fx_net folder
def get_trade_data_files_list():
    '''
    This functions retrieves a list of trade data files from the database.

    Returns: 
        List of tuples containing file_name and file_id if files present.
        If no files present, returns empty list.

    Example:
        trade_files = [(file_name1, file_id1), (file_name2, file_id2)].
    '''
    trade_files = []

    file_name_filter = "trade_data"

    g_drive_file_request = GDRIVE_CLIENT.files().list().execute()
    all_files = g_drive_file_request.get('files', [])

    if not all_files:
        return trade_files
    else:
        for file in all_files:
            if file_name_filter == None:
                trade_files.append((file['name'], file['id']))
            elif file["name"].startswith(file_name_filter):
                trade_files.append((file['name'], file['id']))

    return trade_files

# Move to fx_net folder
def get_files_already_loaded():
    '''
    This function checks the fx_net_db table of FILES_LOADED
    and returns a list of file ids that have already been
    used/loaded by the FX Net Application.

    Returns: List of file_ids in FILES_LOADED table
    '''
    
    files_loaded = FILES_LOADED_WS.get_all_values()
    df = pd.DataFrame(files_loaded[1:],columns=files_loaded[0])
    file_ids_loaded = df['FILE_ID'].tolist()

    return file_ids_loaded

# Move to fx_net folder
def get_eligible_files_to_load():
    '''
    This function gets a list of already loaded file id's
    and compares it against a list (of tuples) of files available
    to load and creates a list of files that haven't yet 
    been loaded into FX Net.

    Returns: List of eligible files to load
    '''

    files_already_loaded = get_files_already_loaded()
    files_to_load = get_trade_data_files_list()
    # print(files_already_loaded)
    # print(files_to_load)

    eligible_files = []
    for file in files_to_load:
        if file[1] not in files_already_loaded:
            eligible_files.append(file)
    # print(eligible_files)

    return eligible_files

# Move to fx_net folder
def load_fx_data():
    '''
    This function first checks if the available files in the shared folder
    have already been loaded and returns a list of files that have not
    been loaded into FX Net yet. 
    It gives the user a prompt to select the file they wish to load, if there 
    are no files available to load it informs the user and returns to the
    menu. 
    Once the file is loaded, the file name, trade date and file id are
    added to the FILES_LOADED table, so it can be checked next time the
    function is run. 

    '''

    file_data = get_eligible_files_to_load()
    file_names = [file_name[0] for file_name in file_data]

    if not file_names:
        rprint("[red]No more data to load")
        rprint("[red]Please choose another option")
        time.sleep(2)
    else:
        choice = menus.menu("Pick a file to load", file_names)
        print(choice)

        for file in file_data:
            if file[0] == choice:
                chosen_file_id = file[1]

        rprint("[green]Loading data to FX Net database...please wait")
        
        # NOTE1: temporary code to get file id is in the above code, 
        # will refactor into a date selection
        # so that the apps can run independantly and give options for 
        #user to select a date to load
        output_file = GSPREAD_CLIENT.open_by_key(chosen_file_id)
        data_to_move = output_file.sheet1.get_all_values()
        TRADES_DATA_WS.append_rows(data_to_move[1:])
        rprint("[green]Data has been successfully loaded into FX Net database")

        file_trade_date = choice[-8:]
        FILES_LOADED_WS.append_row([choice, file_trade_date, chosen_file_id])

# Move to utils folder
def exit_message():
    '''
    TBD
    '''
    rprint("[red]The program is now exiting")
    utils.please_wait()
    rprint("Goodbye!")
    time.sleep(1)
    os.system("clear")

    raise SystemExit

# # Move to trading_simulator folder
# def trading_sim_menu():
#     '''
#     TBD
#     '''
#     os.system("clear")
#     rprint("[green]Opening the Trading Simulator")
#     utils.please_wait()
#     rprint("[green]Trading App is open")
#     time.sleep(2)
#     os.system("clear")

#     while True:
#         ts_response = trading_simulator_menu.run()
#         if ts_response == trading_simulator_menu.choices[0]:

#             rprint("[green]Generating trade file...please wait")
#             data, file = trading_simulator.create_simulated_trade_data(int(random.uniform(50,150)))
#             global file_id
#             file_id = trading_simulator.create_and_save_output_file(data, file) # NOTE1
#             rprint("[green]Data has been successfully generated and saved")
#             trading_simulator.update_system_date()
#             rprint("[green]System Date of the trading application has now been rolled")
#             time.sleep(1)


#             # rprint("[cyan]You will now be automatically logged into FX Net")

#             # while True:
#             #     fx_net_response = menus.menu(menus.menu_2_question, menus.menu_2_choices)
#             #     if fx_net_response == menus.menu_2_choices[0]:
#             #         load_fx_data()
#             #     elif fx_net_response == menus.menu_2_choices[1]:
#             #         reporting_menu()
#             #     elif fx_net_response == menus.menu_2_choices[2]:
#             #         break
#         elif ts_response == trading_simulator_menu.choices[1]:
#             print("Returning to main menu")
#             time.sleep(1)
#             os.system("clear")
#             break

# move to either utils or to fx_net folder
def delete_file(file_id):
    '''
    TBD
    '''
    try:
        GDRIVE_CLIENT.files().delete(fileId=file_id).execute()
        print(f'File with ID {file_id} successfully deleted.')

    except Exception as e:
        print(f'Error deleting file: {e}')

# move to either utils or to fx_net folder
def get_file_list(file_name_filter=None):
    '''
    TBD
    '''
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
def create_table():
    '''
    TBD
    '''
    dates = get_available_report_value_dates()

    if len(dates) == 0:
        rprint("[red]No data stored in FX Net Database")
        rprint("[red]Please load data or select another option")
        time.sleep(2)
    else:
        date = menus.menu_fuzzy("Type or select a date: ", dates)

        os.system("clear")
        trades_data = TRADES_DATA_WS.get_all_values()
        df = pd.DataFrame(trades_data[1:],columns=trades_data[0])
        df = df[df["VALUE_DATE"] == date]

        trade_table = Table(title=f"\n\nFX Netting Data for {date}")

        trade_table.add_column("Client", justify="center", style="green", no_wrap=True)
        trade_table.add_column("CCY", justify="center", style="cyan")
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

        rprint("[cyan]Scroll to see full table if required")
        input("Press Enter to continue")

# move to fx_net folder
def get_most_recent_file():
    '''
    TBD
    '''
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

# Move to fx_net folder
def get_available_report_value_dates():

    all_data = TRADES_DATA_WS.get_all_values()
    df = pd.DataFrame(all_data[1:],columns=all_data[0])

    
    value_dates = df['VALUE_DATE'].unique()
    if len(value_dates) > 0:
        return value_dates
    else:
        return []

if __name__ == "__main__":
    run()

    # INTERIM HELPERS TO DELETE FILES FROM GDRIVE DURING DEVELOPMENT
    # # files = get_file_list("netting_report")
    # files = get_file_list("trade_data")

    # for file in files:
    #     delete_file(file)
    # files = get_file_list()
    # print(get_most_recent_file())
    # create_report_spreadsheet(get_most_recent_file())
    # pass

    # trade_files = get_trade_data_files_list()
    # print(trade_files)

    # get_files_already_loaded()
    # file_data = get_eligible_files_to_load()
    # file_names = [file_name[0] for file_name in file_data]
    
    # choice = menus.menu("Pick a file to load", file_names)
    # print(choice)

    # for file in file_data:
    #     if file[0] == choice:
    #         file_id = file[1]


    # print(file_id)

    # result = get_available_report_value_dates()
    # print(result)