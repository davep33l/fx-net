from . import utils

GSPREAD_CLIENT, GDRIVE_CLIENT = utils.get_google_clients()

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
