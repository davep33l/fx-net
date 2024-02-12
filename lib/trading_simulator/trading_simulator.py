import os
import time
import random
from rich import print as rprint

from lib import utils

def trading_simulator():
    print("From Trading Simulator")

# Move to trading_simulator folder
def trading_sim_menu():
    '''
    TBD
    '''
    os.system("clear")
    rprint("[green]Opening the Trading Simulator")
    utils.please_wait()
    rprint("[green]Trading App is open")
    time.sleep(2)
    os.system("clear")

    while True:
        ts_response = run()
        if ts_response == choices[0]:

            rprint("[green]Generating trade file...please wait")
            data, file = trading_simulator.create_simulated_trade_data(int(random.uniform(50,150)))
            global file_id
            file_id = trading_simulator.create_and_save_output_file(data, file) # NOTE1
            rprint("[green]Data has been successfully generated and saved")
            trading_simulator.update_system_date()
            rprint("[green]System Date of the trading application has now been rolled")
            time.sleep(1)


            # rprint("[cyan]You will now be automatically logged into FX Net")

            # while True:
            #     fx_net_response = menus.menu(menus.menu_2_question, menus.menu_2_choices)
            #     if fx_net_response == menus.menu_2_choices[0]:
            #         load_fx_data()
            #     elif fx_net_response == menus.menu_2_choices[1]:
            #         reporting_menu()
            #     elif fx_net_response == menus.menu_2_choices[2]:
            #         break
        elif ts_response == choices[1]:
            print("Returning to main menu")
            time.sleep(1)
            os.system("clear")
            break

from InquirerPy import inquirer

question = "Do you want to proceed with creating the simulated data?"
choices = ["Yes", "No (previous menu)"]

def run():

    result = inquirer.select(
    message=question,
    choices=choices,
    ).execute()

    return result