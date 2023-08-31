import yfinance as yf
import numpy as np
import pandas as pd


forex_data = yf.download('USDJPY=X', start = "1989-01-01", end = None)

# Set the index to a datetime object
forex_data.index = pd.to_datetime(forex_data.index)
i = 260
in_trade = False
trade_type = ""
entry_price = 0
total_money = 100000
trade_end_dict = {"stoploss":None, "takeprofit":None}

num_trades = 0
take_profits = 0
stop_losses = 0
while i < len(forex_data):
    current_price = float(forex_data.iloc[i]["Close"])
    last_year = forex_data[i-250:i]
    description = last_year["Close"].describe()
    last_year_mean = float(description[1])
    last_year_25th = float(description[4])
    last_year_75th = float(description[6])
    if in_trade:
        if trade_type == "long":
            if current_price>=trade_end_dict["takeprofit"]:
                take_profits+=1
                take_profit = trade_end_dict["takeprofit"]
                return_pct = take_profit/entry_price
                total_money*=return_pct
                in_trade = False
                trade_type = ""
                entry_price = 0
                trade_end_dict = {"stoploss":None, "takeprofit":None}
            elif current_price<=trade_end_dict["stoploss"]:
                stop_losses+=1
                stop_loss = trade_end_dict["stoploss"]
                return_pct = 0.9999
                total_money*=return_pct
                in_trade = False
                trade_type = ""
                entry_price = 0
                trade_end_dict = {"stoploss":None, "takeprofit":None}
        else:
            if current_price<=trade_end_dict["takeprofit"]:
                take_profits+=1
                take_profit = trade_end_dict["takeprofit"]
                return_pct = (2*entry_price - take_profit)/entry_price
                total_money*=return_pct
                in_trade = False
                trade_type = ""
                entry_price = 0
                trade_end_dict = {"stoploss":None, "takeprofit":None}
            elif current_price>=trade_end_dict["stoploss"]:
                stop_losses+=1
                stop_loss = trade_end_dict["stoploss"]
                return_pct = 0.9999
                total_money*=return_pct
                in_trade = False
                trade_type = ""
                entry_price = 0
                trade_end_dict = {"stoploss":None, "takeprofit":None}
    else:
        #under the 25th percentile and stock is undervalued then enter a long position
        if current_price<=last_year_25th:
            in_trade = True
            num_trades+=1
            entry_price = current_price
            trade_type = "long"
            trade_end_dict["stoploss"] = 0.9999*entry_price
            trade_end_dict["takeprofit"] = 0.99*last_year_mean
        elif current_price>=last_year_75th: #over the 75th percentile stock is overvalued then enter a short position
            in_trade = True
            num_trades+=1
            entry_price = current_price
            trade_type = "short"
            trade_end_dict["stoploss"] = 1.0001*entry_price
            trade_end_dict["takeprofit"] = 1.01*last_year_mean
    i+=1


print(total_money)
return_rate = total_money/100000
return_rate*=100
return_rate-=100
print("Return: " + str(return_rate) + "%")

print("Number of trades: " + str(num_trades))

print("Take Profits: " + str(take_profits))
print("Stop Losses: " + str(stop_losses))