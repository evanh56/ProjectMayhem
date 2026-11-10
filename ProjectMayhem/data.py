"""Offline-safe candle normalization and optional MT5 history adapter."""
from __future__ import annotations
from datetime import datetime, timezone
import pandas as pd


def completed_candles(frame: pd.DataFrame, timeframe_minutes: int, now=None) -> pd.DataFrame:
    required = {"time", "open", "high", "low", "close"}
    if not required <= set(frame.columns): raise ValueError("missing candle columns")
    current = pd.Timestamp(now or datetime.now(timezone.utc))
    if current.tzinfo is None: current = current.tz_localize("UTC")
    out = frame.copy(); out["time"] = pd.to_datetime(out["time"], utc=True)
    return out[out["time"] < current.floor(f"{timeframe_minutes}min")].drop_duplicates("time").sort_values("time").reset_index(drop=True)


def discover_symbol(mt, requested: str) -> str:
    if mt.symbol_info(requested) is not None: return requested
    matches = [x.name for x in (mt.symbols_get() or ()) if x.name.upper().startswith(requested.upper())]
    if len(matches) != 1: raise RuntimeError(f"symbol discovery failed for {requested}")
    return matches[0]


def fetch_history(mt, symbol: str, timeframe, count: int, now=None) -> pd.DataFrame:
    rates = mt.copy_rates_from_pos(symbol, timeframe, 0, count)
    if rates is None or len(rates) == 0: raise RuntimeError(f"no history for {symbol}")
    return completed_candles(pd.DataFrame(rates), 15 if timeframe == mt.TIMEFRAME_M15 else 60, now)
