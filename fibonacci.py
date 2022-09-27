import yfinance as yf
import time
import boto3
from datetime import date
import datetime

# These first 3 functions simply calculate the level for when notifications need to be sent out
# The second 2 are only called once the retracement level is hit (when stock is bought)
# For improved functionality, make this into 1 function and return an array
def calcRetracements(swing):
    level = .5
    return max[0] - level*swing

def calcSellRetracement(swing):
    level = 0.236
    return max[0] - level*swing

def calcLossRetracement(swing):
    level = 0.786
    return max[0] - level*swing

# Get data from yahoo finance API using yfinance. If the data fails to download, tries again in 2 seconds
def getData():
    data = yf.download(tickers=ticker, period="5m", interval="5m")
    while(len(data) == 0 or data is None):
        data = yf.download(tickers=ticker, period="5m", interval="5m")
        time.sleep(2)
    return data

# These send the buy/sell/loss emails to anyone who is added to the list
# Realistically, should condense this down into 1 function that takes a parameter to send buy/sell/loss mail
def send_buy_email(stock_ticker, price, min, max):
    ses_client = boto3.client("ses", region_name="us-east-1")
    CHARSET = "UTF-8"
    DATA = str(stock_ticker) + " has hit 0.5 level at price $" + str(price) + ". \nMin: " + str(min) + "\nMax: " + str(max)
    response = ses_client.send_email(
        Destination={
            "ToAddresses": [
                "amol@nirenshah.com", "reviewstopclass@gmail.com",
            ],
        },
        Message={
            "Body": {
                "Text": {
                    "Charset": CHARSET,
                    "Data": DATA,
                }
            },
            "Subject": {
                "Charset": CHARSET,
                "Data": "SPY Fibonacci Retracement Tracker",
            },
        },
        Source="FibonacciiRetracement@gmail.com",
    )

def send_sell_email(stock_ticker, price):
    ses_client = boto3.client("ses", region_name="us-east-1")
    CHARSET = "UTF-8"
    DATA = str(stock_ticker) + " has hit sell level at price $" + str(price) + "."
    response = ses_client.send_email(
        Destination={
            "ToAddresses": [
                "amol@nirenshah.com", "reviewstopclass@gmail.com",
            ],
        },
        Message={
            "Body": {
                "Text": {
                    "Charset": CHARSET,
                    "Data": DATA,
                }
            },
            "Subject": {
                "Charset": CHARSET,
                "Data": "SPY Fibonacci Retracement Tracker",
            },
        },
        Source="FibonacciiRetracement@gmail.com",
    )

def send_loss_email(stock_ticker, price):
    ses_client = boto3.client("ses", region_name="us-east-1")
    CHARSET = "UTF-8"
    DATA = str(stock_ticker) + " has hit loss level at price $" + str(price) + "."
    response = ses_client.send_email(
        Destination={
            "ToAddresses": [
                "amol@nirenshah.com", "reviewstopclass@gmail.com",
            ],
        },
        Message={
            "Body": {
                "Text": {
                    "Charset": CHARSET,
                    "Data": DATA,
                }
            },
            "Subject": {
                "Charset": CHARSET,
                "Data": "SPY Fibonacci Retracement Tracker",
            },
        },
        Source="FibonacciiRetracement@gmail.com",
    )

def send_daily_report(level_count, sell_count, loss_count):
    ses_client = boto3.client("ses", region_name="us-east-1")
    CHARSET = "UTF-8"
    if level_count == 0:
        DATA = "For " + str(date.today()) + ", the SPY retracement tracker detected no retracements, so there is no data to display."
    else:
        DATA = "For " +  str(date.today()) + ", the SPY retracement tracker detected: \n" + "\tRetracement Level Hit: " + str(level_count) + " times\n\tSell Level Hit: " + str(sell_count) + " times\n\tLoss Level Hit: " + str(loss_count) + " times" 
        DATA += "\n\nPercent of levels that resulted in profitable sells: " + str((sell_count/level_count) * 100) + "%\nPercent of levels that resulted in loss sells: " + str((loss_count/level_count) * 100) + "%"
    response = ses_client.send_email(
        Destination={
            "ToAddresses": [
                "amol@nirenshah.com", "reviewstopclass@gmail.com",
            ],
        },
        Message={
            "Body": {
                "Text": {
                    "Charset": CHARSET,
                    "Data": DATA,
                }
            },
            "Subject": {
                "Charset": CHARSET,
                "Data": "Daily Report: SPY Fibonacci Retracement Tracker",
            },
        },
        Source="FibonacciiRetracement@gmail.com",
    )

ticker = "SPY"
level = 0
sell_level = 0
loss_level = 0
level_count = 0
sell_count = 0
loss_count = 0
notify_red_zone = False
data = getData()
min = data[-1:]['Low']
current = data[-1:]['Low']
max = data[-1:]['High']
swing = max[0] - min[0]

while True:
    data = getData()
    current = data[-1:]['Low']
    current_max = data[-1:]['High']

    current_time = datetime.datetime.now()
    if current_time.hour == 21 and current_time.minute >= 50:
        send_daily_report(level_count, sell_count, loss_count)

    if min[0] > current[0]:
        min = current
        max = current_max
        swing = max[0] - min[0]
        level = calcRetracements(swing)
    elif max[0] < current_max[0]:
        max = current_max
        swing = max[0] - min[0]
        level = calcRetracements(swing)


    if current[0] < level:
        if swing >= max[0] * 0.00625:
            send_buy_email(ticker, current[0], min, max)
            sell_level = calcSellRetracement(swing)
            loss_level = calcLossRetracement(swing)
            notify_red_zone = True
            min = current
            max = current_max
            swing = 0
            level = calcRetracements(swing)
            level_count += 1
            
    if current[0] > sell_level and sell_level > 0:
        send_sell_email(ticker, current[0])
        sell_level = 0
        loss_level = 0
        notify_red_zone = False
        sell_count += 1
        
    if current[0] < loss_level:
        send_loss_email(ticker, current[0])
        sell_level = 0
        loss_level = 0
        notify_red_zone = False
        loss_count += 1
        
        

    time.sleep(300)