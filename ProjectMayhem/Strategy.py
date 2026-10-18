import pandas as pd
from datetime import datetime, time

global hourly_ob
global ob_15m
global pos
pos = 0
ob_15 = 0


import Execution as exe
def check_trading_time(start_time_str, end_time_str):
    current_time = datetime.now().time()
    start_time = time.fromisoformat(start_time_str)
    end_time = time.fromisoformat(end_time_str)

    print(f"Debug - Current: {current_time}, Start: {start_time}, End: {end_time}")

    if start_time <= end_time:
        return start_time <= current_time <= end_time
    else:
        return current_time >= start_time or current_time <= end_time


def check_if_in_ob_hr(minute_candle, val):
    filename = 'OrderBlock_1hr.csv' if val == 1 else 'OrderBlock_15m.csv'
    ob_df = pd.read_csv(filename)

    c_open = minute_candle['Open']
    c_close = minute_candle['Close']

    body_top = max(c_open, c_close)
    body_bottom = min(c_open, c_close)

    for index, row in ob_df.iterrows():
        ob_position = row['Position']

        # 5. Define the Top and Bottom of the Order Block Zone
        if ob_position == "Bullish":
            ob_zone_top = row['Close']  # Top of Bullish OB is the Close
            ob_zone_bottom = row['Open']  # Bottom of Bullish OB is the Open
        else:  # "Bearish"
            ob_zone_top = row['Open']  # Top of Bearish OB is the Open
            ob_zone_bottom = row['Close']  # Bottom of Bearish OB is the Close

        body_fully_inside = (body_bottom >= ob_zone_bottom) and (body_top <= ob_zone_top)

        body_overlaps_zone = not (body_top < ob_zone_bottom or body_bottom > ob_zone_top)

        if body_fully_inside or body_overlaps_zone:

            global NoOfCandles
            NoOfCandles += 1
            print(f"--- Successfully tapped into {ob_position} {filename} ---")
            if filename == 'OrderBlock_1hr.csv':
                global hourly_ob
                hourly_ob = row
            else:
                global ob_15m
                global pos
                pos = index
                ob_15m = row
            return True

    return False

def correct_dir(): # Ensures candle broke from POI correctly
    global ob_15m
    global pos
    dt = pd.read_csv('Current_Candle_1m_Data.csv')

    for i in range(pos +1, len(dt) ):
        curr_check = dt.iloc[i]
        if ob_15m['Position'] == 'Bullish':
            if curr_check['Close'] < ob_15m['Open']:
                print("--- Broke out of Order Block in desired direction ---")
                return True

        if ob_15m['Position'] == 'Bearish':
            if curr_check['Close'] > ob_15m['Open']:
                print("--- Broke out of Order Block in desired direction ---")
                return True
    return False

def check_if_in_fvg():
    global pos
    dt = pd.read_csv('Current_Candle_1m_Data.csv')

    for i in range(pos +1, len(dt)):
        curr_candle = dt.iloc[i]

        df = pd.read_csv('FairValueGap_15m.csv')
        for j in range(len(df)):
            fvg_candle = df.iloc[j]
            if fvg_candle['Position'] == 'Bullish':
                if curr_candle['Close'] < fvg_candle['Next_candle'] or curr_candle['Low'] < fvg_candle['Next_candle']:
                    return True
            if fvg_candle['Position'] == 'Bearish':
                if curr_candle['Open'] > fvg_candle['Next_candle'] or curr_candle['High'] > fvg_candle['Next_candle']:
                    return True
                """ NOTE *** In the morning add explicit math to ensure in range (if bullish already greater than open etc...) ***"""
    return False



def run_strategy_check():
    df = pd.read_csv('Current_Candle_1m_Data.csv')

    print(df)
    if check_trading_time('07:00', '02:00'):
        if check_if_in_ob_hr(df.iloc[0], 1): # Check for tag in hourly ob
           if check_if_in_ob_hr(df.iloc[0], 0): #Check for tag in 15m ob
               """
               1. Check that price has broken out in the correct direction
               2. Check for tag of FVG 
               3. Target liquidity (Might add this to Execution.py)
               """
               if correct_dir():
                if check_if_in_fvg():
                    candle_of_joy = df.iloc[-1]
                    exe.main(candle_of_joy)

        if check_if_in_fvg():
            """
            1. Check for FVG
            2. Check for 15OB 
            3. Take Trade
            """
            if check_if_in_ob_hr(df.iloc[0], 0):
                if correct_dir():
                    candle_of_joy = df.iloc[-1]
                    exe.main(candle_of_joy)

    return

def main():
    run_strategy_check()
    return