
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

