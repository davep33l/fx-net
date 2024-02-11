import google_client_manager
from _trading_simulator import trading_simulator as trading_app
import pandas as pd


clients = google_client_manager.get_google_clients()

DATABASE_WORKBOOK = clients[0].open('fx-net-data')

# Worksheet connections
USERS = DATABASE_WORKBOOK.worksheet("USERS").get_all_values()
print(USERS)

df = pd.DataFrame(USERS[1:], columns=USERS[0])

data, file = trading_app.create_simulated_trade_data("20240424",10)

email = input("please provide email: ")

if email in df.values:
    print("yes")
    trading_app.create_and_save_output_file(data, file, clients, email)
else:
    print("Please use a valid user account to store the files")


