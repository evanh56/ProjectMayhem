import csv
import os
from pathlib import Path

import pandas as pd

INITIAL_RUN_COMPLETE = False
SYMBOL = "GBPJPY"
INFO = "Time, Open, High, Low, Close"
M15_FILE = "GBPUSD_15m_Data.csv"


def _mt5():
    try:
        import MetaTrader5 as mt
    except ImportError as exc:
        raise RuntimeError("MetaTrader5 is required only for broker startup and market-data access") from exc
    return mt


def connect_broker():
    mt = _mt5()
    login = os.getenv("MT5_LOGIN")
    password = os.getenv("MT5_PASSWORD")
    server = os.getenv("MT5_SERVER")
    missing = [name for name, value in (("MT5_LOGIN", login), ("MT5_PASSWORD", password), ("MT5_SERVER", server)) if not value]
    if missing:
        raise RuntimeError("Missing required broker configuration: " + ", ".join(missing))
    if not mt.initialize():
        raise RuntimeError("MetaTrader5 initialization failed")
    if not mt.login(int(login), password=password, server=server):
        mt.shutdown()
        raise RuntimeError("MetaTrader5 authentication failed")
    return mt


def shutdown_broker(mt=None):
    (mt or _mt5()).shutdown()


def _write_rows(path, frame, append):
    if frame.empty:
        return
    columns = ["Date", "Open", "High", "Low", "Close"]
    with open(path, "a" if append else "w", newline="") as file:
        writer = csv.writer(file)
        if not append:
            writer.writerow(columns)
        for _, row in frame.iterrows():
            value = row["time"]
            native_time = value.tz_localize(None) if getattr(value, "tz", None) is not None else value
            writer.writerow([native_time, round(row["open"], 3), round(row["high"], 3), round(row["low"], 3), round(row["close"], 3)])


def write_15m(data, path=M15_FILE, initial_run_complete=None):
    global INITIAL_RUN_COMPLETE
    complete = INITIAL_RUN_COMPLETE if initial_run_complete is None else initial_run_complete
    frame = data if not complete else data.iloc[[-1]]
    _write_rows(path, frame, append=complete)
    if initial_run_complete is None and not complete:
        INITIAL_RUN_COMPLETE = True


def write_1hr(data, path="GBPUSD_1hr_Data.csv", initial_run_complete=None):
    complete = INITIAL_RUN_COMPLETE if initial_run_complete is None else initial_run_complete
    frame = data if not complete else data.iloc[[-1]]
    _write_rows(path, frame, append=complete)


def main():
    mt = connect_broker()
    try:
        return mt
    finally:
        shutdown_broker(mt)


if __name__ == "__main__":
    main()
