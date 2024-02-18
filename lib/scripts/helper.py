'''
Not part of the main program.
This is a script used to delete un-used files in
Google Drive to keep the workspace clean

Uncomment out the files variable for the files you wish
to list / delete

'''

from lib.fx_net.fx_net import delete_file, get_file_list

# INTERIM HELPERS TO DELETE FILES FROM GDRIVE DURING DEVELOPMENT
# Un comment the file you wish to filter for and delete
# files = get_file_list("netting_report")
# files = get_file_list("trade_data")
files = get_file_list("payment_report")


for file in files:
    delete_file(file)
files = get_file_list()
