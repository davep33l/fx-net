from lib import app_selector
# from lib.fx_net.fx_net import delete_file, get_file_list, get_most_recent_file

if __name__ == "__main__":
    app_selector.run()

    # INTERIM HELPERS TO DELETE FILES FROM GDRIVE DURING DEVELOPMENT
    # files = get_file_list("netting_report")
    # files = get_file_list("trade_data")
    # files = get_file_list("payment_report")

    # for file in files:
    #     delete_file(file)
    # files = get_file_list()

