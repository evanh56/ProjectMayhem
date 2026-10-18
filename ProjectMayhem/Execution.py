#Taking a trade
import MetaTrader5 as mt
import pandas as pd

def price_to_pip(symbol, live_price):

    if 'JPY' in symbol:
        acc_info = mt.account_info()
        acc_bal = acc_info.balance
        pip_val = acc_bal / 100
        pips = 7
        pip_unit = (pip_val / live_price)
        lot_size = round(pip_unit * pips, 2)
        return lot_size

    if 'GBPUSD' in symbol:
        acc_info = mt.account_info()
        acc_bal = acc_info.balance
        pip_val = acc_bal / 100
        pips = 7
        pip_unit = (pip_val / live_price)
        lot_size = round(pip_unit * pips, 2)
        return lot_size
ticker = 'GBPJPY'
#pricedif =
#mt.initialize()
#acc_info = mt.account_info()
#acc_bal = acc_info.balance

#qty = price_to_pip(ticker, acc_bal)

Sl = 350

def taketrade():
    print("Work in progress")
    return

def main(candle_of_joy):
    return
