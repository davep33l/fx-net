# TESTING.md file

This file will house any development testing performed and final testing performed.

## Deployment to Heroku

Evidence of first initial deployment to Heroku, proof of connection to googlesheets, by printing out contents of the connected sheet. With proof that it is displayed on the web terminal on Heroku. 

![Initial deployment test to Heroku](../testing/screenshots/heroku-deployment-test.png)



# Tests to check when complete

Check everything runs with data in the FX Net database and without it. 


## TESTING EMPTY DATABASE

These tests are to check that the user is correctly prompted and informed that there is no data in the database to run the required actions. 

### Set up

I cleared out the `fx_net_db` database (workbook) of any information on the relevant tables (worksheet), those being `FILES_LOADED` and `TRADES`.

![Screenshot of cleared FILES_LOADED table](../testing/screenshots/cleared_files_loaded_table_test.png)

![Screenshot of cleared TRADES table](../testing/screenshots/cleared_trades_table_test.png)

### TESTS PERFORMED

![](../testing/screenshots/netting-summary-by-value-date-test.gif)

| Test ID | Description | Outcome | Comments | Evidence |
|--------|-------------|---------|----------|----------|
| test1 | Test Netting Summary by Value Date menu option informs the user that there is no data available | Passed | Noticed the UI was not clearing like the other tests. Corrected by creating a new function to (`no_data_message`) control the action of displaing a message when there is no data and applied to all related other functions | ![](../testing/gifs/test1.gif) |
| test2 | Test Netting Summary by Value Date menu option informs the user that there is no data available | Passed || ![](../testing/gifs/test2.gif) |
| test3 | Test Netting Summary by Value Date menu option informs the user that there is no data available | Passed || ![](../testing/gifs/test3.gif) |
| test4 | Test Netting Summary by Value Date menu option informs the user that there is no data available | Passed || ![](../testing/gifs/test4.gif) |
| test5 | Test Netting Summary by Value Date menu option informs the user that there is no data available | Passed || ![](../testing/gifs/test5.gif) |
| test6 | Test Netting Summary by Value Date menu option informs the user that there is no data available | Passed | Was not clearing initially, refactored to include the newly created `no_data_message` function | ![](../testing/gifs/test6.gif) |
| test7 | Test Netting Summary by Value Date menu option informs the user that there is no data available | Passed | Was not clearing initially, refactored to include the newly created `no_data_message` function | ![](../testing/gifs/test7.gif) |



## TESTING TABLES UPDATE CORRECTLY

system date
files loaded
trades

## TESTING FILES GENERATE CORRECTLY

