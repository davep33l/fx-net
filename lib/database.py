from . import utils

GSPREAD_CLIENT, GDRIVE_CLIENT = utils.get_google_clients()
DATABASE_WORKBOOK = GSPREAD_CLIENT.open('fx_net_db')
DATABASE_WORKBOOK_TA = GSPREAD_CLIENT.open('trading_simulator_db')

# Worksheet connections
TRADES_DATA_WS = DATABASE_WORKBOOK.worksheet("TRADES")
FILES_LOADED_WS = DATABASE_WORKBOOK.worksheet("FILES_LOADED")
SYSTEM_INFO_WS = DATABASE_WORKBOOK_TA.worksheet("SYSTEM_INFO")