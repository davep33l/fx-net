# Build in imports
import os
import platform
import random
from datetime import timedelta, datetime

# Third party library imports
import gspread
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build

# Project built imports
from trade_file_generation import create_trade_data

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

        print("1. Proceed with creating simulated data")
        print("2. To Exit the program")

        response = input("Press a number and enter to continue: ")
        if response.lower() == "1":
            print("You selected option 1")
            result = create_trade_data(trading_app_sys_date, int(random.uniform(50,150)))
            file_id = create_output_file(result)
            print("Data has been successfully generated and saved")
            update_system_date()
            print("System Date of the trading application has now been rolled")
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
            pass
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

def create_output_file(data):
    """
    Creates the new file, saves it in google drive and returns 
    the file id
    """

    new_file_name = f'trade_data_{data[1][-3]}'

    try:
        # Create a new file
        new_file_metadata = {
            'name': new_file_name,
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

        return new_file["id"]

    except Exception as e:
        print(f'Error creating new file: {e}')

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

if __name__ == "__main__":
    main()



