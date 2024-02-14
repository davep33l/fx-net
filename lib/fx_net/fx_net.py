'''
TBD
'''

import os
import time
from rich import print as rprint
from rich.console import Console
from rich.table import Table
import pandas as pd

from lib import utils
from lib.database import GDRIVE_CLIENT, GSPREAD_CLIENT
from lib.database import FX_NET_DB_TRADES_TABLE, FX_NET_DB_FILES_LOADED_TABLE
from lib.app_selector import app_selector

# Move to fx_net folder


def fx_net_menu():
    '''
    TBD
    '''
    rprint("[green]Opening the FX Net Application")
    utils.please_wait()
    os.system("clear")
    rprint("[green]FX Net is open")
    time.sleep(1)
    while True:
        os.system("clear")
        rprint("[cyan]--- FX NET ---\n")
        rprint("[bold underline]Main Menu\n")

        fx_net_menu_question = {
            "Please select an option?": {
                "Load FX Data to FX Net Database": load_fx_data,
                "Reporting Menu": reporting_menu,
                "Return to previous menu": return_to_previous_menu,
                "Exit Program": utils.exit_message,
            }}
        utils.list_select_menu(fx_net_menu_question)

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
        rprint("[cyan]--- FX NET ---\n")
        rprint("Reporting / Analysis Menu\n")

        reporting_menu_question = {
            "Please select an option?": {
                "Netting Summary by Value Date": netting_summary_by_value_date,
                "Create Netting Report by Value Date (WIP)": create_netting_report_by_value_date,
                "Create payment files (WIP)": reporting_menu,
                "Trade count by Client - All Trade Dates": trade_count_by_client,
                "Trade count by Client - Trade Date Selector": trade_count_by_client_selector,
                "Trade count by Client and Client Trader": trade_count_by_client_and_trader,
                "Trade count by Bank Trader": trade_count_by_bank_trader,
                "Return to FX Net Main Menu": fx_net_menu,
                "Exit Program": utils.exit_message,
            }}
        utils.list_select_menu(reporting_menu_question)


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
        choice = utils.fuzzy_select_menu("Pick a file to load", file_names)
        print(choice)

        for file in file_data:
            if file[0] == choice:
                chosen_file_id = file[1]

        rprint("[green]Loading data to FX Net database...please wait")
        output_file = GSPREAD_CLIENT.open_by_key(chosen_file_id)
        data_to_move = output_file.sheet1.get_all_values()
        FX_NET_DB_TRADES_TABLE.append_rows(data_to_move[1:])
        rprint("[green]Data has been successfully loaded into FX Net database")

        file_trade_date = choice[-8:]
        FX_NET_DB_FILES_LOADED_TABLE.append_row(
            [choice, file_trade_date, chosen_file_id])


def return_to_previous_menu():
    '''
    Returns to the app_selector menu.
    '''
    print("Returning previous menu")
    time.sleep(1)
    os.system("clear")
    app_selector.run()

# Move to fx_net folder (uses a client)


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
            if file_name_filter is None:
                trade_files.append((file['name'], file['id']))
            elif file["name"].startswith(file_name_filter):
                trade_files.append((file['name'], file['id']))

    return trade_files


def get_files_already_loaded():
    '''
    This function checks the fx_net_db table of FILES_LOADED
    and returns a list of file ids that have already been
    used/loaded by the FX Net Application.

    Returns: List of file_ids in FILES_LOADED table
    '''

    files_loaded = FX_NET_DB_FILES_LOADED_TABLE.get_all_values()
    df = pd.DataFrame(files_loaded[1:], columns=files_loaded[0])
    file_ids_loaded = df['FILE_ID'].tolist()

    return file_ids_loaded


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

# move to either utils or to fx_net folder (uses a client)


def delete_file(file_id):
    '''
    TBD
    '''
    try:
        GDRIVE_CLIENT.files().delete(fileId=file_id).execute()
        print(f'File with ID {file_id} successfully deleted.')

    except Exception as e:
        print(f'Error deleting file: {e}')

# move to either utils or to fx_net folder (uses a client)


def get_file_list(file_name_filter=None):
    '''
    TBD
    '''
    list_of_files = []
    if file_name_filter is None:
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
            if file_name_filter is None:
                print(f"{file['name']} ({file['id']})")
                # list_of_files.append((file['name'], file['id']))
                list_of_files.append((file['id']))

            elif file["name"].startswith(file_name_filter):
                print(f"{file['name']} ({file['id']})")
                # list_of_files.append((file['name'], file['id']))
                list_of_files.append((file['id']))

    return list_of_files

# move to fx_net folder (uses a client)


def netting_summary_by_value_date():
    '''
    TBD
    '''
    dates = get_available_report_dates_by_type("value")

    if len(dates) == 0:
        rprint("[red]No data stored in FX Net Database")
        rprint("[red]Please load data or select another option")
        time.sleep(2)
    else:
        date = utils.fuzzy_select_menu("Type or select a date: ", dates)

        os.system("clear")
        trades_data = FX_NET_DB_TRADES_TABLE.get_all_values()
        df = pd.DataFrame(trades_data[1:], columns=trades_data[0])
        df = df[df["VALUE_DATE"] == date]

        trade_table = Table(title=f"\n\nFX Netting Data for {date}")

        trade_table.add_column(
            "Client",
            justify="center",
            style="green",
            no_wrap=True)
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
                buy_col = df.query(
                    'CLIENT_NAME == @client and BUY_CCY == @ccy')
                sell_col = df.query(
                    'CLIENT_NAME == @client and SELL_CCY == @ccy')
                buy_sum = round(buy_col['BUY_AMT'].sum(), 2)
                sell_sum = round(sell_col['SELL_AMT'].sum(), 2)
                net = round(buy_sum + sell_sum, 2)

                if net < 0:
                    action = f"pay {ccy}"
                else:
                    action = f"receive {ccy}"

                trade_table.add_row(client,
                                    ccy,
                                    "{:,.2f}".format(net),
                                    action)

        console = Console()
        console.print(trade_table)

        rprint("[cyan]Scroll to see full table if required")
        input("Press Enter to continue")

# move to fx_net folder (uses a client)


def get_most_recent_file():
    '''
    TBD
    '''
    trades_data = FX_NET_DB_TRADES_TABLE.get_all_values()
    df = pd.DataFrame(trades_data[1:], columns=trades_data[0])
    unique_value_dates = df['VALUE_DATE'].unique()
    return unique_value_dates[-1]

# move to fx_net folder (uses a client)


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

        # print("Creating Report for value", date)
        # print(df)
        # input("Press Enter to continue")

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

            # trades_data = FX_NET_DB_TRADES_TABLE.get_all_values()
            # df = pd.DataFrame(trades_data[1:], columns=trades_data[0])
            # data = df[df['VALUE_DATE'] == date]
            # print(data)
            # print(type(data))
            headings = df.columns.tolist()
            list_of_data = df.values.tolist()

            workbook = GSPREAD_CLIENT.open_by_key(new_file["id"])
            data_sheet = workbook.add_worksheet(title="Data", rows=100, cols=20)
            data_sheet.update_cell(
                1, 1, f'Netting Report for Value Date {date}')
            workbook.del_worksheet(workbook.sheet1)
            data_sheet.append_row(headings)
            data_sheet.append_rows(list_of_data)

            breakdown_sheet = workbook.add_worksheet(
                title="Netting Breakdown", rows=100, cols=20)

            breakdown_sheet.update_cell(
                1, 1, f'Netting Report for Value Date {date}')

            # Add code for the format of the netting report here
        except Exception as e:
            print(f'Error creating new file: {e}')

        


def trade_count_by_client(trade_date_filter=False):
    os.system("clear")
    trades_data = FX_NET_DB_TRADES_TABLE.get_all_values()
    df = pd.DataFrame(trades_data[1:], columns=trades_data[0])

    dates = get_available_report_dates_by_type("trade")
    date = "All Trade Dates"
    if len(dates) == 0:
        rprint("[red]No data stored in FX Net Database")
        rprint("[red]Please load data or select another option")
        time.sleep(2)
    else:
        if trade_date_filter:
            date = utils.fuzzy_select_menu("Please select a date", dates)
            df = df[df['TRADE_DATE'] == date]

        client_trade_counts = list(df['CLIENT_NAME'].value_counts().items())

        table = Table(title=f"\n\nTrade Count by Client - {date}")
        table.add_column("Client Name", justify="center", style="white")
        table.add_column(
            "Count of Trades Booked",
            justify="center",
            style="white")

        for client, count_of_trades in client_trade_counts:
            table.add_row(client, str(count_of_trades))
        console = Console()
        console.print(table)

        rprint("[cyan]Scroll to see full table if required")
        input("Press Enter to continue")


def trade_count_by_client_selector():
    trade_count_by_client(True)


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
    df = pd.DataFrame(all_data[1:], columns=all_data[0])

    value_dates = df[date_type].unique()
    if len(value_dates) > 0:
        return value_dates
    else:
        return []


def trade_count_by_client_and_trader(trade_date_filter=None):
    os.system("clear")
    trades_data = FX_NET_DB_TRADES_TABLE.get_all_values()
    df = pd.DataFrame(trades_data[1:], columns=trades_data[0])

    client_trade_counts = dict(df.groupby(["CLIENT_NAME", "CLIENT_TRADER"])[
                               "CLIENT_TRADER"].count())

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


def trade_count_by_bank_trader(trade_date_filter=None):
    os.system("clear")
    trades_data = FX_NET_DB_TRADES_TABLE.get_all_values()
    df = pd.DataFrame(trades_data[1:], columns=trades_data[0])

    bank_trader_trade_counts = list(df['BANK_TRADER'].value_counts().items())

    table = Table(title=f"\n\nTrade Count by Bank Trader")
    table.add_column("Bank Trader Name", justify="center", style="white")
    table.add_column("Count of Trades Booked", justify="center", style="white")

    for client, count_of_trades in bank_trader_trade_counts:
        table.add_row(client, str(count_of_trades))
    console = Console()
    console.print(table)

    rprint("[cyan]Scroll to see full table if required")
    input("Press Enter to continue")
