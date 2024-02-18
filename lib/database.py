'''
Database related constant tables for access throughout the program
'''

import gspread
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build


def get_google_clients():
    """
    Function that creates a Google Spreadsheet client and
    creates a Google Drive client that have been authenticated.

    Returns a tuple of clients:
    GSPREAD_CLIENT and GDRIVE_CLIENT
    """

    scope = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive.file",
        "https://www.googleapis.com/auth/drive"
    ]

    creds = Credentials.from_service_account_file('creds.json')
    scoped_creds = creds.with_scopes(scope)
    # Google Sheets and Drive client connections
    gspread_client = gspread.authorize(scoped_creds)
    gdrive_client = build('drive', 'v3', credentials=scoped_creds)

    return gspread_client, gdrive_client


# Google Client connections
GSPREAD_CLIENT, GDRIVE_CLIENT = get_google_clients()

# FX Net database connection
FX_NET_DB = GSPREAD_CLIENT.open('fx_net_db')


# FX Net table connections
FX_NET_DB_TRADES_TABLE = FX_NET_DB.worksheet("TRADES")
FX_NET_DB_FILES_LOADED_TABLE = FX_NET_DB.worksheet("FILES_LOADED")
FX_NET_DB_PAYMENTS_INX_TABLE = FX_NET_DB.worksheet("PAYMENT_INX")


# Trading Simulator connection
TRADING_SIMULATOR_DB = GSPREAD_CLIENT.open('trading_simulator_db')


# Trading Simulator connections
TRADING_SIMULATOR_DB_SYSTEM_INFO_TABLE = TRADING_SIMULATOR_DB.worksheet(
    "SYSTEM_INFO")
