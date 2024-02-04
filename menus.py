from InquirerPy import inquirer

menu_1_question = "Do you want to proceed with creating the simulated data?"
menu_1_choices = ["Yes", "No"]

menu_2_question = "Do you want to load the data into FX Net program?"
menu_2_choices = ["Yes", "Exit"]


def menu(question, choices):

    result = inquirer.select(
    message=question,
    choices=choices,
    ).execute()

    return result
