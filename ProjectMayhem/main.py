import csv
import os
from pathlib import Path
#import MetaTrader5 as mt

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


import os


def connect_broker():
    settings = {
        "MT5_LOGIN": os.getenv("MT5_LOGIN"),
        "MT5_PASSWORD": os.getenv("MT5_PASSWORD"),
        "MT5_SERVER": os.getenv("MT5_SERVER"),
    }

    missing = [
        name for name, value in settings.items()
        if value is None or not value.strip()
    ]

    if missing:
        raise RuntimeError(
            "Missing required broker configuration: " + ", ".join(missing)
        )

    try:
        login = int(settings["MT5_LOGIN"].strip())
    except ValueError as exc:
        raise RuntimeError("MT5_LOGIN must be a numeric account number") from exc

    mt = _mt5()

    if not mt.initialize():
        error = mt.last_error()
        mt.shutdown()
        raise RuntimeError(f"MetaTrader5 initialization failed: {error}")

    try:
        if not mt.login(
            login,
            password=settings["MT5_PASSWORD"],
            server=settings["MT5_SERVER"].strip(),
        ):
            raise RuntimeError(
                f"MetaTrader5 authentication failed: {mt.last_error()}"
            )

        account = mt.account_info()

        if account is None:
            raise RuntimeError(
                f"Unable to retrieve account information: {mt.last_error()}"
            )

        if account.login != login:
            raise RuntimeError("Connected MT5 account does not match MT5_LOGIN")

        if account.trade_mode != mt.ACCOUNT_TRADE_MODE_DEMO:
            raise RuntimeError("Only an MT5 demo account is permitted")

        return mt

    except Exception:
        mt.shutdown()
        raise


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
    if data.empty:
        return
        
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
