import datetime
import yfinance as yf
import time
import boto3


def calcRetracements(swing):
    level = .5
    return max[0] - level*swing

def getData():
    data = yf.download(tickers=ticker, period="5m", interval="5m")
    while(len(data) == 0 or data is None):
        data = yf.download(tickers=ticker, period="5m", interval="5m")
        time.sleep(2)
    return data

def send_level_email():
    ses_client = boto3.client("ses", region_name="us-east-1")
    CHARSET = "UTF-8"

    response = ses_client.send_email(
        Destination={
            "ToAddresses": [
                "amol@nirenshah.com",
            ],
        },
        Message={
            "Body": {
                "Text": {
                    "Charset": CHARSET,
                    "Data": "SPY has hit 0.5 level with enough swing",
                }
            },
            "Subject": {
                "Charset": CHARSET,
                "Data": "SPY Fibonacci Retracement tracker",
            },
        },
        Source="FibonacciiRetracement@gmail.com",
    )


ticker = "SPY"
level = 0

data = getData()
min = data[-1:]['Low']
max = data[-1:]['High']
swing = max[0] - min[0]


send_level_email()

while True:
    data = getData()
    current = data[-1:]['Low']
    current_max = data[-1:]['High']
    # print(min)
    # print(current)
    # print("--------")
    if min[0] > current[0]:
        min = current
        max = current_max
        swing = max[0] - min[0]
        level = calcRetracements(swing)
    elif max[0] < current_max[0]:
        max = current_max
        swing = max[0] - min[0]
        level = calcRetracements(swing)
    print(level)
    # print(current)
    # print(level)
    # print(min)
    # print(max)

    if current[0] > level*0.95 and current[0] < level*1.05:
        if swing >= max[0] * 0.00625:
            print("****************Hit .5 Level***************************")
            min = current
            max = current_max
            swing = 0
            send_level_email()
        # else:
        #     print("\\\\\\\\\\\\\\\\\\\\\\\Hit but not enough swing////////////////////////")
        #     send_email_low_swing()

        
        

    time.sleep(60)