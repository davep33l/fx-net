# Build in imports
import random
from datetime import timedelta, datetime

CLIENTS = {
    'Capital Trading' : ['Max Scott', 'Ava Lee'],
    'Nova Wealth' : ['Leo Chen', 'Mia Hall'],
    'Pulse Trading' : ['Kai Wong', 'Lily Brooks'],
    'Greystone' : ['Mason Cole', 'Ayesha Kumar'],
    'Comet FX' : ['Ivy Li', 'Ethan Carter'],
}

CHANNELS = [
    "Bloomberg", 
    "Reuters", 
    "FX Connect", 
    "Phone"
    ]

TRADING_PAIRS = {
    'USD/GBP': {'low': 0.78, 'high': 0.8},
    'USD/JPY': {'low': 145, 'high': 149}, 
    'USD/CAD': {'low': 1.33, 'high': 1.35}, 
    'USD/EUR': {'low': 0.91, 'high': 0.93}, 
    'GBP/USD': {'low': 1.25, 'high': 1.28}, 
    'GBP/JPY': {'low': 186, 'high': 187}, 
    'GBP/CAD': {'low': 1.7, 'high': 1.72}, 
    'GBP/EUR': {'low': 1.16, 'high': 1.18}, 
    'JPY/USD': {'low': 0.0065, 'high': 0.0068}, 
    'JPY/GBP': {'low': 0.0053, 'high': 0.0056}, 
    'JPY/CAD': {'low': 0.0088, 'high': 0.0092}, 
    'JPY/EUR': {'low': 0.0061, 'high': 0.0064}, 
    'CAD/USD': {'low': 0.72, 'high': 0.76}, 
    'CAD/GBP': {'low': 0.57, 'high': 0.59}, 
    'CAD/JPY': {'low': 109, 'high': 111}, 
    'CAD/EUR': {'low': 0.73, 'high': 0.75}, 
    'EUR/USD': {'low': 1.06, 'high': 1.1}, 
    'EUR/GBP': {'low': 0.84, 'high': 0.86}, 
    'EUR/JPY': {'low': 158, 'high': 162}, 
    'EUR/CAD': {'low': 1.43, 'high': 1.47}
    }

BANK_TRADERS = [
    "Raj Singh",
    "Max Tan",
    "Emma Davis",
    "Mike Taylor",
    "Emily Wilson"
]

def create_trade_data(trade_date, quantity_of_trades):

    """
    Purpose: This function takes in two arguments in order to produce a data
    set of trades for a given trade date. 

    date: This should be passed in as a string in ISO date format YYYYMMDD
    quantity: This should be passed in as in integer (e.g. if you want to 
    produce 10 random trades, pass in the integer 10)

    Returns: A list of trade data
    """

    # Error checking
    try:
        datetime.strptime(trade_date, "%Y%m%d")
    except ValueError:
        raise ValueError(
            "Invalid date format."
            "Please provide a date in the format YYYYMMDD."
            )

    if not isinstance(quantity_of_trades, int) or quantity_of_trades <= 0:
        raise ValueError("Invalid quantity."
                         "Please provide a positive integer for the quantity."
                         )

    full_data = []
    headings = ["CLIENT_NAME", "CLIENT_TRADER", "BANK_TRADER", "TRADE_ID",
                "CCY_PAIR","BUY_CCY","BUY_AMT","RATE","SELL_CCY","SELL_AMT",
                "TRADE_DATE", "VALUE_DATE","CHANNEL"]
    full_data.append(headings)

    for trade_number in range(quantity_of_trades):

        # Get random client name
        client = random.choice(list(CLIENTS.keys()))
        
        # Get random trader associated with the random client
        client_trader = random.choice(CLIENTS[client])

        # Get random bank trader
        bank_trader = random.choice(BANK_TRADERS)

        # Create unique trade ID
        # Adds 1 to make sure the trade numbers start at 1
        formatted_number = '{:04d}'.format(trade_number + 1) 
        trade_id = trade_date + str(formatted_number)

        # Get buy/sell currencies
        ccy_pair = random.choice(list(TRADING_PAIRS.keys()))
        buy_ccy = ccy_pair[0:3]
        sell_ccy = ccy_pair[4:]

        # Get buy amount (round to zero decimals for JPY)
        if buy_ccy == "JPY":
            buy_amt = round(random.uniform(10000,100000),0)
        else:
            buy_amt = round(random.uniform(10000,100000),2)

        # Get random rate between the lows and highs to simulate 
        # the trading range.
        # DISCLAIMER: For purposes of demonstration only, albiet 
        # these currency pairs have traded within this range previously.
        rate = round(
            random.uniform(
                    TRADING_PAIRS[ccy_pair]['low'],
                    TRADING_PAIRS[ccy_pair]['high']),
                    4)

        # Get sell amount (round to zero decimals for JPY)
        if sell_ccy == "JPY":
            sell_amt = -round(buy_amt * rate, 0)
        else:
            sell_amt = -round(buy_amt * rate, 2)

        # Sets the trade date based on the input of the function
        trade_date_string = trade_date
        trade_date_ISO_format = datetime.strptime(trade_date_string, "%Y%m%d")

        # Ensures the value date is always the next business day
        value_date_ISO_format = trade_date_ISO_format + timedelta(1)
        # Check if the day is Saturday (5) or Sunday (6) and increases until it is a weekday
        while value_date_ISO_format.weekday() >= 5:
            value_date_ISO_format += timedelta(days=1)

        value_date_string = value_date_ISO_format.strftime("%Y%m%d")

        # Get random trading channel
        channel = random.choice(CHANNELS)

        trade_data_list = [client, client_trader, bank_trader, trade_id, ccy_pair, buy_ccy, buy_amt, rate, sell_ccy, sell_amt, trade_date_string, value_date_string, channel]
        full_data.append(trade_data_list)

    return full_data


