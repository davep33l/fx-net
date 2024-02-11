from InquirerPy import inquirer

question = "Do you want to proceed with creating the simulated data?"
choices = ["Yes", "No (previous menu)"]

def run():

    result = inquirer.select(
    message=question,
    choices=choices,
    ).execute()

    return result