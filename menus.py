from InquirerPy import inquirer

menu_1_question = "Do you want to proceed with creating the simulated data?"
menu_1_choices = ["Yes", "Exit program"]

menu_2_question = "Please choose an option?"
menu_2_choices = ["Load Data", "Reporting Menu", "Return to previous menu"]

menu_3_question = "Please select an option"
menu_3_choices = ["Show Netting Summary by Value Date (working)",
                  "Create Netting Report by Value Date (WIP)",
                   "Create payment files (WIP)",
                   "Show trade count by clients (WIP)",
                   "Show trade count by client and client trader (WIP)",
                   "Show trade count by bank trader (WIP)",
                   "Return to main menu (working)"]

def menu(question, choices):

    result = inquirer.select(
    message=question,
    choices=choices,
    ).execute()

    return result
