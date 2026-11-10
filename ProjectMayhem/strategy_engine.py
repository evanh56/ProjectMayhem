"""Deterministic, causal H1-context then M15-confirmation model."""
from __future__ import annotations
from dataclasses import dataclass
import pandas as pd

@dataclass(frozen=True)
class Signal:
    symbol: str; side: str; candle_time: pd.Timestamp; entry: float; liquidity: float; reason: str


def _side(c):
    if c.close > c.open: return "buy"
    if c.close < c.open: return "sell"
    return None


def evaluate(symbol: str, h1: pd.DataFrame, m15: pd.DataFrame) -> tuple[Signal | None, str]:
    needed = {"time", "open", "high", "low", "close"}
    if not needed <= set(h1.columns) or not needed <= set(m15.columns): return None, "missing_columns"
    if len(h1) < 2 or len(m15) < 2: return None, "insufficient_warmup"
    context = _side(h1.iloc[-2]); confirmation = _side(m15.iloc[-2])
    if context is None or confirmation != context: return None, "direction_not_confirmed"
    c = m15.iloc[-2]
    liquidity = float(h1.iloc[-2].low if context == "buy" else h1.iloc[-2].high)
    entry = float(c.close)
    if (context == "buy" and liquidity >= entry) or (context == "sell" and liquidity <= entry): return None, "invalid_liquidity_geometry"
    return Signal(symbol, context, pd.Timestamp(c.time), entry, liquidity, "h1_context_m15_confirmation"), "accepted"
