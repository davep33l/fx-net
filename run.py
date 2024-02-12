from lib import app_selector

if __name__ == "__main__":
    app_selector.app_selector()

    # INTERIM HELPERS TO DELETE FILES FROM GDRIVE DURING DEVELOPMENT
    # # files = get_file_list("netting_report")
    # files = get_file_list("trade_data")

    # for file in files:
    #     delete_file(file)
    # files = get_file_list()
    # print(get_most_recent_file())
    # create_report_spreadsheet(get_most_recent_file())
    # pass

    # trade_files = get_trade_data_files_list()
    # print(trade_files)

    # get_files_already_loaded()
    # file_data = get_eligible_files_to_load()
    # file_names = [file_name[0] for file_name in file_data]
    
    # choice = menus.menu("Pick a file to load", file_names)
    # print(choice)

    # for file in file_data:
    #     if file[0] == choice:
    #         file_id = file[1]


    # print(file_id)

    # result = get_available_report_value_dates()
    # print(result)