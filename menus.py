from InquirerPy import inquirer

menu_1_question = "Do you want to proceed with creating the simulated data?"
menu_1_choices = ["Yes", "Exit program"]

menu_2_question = "Do you want to load the data into FX Net program?"
menu_2_choices = ["Yes", "Exit"]

menu_3_question = "Please select an option"
menu_3_choices = ["Create Netting report for most recent file (working)",
                  "Create Netting report spreadsheet",
                   "Create payment files (WIP)",
                   "Show trade count by clients (WIP)",
                   "Show trade count by client and client trader (WIP)",
                   "Show trade count by bank trader (WIP)",
                   "Exit program (working)"]

def menu(question, choices):

    result = inquirer.select(
    message=question,
    choices=choices,
    ).execute()

    return result
