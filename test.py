
import os
import time

from pandas import pandas as pd
from rich import print as rprint
from rich.console import Console
from rich.table import Table

from lib.database import FX_NET_DB_TRADES_TABLE, GDRIVE_CLIENT, GSPREAD_CLIENT, FX_NET_DB_PAYMENTS_INX_TABLE
from lib import utils
from lib.fx_net.fx_net import get_available_report_dates_by_type

def create_payment_files():
    
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
                'name': f'payment_report_vd_{date}',
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

            workbook = GSPREAD_CLIENT.open_by_key(new_file["id"])
            breakdown_sheet = workbook.add_worksheet(title="Payment Report", rows=100, cols=20)
            workbook.del_worksheet(workbook.sheet1)

            # breakdown_sheet.append_row(["Client", "CCY", "OVERALL_NET", "ACTIONS"])
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

            netting_df = pd.DataFrame(netting_data[:], columns=["CLIENT_NAME", "CCY", "OVERALL_NET", "ACTIONS"])
            netting_df['OVERALL_NET'] = pd.to_numeric(netting_df['OVERALL_NET'].str.replace(',', ''), errors='coerce')

            netting_df.drop('ACTIONS', axis='columns', inplace=True)

            # print(netting_df)
            # print(netting_df['OVERALL_NET'].apply(type))
            # print(netting_df)

            payment_inx = FX_NET_DB_PAYMENTS_INX_TABLE.get_all_values()
            pmt_df = pd.DataFrame(payment_inx[1:], columns=payment_inx[0])
            # print(pmt_df)

            result = pd.merge(netting_df, pmt_df, on=['CLIENT_NAME', 'CCY'], how='inner')

            only_payments = result.loc[result['OVERALL_NET'] < 0]

            print(only_payments)

            data_for_gspread = only_payments.values.tolist()
            print(data_for_gspread)

            breakdown_sheet.append_rows(data_for_gspread)

            input("Press Enter to continue")

        except Exception as e:
            print(f'Error creating new file: {e}')

create_payment_files()