# Build in imports
import os
import platform
import random

# Third party library imports
import gspread
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build

# Project built imports
from trade_file_generation import create_trade_data, write_to_csv

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]


CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)

# Google Sheets and Drive client connections
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
GDRIVE_CLIENT = build('drive', 'v3',credentials=SCOPED_CREDS)

# Main Database workbook connection
DATABASE_WORKBOOK = GSPREAD_CLIENT.open('fx-net-data')

# Worksheet connections
TRADES_DATA_WS = DATABASE_WORKBOOK.worksheet("TRADES")
SYSTEM_INFO_WS = DATABASE_WORKBOOK.worksheet("SYSTEM_INFO")

# Variable connections from worksheets
trading_app_sys_date = SYSTEM_INFO_WS.range("A2")[0].value

def main():  

    while True:

        print("Welcome to FX NET\n")
        print("To simulate the output of end of day trading data")
        print("from the upstream application, please run the following")
        print("trade simulation program to generate the trade data.\n")

        response = input("Please press Y proceed and hit enter: ")
        if response.lower() == "y":
            print("you pressed yes")
            result = create_trade_data(trading_app_sys_date, int(random.uniform(50,150)))
            write_to_csv(result)
            break
        elif response.lower() == "n":
            print("you pressed no")
            break
        else:
            if platform.system() == "Windows":
                os.system("cls")
            else:
                os.system("clear")
            print("your input was incorrect, please press Y or N")

if __name__ == "__main__":
    main()


