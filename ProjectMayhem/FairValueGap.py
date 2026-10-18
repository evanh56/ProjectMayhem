import csv
import pandas as pd

def add_fvg(FairValueGap):
    with open('FairValueGap_15m.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([FairValueGap['Date'], FairValueGap['Prev_candle'], FairValueGap['Next_candle'], FairValueGap['Position']])


def check_fvg(FairValueGap, pos, loc):
    df = pd.read_csv('GBPUSD_15m_Data.csv')
    len_df = len(df)

    if loc == 1:  # bearish FVG
        for i in range(pos + 2, len_df):
            if df.iloc[i]['Close'] > FairValueGap['Next_candle'] or df.iloc[i]['High'] > FairValueGap['Next_candle']:
                return False
        return True

    if loc == 0:  # bullish FVG
        for i in range(pos + 2, len_df):
            if df.iloc[i]['Close'] < FairValueGap['Next_candle'] or df.iloc[i]['Low'] < FairValueGap['Next_candle']:
                return False
        return True

    return True


def search_for_fvg():
    df = pd.read_csv('GBPUSD_15m_Data.csv')
    #dt = pd.read_csv('FairValueGap.csv')
    for i in range(1, len(df) -1):
        prev_candle = df.iloc[i-1]
        curr_candle = df.iloc[i]
        next_candle = df.iloc[i+1]


        if curr_candle['Open'] - curr_candle['Close'] < 0: #Bullish FVG
            loc = 0
            if prev_candle['High'] < curr_candle['Close'] and next_candle['Low'] > curr_candle['Open'] and prev_candle['High'] < next_candle['Low']:
                fvg = {
                    'Date': curr_candle['Date'],
                    'Prev_candle': prev_candle['High'],
                    'Next_candle': next_candle['Low'],
                    'Position': 'Bullish'
                }
                if next_candle['High'] - prev_candle['Low'] > 0.00005:
                    if check_fvg(fvg, i, loc):
                        add_fvg(fvg)

        if curr_candle['Open'] - curr_candle['Close'] > 0:  # Bearish FVG
            loc = 1
            if prev_candle['Low'] > curr_candle['Close'] and next_candle['High'] < curr_candle['Open'] and prev_candle['Low'] > next_candle['High']:
                fvg = {
                        'Date': curr_candle['Date'],
                        'Prev_candle': prev_candle['Low'],
                        'Next_candle': next_candle['High'],
                        'Position': 'Bearish'
                }
                if prev_candle['Low'] - next_candle['High'] > 0.00005:
                    if check_fvg(fvg, i, loc):
                        add_fvg(fvg)

def main():
    search_for_fvg()
    return