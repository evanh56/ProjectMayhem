import csv
import MetaTrader5 as mt #import for MT
from datetime import datetime, timezone # Used for live dates
import pandas as pd
import pytz
import time
import tzlocal
import threading

import Execution as ex
import FairValueGap as fvg
import OrderBlockAnalysis as ob
import Liquidity as lqt
import Strategy as s

login = 5057709180
password = 'Q-Fe7aBa'
server = 'MetaQuotes-Demo'

mt.login(login, password, server)

info = 'Time, Open, High, Low, Close'
symbol = 'GBPJPY'

timeframe_1m = mt.TIMEFRAME_M1
NoOfCandles_1m = 1 # Most current Candle
global NoOfCandles

initial_run_complete = False

timeframe_15m = mt.TIMEFRAME_M15
NoOfCandles_15m = 192 # 48H Worth of Data in 15m

timeframe_1H = mt.TIMEFRAME_H1
NoOfCandles_1H = 120 #Previous 5 days worth of Data in 1H

def MT5_account():
    mt.initialize()
    account_info = mt.account_info()
    account_balance = account_info.balance
    print('Account Successfully Logged In')
    print('Connected to MT5 Account: ',account_info.login)
    print('Account Balance: ',account_balance)

def check_system_timezone():
    # Check system timezone
    system_tz = time.tzname
    print(f"System timezone: {system_tz}")

    # Check local timezone using tzlocal
    try:
        local_tz = tzlocal.get_localzone()
        print(f"Local timezone: {local_tz}")
    except:
        print("Could not detect local timezone")

    # Current times
    print(f"UTC time: {datetime.now(timezone.utc)}")
    print(f"Local time: {datetime.now()}")

def get_candle_1m(symbol, timeframe, NoOfCandles):
    utc_now = datetime.now(timezone.utc)
    print(f"Current UTC time: {utc_now}", flush=True)

    if not mt.initialize():
        print("No data received from MT5 for 1 minute. Checking connection...", flush=True)
        mt.symbol_select(symbol, True)
        rates1m = mt.copy_rates_from_pos(symbol, timeframe, 0, NoOfCandles)
        if rates1m is None or len(rates1m) == 0:
            print("Failed to retrieve data after symbol select.", flush=True)
            return pd.DataFrame()

    rates1m = mt.copy_rates_from_pos(symbol, timeframe, 0,NoOfCandles)

    if rates1m is None or len(rates1m) == 0:
        print("No data received from MT5 for 1 minute. Checking connection...", flush=True)
        mt.symbol_select(symbol, True)
        rates1m = mt.copy_rates_from_pos(symbol, timeframe, 0, NoOfCandles)

    df = pd.DataFrame(rates1m)
    df['time'] = pd.to_datetime(df['time'], unit='s', utc=True)
    # Convert from UTC to your local timezone (BST)
    local_tz = pytz.timezone('Europe/London')
    df['time'] = df['time'].dt.tz_convert(local_tz)

    # Remove timezone information for clean CSV output
    df['time'] = df['time'].dt.tz_localize(None)

    print(f"Retrieved {len(df)} candles", flush=True)
    print(f"Time range: {df['time'].min()} to {df['time'].max()}", flush=True)

    return df

def get_candles_15m(symbol, timeframe, NoOfCandles):
    # Get current time in UTC (same as MT5 server)
    utc_now = datetime.now(timezone.utc)
    print(f"Current UTC time: {utc_now}")

    # Use copy_rates_from_pos for more reliable data retrieval
    rates15 = mt.copy_rates_from_pos(symbol, timeframe, 0, NoOfCandles)

    if rates15 is None or len(rates15) == 0:
        print("No data received from MT5 for 15 minute. Checking connection...")
        mt.symbol_select(symbol, True)
        rates15 = mt.copy_rates_from_pos(symbol, timeframe, 0, NoOfCandles)

    df = pd.DataFrame(rates15)
    df['time'] = pd.to_datetime(df['time'], unit='s', utc=True)

    # Convert from UTC to your local timezone (BST)
    local_tz = pytz.timezone('Europe/London')
    df['time'] = df['time'].dt.tz_convert(local_tz)

    # Remove timezone information for clean CSV output
    df['time'] = df['time'].dt.tz_localize(None)

    print(f"Retrieved {len(df)} candles")
    print(f"Time range: {df['time'].min()} to {df['time'].max()}")

    return df

def get_candles_1hr(symbol, timeframe, NoOfCandles):
    utc_now = datetime.now(timezone.utc)
    print(f"Current UTC time: {utc_now}")

    # Use copy_rates_from_pos for more reliable data retrieval
    rates15 = mt.copy_rates_from_pos(symbol, timeframe, 0, NoOfCandles)

    if rates15 is None or len(rates15) == 0:
        print("No data received from MT5 for 1 hour. Checking connection...")
        mt.symbol_select(symbol, True)
        rates15 = mt.copy_rates_from_pos(symbol, timeframe, 0, NoOfCandles)

    df = pd.DataFrame(rates15)
    df['time'] = pd.to_datetime(df['time'], unit='s', utc=True)

    # Convert from UTC to your local timezone (BST)
    local_tz = pytz.timezone('Europe/London')
    df['time'] = df['time'].dt.tz_convert(local_tz)

    # Remove timezone information for clean CSV output
    df['time'] = df['time'].dt.tz_localize(None)

    print(f"Retrieved {len(df)} candles")
    print(f"Time range: {df['time'].min()} to {df['time'].max()}")

    return df

"""
All Functions below are for the sole purpose of writings headings to the following CSV files:
1. Current_Candle_1m_Data.csv
2. GBPUSD_15M.csv
3. FairValueGap_15m.csv
4. OrderBlocks_15m.csv
5. Liquidity_15m.csv
6. GBPUSD_1H.csv
7. OrderBlocks_1H.csv
"""

def data_1m():
    with open('Current_Candle_1m_Data.csv', mode='w',newline='' ) as file:
        writer = csv.writer(file)
        writer.writerow(['Date', 'Open', 'High', 'Low', 'Close'])

def write_1m(data):
    with open('Current_Candle_1m_Data.csv', mode='a',newline='' ) as file:
        writer = csv.writer(file)
        for _, row in data.iterrows():
            naive_time = row['time'].tz_localize(None) if row['time'].tz else row['time']
            writer.writerow([
                naive_time,  # Date
                round(row['open'], 3),  # Open
                round(row['high'], 3),  # High
                round(row['low'], 3),  # Low
                round(row['close'], 3)   # Close
            ])

def data_15m():
    global initial_run_complete
    if not initial_run_complete:
        with open('GBPUSD_15m_Data.csv', mode='w',newline='' ) as file:
            writer = csv.writer(file)
            writer.writerow(['Date', 'Open', 'High', 'Low', 'Close'])

def write_15m(data):
    global initial_run_complete
    data_to_write = data if not initial_run_complete else data.iloc[-1]

    with open('GBPUSD_15m_Data.csv', mode='a',newline='' ) as file:
        writer = csv.writer(file)
        for _, row in data_to_write.iterrows():
            naive_time = row['time'].tz_localize(None) if row['time'].tz else row['time']
            writer.writerow([
                naive_time,  # Date
                round(row['open'], 3),  # Open
                round(row['high'], 3),  # High
                round(row['low'], 3),  # Low
                round(row['close'], 3)   # Close
            ])

def FairValueGap(): #Reset OB file
    with open('FairValueGap_15m.csv',mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Date", "Prev_candle", "Next_candle", "Position"])

def OrderBlock_15m(): #Reset OB file
    with open('OrderBlock_15m.csv',mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Date", "Open", "High", "Low", "Close", "Position"])

def Liquidity():
    with open('Liquidity_15m.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Date", "Open","Loc"])

def data_1Hr():
    global initial_run_complete
    if not initial_run_complete:
        with open('GBPUSD_1hr_Data.csv', mode='w',newline='' ) as file:
            writer = csv.writer(file)
            writer.writerow(['Date', 'Open', 'High', 'Low', 'Close'])

def write_1hr(data):
    global initial_run_complete
    data_to_write = data if not initial_run_complete else data.iloc[-1:]

    with open('GBPUSD_1hr_Data.csv', mode='a',newline='' ) as file:
        writer = csv.writer(file)
        for _, row in data_to_write.iterrows():
            naive_time = row['time'].tz_localize(None) if row['time'].tz else row['time']
            writer.writerow([
                naive_time,   # Date
                round(row['open'], 3),   # Open
                round(row['high'], 3),   # High
                round(row['low'], 3),    # Low
                round(row['close'], 3)   # Close
            ])

def OrderBlock_1hr(): #Reset OB file
    with open('OrderBlock_1hr.csv',mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Date", "Open", "High", "Low", "Close", "Position"])

counter = 0
def initialise(counter):
    if counter == 0:
        MT5_account() #Initialises login information
        counter += 1
    else:
        return

def check_1m():
    print(f"\n[DEBUG] check_1m() FUNCTION WAS CALLED AT {datetime.now().strftime('%H:%M:%S')}", flush=True)
    print(f"\n--- Running trading job at {datetime.now().strftime('%H:%M:%S')} ---", flush=True)
    print(f"----------------------------------------------------------------------\n", flush=True)
    try:
        df_1m = get_candle_1m(symbol, timeframe_1m, NoOfCandles_1m) # Candle Information

        data_1m()
        write_1m(df_1m)

        last_tick = mt.symbol_info_tick(symbol)
        print(f"Latest Candle: {last_tick}", flush=True)
        print(f"--- Job Completed at {datetime.now().strftime('%H:%M:%S')} --- \n", flush=True)

    except Exception as e:
        print(f"Error Occured: {e}", flush=True)
        MT5_account()

def check_15m():
    print(f"\n--- Running trading job at {datetime.now().strftime('%H:%M:%S')} ---")
    print(f"----------------------------------------------------------------------\n")
    global initial_run_complete, NoOfCandles_15m
    get_candles = NoOfCandles_15m if not initial_run_complete else 1

    try:
        df_15 = get_candles_15m(symbol, timeframe_15m, get_candles)  # Candle Information

        data_15m() #Update CSV files
        write_15m(df_15)

        FairValueGap()
        fvg.main()

        data_15 = pd.read_csv('GBPUSD_15m_Data.csv')
        OrderBlock_15m()
        ob.main(data_15, 0)

        Liquidity()
        lqt.main()

        last_tick = mt.symbol_info_tick(symbol)
        print(f"Latest Candle: {last_tick}")
        print(f"--- Job Completed at {datetime.now().strftime('%H:%M:%S')} --- \n")

    except Exception as e:
        print(f"Error Occured: {e}")
        MT5_account()

def check_1hr():
    print(f"\n--- Running trading job at {datetime.now().strftime('%H:%M:%S')} ---")
    print(f"----------------------------------------------------------------------\n")
    global initial_run_complete, NoOfCandles_1H
    get_candles = NoOfCandles_1H if not initial_run_complete else 1
    try:
        df_1h = get_candles_1hr(symbol, timeframe_1H, get_candles)
        check_system_timezone()

        data_1Hr()
        write_1hr(df_1h)

        data_1h = pd.read_csv('GBPUSD_1hr_Data.csv')
        OrderBlock_1hr()
        ob.main(data_1h, 1)

    except Exception as e:
        print(f"Error Occured: {e}")
        MT5_account()


def should_run_now(interval_minutes, offset_minutes=0):
    """
    Checks if the current time matches the scheduled time.
    Args:
        interval_minutes: The interval between runs (e.g., 1, 15, 60).
        offset_minutes: Minutes past the hour to run (e.g., 0, 15, 30, 45).
    Returns:
        bool: True if it's time to run the job.
    """
    now = datetime.now()
    # Calculate total minutes since a reference point (e.g., start of day)
    total_minutes = now.hour * 60 + now.minute
    # Check if the current time aligns with the interval and offset
    return (total_minutes - offset_minutes) % interval_minutes == 0


# Define the schedules for your jobs
schedules = [
    {"function": check_1m,    "interval": 1,   "offset": 0},
    {"function": check_15m,   "interval": 15,  "offset": 0},
    {"function": check_15m,   "interval": 15,  "offset": 15},
    {"function": check_15m,   "interval": 15,  "offset": 30},
    {"function": check_15m,   "interval": 15,  "offset": 45},
    {"function": check_1hr,   "interval": 60,  "offset": 0}
    # {"function": s.main,      "interval": 1,   "offset": 0}  # REMOVE THIS LINE
]


def run_scheduler():
    # Track the last run time for each job to avoid double-execution in the same minute
    last_run_times = {job["function"].__name__: None for job in schedules}

    while True:
        now = datetime.now()
        current_minute = (now.hour, now.minute)  # Use a tuple of (hour, minute) for tracking

        for job in schedules:
            func = job["function"]
            interval = job["interval"]
            offset = job["offset"]

            # Check if it's time to run this job
            if should_run_now(interval, offset):
                # Check if we've already run it this minute
                if last_run_times[func.__name__] != current_minute:
                    print(f"[Scheduler] Starting {func.__name__} at {now.strftime('%H:%M:%S')}", flush=True)
                    # Run the job in a thread to avoid blocking
                    job_thread = threading.Thread(target=func)
                    job_thread.start()
                    # Update the last run time to the current minute
                    last_run_times[func.__name__] = current_minute
            # else:
            # Optional: Debug print to see which jobs are being skipped
            # print(f"[Scheduler] Not time for {func.__name__}. Interval: {interval}, Offset: {offset}, Current Min: {now.minute}")

        # Sleep for a short period before checking again
        time.sleep(0.5)  # Check twice a second


# REMOVE the call to schedule_jobs() in your main() function.
# The schedules are now defined in the list above.

def main():
    global initial_run_complete
    MT5_account()


    print("--- Running Initial Setup .... ---\n")
    check_1m()
    check_15m()
    check_1hr()

    initial_run_complete = True
    print("--- Initial Setup Completed ... ---")
    print("--- Switching to Append Mode ---\n")

    last_tick = mt.symbol_info_tick(symbol)
    print(f"Current Market Price: {last_tick} \n")

    try:
        run_scheduler()
    except KeyboardInterrupt:
        print("Program Terminated by User \n")
    finally:
        mt.shutdown()


    check_1m()
    s.main()

if __name__ == '__main__':
    main()
