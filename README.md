# FX NET

FX NET is a program that can parse FX trading data from a trade file and produce a breakdown/summary of netted ammounts by client, currency and value date. It can also produce formatted payment files for manual review and consumption into a downstream payment application for executing payments. 

In finance and banking, operations staff currently perform manual calculations in order to net FX trading data for clients in order to send payments for the agreed FX trades executed. This is a time consuming process and has risks for manual error which can result in costs (overdraft charges).

## Strategy

**Business Goals**: To automate a manual process and reduce risk within a financial setting by netting FX transaction into netted payments. 

**Business Value**: Removes risk of manual error (and potential cost incurring errors) by operations staff by automating a manual repetative task. Improves the users workflow by allowing for time to be spent on more value added tasks within the financial setting. Provides analysis of data to spot trends. Gives a structured approach to data consumption (from the Trading Application) and data generation (to the Payment Application), by automating the task in between. 

### Background Information

#### What is an FX Trade

An FX trade is an agreement to exchange currencies between two parties at an agreed exchange rate for an agreed value date. Where both parties will pay funds to agreed nominated bank accounts. 

Please see example below simplified flow of trade booking and non-netted (known as gross settlement) settlement flow

![Basic FX Example](/readme/images/fx-example.png)

#### What is Netting

Netting is where counterparts in an FX transaction can agreed to group related parts of a trade as long as they follow this criteria:

- Same currency
- Same client
- Same value date

With those groupings they can reduce the amount of payments they are required to exchange between each other.

![Basic FX Netting Example](/readme/images/netting-example.png)

## Scope

### In Scope

The intial scope for this project is to produce a program that can parse FX trading data and produce netting summaries and payment files for those summaries based on client information held within the FX Net program. 

### Out of scope

This project does not contain any trade booking or trade inception functionality. It however provides a trade output file simulation (where the format of this file defines the requirements for the FX Net program). This simulation represents what an upstream trading application is likely to output at the end of trading day, and outputs the file into an agreed shared location ready for consumption / parsing of the FX Net Application.

The simulator is set to create a file based on these contraints.
1. Possible tradable currencies USD, EUR, GBP, JPY and CAD (and all relevant cross pairs, like USD/JPY and JPY/USD being two differently quoted prices)
2. Trading mandate only allows for spot trading. Meaning that trades can only be value for the next possible value date. For example, if trades were booked on a Wednesday, the value date can only be a Thursday. 

This project does not contain functionality of the downstream payment system. But it does consider an agreed payment format (which form the requirements) in which the payment system would want to receive payment message files once generated. These will be stored in a shared location ready for consumption of the downstream payment system. 

### High Level System Architecture

![High level system architecture](/readme/images/high-level-sys-arch.png)

### Business Requirements / User Stories

#### Requirement 1
Create a program that can parse a trade data file from an upstream FX trading application
##### Sub Requirement 1.1
Format of the trading file will be in a consistent format with the following definitions
1. It is a comma separated file that is ultimately stored within a spreadsheet format
2. All values within the file do not have any metadata to define the type of the value stored within it. For example a date may have the value of 20240120 but it will be stored as text. 
3. The file structure will be as follows:

| Column # | Column Heading | Contents | Data Type | Example | Contraints | Additional Comments |
|----------|----------------|----------|-----------|---------|------------|---------------------|
| 1 | CLIENT_NAME | Name of client the FX is traded with| Text| FX Trading Client | | The FX NET program needs to have a mapping of these clients to link to the client payment instructions |
| 2 | CLIENT_TRADER | Name of the trader for the respective client | Text | John Smith| | |
| 3 | BANK_TRADER | Name of the Bank Trader | Text | John Smith | | |
| 4 | TRADE_ID | Unique Trade ID | Text | 20240121000025 | 14 Chars long | This is made up of the trade date in format YYYYMMDD and an iterative string XXXXXX which represents the trade number for that day. For example; 20240121000025 would represent a trade booked on 21st Jan 2024 and trade number 25 (000025) |
| 5 | CCY_PAIR | Trading pair for the FX trade | Text | USD/JPY | 7 Char (3 for each CCY code and one for a forward slash between them) | |
| 6 | BUY_CCY | Buy Currency of the trade in the perspective of the Bank | Text | USD | | |
| 7 | BUY_AMT | Buy Amount of the trade in the perspective of the Bank | Text | 100,000.00 | | |
| 8 | RATE | The agreed FX rate the trade is booked at | Text | 1.2345 | 4 decimal places | |
| 9 | SELL_CCY | Sell Currency of the trade in the perspective of the Bank | Text | USD | | |
| 10 | SELL_AMT | Sell Amount of the trade in the perspective of the Bank   | Text      | 100,000.00 | | |
| 11 | TRADE_DATE | Trade date for which the FX was booked | Text | 20240121 | | |
| 12 | VALUE_DATE | Value date for which the FX was booked | Text | 20240122 | | |
| 13 | CHANNEL | Trading channel in which the trade was booked | Text | Bloomberg | | | 

#### Requirement 2
Parse the FX trading data and manage relevant format conversions for data processing

#### Requirement 3
Produce netting summary by value date

#### Requirement 4
Produce payment files in accepted format for payment system
##### Sub Requirement 4.1
1. The requirement for the payment system is that the output file must contain

Currency, Amount, Client Payment Instructions, Value Date

## Features
1. Intuitive menu system with prompted responses for selection control
2. Create a shareable file to google drive
3. Analysis options to view additional trends by client, currencies traded etc
4. Produce reports in spreadsheet format 
5. Produce reports in the console for quick viewing of netting breakdown
6. Risk reduction by minimising any user intervention
7. Time saving by automating manual processes

## Trading Application Design / Architecture

- Simple Menu system to ask if data needs to be generated
- Connection to shared storage location
- Creation of trade data as per requirements
- Saving of data file to shared storage
- Trading Application will track a "system" date to ensure a simulated file is only created once per Trade date

### Data Model (Trading Application)

- Trading Application will track a "system" date to ensure a simulated file is only created once per Trade date

## FX NET Application Design / Architecture

- Menu system
- Connection to shared storage location
- Parsing of trade data and converting any relevant formats for processing (by user selection)
- Checking if a file for a specified date already exists
- Production of netting amounts as per requirements
- Production of payment files as per requirements
- Analysis of data

### Data Model (FX NET)

- FX NET will contain the parsed data in a master trade file
- FX NET will contain client payment information

## Deployment

## Technologies Used
### Languages Used
This project was developed solely in Python
### Frameworks, Libraries and Software Used

| What  | Type  | Category  | Purpose  |   
|---|---|---|---|
| [Git](https://git-scm.com/)  | Desktop Software  | Version Control  | This was used as version control from the terminal inside VS Code and was pushed to a remote repository hosted by github.com  |
| [Github](https://github.com/)  | Online Software  | Version Control  | This was used to store the code used for the website and to host the website using github pages  |
| [VS Code](https://code.visualstudio.com/) | Desktop Software  | Development  | The was the application used to develop the website. I used some extensions to assist with the development. Those being: Markdown Preview Github Styling, Git Graph***  |
|[Windows Subsystem for Linux](https://learn.microsoft.com/en-us/windows/wsl/install)|Desktop Software| Development | To enable the development environment match as closely as possible the deployment environment as both are Linux based. Changed mid project from Windows to WSL in order to natively trial some python libraries and os specific commands|
|[Heroku](https://www.salesforce.com/products/heroku/overview/)|Online Software|Deployment|This was used to deploy the project|
|[Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli)|Deskop Software|Development|This was used to provide a local deployment for easier testing (using `heroku local` command)|
|[python](https://www.python.org/)|Deskop Software|Development|Requirement for development|
|[node.js](https://nodejs.org/en)|Deskop Software|Development|Requirement for local development and usage of Heroku CLI deployment|
|[Google Sheets / Drive](https://drive.google.com/drive/u/3/home)|Online Software|Database|This was used a the database back ends for each of the respective parts of the project, and for the output locations for the generated files|
|[Google Cloud Console](https://console.cloud.google.com/)|Online Software|Backend| This was used to set up relevant API's and credential/keys to allow access to the Google Sheets "database" and Google Drive files.|
|[`venv`](https://docs.python.org/3/library/venv.html)|Python Package/Library|Development|This was used to create a virtual environment for package management|
|[`pandas`](https://pandas.pydata.org/docs/)|Python Package/Library| Misc|This was used to help with data manipulation within the application. `pyarrow` was installed additional as a dependency (and stop the pandas notification on its requirement to use)|
|[`google-auth`](https://google-auth.readthedocs.io/en/master/)|Python Package/Library| Misc|This was used to help with data manipulation within the application|
|[`google-api-client-python`](https://github.com/googleapis/google-api-python-client)|Python Package/Library| Misc|This was used to help with data manipulation within the application|
|[draw.io](https://app.diagrams.net/)|Online Software|Flow Chars|This was used to create the flow charts and scenario diagrams|
|[ui.dev/amiresponsive](https://ui.dev/amiresponsive)|Online Software| Misc| This was used to create the responsive image for the top of the readme|

## Testing
## Bugs
## Credits 
### Code
### Acknowledgements
## Additional Notes