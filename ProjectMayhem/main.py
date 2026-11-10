"""Project Mayhem demo-model entry point; broker access is lazy and fail-closed."""
from __future__ import annotations
import argparse, csv, os
from pathlib import Path
import pandas as pd
from .config import load_config, validate_config
from .strategy_engine import evaluate
from .risk import make_plan

INITIAL_RUN_COMPLETE = False

def _mt5():
    try: import MetaTrader5 as mt
    except ImportError as exc: raise RuntimeError("MetaTrader5 is required only for broker startup and market-data access") from exc
    return mt

def connect_broker():
    c = load_config(); errors = validate_config(c)
    if errors: raise RuntimeError("; ".join(errors))
    mt = _mt5()
    if not mt.initialize(): raise RuntimeError(f"MetaTrader5 initialization failed: {mt.last_error()}")
    try:
        if not mt.login(c.login, password=c.password, server=c.server): raise RuntimeError(f"MetaTrader5 authentication failed: {mt.last_error()}")
        account = mt.account_info()
        if account is None or account.login != c.login or account.trade_mode != mt.ACCOUNT_TRADE_MODE_DEMO: raise RuntimeError("account identity/trade mode rejected")
        if getattr(account, "server", c.server) != c.server: raise RuntimeError("connected MT5 server does not match MT5_SERVER")
        if not getattr(account, "trade_allowed", True): raise RuntimeError("trading is not allowed")
        return mt
    except Exception:
        mt.shutdown(); raise

def shutdown_broker(mt=None):
    (mt or _mt5()).shutdown()

def _write_rows(path, frame, append):
    if frame.empty: return
    with open(path, "a" if append else "w", newline="") as file:
        writer = csv.writer(file)
        if not append: writer.writerow(["Date", "Open", "High", "Low", "Close"])
        for _, row in frame.iterrows():
            value = row["time"]; native = value.tz_localize(None) if getattr(value, "tz", None) is not None else value
            writer.writerow([native, round(row["open"], 3), round(row["high"], 3), round(row["low"], 3), round(row["close"], 3)])

def write_15m(data, path="GBPJPY_15m_Data.csv", initial_run_complete=None):
    global INITIAL_RUN_COMPLETE
    complete = INITIAL_RUN_COMPLETE if initial_run_complete is None else initial_run_complete
    if data.empty: return
    _write_rows(path, data if not complete else data.iloc[[-1]], complete)
    if initial_run_complete is None and not complete: INITIAL_RUN_COMPLETE = True

def write_1hr(data, path="GBPJPY_1hr_Data.csv", initial_run_complete=None):
    complete = INITIAL_RUN_COMPLETE if initial_run_complete is None else initial_run_complete
    if data.empty: return
    _write_rows(path, data if not complete else data.iloc[[-1]], complete)

def main(argv=None):
    parser = argparse.ArgumentParser(prog="python -m ProjectMayhem")
    parser.add_argument("command", choices=["run", "check-config", "status", "stop"])
    args = parser.parse_args(argv); c = load_config()
    if args.command == "check-config":
        errors = validate_config(c); print("configuration valid" if not errors else "configuration invalid: " + "; ".join(errors)); return 0 if not errors else 2
    if args.command == "status": print("offline foundation ready"); return 0
    if args.command == "stop": print("stop requested"); return 0
    print("run is fail-closed: broker collection requires a validated demo configuration")
    return 0

if __name__ == "__main__": raise SystemExit(main())
