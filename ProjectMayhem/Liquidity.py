import csv
import pandas as pd

def Add_liq(Liquidity):
    with open('Liquidity_15m.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([Liquidity['Date'], Liquidity['Open'], Liquidity['Loc']])

def check_liq(Liquidity, pos, loc, HrL):
    df = pd.read_csv('GBPUSD_15m_Data.csv')
    len_df = len(df)

    if loc == 1:  # bearish FVG
        for i in range(pos + 1, len_df):
            if HrL =='High':
                if df.iloc[i]['High'] >= Liquidity['Loc'] or df.iloc[i]['Close'] >= Liquidity['Loc']:
                    return False
            if HrL == 'Low':
                if df.iloc[i]['Low'] <= Liquidity['Loc'] or df.iloc[i]['Close'] <= Liquidity['Loc']:
                    return False
        return True

    if loc == 0:  # bullish FVG
        for i in range(pos + 1, len_df):
            if HrL == 'High':
                if df.iloc[i]['High'] >= Liquidity['Loc'] or df.iloc[i]['Close'] >= Liquidity['Loc']:
                    return False
            if HrL == 'Low':
                if df.iloc[i]['Low'] <= Liquidity['Loc'] or df.iloc[i]['Close'] <= Liquidity['Loc']:
                    return False
        return True

def find_liq():
    df = pd.read_csv('GBPUSD_15m_Data.csv')

    for i in range(1, len(df)):
        curr_candle = df.iloc[i]
        if curr_candle['Open'] - curr_candle['Close'] > 0: # Bearish candle
            loc = 1
            if curr_candle['Close'] - curr_candle['Low'] > 0.06: # Bearish Liq
                HrL = 'Low'
                liq_candle = {
                    'Date': curr_candle['Date'],
                    'Open': curr_candle['Close'],
                    'Loc': curr_candle['Low']
                }
                if check_liq(liq_candle, i, loc, HrL):
                    Add_liq(liq_candle)

            if curr_candle['High'] - curr_candle['Open'] > 0.06: # Bullish Liq
                HrL = 'High'
                liq_candle = {
                    'Date': curr_candle['Date'],
                    'Open': curr_candle['Open'],
                    'Loc': curr_candle['High']
                }
                if check_liq(liq_candle, i, loc, HrL):
                    Add_liq(liq_candle)

        if curr_candle['Open'] - curr_candle['Close'] < 0: # Bullish Candle
            loc = 0
            if curr_candle['High'] - curr_candle['Close'] > 0.00018: #Bearish Liq
                HrL = 'Low'
                liq_candle = {
                    'Date': curr_candle['Date'],
                    'Open': curr_candle['Close'],
                    'Loc': curr_candle['Low']
                }
                if check_liq(liq_candle, i, loc, HrL):
                    Add_liq(liq_candle)

            if curr_candle['Open'] - curr_candle['Low'] > 0.00018:
                HrL = 'High'
                liq_candle = {
                    'Date': curr_candle['Date'],
                    'Open': curr_candle['Open'],
                    'Loc': curr_candle['High']
                }
                if check_liq(liq_candle, i, loc, HrL):
                    Add_liq(liq_candle)
    return


def main():
    find_liq()
    return


