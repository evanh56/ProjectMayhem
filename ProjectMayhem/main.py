"""Project Mayhem demo-model CLI; broker access is lazy and fail-closed."""
from __future__ import annotations
import argparse, csv, json
from pathlib import Path
import pandas as pd
from .config import load_config, validate_config
from .data import discover_symbol, fetch_history
from .strategy_engine import evaluate
from .risk import make_plan
from .Execution import PaperExecutor

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
        if getattr(account, "server", c.server) != c.server or not getattr(account, "trade_allowed", True): raise RuntimeError("account identity or trading permission rejected")
        return mt
    except Exception:
        mt.shutdown(); raise

def shutdown_broker(mt=None):
    if mt is not None: mt.shutdown()

def _write_rows(path, frame, append):
    if frame.empty: return
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    with open(path, "a" if append else "w", newline="") as file:
        writer = csv.writer(file)
        if not append: writer.writerow(["Date", "Open", "High", "Low", "Close"])
        for _, row in frame.iterrows(): writer.writerow([pd.Timestamp(row["time"]).tz_localize(None), round(row["open"], 3), round(row["high"], 3), round(row["low"], 3), round(row["close"], 3)])

def write_15m(data, path="GBPJPY_15m_Data.csv", initial_run_complete=None):
    global INITIAL_RUN_COMPLETE
    complete = INITIAL_RUN_COMPLETE if initial_run_complete is None else initial_run_complete
    if not data.empty: _write_rows(path, data if not complete else data.iloc[[-1]], complete)
    if initial_run_complete is None and not complete: INITIAL_RUN_COMPLETE = True

def write_1hr(data, path="GBPJPY_1hr_Data.csv", initial_run_complete=None):
    complete = INITIAL_RUN_COMPLETE if initial_run_complete is None else initial_run_complete
    if not data.empty: _write_rows(path, data if not complete else data.iloc[[-1]], complete)

def run_once(c=None):
    c = c or load_config(); mt = connect_broker(); executor = PaperExecutor(c.log_dir)
    try:
        for requested in c.symbols:
            symbol = discover_symbol(mt, requested); h1 = fetch_history(mt, symbol, mt.TIMEFRAME_H1, c.h1_bars); m15 = fetch_history(mt, symbol, mt.TIMEFRAME_M15, c.m15_bars)
            signal, reason = evaluate(symbol, h1, m15); record = {"symbol": symbol, "reason": reason}
            if signal:
                try:
                    info = mt.symbol_info(symbol); tick = mt.symbol_info_tick(symbol); side = signal.side; entry = tick.ask if side == "buy" else tick.bid
                    plan = make_plan(symbol, side, entry, signal.liquidity, info.point, mt.account_info().equity, info.trade_tick_value, info.trade_tick_size, info.volume_min, info.volume_max, info.volume_step, c.risk_percent, c.target_r, c.stop_buffer_points)
                    record["intent_id"] = executor.submit(plan.symbol, plan.side, plan.entry, plan.stop, plan.target, plan.volume).intent_id
                except (AttributeError, ValueError, RuntimeError) as exc: record["reason"] = f"rejected:{exc}"
            Path(c.log_dir).mkdir(parents=True, exist_ok=True)
            with (Path(c.log_dir) / "signals.jsonl").open("a", encoding="utf-8") as f: f.write(json.dumps(record, default=str, sort_keys=True) + "\n")
    finally: shutdown_broker(mt)

def main(argv=None):
    parser = argparse.ArgumentParser(prog="python -m ProjectMayhem"); parser.add_argument("command", choices=["run", "check-config", "status", "stop"]); args = parser.parse_args(argv); c = load_config()
    if args.command == "check-config":
        errors = validate_config(c); print("configuration valid" if not errors else "configuration invalid: " + "; ".join(errors)); return 0 if not errors else 2
    if args.command == "status": print("offline foundation ready"); return 0
    if args.command == "stop": print("stop requested"); return 0
    try: run_once(c)
    except RuntimeError as exc: print(f"run refused: {exc}"); return 2
    return 0

if __name__ == "__main__": raise SystemExit(main())
