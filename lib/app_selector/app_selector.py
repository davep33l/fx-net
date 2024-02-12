'''
This module serves as an orchestration menu to select the relevant
application you wish to run.
'''
#Build in imports
import os

# Module imports
from ..trading_simulator.trading_simulator import trading_sim_menu
from ..fx_net.fx_net import fx_net_menu
from ..utils import exit_message, list_select_menu

def run():
    '''
    This function runs the app_selector menu with associated functions
    based on the responses given.
    Refer to the list_select_menu function in utils for additional info.
    '''
    while True:
        os.system("clear")

        app_simulator_question = {
                "Please select an option?": {
                "Trading Simulator": trading_sim_menu,
                "FX Net": fx_net_menu,
                "Exit": exit_message,
                }}
        list_select_menu(app_simulator_question)
