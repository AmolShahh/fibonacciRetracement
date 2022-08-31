import datetime
import yfinance as yf
import time
import smtplib
import ssl

def calcRetracements(swing):
    level = .5
    return max[0] - level*swing

def getData():
    data = yf.download(tickers=ticker, period="5m", interval="5m")
    while(len(data) == 0 or data is None):
        data = yf.download(tickers=ticker, period="5m", interval="5m")
        time.sleep(2)
    return data

smtp_server = "smtp.gmail.com"
sender_email = "FibonacciiRetracement@gmail.com"
password = "fibon@acci!"
port = 587
reciever_email = "amol@nirenshah.com"
message = "SPY has hit 0.5 Level"
context = ssl.create_default_context()


ticker = "SPY"
dayStart = str(datetime.datetime.now().date()) + " 08:00:00"
start = str(datetime.datetime.now().date()) + " 08:01:00"
end = str(datetime.datetime.now().date()) + " 15:30:00"

level = 0
#swap this into a do while instead of an if + a while?
if str(datetime.datetime.now()) == dayStart:
       data = getData()
       min = data[-1:]['Low']
       max = data[-1:]['High']
       swing = max[0] - min[0]
       level = calcRetracements(swing)

data = getData()
min = data[-1:]['Low']
max = data[-1:]['High']
swing = max[0] - min[0]
while str(datetime.datetime.now()) > start and str(datetime.datetime.now()) < end:
    data = getData()
    current = data[-1:]['Low']
    current_max = data[-1:]['High']
    print(min)
    print(current)
    print("--------")
    if min[0] > current[0]:
        min = current
        swing = max[0] - min[0]
        level = calcRetracements(swing)
    elif max[0] < current_max[0]:
        max = current_max
        swing = max[0] - min[0]
        level = calcRetracements(swing)
    
    print(current)
    print(level)
    print(min)
    print(max)

    if current[0] > level*0.95 and current[0] < level*1.05:
        if swing >= max[0] * 0.00625:
            print("****************Hit .5 Level***************************")
            min = current
            max = current_max
            swing = 0
            try:
                server = smtplib.SMTP(smtp_server,port)
                server.ehlo() # Can be omitted
                server.starttls(context=context) # Secure the connection
                server.ehlo() # Can be omitted
                server.login(sender_email, password)
                server.sendmail(sender_email, reciever_email, message)
            except Exception as e:
                # Print any error messages to stdout
                print(e)
            finally:
                server.quit()
        else:
            print("\\\\\\\\\\\\\\\\\\\\\\\Hit but not enough swing////////////////////////")
            try:
                server = smtplib.SMTP(smtp_server,port)
                server.ehlo() # Can be omitted
                server.starttls(context=context) # Secure the connection
                server.ehlo() # Can be omitted
                server.login(sender_email, password)
                server.sendmail(sender_email, reciever_email, "Hit 0.5 level without enough swing")
            except Exception as e:
                # Print any error messages to stdout
                print(e)
            finally:
                server.quit()

        
        

    time.sleep(60)