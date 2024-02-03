# Build in imports
import os
import platform
import random

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

        response = input("Please press Y proceed and hit enter: ")
        if response.lower() == "y":
            print("you pressed yes")
            result = create_trade_data(trading_app_sys_date, int(random.uniform(50,150)))
            create_output_file(result)
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

def create_output_file(data):

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

if __name__ == "__main__":
    main()
    show_file_list()



