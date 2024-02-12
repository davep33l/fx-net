import os


from lib import utils


from ..trading_simulator.trading_simulator import trading_sim_menu
from ..fx_net.fx_net import fx_net_menu
from ..utils import exit_message, please_wait

def app_selector():
    print("From App Selector")

    os.system("clear")


    while True:
        response = run()
        if response == choices[0]:
            trading_sim_menu()
        elif response == choices[1]:
            fx_net_menu()
        elif response == choices[2]:
            exit_message()


from InquirerPy import inquirer

question = "Please select an option?"
choices = ["Trading Simulator", "FX Net", "Exit"]

def run():
    print("Please select the app you wish to run!\n")

    result = inquirer.select(
    message=question,
    choices=choices,
    ).execute()

    return result